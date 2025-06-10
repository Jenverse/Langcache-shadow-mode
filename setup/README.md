# 🚀 Setup - Get LangCache Shadow Mode Running

**Everything you need to get shadow mode running in 5 minutes**

---

## 📁 What's in this folder:

### **🎯 Start Here (Run These First)**
- **setup.py** - Automated setup script (run this first!)
- **test.py** - Verify your setup is working

### **📦 Core Shadow Mode Files (The Main Integration Files)**
- **shadow-wrapper-python/** - Contains `langcache_shadow.py` - the Python file you import
- **shadow-wrapper-nodejs/** - Contains `langcache-shadow.js` - the Node.js file you import

### **📋 Code Changes to Enable Shadow Mode (Copy & Paste Ready)**
- **code-changes-to-enable-shadow-mode/** - Exact code changes for different LLM providers:
  - `openai-example.py` - For OpenAI GPT models
  - `anthropic-example.py` - For Anthropic Claude models
  - `azure-openai-example.py` - For Azure OpenAI
  - `custom-llm-example.py` - For any other LLM API

### **⚙️ Configuration Help**
- **data-storage.md** - How to store shadow data (Redis vs files)
- **redis-configuration.md** - Redis setup examples
- **troubleshooting.md** - Common issues and solutions

---

## 🤔 **What's the Difference?**

### **Shadow Wrapper Files** = The Core Integration
- These contain the main `shadow_llm_call()` function
- You download ONE of these based on your programming language
- **Python users**: Get `shadow-wrapper-python/langcache_shadow.py`
- **Node.js users**: Get `shadow-wrapper-nodejs/langcache-shadow.js`

### **Code Changes** = Exact Changes to Enable Shadow Mode
- These show you exactly what code to change for your specific LLM provider
- Copy the example that matches your LLM (OpenAI, Anthropic, etc.)
- Paste it into your application and modify as needed

---

## 🚀 Quick Start (5 Minutes)

### 1. Run the Setup Script
```bash
python setup.py
```
This will:
- Download the shadow wrapper for your language
- Set up environment variables
- Install dependencies
- Create test files

### 2. Test Your Setup
```bash
python test.py
```
This verifies everything is working correctly.

### 3. Make the Code Changes
The setup script downloaded everything you need. Now just make this simple change to your code:

**BEFORE (your current code):**
```python
import openai
response = openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": user_question}]
)
```

**AFTER (with shadow mode):**
```python
import openai
from langcache_shadow import shadow_llm_call

response = shadow_llm_call(
    openai.chat.completions.create,
    user_question,  # ← Add this line
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": user_question}]
)
```

**That's it!** Just wrap your LLM call with `shadow_llm_call()` and add the user question as a parameter.

### 4. Start Collecting Data
- Run your application normally
- Users get the same responses as before
- Shadow mode collects performance data in the background
- Check `shadow_mode.log` to see the data

---


**You'll be collecting shadow mode data in minutes!** 🎯
