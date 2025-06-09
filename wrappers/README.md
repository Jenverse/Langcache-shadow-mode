# LangCache Shadow Mode Wrappers

Language-specific wrapper functions that make it easy to integrate LangCache shadow mode into your existing applications.

## Available Wrappers

- **Python** - `python/langcache_shadow.py`
- **Node.js** - `nodejs/langcache-shadow.js`
- **Go** - `go/langcache_shadow.go` (coming soon)
- **Java** - `java/LangCacheShadow.java` (coming soon)

## How Wrappers Work

1. **Wrap your LLM calls** with shadow mode functions
2. **LLM executes normally** and returns response to user
3. **Cache operations run in background** (search + add if miss)
4. **Shadow data logged** for analysis (Redis or file)
5. **Zero impact** on production performance

## Python Wrapper

### Installation
```bash
# Download the wrapper
curl -O https://raw.githubusercontent.com/redis/langcache-shadow-mode/main/wrappers/python/langcache_shadow.py

# Install dependencies (if not already installed)
pip install requests redis
```

### Configuration
```bash
export LANGCACHE_SHADOW_MODE=true
export LANGCACHE_API_KEY=your-api-key
export LANGCACHE_CACHE_ID=your-cache-id
export LANGCACHE_BASE_URL=https://api.langcache.com
export REDIS_URL=redis://localhost:6379  # Optional
```

### Usage Examples

#### OpenAI Integration
```python
from langcache_shadow import shadow_llm_call
import openai

# Before
response = openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "What is AI?"}]
)

# After
response = shadow_llm_call(
    openai.chat.completions.create,
    "What is AI?",
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "What is AI?"}]
)
```

#### Manual Tracking
```python
from langcache_shadow import track

# Your existing LLM call
response = openai.chat.completions.create(...)
response_text = response.choices[0].message.content

# Add shadow tracking
track("What is AI?", response_text)
```

#### LangChain Integration
```python
from langcache_shadow import shadow_llm_call
from langchain.llms import OpenAI

llm = OpenAI()

# Wrap LangChain calls
response = shadow_llm_call(
    llm.invoke,
    "What is machine learning?",
    "What is machine learning?"
)
```

## Node.js Wrapper

### Installation
```bash
# Download the wrapper
curl -O https://raw.githubusercontent.com/redis/langcache-shadow-mode/main/wrappers/nodejs/langcache-shadow.js

# Install dependencies (if not already installed)
npm install redis
```

### Configuration
```bash
export LANGCACHE_SHADOW_MODE=true
export LANGCACHE_API_KEY=your-api-key
export LANGCACHE_CACHE_ID=your-cache-id
export LANGCACHE_BASE_URL=https://api.langcache.com
export REDIS_URL=redis://localhost:6379  # Optional
```

### Usage Examples

#### OpenAI Integration
```javascript
const { shadowLlmCall } = require('./langcache-shadow');
const OpenAI = require('openai');

const openai = new OpenAI();

// Before
const response = await openai.chat.completions.create({
    model: "gpt-4o-mini",
    messages: [{ role: "user", content: "What is AI?" }]
});

// After
const response = await shadowLlmCall(
    () => openai.chat.completions.create({
        model: "gpt-4o-mini",
        messages: [{ role: "user", content: "What is AI?" }]
    }),
    "What is AI?"
);
```

#### Manual Tracking
```javascript
const { track } = require('./langcache-shadow');

// Your existing LLM call
const response = await openai.chat.completions.create(...);
const responseText = response.choices[0].message.content;

// Add shadow tracking
await track("What is AI?", responseText);
```

#### Express.js Integration
```javascript
const { shadowLlmCall } = require('./langcache-shadow');

app.post('/chat', async (req, res) => {
    const { message } = req.body;
    
    const response = await shadowLlmCall(
        () => openai.chat.completions.create({
            model: "gpt-4o-mini",
            messages: [{ role: "user", content: message }]
        }),
        message
    );
    
    res.json({ response: response.choices[0].message.content });
});
```

## Wrapper Features

### Automatic Response Extraction
Wrappers automatically extract response text from common LLM response formats:
- OpenAI: `response.choices[0].message.content`
- String responses
- Object responses (JSON stringified)

### Error Handling
- Silent failures for shadow operations
- Production LLM calls never affected
- Comprehensive error logging

### Async Operations
- Cache operations run in background threads
- Zero blocking of production responses
- Fire-and-forget logging

### Flexible Logging
- Redis storage (preferred)
- File fallback if Redis unavailable
- Structured JSON format

## Shadow Data Format

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

## Best Practices

1. **Test in Development** - Verify wrapper works with your LLM setup
2. **Monitor Logs** - Check shadow data is being generated
3. **Set Timeouts** - Configure appropriate API timeouts
4. **Handle Errors** - Ensure shadow failures don't affect production
5. **Clean Up** - Remove wrappers when shadow mode testing complete

## Troubleshooting

### No Shadow Data Generated
- Check environment variables are set
- Verify LangCache API credentials
- Test network connectivity

### Performance Impact
- Shadow operations should be async
- Check Redis performance
- Monitor application metrics

### Response Extraction Issues
- Verify LLM response format
- Customize `extractResponseText` function if needed
- Check wrapper logs for errors

## Contributing

To add support for new languages or LLM providers:

1. Follow the existing wrapper patterns
2. Implement async shadow operations
3. Add comprehensive error handling
4. Include usage examples
5. Submit a pull request

## Support

- [Documentation](../docs/)
- [Examples](../examples/)
- [GitHub Issues](https://github.com/redis/langcache-shadow-mode/issues)
