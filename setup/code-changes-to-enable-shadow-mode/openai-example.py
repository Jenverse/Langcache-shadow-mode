#!/usr/bin/env python3
"""
LangCache Shadow Mode - OpenAI Integration Example

This example shows EXACTLY what code changes you need to make to enable
shadow mode in your OpenAI application. It's just 2 simple changes!

WHAT IS SHADOW MODE?
- Your users always get OpenAI responses (zero risk)
- Shadow mode tests LangCache in the background
- Collects data on cache hits, latency, and cost savings
- Helps you decide if LangCache is worth it for your use case
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ============================================================================
# STEP 1: Add these imports (only change to your imports)
# ============================================================================

import openai
from langcache_shadow import shadow_llm_call  # ← ADD THIS LINE

# Configure OpenAI client (no changes needed)
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ============================================================================
# EXAMPLE 1: Basic Chat Function
# ============================================================================

def chat_with_openai_BEFORE(user_message):
    """
    BEFORE: Your original OpenAI code (what you have now)
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ],
        max_tokens=150,
        temperature=0.7
    )
    return response.choices[0].message.content

def chat_with_openai_AFTER(user_message):
    """
    AFTER: Same code with shadow mode enabled (what you change it to)

    WHAT CHANGED:
    1. Wrapped the OpenAI call with shadow_llm_call()
    2. Added user_message as the second parameter
    3. Everything else stays exactly the same!
    """
    response = shadow_llm_call(                    # ← CHANGE 1: Wrap with shadow_llm_call
        client.chat.completions.create,           # ← Your original OpenAI function
        user_message,                             # ← CHANGE 2: Add user message parameter
        # Everything below stays exactly the same:
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ],
        max_tokens=150,
        temperature=0.7
    )
    return response.choices[0].message.content    # ← Same response handling

# ============================================================================
# EXAMPLE 2: Streaming Responses
# ============================================================================

def streaming_BEFORE(user_message):
    """
    BEFORE: Original streaming code
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": user_message}],
        stream=True
    )

    # Handle streaming response
    full_response = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            print(content, end="")
            full_response += content

    return full_response

def streaming_AFTER(user_message):
    """
    AFTER: Same streaming code with shadow mode

    WHAT CHANGED:
    1. Wrapped with shadow_llm_call()
    2. Added user_message parameter
    3. Streaming still works exactly the same!
    """
    response = shadow_llm_call(                    # ← CHANGE 1: Wrap with shadow_llm_call
        client.chat.completions.create,           # ← Your original function
        user_message,                             # ← CHANGE 2: Add user message
        # Everything below stays the same:
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": user_message}],
        stream=True
    )

    # Handle streaming response (no changes needed)
    full_response = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            print(content, end="")
            full_response += content

    return full_response

# ============================================================================
# EXAMPLE 3: Function Calling
# ============================================================================

def function_calling_BEFORE(user_message):
    """
    BEFORE: Original function calling code
    """
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get the current weather",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {"type": "string", "description": "City name"}
                    },
                    "required": ["location"]
                }
            }
        }
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": user_message}],
        tools=tools,
        tool_choice="auto"
    )

    return response

def function_calling_AFTER(user_message):
    """
    AFTER: Same function calling with shadow mode

    WHAT CHANGED:
    1. Wrapped with shadow_llm_call()
    2. Added user_message parameter
    3. Function calling still works exactly the same!
    """
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get the current weather",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {"type": "string", "description": "City name"}
                    },
                    "required": ["location"]
                }
            }
        }
    ]

    response = shadow_llm_call(                    # ← CHANGE 1: Wrap with shadow_llm_call
        client.chat.completions.create,           # ← Your original function
        user_message,                             # ← CHANGE 2: Add user message
        # Everything below stays the same:
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": user_message}],
        tools=tools,
        tool_choice="auto"
    )

    return response

# ============================================================================
# WHAT HAPPENS WHEN YOU RUN THIS?
# ============================================================================

def demo_shadow_mode():
    """
    This function demonstrates shadow mode by running the AFTER versions
    and showing you what data gets collected.
    """
    print("🔍 LangCache Shadow Mode - OpenAI Integration Demo")
    print("=" * 60)
    print()
    print("This demo shows you:")
    print("✅ How to change your OpenAI code to enable shadow mode")
    print("✅ What shadow data gets collected")
    print("✅ How your users are completely unaffected")
    print()

    # Example 1: Basic chat with shadow mode
    print("📝 Example 1: Basic Chat with Shadow Mode")
    print("-" * 40)
    user_query = "What are the benefits of renewable energy?"
    print(f"User asks: '{user_query}'")
    print("🔄 Calling OpenAI with shadow mode enabled...")

    response = chat_with_openai_AFTER(user_query)
    print(f"✅ User gets response: '{response[:80]}...'")
    print("🔍 Shadow mode collected data in background (check shadow_mode.log)")
    print()

    # Example 2: Show what shadow mode does
    print("📊 What Shadow Mode Does:")
    print("-" * 40)
    print("1. 🚀 Calls OpenAI API (user gets normal response)")
    print("2. 🔍 Searches LangCache for similar queries")
    print("3. 📝 Logs performance data:")
    print("   - Cache hit/miss")
    print("   - Response latency")
    print("   - Similarity scores")
    print("   - Token usage")
    print("4. 💾 Stores data for analysis")
    print()

    # Example 3: Streaming still works
    print("📝 Example 2: Streaming Still Works")
    print("-" * 40)
    stream_query = "Explain machine learning in simple terms"
    print(f"User asks: '{stream_query}'")
    print("🔄 Streaming response with shadow mode:")

    streaming_AFTER(stream_query)
    print()
    print("✅ Streaming works exactly the same!")
    print("🔍 Shadow data collected for this query too")
    print()

    print("🎉 Demo Complete!")
    print("📊 Check 'shadow_mode.log' to see the collected data")
    print("🔍 Each query generates detailed performance metrics")

# ============================================================================
# RUN THIS TO SEE SHADOW MODE IN ACTION
# ============================================================================

if __name__ == "__main__":
    # Check if OpenAI API key is configured
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY environment variable not set")
        print("Please add your OpenAI API key to your .env file")
        print()
        print("Add this to your .env file:")
        print("OPENAI_API_KEY=your-openai-api-key-here")
        exit(1)

    # Check if shadow mode is configured
    if not os.getenv("LANGCACHE_SHADOW_MODE"):
        print("⚠️  Warning: LANGCACHE_SHADOW_MODE not enabled")
        print("Shadow mode will not collect data")
        print()
        print("To enable shadow mode, add this to your .env file:")
        print("LANGCACHE_SHADOW_MODE=true")
        print("LANGCACHE_API_KEY=your-langcache-api-key")
        print("LANGCACHE_CACHE_ID=your-cache-id")
        print()

    # Run the demo
    demo_shadow_mode()

    print()
    print("=" * 60)
    print("🎯 SUMMARY: How to Enable Shadow Mode in Your App")
    print("=" * 60)
    print()
    print("1. Add this import:")
    print("   from langcache_shadow import shadow_llm_call")
    print()
    print("2. Change your OpenAI calls from:")
    print("   response = client.chat.completions.create(...)")
    print()
    print("3. To this:")
    print("   response = shadow_llm_call(")
    print("       client.chat.completions.create,")
    print("       user_message,  # ← Add this")
    print("       ...  # ← Everything else stays the same")
    print("   )")
    print()
    print("That's it! Your users get normal responses, shadow mode")
    print("collects performance data in the background.")
    print()
    print("📊 Data saved to: shadow_mode.log")
    print("🔍 Each query generates detailed metrics for analysis")
