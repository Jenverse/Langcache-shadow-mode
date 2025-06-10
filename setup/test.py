#!/usr/bin/env python3
"""
Test script to demonstrate the new shadow mode dataset format
"""

import os
import json
import time
from datetime import datetime

# Set up environment for testing
os.environ['LANGCACHE_SHADOW_MODE'] = 'true'
os.environ['LANGCACHE_API_KEY'] = 'test-api-key'
os.environ['LANGCACHE_CACHE_ID'] = 'test-cache-id'
os.environ['LANGCACHE_BASE_URL'] = 'https://api.langcache.com'

# Import the updated shadow wrapper
from wrappers.python.langcache_shadow import shadow_llm_call

# Mock OpenAI response class for testing
class MockOpenAIResponse:
    def __init__(self, content, model="gpt-4o-mini", tokens=128):
        self.choices = [MockChoice(content)]
        self.model = model
        self.usage = MockUsage(tokens)

class MockChoice:
    def __init__(self, content):
        self.message = MockMessage(content)

class MockMessage:
    def __init__(self, content):
        self.content = content

class MockUsage:
    def __init__(self, total_tokens):
        self.total_tokens = total_tokens

# Mock LLM function
def mock_openai_call(model="gpt-4o-mini", messages=None, **kwargs):
    """Mock OpenAI API call"""
    time.sleep(0.5)  # Simulate API latency
    query = messages[0]["content"] if messages else "test query"
    
    # Simulate different responses based on query
    if "API key" in query:
        response = "To reset your API key, go to your account settings and click 'Generate New Key'."
    elif "hello" in query.lower():
        response = "Hello! How can I help you today?"
    else:
        response = f"This is a mock response to: {query}"
    
    return MockOpenAIResponse(response, model, len(response) // 4)

def test_shadow_mode():
    """Test the shadow mode with various queries"""
    print("🔍 Testing LangCache Shadow Mode Dataset Generation")
    print("=" * 60)
    
    test_queries = [
        "How do I reset my API key?",
        "Hello, how are you?",
        "What is machine learning?",
        "How do I update my API keys?",  # Similar to first query
        "Hi there!"  # Similar to second query
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n📝 Test {i}: {query}")
        
        # Call with shadow mode
        response = shadow_llm_call(
            mock_openai_call,
            query,
            model="openai/gpt-4o-mini",
            messages=[{"role": "user", "content": query}]
        )
        
        print(f"✅ Response: {response.choices[0].message.content[:50]}...")
        
        # Small delay between requests
        time.sleep(0.1)
    
    print(f"\n📊 Shadow data logged to: shadow_mode.log")
    print("🔍 Check the log file to see the dataset format!")

def show_sample_dataset():
    """Show what the dataset format looks like"""
    print("\n📋 Expected Dataset Format:")
    print("-" * 40)
    
    sample_data = {
        "request_id": "550e8400-e29b-41d4-a716-446655440000",
        "ts_request": "2025-01-27T15:04:32.123Z",
        "query": "How do I reset my API key?",
        "rag_response": "To reset your API key, go to your account settings and click 'Generate New Key'.",
        "cache_hit": True,
        "cache_query": "How do I update my API keys?",
        "cache_response": "You can update your API keys in the account settings section.",
        "vector_distance": 0.14,
        "cached_id": "faq:api-reset:dskjfhkjsdg",
        "latency_cache_ms": 8.0,
        "latency_llm_ms": 612.0,
        "tokens_llm": 128,
        "model_name": "openai/gpt-4o-mini",
        "langcache_version": "v0.9.1"
    }
    
    print(json.dumps(sample_data, indent=2))

if __name__ == "__main__":
    show_sample_dataset()
    
    # Note: Actual testing requires LangCache API access
    print("\n⚠️  Note: To run actual tests, you need:")
    print("   1. Valid LangCache API credentials")
    print("   2. Redis instance (optional)")
    print("   3. Update environment variables in .env file")
    print("\n🚀 To test with real data:")
    print("   python test_shadow_dataset.py")
