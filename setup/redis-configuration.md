# Redis Configuration Examples for LangCache Shadow Mode

## 🗄️ Redis URL Configuration Options

The `REDIS_URL` environment variable tells the shadow mode where to store collected data. Here are common configuration patterns:

## 📋 Basic Configurations

### Local Redis (Default)
```bash
# .env file
REDIS_URL=redis://localhost:6379
```
- **Use case**: Development, local testing
- **Database**: Uses default database (0)
- **Authentication**: None required

### Local Redis with Specific Database
```bash
# .env file
REDIS_URL=redis://localhost:6379/5
```
- **Use case**: Separate shadow data from other Redis data
- **Database**: Uses database 5 (0-15 available)
- **Benefit**: Isolates shadow mode data

### Remote Redis Server
```bash
# .env file
REDIS_URL=redis://your-redis-server.com:6379
```
- **Use case**: Production environments, shared Redis
- **Database**: Default database (0)
- **Network**: Connects to remote Redis instance

## 🔐 Authenticated Redis

### Redis with Password
```bash
# .env file
REDIS_URL=redis://:your-password@localhost:6379
```
- **Format**: `redis://:password@host:port`
- **Use case**: Secured Redis instances
- **Note**: Colon before password is required

### Redis with Username and Password
```bash
# .env file
REDIS_URL=redis://username:password@localhost:6379
```
- **Format**: `redis://username:password@host:port`
- **Use case**: Redis 6+ with ACL authentication
- **Security**: More granular access control

### Redis with Password and Database
```bash
# .env file
REDIS_URL=redis://:your-password@localhost:6379/3
```
- **Combines**: Authentication + specific database
- **Use case**: Secured Redis with data isolation

## 🔒 Secure Redis (TLS/SSL)

### Redis with TLS
```bash
# .env file
REDIS_URL=rediss://username:password@your-redis.com:6380
```
- **Protocol**: `rediss://` (note the 's')
- **Port**: Usually 6380 for TLS
- **Use case**: Production environments requiring encryption

### Redis with TLS and Certificate Verification
```bash
# .env file
REDIS_URL=rediss://username:password@your-redis.com:6380?ssl_cert_reqs=required
```
- **Security**: Full certificate verification
- **Use case**: High-security environments

## ☁️ Cloud Redis Services

### AWS ElastiCache
```bash
# .env file
REDIS_URL=redis://your-cluster.cache.amazonaws.com:6379
```
- **Service**: AWS ElastiCache for Redis
- **Authentication**: Usually no password (VPC security)
- **Clustering**: May require cluster-aware client

### AWS ElastiCache with Auth Token
```bash
# .env file
REDIS_URL=redis://:your-auth-token@your-cluster.cache.amazonaws.com:6379
```
- **Security**: ElastiCache with AUTH token enabled
- **Use case**: Enhanced security for ElastiCache

### Google Cloud Memorystore
```bash
# .env file
REDIS_URL=redis://10.0.0.3:6379
```
- **Network**: Private IP within VPC
- **Authentication**: Usually none (VPC security)
- **Use case**: Google Cloud Redis instances

### Azure Cache for Redis
```bash
# .env file
REDIS_URL=redis://:your-access-key@your-cache.redis.cache.windows.net:6380
```
- **Port**: 6380 (SSL) or 6379 (non-SSL)
- **Authentication**: Access key required
- **SSL**: Recommended for production

### Redis Cloud (Redis Labs)
```bash
# .env file
REDIS_URL=redis://:password@redis-12345.c1.us-east-1-1.ec2.cloud.redislabs.com:12345
```
- **Service**: Redis Cloud managed service
- **Port**: Custom port assigned by Redis Cloud
- **Authentication**: Password required

## 🐳 Docker & Container Environments

### Docker Compose Redis
```bash
# .env file
REDIS_URL=redis://redis:6379
```
- **Service name**: `redis` (from docker-compose.yml)
- **Network**: Docker internal network
- **Use case**: Multi-container applications

### Kubernetes Redis Service
```bash
# .env file
REDIS_URL=redis://redis-service.default.svc.cluster.local:6379
```
- **Service**: Kubernetes service name
- **Namespace**: `default` (adjust as needed)
- **DNS**: Kubernetes internal DNS

### Docker with Custom Network
```bash
# .env file
REDIS_URL=redis://redis-container:6379
```
- **Container**: Named Redis container
- **Network**: Custom Docker network

## 🔧 Advanced Configurations

### Redis Sentinel (High Availability)
```bash
# .env file
REDIS_URL=redis-sentinel://sentinel1:26379,sentinel2:26379,sentinel3:26379/mymaster
```
- **Service**: Redis Sentinel for HA
- **Format**: Multiple sentinel endpoints
- **Master**: `mymaster` is the master name

### Redis Cluster
```bash
# .env file
REDIS_URL=redis://node1:7000,node2:7000,node3:7000
```
- **Cluster**: Multiple Redis cluster nodes
- **Port**: 7000 is common for cluster mode
- **Client**: Requires cluster-aware Redis client

### Connection Pool Settings
```bash
# .env file
REDIS_URL=redis://localhost:6379?max_connections=20&retry_on_timeout=true
```
- **Pool size**: Maximum connections
- **Retry**: Automatic retry on timeout
- **Use case**: High-throughput applications

## 📊 Configuration for Different Environments

### Development Environment
```bash
# .env.development
REDIS_URL=redis://localhost:6379/1
LANGCACHE_SHADOW_MODE=true
```

### Staging Environment
```bash
# .env.staging
REDIS_URL=redis://:staging-password@staging-redis:6379/2
LANGCACHE_SHADOW_MODE=true
```

### Production Environment
```bash
# .env.production
REDIS_URL=rediss://username:password@prod-redis.company.com:6380/0
LANGCACHE_SHADOW_MODE=true
```

## 🧪 Testing Your Redis Configuration

### Test Redis Connection
```python
import redis
import os
from dotenv import load_dotenv

load_dotenv()

try:
    r = redis.from_url(os.getenv('REDIS_URL'))
    r.ping()
    print("✅ Redis connection successful!")
    
    # Test shadow mode key
    test_key = "shadow:test"
    r.set(test_key, "test-value")
    value = r.get(test_key)
    r.delete(test_key)
    
    print("✅ Redis read/write operations working!")
    
except Exception as e:
    print(f"❌ Redis connection failed: {e}")
```

### Test with Shadow Mode
```bash
# Run the test script
python test_shadow_mode.py

# Check if shadow data is being stored
redis-cli -u $REDIS_URL KEYS "shadow:*"
```

## 🚨 Common Issues & Solutions

### Connection Refused
```bash
# Error: Connection refused
# Solution: Check if Redis is running
redis-cli ping

# Or check specific URL
redis-cli -u $REDIS_URL ping
```

### Authentication Failed
```bash
# Error: NOAUTH Authentication required
# Solution: Add password to REDIS_URL
REDIS_URL=redis://:your-password@localhost:6379
```

### Wrong Database
```bash
# Error: Data not found
# Solution: Check database number
REDIS_URL=redis://localhost:6379/0  # Use database 0
```

### SSL/TLS Issues
```bash
# Error: SSL connection failed
# Solution: Use correct protocol and port
REDIS_URL=rediss://localhost:6380  # Note 'rediss' and port 6380
```

## 📋 Best Practices

### Security
- ✅ Use TLS (`rediss://`) in production
- ✅ Use strong passwords for authentication
- ✅ Restrict network access to Redis
- ✅ Use dedicated database for shadow data

### Performance
- ✅ Use connection pooling for high-volume apps
- ✅ Choose Redis instance close to your application
- ✅ Monitor Redis memory usage
- ✅ Set appropriate timeouts

### Data Management
- ✅ Use separate database for shadow data (`/1`, `/2`, etc.)
- ✅ Set expiration on shadow keys if needed
- ✅ Monitor disk space for Redis persistence
- ✅ Backup shadow data before analysis

---

**Remember**: The Redis URL you configure determines where your shadow mode data gets stored. Choose the option that best fits your infrastructure and security requirements! 🔒
