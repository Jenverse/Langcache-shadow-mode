#!/usr/bin/env python3
"""
Simple Chatbot with LangCache Shadow Mode

This example shows exactly how to integrate shadow mode using the same
method taught in the setup folder. It's a basic Flask chatbot that
demonstrates shadow mode data collection.
"""

import os
from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv
import secrets

# Load environment variables
load_dotenv()

# Import OpenAI and shadow mode (exactly like setup instructions)
import openai
from langcache_shadow import shadow_llm_call

app = Flask(__name__)
# Generate new random secret key on each restart to invalidate old sessions
app.secret_key = secrets.token_hex(32)
app.permanent_session_lifetime = 0  # Sessions expire when browser closes
print(f"🔐 New session key generated - all previous sessions invalidated")

# No default configuration - users must configure their own credentials for security

def get_config_value(key):
    """Get configuration value from session only - no environment fallbacks for security"""
    try:
        # Only use session-configured values (user must configure their own)
        if 'config' in session and key in session['config']:
            return session['config'][key]
    except RuntimeError:
        # Outside request context, skip session check
        pass
    # No fallbacks - return None if not configured by user
    return None

def mask_sensitive_value(value):
    """Mask sensitive values for display - only if there's actually a value"""
    if not value or len(value.strip()) == 0:
        return ''  # Return empty string, not masked placeholder
    if len(value) <= 8:
        return '*' * len(value)
    return value[:4] + '*' * (len(value) - 8) + value[-4:]

# Configure OpenAI
def get_openai_client():
    api_key = get_config_value('openai_api_key')
    if api_key:
        return openai.OpenAI(api_key=api_key)
    return None

# Initialize client as None - will be set when user configures API key
client = None

def chat_with_ai(user_message):
    """
    Chat function using shadow mode - exactly like the setup example
    """
    # BEFORE shadow mode:
    # response = client.chat.completions.create(
    #     model="gpt-4o-mini",
    #     messages=[{"role": "user", "content": user_message}],
    #     max_tokens=150
    # )
    
    # AFTER shadow mode (exactly like setup instructions):
    response = shadow_llm_call(
        client.chat.completions.create,
        user_message,  # ← Add this parameter
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": user_message}],
        max_tokens=150
    )
    
    return response.choices[0].message.content

def chat_with_langcache_live(user_message):
    """Get response from LangCache directly (live mode) with detailed metadata"""
    import requests
    import time

    # LangCache API configuration (use app config)
    langcache_url = get_config_value('langcache_base_url')
    langcache_api_key = get_config_value('langcache_api_key')
    langcache_cache_id = get_config_value('langcache_cache_id')

    print(f"🔧 LIVE MODE DEBUG:")
    print(f"   LangCache URL: {langcache_url}")
    print(f"   API Key: {'✅ Set' if langcache_api_key else '❌ Missing'}")
    print(f"   Cache ID: {'✅ Set' if langcache_cache_id else '❌ Missing'}")

    if not langcache_api_key or not langcache_cache_id:
        print("❌ LIVE MODE: LangCache credentials missing, falling back to OpenAI")
        response = get_openai_response(user_message)
        return {
            'response': response,
            'cached': False,
            'source': 'openai',
            'reason': 'missing_credentials',
            'similarity': None,
            'matched_query': None
        }

    try:
        # First, search LangCache for existing response (same API as shadow mode)
        search_url = f"{langcache_url}/v1/caches/{langcache_cache_id}/search"
        search_payload = {
            "prompt": user_message  # Use 'prompt' like shadow mode, not 'query'
        }

        print(f"🔍 LIVE MODE: Searching LangCache...")
        print(f"   Search URL: {search_url}")

        cache_start = time.time()
        search_response = requests.post(
            search_url,
            headers={
                'Authorization': f'Bearer {langcache_api_key}',
                'Content-Type': 'application/json'
            },
            json=search_payload,
            timeout=10
        )
        cache_latency = round((time.time() - cache_start) * 1000, 1)

        print(f"🔍 LIVE MODE: Search response status: {search_response.status_code}")

        if search_response.status_code == 200:
            search_results = search_response.json()
            print(f"🔍 LIVE MODE: Found {len(search_results)} results")

            # If we have a good match (similarity > 0.8), return cached response
            if search_results and len(search_results) > 0:
                best_match = search_results[0]
                similarity = best_match.get('similarity', 0)
                matched_query = best_match.get('prompt', '')
                cached_response = best_match.get('response', '')

                print(f"🔍 LIVE MODE: Best match similarity: {similarity:.3f}")
                print(f"🔍 LIVE MODE: Matched query: {matched_query[:50]}...")

                if similarity > 0.8:  # High similarity threshold for live mode
                    if cached_response:
                        print(f"🎯 LIVE MODE: Cache HIT! Using cached response")
                        return {
                            'response': cached_response,
                            'cached': True,
                            'source': 'langcache',
                            'similarity': similarity,
                            'matched_query': matched_query,
                            'reason': 'cache_hit',
                            'cache_latency': cache_latency
                        }

                print(f"🔄 LIVE MODE: Similarity too low ({similarity:.3f} < 0.8), getting fresh response")
            else:
                print("🔄 LIVE MODE: No search results, getting fresh response")
        else:
            print(f"❌ LIVE MODE: Search failed with status {search_response.status_code}")
            print(f"   Response: {search_response.text}")

        # No good cache hit, get fresh response from OpenAI
        print("🔄 LIVE MODE: Getting fresh response from OpenAI")
        llm_start = time.time()
        fresh_response = get_openai_response(user_message)
        llm_latency = round((time.time() - llm_start) * 1000, 1)

        # Store the new response in LangCache for future use (same API as shadow mode)
        store_url = f"{langcache_url}/v1/caches/{langcache_cache_id}/entries"
        store_payload = {
            "prompt": user_message,
            "response": fresh_response
        }

        print(f"💾 LIVE MODE: Storing new response in LangCache...")
        store_response = requests.post(
            store_url,
            headers={
                'Authorization': f'Bearer {langcache_api_key}',
                'Content-Type': 'application/json'
            },
            json=store_payload,
            timeout=10
        )

        if store_response.status_code == 200:
            print("💾 LIVE MODE: ✅ Successfully stored new response")
        else:
            print(f"💾 LIVE MODE: ❌ Failed to store response: {store_response.status_code}")

        return {
            'response': fresh_response,
            'cached': False,
            'source': 'openai',
            'similarity': None,
            'matched_query': None,
            'reason': 'cache_miss',
            'llm_latency': llm_latency
        }

    except Exception as e:
        print(f"⚠️ LIVE MODE: LangCache error: {e}")
        response = get_openai_response(user_message)
        return {
            'response': response,
            'cached': False,
            'source': 'openai',
            'reason': f'error: {str(e)}',
            'similarity': None,
            'matched_query': None
        }

def get_openai_response(user_message):
    """Get response directly from OpenAI (without shadow mode)"""
    if not client:
        return "Please configure your OpenAI API key in the Configuration page."

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": user_message}
        ],
        max_tokens=500,
        temperature=0.7
    )

    return response.choices[0].message.content

@app.route('/')
def home():
    """Main chat page"""
    return render_template('index.html')

@app.route('/api/health')
def health_check():
    """Health check endpoint for deployment verification"""
    return jsonify({
        'status': 'healthy',
        'message': 'LangCache Shadow Mode Demo is running!',
        'version': '2.0'
    })

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    import time

    try:
        user_message = request.json.get('message', '')
        mode = request.json.get('mode', 'shadow')  # Default to shadow mode

        if not user_message:
            return jsonify({'error': 'No message provided'}), 400

        start_time = time.time()

        # Get response with metadata
        if mode == 'live':
            response_data = chat_with_langcache_live(user_message)
            if isinstance(response_data, dict):
                ai_response = response_data['response']
                cache_info = response_data
            else:
                ai_response = response_data
                cache_info = {'cached': False, 'source': 'openai'}
        else:
            # Shadow mode: Get AI response while collecting shadow data
            llm_start = time.time()
            ai_response = chat_with_ai(user_message)
            llm_latency = round((time.time() - llm_start) * 1000, 1)
            cache_info = {
                'cached': False,
                'source': 'shadow_mode',
                'llm_latency': llm_latency
            }

        total_latency = round((time.time() - start_time) * 1000, 1)
        cache_info['total_latency'] = total_latency

        return jsonify({
            'response': ai_response,
            'status': 'success',
            'mode': mode,
            'cache_info': cache_info
        })

    except Exception as e:
        # Provide user-friendly error messages
        error_message = str(e).lower()

        if 'unauthorized' in error_message or '401' in error_message:
            user_friendly_error = "🔑 Please enter your OpenAI API key in Configuration. Your API key may be missing or invalid."
        elif 'not found' in error_message or '404' in error_message:
            user_friendly_error = "🔍 Service not found. Please enter your LangCache Base URL in Configuration."
        elif 'connection' in error_message or 'timeout' in error_message:
            user_friendly_error = "🌐 Connection failed. Please check your internet connection and enter valid URLs in Configuration."
        elif 'redis' in error_message:
            user_friendly_error = "📊 Redis connection failed. Please enter your Redis connection URL in Configuration."
        elif 'configure' in error_message or 'api key' in error_message:
            user_friendly_error = "⚙️ Please enter your API keys and configuration settings to get started."
        else:
            user_friendly_error = "⚙️ Please enter your API keys and configuration settings. Visit the Configuration page to set up your credentials."

        return jsonify({
            'error': user_friendly_error,
            'status': 'error',
            'action': 'Please visit the Configuration page to set up your credentials.'
        }), 500

@app.route('/shadow-status')
def shadow_status():
    """Check if shadow mode is working"""
    shadow_enabled = os.getenv('LANGCACHE_SHADOW_MODE', 'false').lower() == 'true'

    # Count shadow data entries from Redis first, then fallback to file
    shadow_count = 0
    data_source = 'none'

    try:
        import redis
        redis_url = get_config_value('redis_url')
        if not redis_url:
            # No Redis configured by user
            shadow_count = 0
            data_source = 'not_configured'
        else:
            redis_client = redis.from_url(redis_url)

        # Count shadow keys in Redis
        shadow_keys = redis_client.keys("shadow:*")
        shadow_count = len(shadow_keys)
        data_source = 'redis'

    except Exception as e:
        # Fallback to file count
        try:
            with open('shadow_mode.log', 'r') as f:
                shadow_count = sum(1 for line in f if line.strip())
            data_source = 'file'
        except FileNotFoundError:
            shadow_count = 0
            data_source = 'none'

    return jsonify({
        'shadow_mode_enabled': shadow_enabled,
        'shadow_data_collected': shadow_count,
        'data_source': data_source
    })

@app.route('/data-analysis')
def data_analysis():
    """Data analysis page"""
    return render_template('data_analysis.html')

@app.route('/config')
def config_page():
    """Configuration page"""
    return render_template('config.html')

@app.route('/api/config', methods=['GET', 'POST'])
def handle_config():
    """Handle configuration API"""
    if request.method == 'GET':
        # Get session config (user-configured values only)
        session_config = session.get('config', {})

        # Return configuration - only mask values that user has actually configured in session
        # For new users, show empty fields with placeholders instead of env defaults
        return jsonify({
            'status': 'success',
            'config': {
                'langcache_base_url': session_config.get('langcache_base_url', ''),
                'langcache_api_key_masked': mask_sensitive_value(session_config.get('langcache_api_key', '')),
                'langcache_cache_id_masked': mask_sensitive_value(session_config.get('langcache_cache_id', '')),
                'openai_api_key_masked': mask_sensitive_value(session_config.get('openai_api_key', '')),
                'redis_url_masked': mask_sensitive_value(session_config.get('redis_url', ''))
            }
        })

    elif request.method == 'POST':
        # Update configuration in session (user-specific)
        try:
            config_data = request.json

            # Initialize session config if not exists
            if 'config' not in session:
                session['config'] = {}

            # Update session config with new values (only if provided and not masked)
            key_mapping = {
                'langcacheBaseUrl': 'langcache_base_url',
                'langcacheApiKey': 'langcache_api_key',
                'langcacheCacheId': 'langcache_cache_id',
                'openaiApiKey': 'openai_api_key',
                'redisUrl': 'redis_url'
            }

            for key, value in config_data.items():
                if value and not value.startswith('*') and len(value.strip()) > 0:  # Don't update masked or empty values
                    if key in key_mapping:
                        session['config'][key_mapping[key]] = value.strip()

            # Mark session as modified
            session.modified = True

            # Reinitialize OpenAI client with new API key
            global client
            client = get_openai_client()

            return jsonify({
                'status': 'success',
                'message': 'Configuration updated successfully! (Session-specific)'
            })

        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'Error updating configuration: {str(e)}'
            }), 500

@app.route('/api/test-connections', methods=['POST'])
def test_connections():
    """Test all configured connections"""
    results = {
        'langcache': False,
        'openai': False,
        'redis': False,
        'all_connected': False
    }

    # Test LangCache connection
    try:
        import requests
        langcache_url = get_config_value('langcache_base_url')
        langcache_api_key = get_config_value('langcache_api_key')
        langcache_cache_id = get_config_value('langcache_cache_id')

        if langcache_url and langcache_api_key and langcache_cache_id:
            test_url = f"{langcache_url}/v1/caches/{langcache_cache_id}/search"
            response = requests.post(
                test_url,
                headers={'Authorization': f'Bearer {langcache_api_key}'},
                json={'prompt': 'test'},
                timeout=5
            )
            results['langcache'] = response.status_code in [200, 404]  # 404 is OK (no results)
    except Exception:
        pass

    # Test OpenAI connection
    try:
        test_client = get_openai_client()
        if test_client:
            response = test_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": "test"}],
                max_tokens=1
            )
            results['openai'] = True
    except Exception:
        pass

    # Test Redis connection
    try:
        import redis
        redis_url = get_config_value('redis_url')
        if redis_url:
            redis_client = redis.from_url(redis_url)
            redis_client.ping()
            results['redis'] = True
    except Exception:
        pass

    results['all_connected'] = all(results[key] for key in ['langcache', 'openai', 'redis'])

    return jsonify(results)

@app.route('/api/shadow-data')
def get_shadow_data():
    """Get shadow mode data for analysis"""
    import json
    import statistics
    import redis

    shadow_data = []
    metrics = {
        'total_queries': 0,
        'cache_hits': 0,
        'cache_misses': 0,
        'hit_rate': 0,
        'avg_llm_latency': 0,
        'avg_cache_latency': 0,
        'latency_improvement': 0,
        'total_tokens': 0,
        'tokens_saved': 0,
        'cost_savings_estimate': 0
    }

    # Try to get data from Redis first, then fallback to file
    redis_client = None
    try:
        redis_url = get_config_value('redis_url')
        if not redis_url:
            # No Redis configured - return empty data
            return jsonify({
                'data': [],
                'metrics': metrics
            })

        redis_client = redis.from_url(redis_url)

        # Get all shadow keys from Redis
        shadow_keys = redis_client.keys("shadow:*")
        for key in shadow_keys:
            try:
                data_str = redis_client.get(key)
                if data_str:
                    data = json.loads(data_str)
                    shadow_data.append(data)
            except (json.JSONDecodeError, Exception):
                continue

        print(f"📊 Loaded {len(shadow_data)} records from Redis")

    except Exception as e:
        print(f"⚠️  Redis connection failed: {e}, trying file fallback...")
        redis_client = None

    # Fallback to file if Redis fails or no data found
    if not shadow_data:
        try:
            with open('shadow_mode.log', 'r') as f:
                for line in f:
                    if line.strip():
                        try:
                            data = json.loads(line)
                            shadow_data.append(data)
                        except json.JSONDecodeError:
                            continue
            print(f"📊 Loaded {len(shadow_data)} records from file")
        except FileNotFoundError:
            print("📊 No shadow data found in file or Redis")

        # Calculate metrics
        if shadow_data:
            metrics['total_queries'] = len(shadow_data)
            metrics['cache_hits'] = sum(1 for d in shadow_data if d.get('cache_hit', False))
            metrics['cache_misses'] = metrics['total_queries'] - metrics['cache_hits']
            metrics['hit_rate'] = round((metrics['cache_hits'] / metrics['total_queries']) * 100, 1) if metrics['total_queries'] > 0 else 0

            # Latency analysis
            llm_latencies = [d.get('latency_llm_ms', 0) for d in shadow_data if d.get('latency_llm_ms')]
            cache_latencies = [d.get('latency_cache_ms', 0) for d in shadow_data if d.get('latency_cache_ms')]

            if llm_latencies:
                metrics['avg_llm_latency'] = round(statistics.mean(llm_latencies), 1)
            if cache_latencies:
                metrics['avg_cache_latency'] = round(statistics.mean(cache_latencies), 1)

            metrics['latency_improvement'] = round(((metrics['avg_llm_latency'] - metrics['avg_cache_latency']) / metrics['avg_llm_latency']) * 100, 1) if metrics['avg_llm_latency'] > 0 else 0

            # Token analysis
            metrics['total_tokens'] = sum(d.get('tokens_llm', 0) for d in shadow_data)
            metrics['tokens_saved'] = sum(d.get('tokens_llm', 0) for d in shadow_data if d.get('cache_hit', False))

            # Cost estimate (rough - $0.002 per 1K tokens for GPT-4o-mini)
            cost_per_1k_tokens = 0.002
            metrics['cost_savings_estimate'] = round((metrics['tokens_saved'] / 1000) * cost_per_1k_tokens, 4)

    # Calculate metrics if we have data
    if shadow_data:
        metrics['total_queries'] = len(shadow_data)
        metrics['cache_hits'] = sum(1 for d in shadow_data if d.get('cache_hit', False))
        metrics['cache_misses'] = metrics['total_queries'] - metrics['cache_hits']
        metrics['hit_rate'] = round((metrics['cache_hits'] / metrics['total_queries']) * 100, 1) if metrics['total_queries'] > 0 else 0

        # Latency analysis
        llm_latencies = [d.get('latency_llm_ms', 0) for d in shadow_data if d.get('latency_llm_ms')]
        cache_latencies = [d.get('latency_cache_ms', 0) for d in shadow_data if d.get('latency_cache_ms')]

        if llm_latencies:
            metrics['avg_llm_latency'] = round(statistics.mean(llm_latencies), 1)
        if cache_latencies:
            metrics['avg_cache_latency'] = round(statistics.mean(cache_latencies), 1)

        metrics['latency_improvement'] = round(((metrics['avg_llm_latency'] - metrics['avg_cache_latency']) / metrics['avg_llm_latency']) * 100, 1) if metrics['avg_llm_latency'] > 0 else 0

        # Token analysis
        metrics['total_tokens'] = sum(d.get('tokens_llm', 0) for d in shadow_data)
        metrics['tokens_saved'] = sum(d.get('tokens_llm', 0) for d in shadow_data if d.get('cache_hit', False))

        # Cost estimate (rough - $0.002 per 1K tokens for GPT-4o-mini)
        cost_per_1k_tokens = 0.002
        metrics['cost_savings_estimate'] = round((metrics['tokens_saved'] / 1000) * cost_per_1k_tokens, 4)

    # Sort data by timestamp (newest first)
    shadow_data.sort(key=lambda x: x.get('ts_request', ''), reverse=True)

    # Limit to last 100 entries for performance
    shadow_data = shadow_data[:100]

    return jsonify({
        'data': shadow_data,
        'metrics': metrics
    })

if __name__ == '__main__':
    # Check required environment variables
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ Error: OPENAI_API_KEY not set")
        print("Please add your OpenAI API key to .env file")
        exit(1)
    
    if not os.getenv('LANGCACHE_SHADOW_MODE'):
        print("⚠️  Warning: LANGCACHE_SHADOW_MODE not enabled")
        print("Shadow mode will not collect data")
    else:
        print("🔍 Shadow mode enabled - collecting data in background")
    
    print("🚀 Starting simple chatbot with shadow mode...")

    # Check Redis connection
    redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
    try:
        import redis
        redis_client = redis.from_url(redis_url)
        redis_client.ping()
        print(f"📊 Shadow data will be saved to: Redis ({redis_url.split('@')[-1] if '@' in redis_url else redis_url})")
    except Exception as e:
        print(f"⚠️  Redis connection failed: {e}")
        print("📊 Shadow data will be saved to: shadow_mode.log (file fallback)")

    print("🌐 Open: http://localhost:5002")
    print("📊 View data analysis at: http://localhost:5002/data-analysis")

    app.run(debug=True, host='0.0.0.0', port=5002)

# For Vercel deployment - expose the app object
# Vercel will automatically detect this as the WSGI application
if __name__ != '__main__':
    # This runs when imported by Vercel
    pass
