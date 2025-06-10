#!/usr/bin/env python3
"""
LangCache Shadow Mode - Quick Setup Script

This script gets you from zero to shadow mode in 5 minutes.
"""

import os
import sys
import subprocess
import urllib.request
from pathlib import Path

def print_banner():
    print("""
🚀 LangCache Shadow Mode - Quick Setup
======================================

Get shadow mode running in 5 minutes and start collecting data!

This script will:
✅ Install dependencies
✅ Download shadow mode wrapper
✅ Configure environment
✅ Test your setup
✅ Create integration examples

""")

def check_python_version():
    """Ensure Python 3.8+"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8+ required")
        print(f"   Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version.split()[0]}")

def check_dependencies():
    """Check if required packages are available"""
    required = ['requests']
    missing = []
    
    for package in required:
        try:
            __import__(package)
            print(f"✅ {package} is available")
        except ImportError:
            missing.append(package)
            print(f"⚠️  {package} is missing")
    
    if missing:
        print(f"\n📦 Installing missing packages: {', '.join(missing)}")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing)
            print("✅ Dependencies installed successfully")
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies")
            print("   Please run: pip install requests")
            sys.exit(1)

def download_shadow_wrapper():
    """Download the shadow mode wrapper"""
    wrapper_url = "https://raw.githubusercontent.com/Jenverse/Langcache-shadow-mode/main/shadow-wrapper/python/langcache_shadow.py"
    local_path = "langcache_shadow.py"
    
    if os.path.exists(local_path):
        print(f"✅ Shadow wrapper already exists: {local_path}")
        return local_path
    
    try:
        print(f"📥 Downloading shadow mode wrapper...")
        urllib.request.urlretrieve(wrapper_url, local_path)
        print(f"✅ Downloaded: {local_path}")
        return local_path
    except Exception as e:
        print(f"❌ Failed to download wrapper: {e}")
        print("   Please contact LangCache support for the wrapper file")
        sys.exit(1)

def setup_environment():
    """Help user set up environment variables"""
    print("\n🔧 Environment Setup")
    print("=" * 30)
    
    # Check if .env file exists
    env_file = Path(".env")
    if env_file.exists():
        print("✅ Found existing .env file")
        with open(env_file, 'r') as f:
            content = f.read()
            if 'LANGCACHE_SHADOW_MODE' in content:
                print("✅ LangCache configuration already present")
                return
    
    print("\n📝 Setting up environment variables...")
    
    # Get credentials from user
    api_key = input("Enter your LangCache API key: ").strip()
    cache_id = input("Enter your LangCache Cache ID: ").strip()
    
    if not api_key or not cache_id:
        print("❌ API key and Cache ID are required")
        sys.exit(1)
    
    # Create/update .env file
    env_content = f"""
# LangCache Shadow Mode Configuration
LANGCACHE_SHADOW_MODE=true
LANGCACHE_API_KEY={api_key}
LANGCACHE_CACHE_ID={cache_id}
LANGCACHE_BASE_URL=https://api.langcache.com
REDIS_URL=redis://localhost:6379

# Optional: Timeout settings
LANGCACHE_TIMEOUT=10
"""
    
    with open(".env", "a") as f:
        f.write(env_content)
    
    print("✅ Environment variables configured in .env file")
    print("\n⚠️  Important: Add .env to your .gitignore file to protect your API keys!")

def create_example_integration():
    """Create an example integration file"""
    example_code = '''#!/usr/bin/env python3
"""
Example: LangCache Shadow Mode Integration

This shows how to integrate shadow mode with your existing LLM calls.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the shadow wrapper
from langcache_shadow import shadow_llm_call

# Example with OpenAI
def example_openai_integration():
    """Example integration with OpenAI"""
    try:
        import openai
        
        # Your existing LLM call
        def your_existing_llm_call(user_query):
            return openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": user_query}]
            )
        
        # Shadow mode version (minimal change)
        def your_shadow_mode_call(user_query):
            return shadow_llm_call(
                openai.chat.completions.create,
                user_query,  # <- Add this parameter
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": user_query}]
            )
        
        # Test it
        test_query = "What is machine learning?"
        print(f"Testing query: {test_query}")
        
        response = your_shadow_mode_call(test_query)
        print(f"Response: {response.choices[0].message.content[:100]}...")
        print("✅ Shadow mode integration working!")
        
    except ImportError:
        print("⚠️  OpenAI not installed. Install with: pip install openai")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🧪 Testing LangCache Shadow Mode Integration")
    print("=" * 50)
    example_openai_integration()
'''
    
    with open("example_shadow_integration.py", "w") as f:
        f.write(example_code)
    
    print("✅ Created example_shadow_integration.py")

def create_test_script():
    """Create a simple test script"""
    test_code = '''#!/usr/bin/env python3
"""
LangCache Shadow Mode Test Script

Run this to verify shadow mode is working correctly.
"""

import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_shadow_mode():
    """Test shadow mode configuration"""
    print("🧪 Testing LangCache Shadow Mode")
    print("=" * 40)
    
    # Check environment variables
    required_vars = ['LANGCACHE_SHADOW_MODE', 'LANGCACHE_API_KEY', 'LANGCACHE_CACHE_ID']
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: {'*' * 10}")  # Hide actual values
        else:
            print(f"❌ {var}: Not set")
            return False
    
    # Test wrapper import
    try:
        from langcache_shadow import config
        print(f"✅ Shadow wrapper imported successfully")
        print(f"✅ Shadow mode enabled: {config.enabled}")
    except ImportError as e:
        print(f"❌ Failed to import shadow wrapper: {e}")
        return False
    
    print("\\n🎉 Shadow mode is configured correctly!")
    print("\\nNext steps:")
    print("1. Integrate shadow_llm_call() into your application")
    print("2. Run your application normally for 2 weeks")
    print("3. Check shadow_mode.log for collected data")
    print("4. Contact LangCache for analysis and results")
    
    return True

if __name__ == "__main__":
    test_shadow_mode()
'''
    
    with open("test_shadow_mode.py", "w") as f:
        f.write(test_code)
    
    print("✅ Created test_shadow_mode.py")

def print_next_steps():
    """Print next steps for the customer"""
    print("""
🎉 Setup Complete!
==================

Your LangCache shadow mode is now configured. Here's what to do next:

1. 🧪 Test the setup:
   python test_shadow_mode.py

2. 📖 Review the example:
   python example_shadow_integration.py

3. 🔧 Integrate with your app:
   - Replace your LLM calls with shadow_llm_call()
   - See example_shadow_integration.py for guidance

4. 🚀 Run your pilot:
   - Use your application normally for 2 weeks
   - Shadow data will be collected automatically
   - Check shadow_mode.log for data

5. 📊 Get your results:
   - Contact your LangCache representative
   - We'll analyze your data and provide recommendations

📞 Support:
   - Email: support@langcache.com
   - Documentation: https://docs.langcache.com/shadow-mode
   - Your LangCache representative: [contact info]

🎯 Questions? We're here to help make your pilot successful!
""")

def main():
    """Main setup flow"""
    print_banner()
    
    try:
        check_python_version()
        check_dependencies()
        download_shadow_wrapper()
        setup_environment()
        create_example_integration()
        create_test_script()
        print_next_steps()
        
    except KeyboardInterrupt:
        print("\\n❌ Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\\n❌ Setup failed: {e}")
        print("Please contact LangCache support for assistance")
        sys.exit(1)

if __name__ == "__main__":
    main()
