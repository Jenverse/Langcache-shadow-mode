# Getting Started with LangCache Shadow Mode

This guide will help you integrate LangCache shadow mode into your existing LLM applications in just a few minutes.

## What is Shadow Mode?

Shadow mode allows you to run LangCache alongside your existing LLM applications without affecting production traffic. It:

- ✅ **Mirrors queries** to both your LLM and LangCache
- ✅ **Serves only LLM responses** to end users (zero risk)
- ✅ **Logs comparison data** for analysis (hit rates, latency, similarity)
- ✅ **Builds confidence** before switching to live caching

## Prerequisites

- Existing LLM application (any language)
- LangCache API credentials
- Redis instance for logging (optional)

## Quick Setup

### 1. Get Your LangCache Credentials

You'll need:
- `LANGCACHE_API_KEY` - Your LangCache API key
- `LANGCACHE_CACHE_ID` - Your cache instance ID
- `LANGCACHE_BASE_URL` - LangCache service URL (usually `https://api.langcache.com`)

### 2. Set Environment Variables

```bash
export LANGCACHE_SHADOW_MODE=true
export LANGCACHE_API_KEY=your-api-key
export LANGCACHE_CACHE_ID=your-cache-id
export LANGCACHE_BASE_URL=https://api.langcache.com
export REDIS_URL=redis://localhost:6379  # Optional
```

### 3. Choose Your Integration Method

## Option A: Wrapper Functions (Recommended)

### Python Integration

1. **Download the wrapper:**
   ```bash
   curl -O https://raw.githubusercontent.com/redis/langcache-shadow-mode/main/wrappers/python/langcache_shadow.py
   ```

2. **Modify your LLM calls:**
   ```python
   # Before
   import openai
   response = openai.chat.completions.create(
       model="gpt-4o-mini",
       messages=[{"role": "user", "content": query}]
   )
   
   # After
   from langcache_shadow import shadow_llm_call
   response = shadow_llm_call(
       openai.chat.completions.create,
       query,
       model="gpt-4o-mini",
       messages=[{"role": "user", "content": query}]
   )
   ```

### Node.js Integration

1. **Download the wrapper:**
   ```bash
   curl -O https://raw.githubusercontent.com/redis/langcache-shadow-mode/main/wrappers/nodejs/langcache-shadow.js
   ```

2. **Modify your LLM calls:**
   ```javascript
   // Before
   const response = await openai.chat.completions.create({
       model: "gpt-4o-mini",
       messages: [{ role: "user", content: query }]
   });
   
   // After
   const { shadowLlmCall } = require('./langcache-shadow');
   const response = await shadowLlmCall(
       () => openai.chat.completions.create({
           model: "gpt-4o-mini",
           messages: [{ role: "user", content: query }]
       }),
       query
   );
   ```

## Option B: Manual Tracking

If you prefer more control, use the simple tracking functions:

### Python
```python
from langcache_shadow import track

# Your existing LLM call
response = openai.chat.completions.create(...)
response_text = response.choices[0].message.content

# Add shadow tracking
track(query, response_text)
```

### Node.js
```javascript
const { track } = require('./langcache-shadow');

// Your existing LLM call
const response = await openai.chat.completions.create(...);
const responseText = response.choices[0].message.content;

// Add shadow tracking
await track(query, responseText);
```

## Option C: API Wrapper Service

For more complex setups, you can run the LangCache operations wrapper:

```bash
cd langcache-operations/embeddings
python main.py  # Runs on localhost:8080
```

Then modify your application to call the wrapper instead of LangCache directly.

## Verification

### 1. Check Logs

**Redis logs:**
```bash
redis-cli KEYS "shadow:*"
redis-cli GET "shadow:your-request-id"
```

**File logs:**
```bash
tail -f shadow_mode.log
```

### 2. Sample Log Entry

```json
{
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2025-01-27T15:04:32.123Z",
  "query": "What is machine learning?",
  "llm_response": "Machine learning is a subset of AI...",
  "llm_latency_ms": 1250,
  "cache_hit": false,
  "cache_latency_ms": 45,
  "cache_response": null,
  "similarity_score": null
}
```

## Next Steps

1. **Run for 24-48 hours** to collect baseline data
2. **Analyze the logs** using our analytics tools
3. **Review hit rates and performance** metrics
4. **Adjust similarity thresholds** if needed
5. **Switch to production caching** when confident

## Troubleshooting

### Common Issues

**Shadow mode not working:**
- Check environment variables are set correctly
- Verify LangCache API credentials
- Check network connectivity to LangCache service

**No logs appearing:**
- Verify Redis connection
- Check file permissions for log files
- Enable debug logging

**Performance impact:**
- Shadow operations run asynchronously
- If you notice impact, check Redis performance
- Consider reducing logging frequency

### Debug Mode

Enable debug logging:

```bash
export LANGCACHE_DEBUG=true
```

### Support

- [Documentation](../README.md)
- [API Reference](api-reference.md)
- [Best Practices](best-practices.md)
- [GitHub Issues](https://github.com/redis/langcache-shadow-mode/issues)
