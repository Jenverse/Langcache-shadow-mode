# LangCache Demo LLM Application

A professional Flask-based web application demonstrating semantic caching with Redis LangCache. This application showcases how semantic similarity matching can dramatically improve LLM response times and reduce API costs.

## 🌟 Features

### Core Functionality
- **Semantic Similarity Matching**: Finds semantically similar queries using vector embeddings
- **Real-time Cache Operations**: Instant cache hits vs. LLM generation
- **Professional UI**: Clean, modern interface with Redis LangCache branding
- **Comprehensive Analytics**: Detailed logging and performance metrics

### User Interface
- **Chat Interface**: Clean, intuitive query input and response display
- **Cache Indicators**: Clear visual indicators for cache hits vs. LLM responses
- **Analytics Dashboard**: Real-time logs with cache operations history
- **Performance Metrics**: Response time comparisons and cache hit ratios

### Technical Features
- **Multiple Model Support**: Configurable embedding and LLM models
- **RESTful API**: Easy integration endpoints
- **Health Monitoring**: LangCache service health checks
- **Error Handling**: Graceful fallbacks and error recovery

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Flask App     │    │  Redis LangCache│
│                 │◄──►│                 │◄──►│   (Managed)     │
│  - Chat UI      │    │ - Query Handler │    │ - Semantic Search│
│  - Analytics    │    │ - Cache Logic   │    │ - Vector Storage│
│  - Logs         │    │ - Health Check  │    │ - Similarity    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   Gemini API    │
                       │  (LLM Provider) │
                       └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Redis LangCache service access
- Google Gemini API key

### Installation

1. **Navigate to the LLM app directory**
   ```bash
   cd llm-app
   ```

2. **Install dependencies**
   ```bash
   pip install -r ../requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp ../.env.example ../.env
   # Edit .env with your actual API keys
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   - Open: `http://localhost:5002`
   - Start asking questions to see semantic caching in action!

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini API key | ✅ Yes |
| `LANGCACHE_BASE_URL` | LangCache service URL | ✅ Yes |
| `LANGCACHE_API_KEY` | LangCache authentication token | ✅ Yes |
| `LANGCACHE_CACHE_ID` | Your cache instance ID | ✅ Yes |

### Model Configuration

The application supports multiple models:

**Embedding Models:**
- `openAI-text-embedding-large` (default)
- `Redis-LangCache-Embed`

**LLM Models:**
- `Gemini-1.5-flash` (default)

## 🎯 Usage Examples

### Semantic Matching Examples

These queries demonstrate semantic similarity matching:

```
Query 1: "What is machine learning?"
Query 2: "What is ML?"
Result: Cache HIT - semantically similar

Query 1: "How do neural networks work?"
Query 2: "Explain neural nets"
Result: Cache HIT - semantically similar

Query 1: "What is artificial intelligence?"
Query 2: "Define AI"
Result: Cache HIT - semantically similar
```

### Performance Comparison

| Scenario | Response Time | Source |
|----------|---------------|---------|
| **Cache Miss** (first time) | 5-15 seconds | 🔄 LLM Generation |
| **Cache Hit** (similar query) | 0.5-1 second | 🗄️ Redis LangCache |
| **Speed Improvement** | **40x+ faster** | ⚡ Dramatic improvement |

## 📊 API Endpoints

### Query Processing
```http
POST /query
Content-Type: application/json

{
  "query": "What is machine learning?",
  "use_cache": true,
  "llm_model": "Gemini-1.5-flash",
  "embedding_model": "openAI-text-embedding-large"
}
```

**Response:**
```json
{
  "response": "Machine learning is...",
  "time_taken": 0.8,
  "source": "cache",
  "similarity": 0.95
}
```

### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "langcache_configured": true,
  "langcache_health": {
    "checks": [...],
    "ok": true
  },
  "base_url": "https://your-langcache-service.com",
  "cache_id": "your-cache-id"
}
```

### Analytics
```http
GET /logs
```

**Response:**
```json
{
  "operations": [...],
  "total_operations": 10,
  "cache_hits": 7,
  "cache_misses": 3
}
```

## 🎨 UI Components

### Chat Interface
- **Query Input**: Text input with submit button
- **Response Display**: Formatted responses with source indicators
- **Cache Indicators**: 
  - 🗄️ **Served from Redis LangCache** (green theme)
  - ✓ **From LLM** (red theme)

### Analytics Dashboard
- **Cache ID Display**: Shows current cache instance
- **Real-time Stats**: Total operations, hits, misses
- **Detailed Logs Table**: 
  - Timestamp
  - Query text
  - Source (Cache/LLM)
  - Matched query
  - Similarity score
  - Response time
  - Model used

## 🔧 Technical Implementation

### Cache Logic Flow

1. **Query Received**: User submits a query
2. **Cache Search**: Search LangCache for semantic matches
3. **Similarity Check**: Compare embeddings with threshold
4. **Cache Hit**: Return cached response if match found
5. **Cache Miss**: Generate new response via LLM
6. **Cache Store**: Store new response for future matches
7. **Response**: Return result with performance metrics

### Error Handling

- **LangCache Unavailable**: Graceful fallback to LLM
- **API Key Issues**: Clear error messages
- **Network Errors**: Retry logic and timeouts
- **Invalid Queries**: Input validation and sanitization

### Performance Optimization

- **Async Operations**: Non-blocking cache operations
- **Connection Pooling**: Efficient HTTP connections
- **Timeout Management**: Configurable request timeouts
- **Memory Management**: Efficient log storage

## 🛠️ Development

### Project Structure
```
llm-app/
├── app.py                 # Main Flask application
├── templates/
│   └── index.html        # Main UI template
├── static/
│   ├── css/
│   │   └── styles.css    # Application styles
│   ├── js/
│   │   └── main.js       # Frontend JavaScript
│   └── images/
│       └── redis-logo.svg # Redis branding assets
└── README.md             # This file
```

### Key Files

- **`app.py`**: Main Flask application with all routes and logic
- **`templates/index.html`**: Single-page application template
- **`static/css/styles.css`**: Professional styling with green theme
- **`static/js/main.js`**: Frontend JavaScript for UI interactions

## 🎯 Customization

### Styling
- **Color Scheme**: Green theme for cache hits, red for LLM
- **Icons**: Database emoji for cache, checkmarks for LLM
- **Typography**: Clean, professional fonts
- **Layout**: Responsive design for all screen sizes

### Functionality
- **Models**: Easy to add new embedding/LLM models
- **Thresholds**: Configurable similarity thresholds
- **Logging**: Detailed operation logging
- **Metrics**: Comprehensive performance tracking

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

MIT License - see the [LICENSE](../LICENSE) file for details.

---

**Built with ❤️ for the LangCache community**
