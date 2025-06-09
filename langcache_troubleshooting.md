# LangCache Troubleshooting Guide

## Common Issues and Solutions

### Service Unavailability

#### Symptoms
- Cannot connect to LangCache API
- Timeout errors when making requests
- "Service Unavailable" messages

#### Troubleshooting Steps
1. **Check Service Status**
   - Visit our status page at status.langcache.com
   - Verify if there's a known outage

2. **Verify Network Connectivity**
   - Test basic connectivity: `curl -X GET "https://api.langcache.com/v1/caches/your-cache-id/health"`
   - Check if your network allows outbound connections to our API endpoints

3. **Authentication Issues**
   - Confirm your API key is valid and not expired
   - Ensure the API key has proper permissions
   - Verify the correct format: `Authorization: Bearer your-api-key`

4. **Contact Support**
   - If issues persist, contact support with your cache ID and error messages

### Cache Performance Issues

#### Symptoms
- Slow response times
- Low cache hit rates
- Unexpected cache misses

#### Troubleshooting Steps
1. **Check Query Patterns**
   - Verify queries are semantically similar enough for matching
   - Review similarity threshold settings (recommended: 0.75-0.85)

2. **Inspect Cache Contents**
   - Use the dashboard to view current cache entries
   - Verify entries haven't expired (check TTL settings)

3. **Optimize Settings**
   - Adjust similarity thresholds if needed
   - Consider increasing cache size limits
   - Review attribute filtering settings

### External Dependency Issues

#### Symptoms
- Errors related to OpenAI or other external services
- Rate limiting messages
- Authentication failures with external APIs

#### Troubleshooting Steps
1. **Check External Service Status**
   - Verify OpenAI status at status.openai.com
   - Check other external dependencies' status pages

2. **Review Rate Limits**
   - Check if you've exceeded API rate limits
   - Consider implementing request throttling

3. **Verify Credentials**
   - Ensure external API keys are valid and not expired
   - Check for proper authentication configuration

### Data Storage Issues

#### Symptoms
- "Database unavailable" errors
- Data retrieval failures
- Cache entry storage problems

#### Troubleshooting Steps
1. **Check Storage Capacity**
   - Verify you haven't exceeded storage limits
   - Consider cleaning up unused cache entries

2. **Review Cache Configuration**
   - Check TTL settings for appropriate expiration
   - Verify cache size limits are appropriate for your usage

3. **Data Integrity**
   - Test with simple cache operations to verify functionality
   - Check for error messages related to data corruption

### Authentication Service Issues

#### Symptoms
- "Unauthorized" errors
- Token validation failures
- Cannot access management functions

#### Troubleshooting Steps
1. **Verify Credentials**
   - Check API key format and validity
   - Ensure you're using the correct authentication headers

2. **Token Issues**
   - Check if tokens have expired
   - Verify clock synchronization between your systems

3. **Permission Settings**
   - Review access control settings for your account
   - Verify user roles and permissions

## Quick Diagnostic Commands

### Test API Connectivity
```bash
curl -X GET "https://api.langcache.com/v1/caches/your-cache-id/health" \
  -H "Authorization: Bearer your-api-key" \
  -H "Accept: application/json"
```

### Test Cache Search
```bash
curl -X POST "https://api.langcache.com/v1/caches/your-cache-id/search" \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "test query", "distanceThreshold": 0.85}'
```

### Test Cache Add
```bash
curl -X POST "https://api.langcache.com/v1/caches/your-cache-id/entries" \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "test query", "response": "test response"}'
```

## When to Contact Support

Please contact our support team if:
- Issues persist after trying the troubleshooting steps
- You experience unexpected service behavior
- You need assistance with configuration optimization
- You encounter error messages not covered in this guide

When contacting support, please provide:
- Your cache ID (not your API key)
- Detailed error messages
- Steps you've already taken to troubleshoot
- Timestamps of when the issues occurred

## Support Channels
- Email: support@langcache.com
- Support Portal: support.langcache.com
- Documentation: docs.langcache.com