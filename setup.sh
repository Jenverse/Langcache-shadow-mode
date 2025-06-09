#!/bin/bash

# LangCache Shadow Mode Setup Script
# This script helps you set up shadow mode for your LangCache integration

set -e

echo "🔍 LangCache Shadow Mode Setup"
echo "================================"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cat > .env << 'EOF'
# LangCache Configuration
LANGCACHE_BASE_URL=https://api.langcache.com
LANGCACHE_API_KEY=your-langcache-api-key
LANGCACHE_CACHE_ID=your-cache-id

# Shadow Mode Configuration
LANGCACHE_SHADOW_MODE=true
REDIS_URL=redis://localhost:6379

# Optional: Timeout settings
LANGCACHE_TIMEOUT=10

# Example App Configuration (for Flask example)
GEMINI_API_KEY=your-gemini-api-key
LOCAL_HOST=0.0.0.0
LOCAL_PORT=8080
LOCAL_DEBUG=true
EOF
    echo "✅ Created .env file with default configuration"
    echo "⚠️  Please edit .env file with your actual API keys and configuration"
else
    echo "✅ .env file already exists"
fi

# Create necessary directories
echo ""
echo "📁 Creating directories..."
mkdir -p logs
mkdir -p data

# Check Python dependencies for examples
echo ""
echo "🐍 Checking Python dependencies..."
if command -v python3 &> /dev/null; then
    echo "✅ Python 3 found"
    
    # Check if pip is available
    if command -v pip3 &> /dev/null; then
        echo "✅ pip3 found"
        
        # Install Python dependencies for examples
        echo "📦 Installing Python dependencies for examples..."
        pip3 install -r examples/flask-app/requirements.txt 2>/dev/null || echo "⚠️  Could not install Python dependencies automatically"
    else
        echo "⚠️  pip3 not found - you may need to install Python dependencies manually"
    fi
else
    echo "⚠️  Python 3 not found - Python examples will not work"
fi

# Check Node.js dependencies
echo ""
echo "🟢 Checking Node.js..."
if command -v node &> /dev/null; then
    echo "✅ Node.js found"
    
    if command -v npm &> /dev/null; then
        echo "✅ npm found"
    else
        echo "⚠️  npm not found - you may need to install Node.js dependencies manually"
    fi
else
    echo "⚠️  Node.js not found - Node.js examples will not work"
fi

# Check Redis
echo ""
echo "🔴 Checking Redis..."
if command -v redis-cli &> /dev/null; then
    echo "✅ Redis CLI found"
    
    # Test Redis connection
    if redis-cli ping &> /dev/null; then
        echo "✅ Redis server is running"
    else
        echo "⚠️  Redis server is not running"
        echo "   Start Redis with: redis-server"
        echo "   Or use Docker: docker run -d -p 6379:6379 redis:alpine"
    fi
else
    echo "⚠️  Redis not found"
    echo "   Install Redis or use Docker: docker run -d -p 6379:6379 redis:alpine"
fi

echo ""
echo "🎯 Quick Start Options:"
echo ""
echo "1. 📝 Edit .env file with your API keys:"
echo "   nano .env"
echo ""
echo "2. 🐍 Try Python wrapper:"
echo "   python3 -c \"from wrappers.python.langcache_shadow import track; print('Python wrapper ready!')\""
echo ""
echo "3. 🟢 Try Node.js wrapper:"
echo "   node -e \"const {track} = require('./wrappers/nodejs/langcache-shadow'); console.log('Node.js wrapper ready!');\""
echo ""
echo "4. 🌐 Run Flask example:"
echo "   cd examples/flask-app"
echo "   python3 app.py"
echo ""
echo "5. 📊 Analyze shadow data:"
echo "   python3 analytics/analyze_shadow_data.py --source redis"
echo ""
echo "6. 🔍 View shadow logs:"
echo "   tail -f shadow_mode.log"
echo "   # or"
echo "   redis-cli KEYS 'shadow:*'"
echo ""

echo "✅ Setup complete!"
echo ""
echo "📚 Next steps:"
echo "1. Configure your API keys in .env"
echo "2. Choose a wrapper (Python/Node.js) or use the Flask example"
echo "3. Integrate shadow mode into your application"
echo "4. Run your application and monitor shadow logs"
echo "5. Analyze the data to validate cache performance"
echo ""
echo "📖 Documentation: docs/getting-started.md"
echo "🆘 Support: https://github.com/redis/langcache-shadow-mode/issues"
echo ""
echo "🎉 Happy shadow mode testing!"
