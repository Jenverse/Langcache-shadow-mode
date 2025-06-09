# LangCache Operations API Wrapper

This is a Python Flask wrapper for the managed LangCache service that follows the Postman YAML structure exactly. The API provides all cache operations including Add, Search, Retrieve, and Delete operations by connecting to your managed LangCache instance.

## Features

✅ **Managed Service Integration** - Connects to Redis LangCache managed service
✅ **Complete API Wrapper** following the Postman YAML structure
✅ **Health Check** - Monitor cache operational status
✅ **Semantic Search** - Advanced similarity search with configurable thresholds
✅ **Add Cache Entry** - Save new entries with metadata
✅ **Delete Operations** - Remove specific or multiple cache entries
✅ **Error Handling** - Proper HTTP status codes and error messages
✅ **Environment Configuration** - Secure credential management
✅ **Production Ready** - Uses your actual LangCache service credentials

## API Endpoints

### 1. Health Check
```http
GET /v1/caches/{cacheId}/health
```
Returns operational status of the cache configuration.

### 2. Search Cache
```http
POST /v1/caches/{cacheId}/search
Content-Type: application/json

{
  "prompt": "What is the capital of France?",
  "attributes": {
    "language": "en"
  },
  "scope": {
    "applicationId": "my-app",
    "userId": "user-123"
  },
  "distanceThreshold": 0.85
}
```

### 3. Add Cache Entry
```http
POST /v1/caches/{cacheId}/entries
Content-Type: application/json

{
  "prompt": "What is the capital of France?",
  "response": "The capital of France is Paris.",
  "attributes": {
    "language": "en",
    "category": "geography"
  },
  "scope": {
    "applicationId": "my-app",
    "userId": "user-123"
  },
  "ttlMillis": 3600000
}
```

### 4. Delete Single Entry
```http
DELETE /v1/caches/{cacheId}/entries/{entryId}
```

### 5. Delete Multiple Entries
```http
DELETE /v1/caches/{cacheId}/entries
Content-Type: application/json

{
  "attributes": {
    "category": "math"
  },
  "scope": {
    "userId": "user-123"
  }
}
```

## Configuration

Your managed LangCache service credentials are configured in the root `.env` file:

```bash
# LangCache Managed Service Configuration
LANGCACHE_BASE_URL=your_langcache_service_url
LANGCACHE_API_KEY=your_api_key_here
LANGCACHE_CACHE_ID=your_cache_id_here

# Local Wrapper Service Configuration
LOCAL_HOST=0.0.0.0
LOCAL_PORT=8080
LOCAL_DEBUG=true
```

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the wrapper service:**
   ```bash
   cd langcache-operations/embeddings
   python3 main.py
   ```

3. **Test the API:**
   ```bash
   # Health check
   curl -X GET "http://localhost:8080/v1/caches/{your-cache-id}/health"

   # Add cache entry
   curl -X POST "http://localhost:8080/v1/caches/{your-cache-id}/entries" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "What is the capital of France?", "response": "The capital of France is Paris."}'

   # Search cache
   curl -X POST "http://localhost:8080/v1/caches/{your-cache-id}/search" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "What is the capital city of France?", "distanceThreshold": 0.8}'
   ```

## Response Formats

All responses follow the exact structure defined in the Postman YAML:

**Search Response:**
```json
[
  {
    "id": "entry-uuid",
    "prompt": "What is the capital of France?",
    "response": "The capital of France is Paris.",
    "distance": 0.0,
    "attributes": {"language": "en"},
    "scope": {"applicationId": "demo-app"},
    "metadata": {
      "createdAt": "2024-01-01T12:00:00Z",
      "lastAccessed": "2024-01-01T12:00:00Z",
      "hitCount": 1
    }
  }
]
```

**Add Entry Response:**
```json
{
  "entryId": "entry-uuid",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

## Error Handling

The API returns proper HTTP status codes and error messages:

- **400 Bad Request** - Invalid request parameters
- **401 Unauthorized** - Authentication required
- **404 Not Found** - Cache or entry not found
- **503 Service Unavailable** - Internal server error

## Architecture

This wrapper service provides:
- **LangCacheClient** - HTTP client for managed service communication
- **Route handlers** - API endpoint implementations that proxy to managed service
- **Error handling** - Proper error response formatting and status codes
- **Environment configuration** - Secure credential management

## Production Deployment

For production deployment:

1. **Use a production WSGI server** (gunicorn, uwsgi)
2. **Set up proper logging** and monitoring
3. **Configure environment variables** securely
4. **Add rate limiting** if needed
5. **Set up SSL/TLS** for secure communication

## Security

- ✅ **No hardcoded credentials** - All sensitive data in environment variables
- ✅ **Secure API communication** - Uses Bearer token authentication
- ✅ **Environment isolation** - Credentials loaded from .env file only
- ✅ **Error handling** - No sensitive information leaked in error responses
