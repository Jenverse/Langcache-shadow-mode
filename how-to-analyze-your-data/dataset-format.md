# LangCache Shadow Mode Pilot Dataset Format

## 🎯 Overview

This document describes the exact dataset format generated during the **two-week LangCache shadow mode pilot experiment**. The system mirrors 100% of production traffic to both your LLM/RAG system (ground truth) and the semantic cache (shadow mode) for comprehensive analysis.

## 🏗️ Architecture

```
User ⇢ Orchestrator ─┬─► LLM / RAG (ground‑truth) ──► User
                    └─► Semantic Cache (shadow, Redis) ──► Logs Only
```

- **100% traffic mirroring** for two-week pilot (24h dry-run first)
- **Async observer** logs caching operations without affecting production
- **Single versioned JSON line** per query lifecycle

## 📋 Dataset Schema

Each query generates exactly **one JSON record** with the following structure:

```json
{
  "request_id": "uuid4",
  "ts_request": "2025-05-27T15:04:32.123Z",
  "query": "How do I reset my API key?",
  "rag_response": "...",
  "cache_hit": true,
  "cache_query": "How do I update my API keys?",
  "cache_response": ".....",
  "vector_distance": 0.14,
  "cached_id": "faq:api-reset:dskjfhkjsdg",
  "latency_cache_ms": 8,
  "latency_llm_ms": 612,
  "tokens_llm": 128,
  "model_name": "openai/gpt-4o-mini",
  "langcache_version": "v0.9.1"
}
```

## 📊 Field Definitions

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `request_id` | string | Unique identifier for each query | `"550e8400-e29b-41d4-a716-446655440000"` |
| `ts_request` | string | ISO 8601 timestamp when query was received | `"2025-05-27T15:04:32.123Z"` |
| `query` | string | Original user query | `"How do I reset my API key?"` |
| `rag_response` | string | Ground truth response from LLM/RAG | `"To reset your API key, go to..."` |
| `cache_hit` | boolean | Whether cache found a similar query | `true` |
| `cache_query` | string/null | Most similar cached query (if hit) | `"How do I update my API keys?"` |
| `cache_response` | string/null | Cached response (if hit) | `"You can update your API keys..."` |
| `vector_distance` | float/null | Semantic distance (0.0 = identical) | `0.14` |
| `cached_id` | string/null | Unique ID of cached entry | `"faq:api-reset:dskjfhkjsdg"` |
| `latency_cache_ms` | float | Cache search latency in milliseconds | `8.0` |
| `latency_llm_ms` | float | LLM response latency in milliseconds | `612.0` |
| `tokens_llm` | integer | Token count for LLM response | `128` |
| `model_name` | string | LLM model used | `"openai/gpt-4o-mini"` |
| `langcache_version` | string | LangCache version | `"v0.9.1"` |

## 🔧 Implementation

### Updated Shadow Mode Wrapper

The Python wrapper (`wrappers/python/langcache_shadow.py`) has been updated to generate this exact format:

```python
from langcache_shadow import shadow_llm_call

# Replace your LLM calls
response = shadow_llm_call(
    openai.chat.completions.create,
    query="How do I reset my API key?",
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": query}]
)
```

### Data Storage

- **Primary**: Redis with keys `shadow:{request_id}`
- **Fallback**: JSONL file `shadow_mode.log`
- **Format**: One JSON object per line (JSONL)

## 📈 Analysis Tools

### Quick Analysis
```bash
# Analyze pilot data
python analyze_pilot_data.py --file shadow_mode.log

# Check Redis data
redis-cli KEYS "shadow:*" | wc -l
```

### Key Metrics Generated

1. **Cache Performance**
   - Hit rate percentage
   - Average similarity scores
   - Vector distance distribution

2. **Latency Analysis**
   - LLM vs Cache response times
   - Performance percentiles (P50, P90, P95, P99)
   - Latency improvement potential

3. **Cost Analysis**
   - Total tokens processed
   - Tokens saved through caching
   - Estimated cost savings

4. **Usage Patterns**
   - Hourly/daily traffic patterns
   - Model usage distribution
   - Peak usage times

## 🎯 Pilot Experiment Goals

### Success Metrics
- ✅ **Hit Rate > 20%**: Semantic cache finding relevant matches
- ✅ **Latency Improvement > 50%**: Cache significantly faster than LLM
- ✅ **Similarity Score > 0.7**: High-quality semantic matching
- ✅ **Zero Production Impact**: No user-facing issues

### Data Collection Period
- **Phase 1**: 24-hour dry run (validation)
- **Phase 2**: 14-day full pilot (data collection)
- **Total**: ~15 days of comprehensive data

## 🔍 Sample Queries & Expected Results

### High Similarity Match (Expected Hit)
```json
{
  "query": "How do I reset my API key?",
  "cache_query": "How do I update my API keys?",
  "vector_distance": 0.12,
  "cache_hit": true
}
```

### Low Similarity (Expected Miss)
```json
{
  "query": "What's the weather today?",
  "cache_query": null,
  "vector_distance": null,
  "cache_hit": false
}
```

## 🚀 Getting Started

1. **Update your wrapper**:
   ```bash
   # Use the updated Python wrapper
   cp wrappers/python/langcache_shadow.py your_project/
   ```

2. **Configure environment**:
   ```bash
   export LANGCACHE_SHADOW_MODE=true
   export LANGCACHE_API_KEY=your-api-key
   export LANGCACHE_CACHE_ID=your-cache-id
   ```

3. **Integrate with your LLM calls**:
   ```python
   # Minimal change to existing code
   response = shadow_llm_call(your_llm_function, query, **kwargs)
   ```

4. **Monitor data collection**:
   ```bash
   # Check log file
   tail -f shadow_mode.log
   
   # Analyze results
   python analyze_pilot_data.py --file shadow_mode.log
   ```

## 📋 Data Quality Checklist

- ✅ Each record contains all required fields
- ✅ Timestamps are in ISO 8601 format with milliseconds
- ✅ Vector distances are between 0.0 and 1.0
- ✅ Latencies are in milliseconds (float)
- ✅ Token counts are positive integers
- ✅ Request IDs are unique UUIDs

## 🎉 Expected Outcomes

After the two-week pilot, you'll have:

1. **Comprehensive dataset** with thousands of real user queries
2. **Performance benchmarks** comparing LLM vs cache latency
3. **Cost analysis** showing potential savings
4. **Similarity insights** revealing semantic matching quality
5. **Usage patterns** identifying peak times and common queries
6. **Confidence metrics** for production deployment decision

This dataset format provides all the essentials for making data-driven decisions about semantic caching deployment! 🚀
