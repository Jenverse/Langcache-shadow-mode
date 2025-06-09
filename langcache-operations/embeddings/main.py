from flask import Flask, request, jsonify
import logging
import os
import requests
from typing import Dict
from dotenv import load_dotenv

# Load environment variables from root directory
import os.path
env_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path=env_path)

# Environment variables are loaded from .env file only

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration from environment variables
CONFIG = {
    'langcache_base_url': os.getenv('LANGCACHE_BASE_URL'),
    'langcache_api_key': os.getenv('LANGCACHE_API_KEY'),
    'langcache_cache_id': os.getenv('LANGCACHE_CACHE_ID'),
    'local_host': os.getenv('LOCAL_HOST', '0.0.0.0'),
    'local_port': int(os.getenv('LOCAL_PORT', 8080)),
    'local_debug': os.getenv('LOCAL_DEBUG', 'true').lower() == 'true'
}

# Validate required configuration
if not CONFIG['langcache_base_url']:
    raise ValueError("LANGCACHE_BASE_URL environment variable is required")
if not CONFIG['langcache_api_key']:
    raise ValueError("LANGCACHE_API_KEY environment variable is required")
if not CONFIG['langcache_cache_id']:
    raise ValueError("LANGCACHE_CACHE_ID environment variable is required")

logger.info(f"Connecting to LangCache at: {CONFIG['langcache_base_url']}")
logger.info(f"Using Cache ID: {CONFIG['langcache_cache_id']}")

class LangCacheClient:
    """Client for interacting with the managed LangCache service"""

    def __init__(self, base_url: str, api_key: str, cache_id: str):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.cache_id = cache_id
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })

    def _make_request(self, method: str, endpoint: str, **kwargs):
        """Make a request to the LangCache service"""
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.request(method, url, **kwargs)
            logger.debug(f"{method} {url} -> {response.status_code}")
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise

    def health_check(self):
        """Check cache health"""
        response = self._make_request('GET', f'/v1/caches/{self.cache_id}/health')
        return response.json(), response.status_code

    def search_cache(self, data: Dict):
        """Search the cache"""
        response = self._make_request('POST', f'/v1/caches/{self.cache_id}/search', json=data)
        return response.json(), response.status_code

    def add_entry(self, data: Dict):
        """Add entry to cache"""
        response = self._make_request('POST', f'/v1/caches/{self.cache_id}/entries', json=data)
        return response.json(), response.status_code

    def delete_entry(self, entry_id: str):
        """Delete a specific entry"""
        response = self._make_request('DELETE', f'/v1/caches/{self.cache_id}/entries/{entry_id}')
        return response.json(), response.status_code

    def delete_entries(self, data: Dict):
        """Delete multiple entries"""
        response = self._make_request('DELETE', f'/v1/caches/{self.cache_id}/entries', json=data)
        return response.json(), response.status_code

# Initialize LangCache client
langcache_client = LangCacheClient(
    CONFIG['langcache_base_url'],
    CONFIG['langcache_api_key'],
    CONFIG['langcache_cache_id']
)

def create_error_response(message: str, status_code: int):
    """Create standardized error response"""
    return jsonify({"message": message}), status_code

def handle_langcache_response(response_data, status_code: int):
    """Handle response from LangCache service"""
    if status_code >= 400:
        # Extract error message if available
        if isinstance(response_data, dict) and 'message' in response_data:
            return create_error_response(response_data['message'], status_code)
        else:
            return create_error_response("LangCache service error", status_code)
    return jsonify(response_data), status_code

@app.route('/v1/caches/<cache_id>/health', methods=['GET'])
def get_cache_health(cache_id: str):
    """Return information about the operational status of the cache configuration"""
    try:
        # Make request to managed LangCache service
        response_data, status_code = langcache_client.health_check()
        return handle_langcache_response(response_data, status_code)

    except Exception as e:
        logger.error(f"Health check error: {str(e)}")
        return create_error_response("An internal error occurred", 503)

@app.route('/v1/caches/<cache_id>/search', methods=['POST'])
def search_cache(cache_id: str):
    """Search and return semantically-similar entries from the cache"""
    try:
        # Parse request body
        data = request.get_json()
        if not data:
            return create_error_response("Request body is required", 400)

        # Validate required fields
        if 'prompt' not in data:
            return create_error_response("Prompt is required", 400)

        # Make request to managed LangCache service
        response_data, status_code = langcache_client.search_cache(data)
        return handle_langcache_response(response_data, status_code)

    except ValueError as e:
        return create_error_response(str(e), 400)
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        return create_error_response("An internal error occurred", 503)

@app.route('/v1/caches/<cache_id>/entries', methods=['POST'])
def save_cache_entry(cache_id: str):
    """Save a new cache entry"""
    try:
        # Parse request body
        data = request.get_json()
        if not data:
            return create_error_response("Request body is required", 400)

        # Validate required fields
        if 'prompt' not in data or 'response' not in data:
            return create_error_response("Prompt and response are required", 400)

        # Make request to managed LangCache service
        response_data, status_code = langcache_client.add_entry(data)
        return handle_langcache_response(response_data, status_code)

    except ValueError as e:
        return create_error_response(str(e), 400)
    except Exception as e:
        logger.error(f"Save entry error: {str(e)}")
        return create_error_response("An internal error occurred", 503)

@app.route('/v1/caches/<cache_id>/entries/<entry_id>', methods=['DELETE'])
def delete_cache_entry(cache_id: str, entry_id: str):
    """Delete a cache entry"""
    try:
        # Make request to managed LangCache service
        response_data, status_code = langcache_client.delete_entry(entry_id)
        return handle_langcache_response(response_data, status_code)

    except Exception as e:
        logger.error(f"Delete entry error: {str(e)}")
        return create_error_response("An internal error occurred", 503)

@app.route('/v1/caches/<cache_id>/entries', methods=['DELETE'])
def delete_multiple_cache_entries(cache_id: str):
    """Delete multiple cache entries"""
    try:
        # Parse request body
        data = request.get_json()
        if not data:
            return create_error_response("Request body is required", 400)

        # Make request to managed LangCache service
        response_data, status_code = langcache_client.delete_entries(data)
        return handle_langcache_response(response_data, status_code)

    except ValueError as e:
        return create_error_response(str(e), 400)
    except Exception as e:
        logger.error(f"Delete multiple entries error: {str(e)}")
        return create_error_response("An internal error occurred", 503)

# Health check for the service itself
@app.route('/health', methods=['GET'])
def service_health():
    """Service health check"""
    return jsonify({"status": "healthy", "service": "langcache-wrapper"}), 200

# Error handlers
@app.errorhandler(401)
def unauthorized(_error):
    """Handle unauthorized access"""
    return create_error_response("Unauthorized", 401)

@app.errorhandler(404)
def not_found(_error):
    """Handle not found errors"""
    return create_error_response("Resource not found", 404)

@app.errorhandler(500)
def internal_error(_error):
    """Handle internal server errors"""
    return create_error_response("An internal error occurred", 503)

if __name__ == '__main__':
    # Start the Flask application
    app.run(
        host=CONFIG['local_host'],
        port=CONFIG['local_port'],
        debug=CONFIG['local_debug']
    )