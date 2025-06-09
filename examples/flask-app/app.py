import os
import time
import logging
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()  # Load from current directory first

# Environment variables loaded successfully

# Configure the Google Generative AI API
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set")

genai.configure(api_key=api_key)

app = Flask(__name__)

# Available models for demonstration purposes
embedding_models = ["openAI-text-embedding-large", "Redis-LangCache-Embed"]
llm_models = ["Gemini-1.5-flash"]

# Cache operations log
cache_operations_log = []

# LangCache configuration
LANGCACHE_BASE_URL = os.getenv('LANGCACHE_BASE_URL')
LANGCACHE_API_KEY = os.getenv('LANGCACHE_API_KEY')
LANGCACHE_CACHE_ID = os.getenv('LANGCACHE_CACHE_ID')

# Shadow mode configuration
SHADOW_MODE = os.getenv('LANGCACHE_SHADOW_MODE', 'false').lower() == 'true'

# Validate LangCache configuration
if not LANGCACHE_BASE_URL or not LANGCACHE_API_KEY or not LANGCACHE_CACHE_ID:
    logger.warning("LangCache configuration incomplete - using fallback mode")
    USE_LANGCACHE = False
else:
    USE_LANGCACHE = True
    logger.info(f"LangCache configured: {LANGCACHE_BASE_URL}")
    logger.info(f"Cache ID: {LANGCACHE_CACHE_ID}")
    if SHADOW_MODE:
        logger.info("🔍 SHADOW MODE ENABLED - Cache responses will not be served to users")

import requests
import json
import uuid
import threading
from datetime import datetime

# Shadow mode logging setup
try:
    import redis
    redis_client = redis.from_url(os.getenv('REDIS_URL', 'redis://localhost:6379')) if SHADOW_MODE else None
except ImportError:
    redis_client = None
    if SHADOW_MODE:
        logger.warning("Redis not available - shadow data will be logged to file")

def log_shadow_data(shadow_data):
    """Log shadow mode data asynchronously"""
    def _log():
        try:
            shadow_data.update({
                "request_id": str(uuid.uuid4()),
                "timestamp": datetime.utcnow().isoformat()
            })

            if redis_client:
                key = f"shadow:{shadow_data['request_id']}"
                redis_client.set(key, json.dumps(shadow_data))
            else:
                with open("shadow_mode.log", "a") as f:
                    f.write(json.dumps(shadow_data) + "\n")
        except Exception as e:
            logger.error(f"Shadow logging error: {e}")

    if SHADOW_MODE:
        threading.Thread(target=_log, daemon=True).start()

def search_langcache(query_text):
    """Search LangCache for semantically similar entries"""
    try:
        url = f"{LANGCACHE_BASE_URL}/v1/caches/{LANGCACHE_CACHE_ID}/search"
        headers = {
            'Authorization': f'Bearer {LANGCACHE_API_KEY}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        data = {
            "prompt": query_text
        }

        logger.info(f"Searching LangCache: {url}")
        response = requests.post(url, json=data, headers=headers, timeout=10)

        if response.status_code == 200:
            results = response.json()
            logger.info(f"LangCache search returned {len(results)} results")
            return results
        else:
            logger.warning(f"LangCache search failed: {response.status_code} - {response.text}")
            return []

    except Exception as e:
        logger.error(f"LangCache search error: {e}")
        return []

def store_in_langcache(query_text, response_text):
    """Store a new entry in LangCache"""
    try:
        url = f"{LANGCACHE_BASE_URL}/v1/caches/{LANGCACHE_CACHE_ID}/entries"
        headers = {
            'Authorization': f'Bearer {LANGCACHE_API_KEY}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        data = {
            "prompt": query_text,
            "response": response_text
        }

        logger.info(f"Storing in LangCache: {url}")
        response = requests.post(url, json=data, headers=headers, timeout=10)

        if response.status_code == 201:
            result = response.json()
            logger.info(f"Successfully stored in LangCache: {result}")
            return True
        else:
            logger.warning(f"LangCache store failed: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        logger.error(f"LangCache store error: {e}")
        return False

def check_langcache_health():
    """Check LangCache health"""
    try:
        url = f"{LANGCACHE_BASE_URL}/v1/caches/{LANGCACHE_CACHE_ID}/health"
        headers = {
            'Authorization': f'Bearer {LANGCACHE_API_KEY}',
            'Accept': 'application/json',
            'User-Agent': 'LangCache-Demo/1.0',
            'Cache-Control': 'no-cache',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        }

        logger.info(f"=== HEALTH CHECK DEBUG ===")
        logger.info(f"URL: {url}")
        logger.info(f"Headers: {headers}")
        logger.info(f"API Key length: {len(LANGCACHE_API_KEY)}")
        logger.info(f"API Key first 20 chars: {LANGCACHE_API_KEY[:20]}...")
        logger.info(f"API Key last 20 chars: ...{LANGCACHE_API_KEY[-20:]}")

        # Try with explicit HTTP/1.1 and no session
        response = requests.get(url, headers=headers, timeout=10, verify=True)

        logger.info(f"Response status: {response.status_code}")
        logger.info(f"Response headers: {dict(response.headers)}")
        logger.info(f"Response text: {response.text}")
        logger.info(f"=== HEALTH CHECK DEBUG END ===")

        if response.status_code == 200:
            return response.json(), True
        else:
            return {"error": response.text, "status_code": response.status_code}, False

    except Exception as e:
        logger.error(f"LangCache health check error: {e}")
        return {"error": str(e)}, False

@app.route("/")
def index():
    """Render the main chat interface."""
    return render_template("index.html",
                           embedding_models=embedding_models,
                           llm_models=llm_models)

@app.route("/query", methods=["POST"])
def query():
    """Process a query from the user and return a response."""
    data = request.json
    query_text = data.get("query", "")
    use_cache = data.get("use_cache", True)
    llm_model = data.get("llm_model", llm_models[0])
    embedding_model = data.get("embedding_model", embedding_models[0])

    # Record start time for performance measurement
    start_time = time.time()

    # Check LangCache first if enabled
    matched_query = None

    # Debug logging
    logger.info(f"=== LANGCACHE DEBUG START ===")
    logger.info(f"Original query: '{query_text}'")
    logger.info(f"Use cache: {use_cache}")
    logger.info(f"LangCache enabled: {USE_LANGCACHE}")

    if USE_LANGCACHE:
        # Search LangCache for semantic matches (always do this for logging)
        try:
            search_response = search_langcache(query_text)
            cache_hit = search_response and len(search_response) > 0

            if SHADOW_MODE:
                # SHADOW MODE: Always call LLM, ignore cache response
                logger.info(f"🔍 SHADOW MODE: Always generating LLM response")
                response = generate_gemini_response(query_text)
                source = "llm"
                similarity = None
                matched_query = None

                # Still add to cache if miss (for future analysis)
                if not cache_hit:
                    store_in_langcache(query_text, response)
                    logger.info(f"💾 STORED in LangCache (shadow mode)")

                # Log shadow data for analysis
                if cache_hit:
                    best_match = search_response[0]
                    cache_response = best_match.get('response', '')
                    cache_similarity = 1.0 - best_match.get('distance', 1.0)
                    matched_query = best_match.get('prompt', '')

                    shadow_data = {
                        "query": query_text,
                        "llm_response": response,
                        "cache_hit": True,
                        "cache_response": cache_response,
                        "similarity_score": cache_similarity,
                        "matched_query": matched_query,
                        "llm_latency_ms": (time.time() - start_time) * 1000
                    }
                    log_shadow_data(shadow_data)
                    logger.info(f"🔍 SHADOW: Cache HIT logged (similarity: {cache_similarity:.3f})")
                else:
                    shadow_data = {
                        "query": query_text,
                        "llm_response": response,
                        "cache_hit": False,
                        "cache_response": None,
                        "similarity_score": None,
                        "matched_query": None,
                        "llm_latency_ms": (time.time() - start_time) * 1000
                    }
                    log_shadow_data(shadow_data)
                    logger.info(f"🔍 SHADOW: Cache MISS logged")

            else:
                # NORMAL MODE: Use cache if hit
                if cache_hit:
                    # Cache hit! Use the best match
                    best_match = search_response[0]  # First result is best match
                    response = best_match.get('response', '')
                    source = "cache"
                    similarity = 1.0 - best_match.get('distance', 1.0)  # Convert distance to similarity
                    matched_query = best_match.get('prompt', '')

                    logger.info(f"✅ LANGCACHE HIT! Found semantic match")
                    logger.info(f"Matched query: '{matched_query}'")
                    logger.info(f"Similarity: {similarity:.3f}")
                    logger.info(f"Response length: {len(response)} characters")
                else:
                    # Cache miss - generate new response
                    logger.info(f"❌ LANGCACHE MISS - No semantic matches found")
                    response = generate_gemini_response(query_text)
                    source = "llm"
                    similarity = None

                    # Store in LangCache for future use
                    store_in_langcache(query_text, response)
                    logger.info(f"💾 STORED in LangCache")

        except Exception as e:
            logger.error(f"LangCache error: {e}")
            logger.info(f"🔄 Fallback to LLM generation")
            response = generate_gemini_response(query_text)
            source = "llm"
            similarity = None
    else:
        # Cache disabled or not configured - generate new response
        logger.info(f"🔄 Cache disabled - generating new response")
        response = generate_gemini_response(query_text)
        source = "llm"
        similarity = None

    logger.info(f"=== LANGCACHE DEBUG END ===")
    logger.info(f"Final source: {source}, similarity: {similarity}")

    # Calculate elapsed time
    elapsed_time = time.time() - start_time

    # Get cache ID from environment
    cache_id = os.getenv('LANGCACHE_CACHE_ID', 'local-demo-cache')

    # Log the operation
    operation_log = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "query": query_text,
        "source": source,
        "similarity": similarity,
        "response_time": elapsed_time,
        "matched_query": matched_query,
        "embedding_model": embedding_model,
        "llm_model": llm_model,
        "cache_id": cache_id
    }
    cache_operations_log.append(operation_log)

    return jsonify({
        "response": response,
        "time_taken": elapsed_time,
        "source": source,
        "similarity": similarity
    })

@app.route("/logs", methods=["GET"])
def get_logs():
    """Get cache operations log."""
    return jsonify({
        "operations": cache_operations_log,
        "total_operations": len(cache_operations_log),
        "cache_hits": len([op for op in cache_operations_log if op["source"] == "cache"]),
        "cache_misses": len([op for op in cache_operations_log if op["source"] == "llm"])
    })

@app.route("/health", methods=["GET"])
def health_check():
    """Check LangCache health and return status."""
    if not USE_LANGCACHE:
        return jsonify({
            "status": "LangCache disabled",
            "langcache_configured": False
        })

    health_data, is_healthy = check_langcache_health()

    return jsonify({
        "status": "healthy" if is_healthy else "unhealthy",
        "langcache_configured": True,
        "langcache_health": health_data,
        "base_url": LANGCACHE_BASE_URL,
        "cache_id": LANGCACHE_CACHE_ID
    })

def generate_gemini_response(query):
    """Generate a response using Gemini 1.5 Flash."""
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(query)
        return response.text
    except Exception as e:
        print(f"Error generating response: {e}")
        return f"I'm sorry, I couldn't generate a response. Error: {str(e)}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)