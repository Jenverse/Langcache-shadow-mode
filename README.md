# 🔍 LangCache Shadow Mode

**Test semantic caching risk-free in your production environment**

Shadow Mode lets you validate LangCache's performance alongside your existing LLM applications without affecting your users. See exactly how much you'll save in costs and latency before committing to semantic caching.

https://drive.google.com/file/d/1GFIgK_lHlE3i5srhDxptciQpPLGQbLbL/view?usp=drive_link

---

## 🎯 What is Shadow Mode?

Shadow Mode runs **parallel** to your production LLM calls:

```
User Query
    ↓
Your Application
    ├─► LLM (Production Response) ──► User Gets This ✅
    └─► LangCache (Shadow Test) ──► Data Collection Only 📊
```

- ✅ **Zero Risk**: Users always get LLM responses (never cached)
- ✅ **Zero Changes**: Minimal code modification required  
- ✅ **Real Data**: Test with your actual production queries
- ✅ **Concrete Results**: See exact cost savings and performance gains

---

## 🚀 Quick Start (5 Minutes)

### 1. **Get Your Credentials**
Contact your LangCache representative for:
- API Key
- Cache ID  
- Setup support

### 2. **Install Shadow Mode**
```bash
# Download the setup script
curl -O https://github.com/Jenverse/Langcache-shadow-mode/raw/main/setup/setup.py
python setup.py
```

### 3. **Integrate (One Line Change)**
```python
# BEFORE
response = openai.chat.completions.create(
    model="gpt-4o-mini", 
    messages=[{"role": "user", "content": query}]
)

# AFTER  
from langcache_shadow import shadow_llm_call
response = shadow_llm_call(
    openai.chat.completions.create,
    query,  # ← Add this
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": query}]
)
```

### 4. **Run Your 2-Week Pilot**
- Use your application normally
- Shadow mode collects data automatically
- Get comprehensive analysis and ROI report

**[👉 Full Quick Start Guide](setup/README.md)**

---

## 📊 What You'll Discover

After your 2-week pilot, you'll get a detailed report showing:

### Performance Impact
- **Cache Hit Rate**: % of queries that would be served from cache
- **Latency Improvement**: How much faster responses could be  
- **Similarity Matching**: Quality of semantic search results

### Cost Analysis  
- **Token Savings**: Exact number of LLM tokens saved
- **Monthly Savings**: Dollar amount you'd save each month
- **ROI Timeline**: When LangCache pays for itself

### Usage Insights
- **Peak Times**: When caching provides most value
- **Query Patterns**: Which types of queries benefit most
- **Optimization Opportunities**: How to maximize cache effectiveness

---

## 🎮 See It In Action

### Demo Applications
- **[Simple Chatbot](examples/simple-chatbot/)** - Basic Q&A with shadow mode
- **[RAG Application](examples/rag-application/)** - Document search with caching
- **[Production Example](examples/production-example/)** - Enterprise-grade setup

### Code Changes to Enable Shadow Mode
- **[OpenAI](setup/code-changes-to-enable-shadow-mode/openai-example.py)** - GPT models
- **[Anthropic](setup/code-changes-to-enable-shadow-mode/anthropic-example.py)** - Claude models
- **[Azure OpenAI](setup/code-changes-to-enable-shadow-mode/azure-openai-example.py)** - Enterprise OpenAI
- **[Custom LLM](setup/code-changes-to-enable-shadow-mode/custom-llm-example.py)** - Any API-based LLM

---

## 📁 Repository Guide

### 🚀 **Get Started**
- **[Setup](setup/)** - Everything you need to get running in 5 minutes
- **[Examples](examples/)** - Working demo you can try immediately
- **[How to Analyze Your Data](how-to-analyze-your-data/)** - Tools to analyze your shadow mode results

---

## 🎯 Why Choose Shadow Mode?

### Traditional Approach ❌
- "Trust us, caching will work for you"
- Theoretical performance improvements
- Risk of production issues
- Unclear ROI and business case

### Shadow Mode Approach ✅  
- "Let's prove it with your own data"
- Concrete metrics from your actual queries
- Zero risk to production systems
- Clear ROI with real numbers

---


### Questions?

**Common Questions:**
- *"Will this slow down my application?"* → No, shadow mode runs asynchronously
- *"What if I want to stop early?"* → Just set `LANGCACHE_SHADOW_MODE=false`
- *"Do you see my user data?"* → No, all data stays in your environment
- *"How much work is integration?"* → Usually under 10 lines of code changes

---


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
