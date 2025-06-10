# 🚀 Vercel Deployment Guide

## Quick Deploy to Vercel

### Option 1: One-Click Deploy
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/Jenverse/Langcache-shadow-mode)

### Option 2: Manual Setup

1. **Fork/Clone this repository**
2. **Go to [vercel.com](https://vercel.com) and sign up**
3. **Connect your GitHub account**
4. **Import your repository**
5. **Configure deployment settings:**
   - Framework Preset: `Other`
   - Build Command: `pip install -r requirements.txt`
   - Output Directory: (leave empty)
   - Install Command: (leave empty)

6. **Deploy!**

## 🔧 Configuration

### Environment Variables (Optional)
You can set these in Vercel dashboard, but the app works without them:

```
FLASK_ENV=production
```

### App Configuration
- All configuration is done through the web interface
- No environment variables needed for API keys
- Each user configures their own credentials securely

## 🌐 Access Your Deployed App

After deployment, your app will be available at:
- `https://your-app-name.vercel.app`
- `https://your-app-name.vercel.app/config` - Configuration page
- `https://your-app-name.vercel.app/data-analysis` - Analytics dashboard
- `https://your-app-name.vercel.app/api/health` - Health check

## 🔐 Security Features

- **Session-based configuration**: Each user configures their own API keys
- **No shared credentials**: Safe for multiple users
- **Secure storage**: Credentials stored in browser session only
- **Auto-cleanup**: Credentials cleared when session ends

## 🎯 Perfect for Customer Demos

- **Professional URL**: Share `your-app.vercel.app` with customers
- **No setup required**: Customers just need to configure their API keys
- **Real-time analytics**: Show LangCache performance benefits
- **Cost calculator**: Demonstrate savings potential

## 🛠️ Troubleshooting

### Common Issues:

1. **Build fails**: Check that all dependencies are in `requirements.txt`
2. **App doesn't start**: Verify `vercel.json` configuration
3. **Routes not working**: Ensure Flask app is properly configured

### Health Check:
Visit `/api/health` to verify deployment is working.

## 📊 Features Available

- ✅ Shadow Mode vs Live Mode toggle
- ✅ Real-time latency comparison
- ✅ Cost calculator with configurable pricing
- ✅ Redis data storage for analytics
- ✅ Professional configuration interface
- ✅ User-friendly error messages
- ✅ Connection testing for all services
