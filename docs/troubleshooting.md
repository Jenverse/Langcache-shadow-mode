# LangCache Shadow Mode Troubleshooting Guide

This guide helps you diagnose and resolve common issues with LangCache shadow mode integration using the managed service.

## 🔍 Quick Diagnostics

### 1. Test LangCache Managed Service Connection

#### Health Check
```http
GET {{langcache_base_url}}/v1/caches/{{cache_id}}/health
Authorization: Bearer {{langcache_api_key}}
Accept: application/json
Cache-Control: no-cache
Postman-Token: {{$guid}}
```

**Expected Response (200 OK):**
```json
{
  "checks": [
    {
      "name": "cache_connectivity",
      "status": "healthy"
    }
  ],
  "ok": true
}
```

**❌ Common Issues:**
- **401 Unauthorized**: Invalid API key
- **404 Not Found**: Invalid cache ID
- **503 Service Unavailable**: Service down

### 2. Test Cache Search Operation

#### Search Request
```http
POST {{langcache_base_url}}/v1/caches/{{cache_id}}/search
Authorization: Bearer {{langcache_api_key}}
Content-Type: application/json
Accept: application/json

{
  "prompt": "What is machine learning?",
  "attributes": {
    "language": "en"
  },
  "scope": {
    "applicationId": "shadow-mode-test",
    "userId": "test-user"
  },
  "distanceThreshold": 0.85
}
```

**Expected Response (200 OK):**
```json
[
  {
    "id": "entry-123",
    "prompt": "What is machine learning?",
    "response": "Machine learning is a subset of AI...",
    "distance": 0.12,
    "attributes": {
      "language": "en"
    },
    "scope": {
      "applicationId": "shadow-mode-test",
      "userId": "test-user"
    }
  }
]
```

**❌ Common Issues:**
- **Empty array `[]`**: No matches found (normal for new cache)
- **400 Bad Request**: Invalid request format
- **422 Unprocessable Entity**: Invalid parameters

### 3. Test Cache Add Operation

#### Add Entry Request
```http
POST {{langcache_base_url}}/v1/caches/{{cache_id}}/entries
Authorization: Bearer {{langcache_api_key}}
Content-Type: application/json
Accept: application/json

{
  "prompt": "What is artificial intelligence?",
  "response": "Artificial intelligence (AI) is the simulation of human intelligence in machines...",
  "attributes": {
    "language": "en",
    "category": "technology"
  },
  "scope": {
    "applicationId": "shadow-mode-test",
    "userId": "test-user"
  },
  "ttlMillis": 3600000
}
```

**Expected Response (201 Created):**
```json
{
  "id": "entry-456",
  "prompt": "What is artificial intelligence?",
  "response": "Artificial intelligence (AI) is the simulation of human intelligence in machines...",
  "attributes": {
    "language": "en",
    "category": "technology"
  },
  "scope": {
    "applicationId": "shadow-mode-test",
    "userId": "test-user"
  },
  "ttlMillis": 3600000,
  "createdAt": "2025-01-27T15:04:32.123Z"
}
```

## 🚨 Common Shadow Mode Issues

### Issue 1: Shadow Mode Not Activating

**Symptoms:**
- No shadow logs generated
- Cache operations not happening
- Environment variable ignored

**Diagnosis Steps:**

1. **Check Environment Variables:**
   ```bash
   echo $LANGCACHE_SHADOW_MODE
   echo $LANGCACHE_API_KEY
   echo $LANGCACHE_CACHE_ID
   echo $LANGCACHE_BASE_URL
   ```

2. **Test Manual API Call:**
   ```bash
   curl -X GET "https://api.langcache.com/v1/caches/your-cache-id/health" \
     -H "Authorization: Bearer your-api-key" \
     -H "Accept: application/json" \
     -H "Cache-Control: no-cache"
   ```

**Solutions:**
- ✅ Set `LANGCACHE_SHADOW_MODE=true` (not `True` or `1`)
- ✅ Verify all required environment variables are set
- ✅ Restart application after setting environment variables
- ✅ Check application logs for shadow mode initialization messages

### Issue 2: Authentication Failures

**Symptoms:**
- 401 Unauthorized responses
- "Invalid API key" errors
- Authentication header issues

**Diagnosis with Postman:**

1. **Test API Key Format:**
   ```http
   GET {{langcache_base_url}}/v1/caches/{{cache_id}}/health
   Authorization: Bearer YOUR_ACTUAL_API_KEY
   ```

2. **Check Required Headers:**
   ```http
   POST {{langcache_base_url}}/v1/caches/{{cache_id}}/search
   Authorization: Bearer {{langcache_api_key}}
   Content-Type: application/json
   Accept: application/json
   Cache-Control: no-cache
   Postman-Token: {{$guid}}
   ```

**Solutions:**
- ✅ Verify API key is correct (no extra spaces/characters)
- ✅ Ensure `Bearer ` prefix in Authorization header
- ✅ Check API key hasn't expired
- ✅ Verify cache ID belongs to your account

### Issue 3: Cache Operations Failing

**Symptoms:**
- Search returns errors
- Add operations fail
- Timeout errors

**Diagnosis Steps:**

1. **Test Search with Minimal Payload:**
   ```http
   POST {{langcache_base_url}}/v1/caches/{{cache_id}}/search
   Authorization: Bearer {{langcache_api_key}}
   Content-Type: application/json

   {
     "prompt": "test query"
   }
   ```

2. **Test Add with Minimal Payload:**
   ```http
   POST {{langcache_base_url}}/v1/caches/{{cache_id}}/entries
   Authorization: Bearer {{langcache_api_key}}
   Content-Type: application/json

   {
     "prompt": "test query",
     "response": "test response"
   }
   ```

**Solutions:**
- ✅ Start with minimal payloads, add complexity gradually
- ✅ Check network connectivity and timeouts
- ✅ Verify JSON format is valid
- ✅ Check service status page

### Issue 4: No Shadow Data in Logs

**Symptoms:**
- Shadow mode active but no logs
- Redis empty or file not created
- Missing log entries

**Diagnosis Steps:**

1. **Check Redis Connection:**
   ```bash
   redis-cli ping
   redis-cli KEYS "shadow:*"
   ```

2. **Check File Logging:**
   ```bash
   ls -la shadow_mode.log
   tail -f shadow_mode.log
   ```

3. **Test Manual Logging:**
   ```python
   from langcache_shadow import track
   track("test query", "test response")
   ```

**Solutions:**
- ✅ Verify Redis is running and accessible
- ✅ Check file permissions for log directory
- ✅ Ensure async operations aren't being blocked
- ✅ Check application error logs

### Issue 5: Performance Impact

**Symptoms:**
- Slower response times
- Increased memory usage
- Application timeouts

**Diagnosis Steps:**

1. **Monitor Application Metrics:**
   - Response time before/after shadow mode
   - Memory usage patterns
   - CPU utilization

2. **Check Shadow Operation Timing:**
   ```python
   import time
   start = time.time()
   # Your shadow operation
   print(f"Shadow operation took: {time.time() - start}ms")
   ```

**Solutions:**
- ✅ Ensure shadow operations are truly async
- ✅ Reduce logging frequency if needed
- ✅ Optimize Redis connection pooling
- ✅ Set appropriate timeouts

## 🔧 Debug Mode

### Enable Debug Logging

**Python:**
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Set environment variable
export LANGCACHE_DEBUG=true
```

**Node.js:**
```javascript
// Set environment variable
export DEBUG=langcache:*
```

### Debug Postman Collection

We provide a comprehensive Postman collection for systematic testing:

#### Import the Collection
1. Download: [`postman-collection.json`](postman-collection.json)
2. Open Postman → Import → Upload the JSON file
3. Set collection variables:
   - `langcache_base_url`: `https://api.langcache.com`
   - `langcache_api_key`: Your actual API key
   - `cache_id`: Your actual cache ID

#### Test Sequence
Run these requests in order:

1. **Health Check** - Verify service connectivity
2. **Search Empty Cache** - Test search on new cache
3. **Add Test Entry** - Add a known entry
4. **Search for Exact Match** - Verify entry was added
5. **Search for Similar Query** - Test semantic matching
6. **Search with Strict Threshold** - Test threshold behavior
7. **Add Shadow Mode Test Entry** - Add realistic test data
8. **Test Shadow Mode Scenario** - Test semantic similarity
9. **Bulk Add for Testing** - Build up cache content
10. **Test Error Handling** - Verify error responses
11. **Test Malformed Request** - Validate request format

#### Expected Results
- ✅ Health Check: 200 OK with `"ok": true`
- ✅ Search Empty: 200 OK with empty array `[]`
- ✅ Add Entry: 201 Created with entry details
- ✅ Search Exact: 200 OK with low distance match
- ✅ Search Similar: 200 OK with moderate distance match
- ✅ Error Tests: Appropriate error codes (401, 404, 400)

## 📊 Monitoring Shadow Mode

### Key Metrics to Track

1. **Shadow Operation Success Rate:**
   ```bash
   # Count successful vs failed operations
   redis-cli KEYS "shadow:*" | wc -l
   grep "error" shadow_mode.log | wc -l
   ```

2. **Cache Hit Rate:**
   ```bash
   # Analyze shadow data
   python3 analytics/analyze_shadow_data.py --source redis
   ```

3. **Performance Impact:**
   - Response time distribution
   - Memory usage trends
   - Error rates

### Alerting Thresholds

- **Shadow operation failure rate > 5%**
- **Cache API response time > 1000ms**
- **Redis connection failures**
- **Missing shadow logs for > 10 minutes**

## 🆘 Getting Help

### Before Contacting Support

1. ✅ Run through this troubleshooting guide
2. ✅ Test with Postman collection
3. ✅ Collect relevant logs and error messages
4. ✅ Note your environment details

### Information to Provide

- **Environment:** Production/Staging/Development
- **Language/Framework:** Python/Node.js/etc.
- **LangCache Configuration:** API endpoint, cache ID (not API key)
- **Error Messages:** Full error text and stack traces
- **Postman Test Results:** Which operations work/fail
- **Timeline:** When did the issue start?

### Support Channels

- 📖 [Documentation](../README.md)
- 🐛 [GitHub Issues](https://github.com/redis/langcache-shadow-mode/issues)
- 💬 [Community Discussions](https://github.com/redis/langcache-shadow-mode/discussions)
- 📧 [Enterprise Support](mailto:support@redis.com) (for enterprise customers)

## 📋 Troubleshooting Checklist

### Pre-Integration Checklist
- [ ] LangCache managed service account set up
- [ ] API key and cache ID obtained
- [ ] Network connectivity to LangCache service verified
- [ ] Postman collection tests passing

### Shadow Mode Integration Checklist
- [ ] Environment variables set correctly
- [ ] Shadow mode wrapper/code integrated
- [ ] Redis running and accessible (or file logging configured)
- [ ] Test queries generating shadow logs
- [ ] No performance impact on production

### Production Monitoring Checklist
- [ ] Shadow operation success rate monitoring
- [ ] Cache hit rate tracking
- [ ] Performance metrics baseline established
- [ ] Alerting configured for failures
- [ ] Regular log analysis scheduled
