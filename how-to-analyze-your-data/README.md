# 📊 How to Analyze Your Shadow Mode Data

**After running shadow mode for a few days or weeks, use these tools to analyze your results and make data-driven decisions about LangCache.**

---

## 📁 What's in this folder:

### **📊 Analysis Tools**
- **analyze_pilot_data.py** - Main analysis script (run this!)
- **dataset-format.md** - Understanding your shadow data structure

### **📋 Pilot Program Materials**
- **PILOT_GUIDE.md** - Complete 2-week pilot program guide

---

## 🚀 Quick Analysis (5 Minutes)

### 1. Run the Analysis Script
```bash
# Analyze your shadow data
python analyze_pilot_data.py --file ../shadow_mode.log
```

### 2. Get Your Results
```
🎯 LANGCACHE SHADOW MODE RESULTS
================================
Total Queries: 1,247
Cache Hit Rate: 34.2%
Average Latency Improvement: 89%
Estimated Monthly Cost Savings: $847
ROI Timeline: 2.3 months
```

### 3. Make Your Decision
- **Hit rate > 20%**: LangCache will provide good value
- **Latency improvement > 50%**: Significant performance gains
- **Monthly savings > $100**: Clear cost benefits

---

## 📊 What the Analysis Shows You

### **Performance Metrics**
- **Cache Hit Rate**: % of queries that would be served from cache
- **Latency Improvement**: How much faster cache responses are
- **Similarity Scores**: Quality of semantic matching

### **Cost Analysis**
- **Token Savings**: Exact number of LLM tokens saved
- **Monthly Cost Savings**: Dollar amount you'd save each month
- **ROI Timeline**: When LangCache pays for itself

### **Usage Insights**
- **Peak Times**: When caching provides most value
- **Query Patterns**: Which types of queries benefit most
- **Optimization Opportunities**: How to maximize cache effectiveness

---

## 📋 Understanding Your Data

### **Shadow Data Format**
Each query in your `shadow_mode.log` looks like this:

```json
{
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "ts_request": "2025-01-27T15:04:32.123Z",
  "query": "What is machine learning?",
  "rag_response": "Machine learning is a subset of AI...",
  "cache_hit": true,
  "cache_query": "How does machine learning work?",
  "cache_response": "Machine learning works by...",
  "vector_distance": 0.14,
  "cached_id": "ml-basics-001",
  "latency_cache_ms": 12.5,
  "latency_llm_ms": 847.2,
  "tokens_llm": 156,
  "model_name": "openai/gpt-4o-mini",
  "langcache_version": "v0.9.1"
}
```

### **Key Fields to Understand**
- **cache_hit**: `true` = found similar query, `false` = new query
- **vector_distance**: Lower = more similar (0.0 = identical, 1.0 = completely different)
- **latency_llm_ms**: Time for LLM response
- **latency_cache_ms**: Time for cache search
- **tokens_llm**: Cost indicator (fewer tokens = lower cost)

---

## 🎯 Making Your Decision

### **Strong Case for LangCache** ✅
- Hit rate > 30%
- Latency improvement > 70%
- Monthly savings > $500
- High query volume (>1000/week)

### **Good Case for LangCache** ✅
- Hit rate > 20%
- Latency improvement > 50%
- Monthly savings > $100
- Moderate query volume (>500/week)

### **Weak Case for LangCache** ⚠️
- Hit rate < 15%
- Latency improvement < 30%
- Monthly savings < $50
- Low query volume (<100/week)

---

## 📈 Advanced Analysis

### **Custom Analysis**
```bash
# Analyze specific time periods
python analyze_pilot_data.py --file shadow_mode.log --start-date 2025-01-01 --end-date 2025-01-07

# Focus on high-similarity matches only
python analyze_pilot_data.py --file shadow_mode.log --min-similarity 0.8

# Analyze by query type
python analyze_pilot_data.py --file shadow_mode.log --group-by-hour
```

### **Export Results**
```bash
# Generate detailed report
python analyze_pilot_data.py --file shadow_mode.log --export-csv results.csv

# Create presentation-ready summary
python analyze_pilot_data.py --file shadow_mode.log --summary-only > summary.txt
```

---

## 🎉 Next Steps

### **If Results Look Good**
1. **Contact LangCache** to discuss production deployment
2. **Plan your rollout** strategy (gradual vs full deployment)
3. **Set up monitoring** for production cache performance
4. **Calculate exact ROI** based on your usage patterns

### **If Results Need Improvement**
1. **Extend the pilot** to collect more data
2. **Optimize query patterns** to improve hit rates
3. **Adjust similarity thresholds** for better matching
4. **Focus on high-value use cases** first

### **If Results Don't Meet Expectations**
1. **Analyze why** hit rates were low
2. **Consider different use cases** that might benefit more
3. **Evaluate alternative solutions** for your specific needs
4. **Keep LangCache in mind** for future projects

---

## 📞 Get Help

### **Questions About Your Results?**
- 📧 **Email**: analysis@langcache.com
- 📱 **Schedule a call**: [Calendar link]
- 💬 **Your LangCache rep**: Direct support

### **Need Custom Analysis?**
Our team can help you:
- Interpret complex results
- Optimize for your specific use case
- Plan your production deployment
- Calculate detailed ROI projections

**Your shadow mode data contains valuable insights - let's help you unlock them!** 🚀
