# LangCache Shadow Mode

A comprehensive shadow mode implementation for Redis LangCache that enables risk-free validation of semantic caching performance in production environments.

## 🎯 Overview

Shadow mode allows you to run LangCache alongside your existing LLM applications without affecting production traffic. It mirrors queries to both your LLM and the semantic cache, logs comparison data (hit rates, latency, similarity scores), and provides detailed analytics - all while serving only LLM responses to end users.

## 🏗️ Architecture

```
User Query
    ↓
Application
    ├─► LLM (Production Response) ──► User
    └─► LangCache (Shadow Analysis) ──► Logs Only
```

## 🌟 Key Benefits

✅ **Zero Risk** - Production traffic unaffected
✅ **Real Performance Data** - Actual cache hit rates and latency comparisons
✅ **Trust Building** - Concrete metrics for stakeholders
✅ **Easy Integration** - Minimal code changes required
✅ **Comprehensive Analytics** - Detailed logging and reporting

## 📁 Repository Structure

```
LangCache-Shadow-Mode/
├── wrappers/                    # Language-specific wrapper implementations
│   ├── python/                  # Python wrapper for shadow mode
│   ├── nodejs/                  # Node.js wrapper for shadow mode
│   ├── go/                      # Go wrapper for shadow mode
│   └── java/                    # Java wrapper for shadow mode
├── langcache-operations/        # LangCache API wrapper service
├── examples/                    # Example implementations
│   ├── flask-app/              # Flask application example
│   ├── express-app/            # Express.js application example
│   └── spring-boot-app/        # Spring Boot application example
├── analytics/                   # Analytics and reporting tools
├── docs/                       # Documentation
└── tests/                      # Test suites
```

## 🚀 Quick Start

### Option 1: Wrapper Functions (Recommended)

#### Python
```python
# Download python/langcache_shadow.py to your project
from langcache_shadow import shadow_llm_call

# Replace your LLM calls with the wrapper
response = shadow_llm_call(
    llm_function=openai.chat.completions.create,
    query="What is AI?",
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "What is AI?"}]
)
```

#### Node.js
```javascript
// Download nodejs/langcache-shadow.js to your project
const { shadowLlmCall } = require('./langcache-shadow');

// Replace your LLM calls with the wrapper
const response = await shadowLlmCall(
    () => openai.chat.completions.create({
        model: "gpt-4o-mini",
        messages: [{ role: "user", content: query }]
    }),
    query
);
```

### Option 2: API Wrapper Service

```bash
# Run the LangCache operations wrapper
cd langcache-operations/embeddings
python main.py

# Set shadow mode environment variable
export LANGCACHE_SHADOW_MODE=true
```

## ⚙️ Configuration

Set these environment variables:

```bash
export LANGCACHE_API_KEY=your-langcache-api-key
export LANGCACHE_CACHE_ID=your-cache-id
export LANGCACHE_BASE_URL=https://api.langcache.com
export REDIS_URL=redis://localhost:6379
export LANGCACHE_SHADOW_MODE=true
```

## 📊 Analytics & Reporting

Shadow mode collects comprehensive data for analysis:

```json
{
  "request_id": "uuid4",
  "timestamp": "2025-01-27T15:04:32.123Z",
  "query": "How do I reset my API key?",
  "llm_response": "To reset your API key, go to Settings...",
  "cache_hit": true,
  "cache_response": "You can reset your API key by visiting...",
  "similarity_score": 0.89,
  "cache_latency_ms": 8,
  "llm_latency_ms": 612,
  "model_name": "openai/gpt-4o-mini"
}
```

## 📖 Documentation

- [Getting Started Guide](docs/getting-started.md)
- [Quick Reference](docs/quick-reference.md)
- [Troubleshooting Guide](docs/troubleshooting.md)
- [Wrapper Implementation Guide](docs/wrappers.md)
- [Postman Collection](docs/postman-collection.json)
- [Analytics & Reporting](docs/analytics.md)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- [Documentation](docs/)
- [Issues](https://github.com/redis/langcache-shadow-mode/issues)
- [Discussions](https://github.com/redis/langcache-shadow-mode/discussions)
