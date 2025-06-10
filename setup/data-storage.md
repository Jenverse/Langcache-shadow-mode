# LangCache Shadow Mode - Data Storage Options

## 🗄️ Where Your Shadow Mode Data Gets Stored

**Important**: All shadow mode data stays in YOUR environment. LangCache never has direct access to your shadow logs.

## 📊 Storage Option 1: Redis (Recommended)

### Setup
```bash
# Use your existing Redis instance
export REDIS_URL=redis://localhost:6379

# Or use a dedicated Redis for shadow mode
export REDIS_URL=redis://your-redis-host:6379/1
```

### Benefits
- ✅ **Fast queries**: Easy to search and filter data
- ✅ **Scalable**: Handles high-volume applications
- ✅ **Multi-instance**: Share data across multiple app instances
- ✅ **Real-time**: Monitor data collection in real-time

### Data Structure
```bash
# Redis keys
shadow:550e8400-e29b-41d4-a716-446655440000
shadow:661f9511-e29b-41d4-a716-446655440001
shadow:772fa622-e29b-41d4-a716-446655440002

# Each key contains full JSON record
redis-cli GET "shadow:550e8400-e29b-41d4-a716-446655440000"
```

### Monitoring
```bash
# Count total records
redis-cli KEYS "shadow:*" | wc -l

# View latest records
redis-cli --scan --pattern "shadow:*" | head -5 | xargs redis-cli MGET

# Real-time monitoring
redis-cli MONITOR | grep shadow
```

## 📁 Storage Option 2: Local File (Fallback)

### Setup
```bash
# No Redis? Data automatically goes to file
# File created in your application directory: shadow_mode.log
```

### Benefits
- ✅ **Simple**: No additional infrastructure needed
- ✅ **Portable**: Easy to copy/transfer for analysis
- ✅ **Standard format**: JSONL (JSON Lines)
- ✅ **Version control friendly**: Can be tracked in git (if desired)

### Data Structure
```bash
# File: shadow_mode.log (JSONL format)
{"request_id": "550e8400...", "ts_request": "2025-01-27T15:04:32.123Z", ...}
{"request_id": "661f9511...", "ts_request": "2025-01-27T15:05:15.456Z", ...}
{"request_id": "772fa622...", "ts_request": "2025-01-27T15:06:22.789Z", ...}
```

### Monitoring
```bash
# Count total records
wc -l shadow_mode.log

# View latest records
tail -10 shadow_mode.log

# Real-time monitoring
tail -f shadow_mode.log

# Pretty print JSON
tail -5 shadow_mode.log | jq '.'
```

## 🔧 Configuration Examples

### Option A: Use Existing Redis
```bash
# .env file
LANGCACHE_SHADOW_MODE=true
REDIS_URL=redis://your-existing-redis:6379
LANGCACHE_API_KEY=your-api-key
LANGCACHE_CACHE_ID=your-cache-id
```

### Option B: Dedicated Redis Database
```bash
# .env file
LANGCACHE_SHADOW_MODE=true
REDIS_URL=redis://localhost:6379/5  # Use database 5
LANGCACHE_API_KEY=your-api-key
LANGCACHE_CACHE_ID=your-cache-id
```

### Option C: Redis with Authentication
```bash
# .env file
LANGCACHE_SHADOW_MODE=true
REDIS_URL=redis://username:password@redis-host:6379
LANGCACHE_API_KEY=your-api-key
LANGCACHE_CACHE_ID=your-cache-id
```

### Option D: File-only (No Redis)
```bash
# .env file
LANGCACHE_SHADOW_MODE=true
# Don't set REDIS_URL - will automatically use file storage
LANGCACHE_API_KEY=your-api-key
LANGCACHE_CACHE_ID=your-cache-id
```

## 📈 Data Analysis

### Redis Analysis
```python
import redis
import json

# Connect to Redis
r = redis.from_url("redis://localhost:6379")

# Get all shadow data
keys = r.keys("shadow:*")
data = []
for key in keys:
    record = json.loads(r.get(key))
    data.append(record)

print(f"Total records: {len(data)}")
```

### File Analysis
```python
import json

# Load from file
data = []
with open("shadow_mode.log", "r") as f:
    for line in f:
        if line.strip():
            data.append(json.loads(line))

print(f"Total records: {len(data)}")
```

### Using Provided Analysis Script
```bash
# For Redis data
python analyze_pilot_data.py --source redis --redis-url redis://localhost:6379

# For file data
python analyze_pilot_data.py --source file --file shadow_mode.log
```

## 🔒 Data Security & Privacy

### What Stays Local
- ✅ **All shadow logs**: Complete dataset never leaves your environment
- ✅ **User queries**: Original user questions stay private
- ✅ **LLM responses**: Your model responses stay private
- ✅ **Performance data**: Latency and token metrics stay private

### What Goes to LangCache
- 🔄 **Cache operations**: Search and store requests (same as production)
- 📊 **Operational metrics**: Basic health/status information
- ❌ **No shadow logs**: We never see your collected analytics data

### Data Retention Control
```bash
# Redis: Set expiration on shadow data (optional)
redis-cli EXPIRE "shadow:request-id" 2592000  # 30 days

# File: Rotate logs (optional)
mv shadow_mode.log shadow_mode_$(date +%Y%m%d).log
```

## 🎯 Recommendations by Use Case

### High-Volume Applications (>10K queries/day)
- ✅ **Use Redis**: Better performance for large datasets
- ✅ **Dedicated database**: Use separate Redis DB for shadow data
- ✅ **Set expiration**: Automatically clean up old data

### Low-Volume Applications (<1K queries/day)
- ✅ **File storage**: Simpler setup, adequate performance
- ✅ **Version control**: Can track shadow_mode.log in git
- ✅ **Easy sharing**: Simple to send file to LangCache for analysis

### Multi-Instance Applications
- ✅ **Shared Redis**: All instances write to same Redis
- ✅ **Unique request IDs**: Avoid conflicts between instances
- ✅ **Centralized analysis**: Single dataset for all instances

### Security-Sensitive Applications
- ✅ **Local file**: No network storage of sensitive data
- ✅ **Encrypted Redis**: Use Redis with TLS/encryption
- ✅ **Data retention**: Automatically purge old shadow data

## 📞 Support

### Common Issues
- **Redis connection fails**: Check REDIS_URL, network connectivity
- **File permissions**: Ensure app can write to shadow_mode.log
- **Disk space**: Monitor log file size in high-volume applications

### Getting Help
- 📧 **Email**: support@langcache.com
- 📱 **Slack**: [Your support channel]
- 📖 **Docs**: https://docs.langcache.com/shadow-mode

---

**Remember**: Your data stays in your environment. You have complete control over storage, retention, and access! 🔒
