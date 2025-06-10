# 🤖 Simple Chatbot - LangCache Shadow Mode Demo

**A basic chatbot that demonstrates shadow mode using the exact same integration method from the setup folder.**

## 🎯 What This Shows

- ✅ **Exact same integration** as taught in setup folder
- ✅ **Real shadow mode data collection** in background
- ✅ **Zero user impact** - users get normal responses
- ✅ **Live status monitoring** - see data being collected
- ✅ **Data analysis dashboard** - view metrics and logs in table format
- ✅ **Simple, clear code** - easy to understand

## 🚀 Quick Start

### 1. Copy the Shadow Wrapper
```bash
# Copy from setup folder
cp ../setup/shadow-wrapper-python/langcache_shadow.py .
```

### 2. Set Up Environment
```bash
# Create .env file
cat > .env << EOF
# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key-here

# LangCache Shadow Mode Configuration
LANGCACHE_SHADOW_MODE=true
LANGCACHE_API_KEY=your-langcache-api-key
LANGCACHE_CACHE_ID=your-cache-id
LANGCACHE_BASE_URL=https://api.langcache.com
REDIS_URL=redis://localhost:6379
EOF
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Chatbot
```bash
python app.py
```

### 5. Open in Browser
Visit: http://localhost:5000

## 🎮 Try It Out

### Test Questions
Ask these questions to see shadow mode in action:

1. **"What is machine learning?"** (first time - cache miss)
2. **"How does AI work?"** (different question - cache miss)
3. **"Explain machine learning"** (similar to #1 - should be cache hit!)
4. **"How do artificial intelligence systems work?"** (similar to #2 - should be cache hit!)

### What to Watch
- **Shadow Mode Status** - Shows if data collection is working
- **Data Count** - Increases with each question
- **📊 Data Analysis Tab** - Click "View Data Analysis" to see:
  - Real-time metrics (hit rate, latency, cost savings)
  - Complete log data in table format
  - Similarity scores and performance analysis
- **Log File** - Check `shadow_mode.log` for raw detailed data

## 📊 Understanding the Data

Each question generates shadow data like this:

```json
{
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "ts_request": "2025-01-27T15:04:32.123Z",
  "query": "What is machine learning?",
  "rag_response": "Machine learning is a subset of AI...",
  "cache_hit": false,
  "cache_query": null,
  "cache_response": null,
  "vector_distance": null,
  "cached_id": null,
  "latency_cache_ms": 12.5,
  "latency_llm_ms": 847.2,
  "tokens_llm": 156,
  "model_name": "openai/gpt-4o-mini",
  "langcache_version": "v0.9.1"
}
```

### Key Fields
- **cache_hit**: `true` = found similar question, `false` = new question
- **vector_distance**: Lower = more similar (0.0 = identical)
- **latency_llm_ms**: Time for OpenAI response
- **latency_cache_ms**: Time for cache search

## 🔍 The Integration Code

This example uses **exactly the same integration** as the setup folder:

```python
# BEFORE (without shadow mode)
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": user_message}]
)

# AFTER (with shadow mode)
from langcache_shadow import shadow_llm_call

response = shadow_llm_call(
    client.chat.completions.create,
    user_message,  # ← Add this parameter
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": user_message}]
)
```

**That's it!** Just one import and one parameter change.

## 📈 Expected Results

After chatting for a while, you should see:

### Cache Hits Increasing
- Similar questions start getting cache hits
- Response times improve for cached queries
- Token usage decreases for cache hits

### Performance Data
- Average LLM latency: ~800ms
- Average cache latency: ~15ms
- Potential latency improvement: ~98%

## 🎯 What This Proves

1. **Integration is simple** - just wrap your LLM calls
2. **Zero user impact** - users get normal responses
3. **Data collection works** - shadow logs capture everything
4. **Semantic matching works** - similar questions get cache hits
5. **Performance gains are real** - cache is much faster

## 🔧 Customization

### Change the Model
```python
# Use a different OpenAI model
response = shadow_llm_call(
    client.chat.completions.create,
    user_message,
    model="gpt-4",  # ← Change this
    messages=[{"role": "user", "content": user_message}]
)
```

### Add System Prompts
```python
response = shadow_llm_call(
    client.chat.completions.create,
    user_message,
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": user_message}
    ]
)
```

## 📊 Analyze Your Data

```bash
# View shadow data
tail -f shadow_mode.log

# Count cache hits vs misses
grep '"cache_hit": true' shadow_mode.log | wc -l
grep '"cache_hit": false' shadow_mode.log | wc -l

# Analyze with provided tools
python ../docs/analysis-tools/analyze_pilot_data.py --file shadow_mode.log
```

This simple example proves that LangCache shadow mode works with real applications and provides concrete data for decision-making! 🚀
