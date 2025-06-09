# LangCache Shadow Mode Quick Reference

## 🚀 Quick Setup (2 minutes)

### 1. Environment Variables
```bash
export LANGCACHE_SHADOW_MODE=true
export LANGCACHE_API_KEY=your-api-key
export LANGCACHE_CACHE_ID=your-cache-id
export LANGCACHE_BASE_URL=https://api.langcache.com
export REDIS_URL=redis://localhost:6379  # Optional
```

### 2. Python Integration
```python
# Download wrapper
curl -O https://raw.githubusercontent.com/redis/langcache-shadow-mode/main/wrappers/python/langcache_shadow.py

# Replace LLM calls
from langcache_shadow import shadow_llm_call
response = shadow_llm_call(openai.chat.completions.create, query, ...)
```

### 3. Node.js Integration
```javascript
// Download wrapper
curl -O https://raw.githubusercontent.com/redis/langcache-shadow-mode/main/wrappers/nodejs/langcache-shadow.js

// Replace LLM calls
const { shadowLlmCall } = require('./langcache-shadow');
const response = await shadowLlmCall(() => openai.chat.completions.create(...), query);
```

## 🔍 Quick Diagnostics

### Test LangCache Connection
```bash
curl -X GET "https://api.langcache.com/v1/caches/YOUR_CACHE_ID/health" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Accept: application/json"
```

### Check Shadow Logs
```bash
# Redis
redis-cli KEYS "shadow:*"
redis-cli GET "shadow:latest-request-id"

# File
tail -f shadow_mode.log
```

### Analyze Shadow Data
```bash
python3 analytics/analyze_shadow_data.py --source redis
```

## 📊 Expected Shadow Data Format

```json
{
  "request_id": "uuid",
  "timestamp": "2025-01-27T15:04:32.123Z",
  "query": "User query",
  "llm_response": "LLM response text",
  "llm_latency_ms": 1250,
  "cache_hit": true,
  "cache_response": "Cached response text",
  "similarity_score": 0.89,
  "matched_query": "Similar cached query"
}
```

## 🚨 Common Issues & Quick Fixes

| Issue | Quick Fix |
|-------|-----------|
| No shadow logs | Check `LANGCACHE_SHADOW_MODE=true` |
| 401 Unauthorized | Verify API key format |
| 404 Not Found | Check cache ID |
| No Redis data | Ensure Redis running: `redis-server` |
| Performance impact | Verify async operations |

## 🔧 Debug Commands

### Environment Check
```bash
echo "Shadow Mode: $LANGCACHE_SHADOW_MODE"
echo "API Key: ${LANGCACHE_API_KEY:0:10}..." 
echo "Cache ID: $LANGCACHE_CACHE_ID"
```

### Redis Debug
```bash
redis-cli ping
redis-cli INFO memory
redis-cli KEYS "shadow:*" | head -5
```

### Python Debug
```python
import os
print("Shadow Mode:", os.getenv('LANGCACHE_SHADOW_MODE'))
from langcache_shadow import config
print("Config enabled:", config.enabled)
```

## 📈 Key Metrics

### Success Indicators
- ✅ Shadow logs being generated
- ✅ Cache hit rate > 20%
- ✅ No performance degradation
- ✅ Similarity scores > 0.7 for hits

### Warning Signs
- ⚠️ No logs for > 10 minutes
- ⚠️ All cache misses
- ⚠️ Response time increase > 10%
- ⚠️ Error rate > 5%

## 🛠️ Postman Quick Test

1. Import: [`postman-collection.json`](postman-collection.json)
2. Set variables: `langcache_api_key`, `cache_id`
3. Run: "Health Check" → "Search Empty Cache" → "Add Test Entry"
4. Expected: 200 OK → 200 OK (empty array) → 201 Created

## 📞 Support Checklist

Before contacting support:
- [ ] Postman health check passes
- [ ] Environment variables set correctly  
- [ ] Shadow logs being generated
- [ ] Error messages collected
- [ ] Performance impact measured

## 🎯 Production Readiness

### Before Go-Live
- [ ] 48+ hours of shadow data collected
- [ ] Hit rate analysis completed
- [ ] Performance impact < 5%
- [ ] Error handling tested
- [ ] Monitoring alerts configured

### Deployment Steps
1. Set `LANGCACHE_SHADOW_MODE=false`
2. Update application to use cache responses
3. Monitor hit rates and performance
4. Gradually increase cache usage

## 📚 Links

- [Full Documentation](../README.md)
- [Getting Started Guide](getting-started.md)
- [Troubleshooting Guide](troubleshooting.md)
- [Wrapper Documentation](../wrappers/README.md)
- [GitHub Issues](https://github.com/redis/langcache-shadow-mode/issues)
