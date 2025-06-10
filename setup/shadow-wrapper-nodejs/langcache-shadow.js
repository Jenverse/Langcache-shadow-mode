/**
 * LangCache Shadow Mode Wrapper for Node.js
 * 
 * This wrapper enables shadow mode for LangCache, allowing you to run semantic caching
 * alongside your existing LLM applications without affecting production traffic.
 * 
 * Usage:
 *   const { shadowLlmCall } = require('./langcache-shadow');
 *   
 *   const response = await shadowLlmCall(
 *     () => openai.chat.completions.create({
 *       model: "gpt-4o-mini",
 *       messages: [{ role: "user", content: query }]
 *     }),
 *     query
 *   );
 */

const https = require('https');
const http = require('http');
const { URL } = require('url');
const { v4: uuidv4 } = require('crypto').randomUUID ? require('crypto') : { v4: () => Math.random().toString(36) };

class ShadowModeConfig {
    constructor() {
        this.enabled = process.env.LANGCACHE_SHADOW_MODE?.toLowerCase() === 'true';
        this.apiKey = process.env.LANGCACHE_API_KEY;
        this.cacheId = process.env.LANGCACHE_CACHE_ID;
        this.baseUrl = process.env.LANGCACHE_BASE_URL || 'https://api.langcache.com';
        this.redisUrl = process.env.REDIS_URL || 'redis://localhost:6379';
        this.timeout = parseInt(process.env.LANGCACHE_TIMEOUT || '10000');
        
        // Validate required configuration
        if (this.enabled && (!this.apiKey || !this.cacheId)) {
            console.warn('Shadow mode enabled but missing required configuration');
            this.enabled = false;
        }
    }
}

class LangCacheClient {
    constructor(config) {
        this.config = config;
    }
    
    async searchCache(query) {
        try {
            const startTime = Date.now();
            const url = `${this.config.baseUrl}/v1/caches/${this.config.cacheId}/search`;
            const data = { prompt: query };
            
            const response = await this._makeRequest(url, 'POST', data);
            const latency = Date.now() - startTime;
            
            if (response.statusCode === 200) {
                const results = JSON.parse(response.body);
                return {
                    hit: results.length > 0,
                    results: results,
                    latency_ms: latency
                };
            } else {
                console.warn(`Cache search failed: ${response.statusCode}`);
                return { hit: false, results: [], latency_ms: 0 };
            }
        } catch (error) {
            console.error(`Cache search error: ${error.message}`);
            return { hit: false, results: [], latency_ms: 0 };
        }
    }
    
    async addToCache(query, response) {
        try {
            const url = `${this.config.baseUrl}/v1/caches/${this.config.cacheId}/entries`;
            const data = { prompt: query, response: response };
            
            const result = await this._makeRequest(url, 'POST', data);
            return result.statusCode === 201;
        } catch (error) {
            console.error(`Cache add error: ${error.message}`);
            return false;
        }
    }
    
    _makeRequest(url, method, data) {
        return new Promise((resolve, reject) => {
            const urlObj = new URL(url);
            const isHttps = urlObj.protocol === 'https:';
            const client = isHttps ? https : http;
            
            const options = {
                hostname: urlObj.hostname,
                port: urlObj.port || (isHttps ? 443 : 80),
                path: urlObj.pathname + urlObj.search,
                method: method,
                headers: {
                    'Authorization': `Bearer ${this.config.apiKey}`,
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                timeout: this.config.timeout
            };
            
            const req = client.request(options, (res) => {
                let body = '';
                res.on('data', (chunk) => body += chunk);
                res.on('end', () => {
                    resolve({
                        statusCode: res.statusCode,
                        body: body
                    });
                });
            });
            
            req.on('error', reject);
            req.on('timeout', () => reject(new Error('Request timeout')));
            
            if (data) {
                req.write(JSON.stringify(data));
            }
            req.end();
        });
    }
}

class ShadowLogger {
    constructor(config) {
        this.config = config;
        this.redisClient = null;
        
        // Initialize Redis client if available
        try {
            const redis = require('redis');
            this.redisClient = redis.createClient({ url: config.redisUrl });
            this.redisClient.on('error', (err) => {
                console.warn(`Redis connection error: ${err.message}`);
                this.redisClient = null;
            });
        } catch (error) {
            console.warn('Redis not available - shadow data will be logged to file');
        }
    }
    
    async logShadowData(shadowData) {
        try {
            // Add timestamp and request ID
            shadowData.request_id = uuidv4();
            shadowData.timestamp = new Date().toISOString();
            
            if (this.redisClient) {
                // Store in Redis
                const key = `shadow:${shadowData.request_id}`;
                await this.redisClient.set(key, JSON.stringify(shadowData));
            } else {
                // Fallback to file logging
                const fs = require('fs');
                fs.appendFileSync('shadow_mode.log', JSON.stringify(shadowData) + '\n');
            }
        } catch (error) {
            console.error(`Shadow logging error: ${error.message}`);
        }
    }
}

// Global instances
const config = new ShadowModeConfig();
const langcacheClient = config.enabled ? new LangCacheClient(config) : null;
const shadowLogger = config.enabled ? new ShadowLogger(config) : null;

/**
 * Wrapper function that calls LLM and performs shadow mode operations
 * 
 * @param {Function} llmFunction - The LLM function to call
 * @param {string} query - The user query string
 * @returns {Promise<any>} The LLM response (unchanged)
 */
async function shadowLlmCall(llmFunction, query) {
    const startTime = Date.now();
    
    // Always call the LLM function first
    const llmResponse = await llmFunction();
    const llmLatency = Date.now() - startTime;
    
    // Extract response text
    const responseText = extractResponseText(llmResponse);
    
    // Perform shadow mode operations if enabled
    if (config.enabled && langcacheClient && shadowLogger) {
        // Run shadow operations in background (don't await)
        performShadowOperations(query, responseText, llmLatency)
            .catch(error => console.error(`Shadow operations error: ${error.message}`));
    }
    
    return llmResponse;
}

/**
 * Extract text response from LLM response object
 */
function extractResponseText(llmResponse) {
    try {
        // Handle OpenAI response format
        if (llmResponse.choices && llmResponse.choices.length > 0) {
            return llmResponse.choices[0].message.content;
        }
        
        // Handle string responses
        if (typeof llmResponse === 'string') {
            return llmResponse;
        }
        
        // Handle object responses
        if (typeof llmResponse === 'object') {
            return JSON.stringify(llmResponse);
        }
        
        // Fallback
        return String(llmResponse);
    } catch (error) {
        console.error(`Error extracting response text: ${error.message}`);
        return String(llmResponse);
    }
}

/**
 * Perform shadow mode cache operations
 */
async function performShadowOperations(query, llmResponse, llmLatency) {
    try {
        // Search cache
        const cacheResult = await langcacheClient.searchCache(query);
        
        // Add to cache if miss
        if (!cacheResult.hit) {
            await langcacheClient.addToCache(query, llmResponse);
        }
        
        // Prepare shadow data
        const shadowData = {
            query: query,
            llm_response: llmResponse,
            llm_latency_ms: llmLatency,
            cache_hit: cacheResult.hit,
            cache_latency_ms: cacheResult.latency_ms,
            cache_response: cacheResult.results.length > 0 ? cacheResult.results[0].response : null,
            similarity_score: cacheResult.results.length > 0 ? (1.0 - (cacheResult.results[0].distance || 1.0)) : null
        };
        
        // Log shadow data
        await shadowLogger.logShadowData(shadowData);
    } catch (error) {
        console.error(`Shadow operations error: ${error.message}`);
    }
}

/**
 * Simple tracking function for manual shadow mode integration
 * 
 * @param {string} query - The user query
 * @param {string} llmResponse - The LLM response text
 */
async function track(query, llmResponse) {
    if (config.enabled && langcacheClient && shadowLogger) {
        await performShadowOperations(query, llmResponse, 0);
    }
}

module.exports = {
    shadowLlmCall,
    track,
    config
};
