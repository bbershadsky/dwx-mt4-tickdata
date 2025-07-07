# 🚀 Render Deployment Guide

## 🎯 Why Render?

- ✅ **Free tier**: 750 hours/month (enough for 24/7 usage)
- ✅ **WebSocket support**: Perfect for real-time data
- ✅ **Auto-deploy**: From GitHub automatically
- ✅ **SSL certificates**: Built-in HTTPS
- ✅ **Zero config**: Just push your code

## 📋 Prerequisites

1. **GitHub account**
2. **Render account** (free at [render.com](https://render.com))
3. **Your MT4 tick data system** (working locally)

## 🚀 Quick Deploy (5 minutes)

### **Step 1: Create GitHub Repository**

```bash
cd dwx/dwxconnect/python
git init
git add .
git commit -m "Initial commit"
```

Create a new repository on GitHub, then:

```bash
git remote add origin https://github.com/yourusername/dwx-web-server.git
git branch -M main
git push -u origin main
```

### **Step 2: Deploy to Render**

1. **Sign up at [render.com](https://render.com)**
2. **Connect your GitHub account**
3. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Choose your repository: `dwx-web-server`

4. **Configure the service:**
   - **Name**: `dwx-tick-data-server`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python start.py`
   - **Plan**: `Free` (0$/month)

5. **Set Environment Variables:**
   ```bash
   ENVIRONMENT=production
   HOST=0.0.0.0
   DEBUG=false
   LOG_LEVEL=INFO
   SYMBOLS=EURUSDi,GBPUSDi,USDCHFi,USDJPYi,AUDUSDi,USDCADi
   TIMEFRAMES=M1,M5,M15,M30,H1,H4,D1
   WEBSOCKET_ASYNC_MODE=gevent
   MAX_TICK_HISTORY=500
   MAX_BAR_HISTORY=50
   ```

6. **Click "Create Web Service"**

### **Step 3: Access Your App**

Your app will be available at:
```
https://your-app-name.onrender.com
```

## 🔧 Advanced Configuration

### **Using render.yaml (Recommended)**

Create a `render.yaml` file in your project root:

```yaml
services:
  - type: web
    name: dwx-tick-data-server
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: python start.py
    envVars:
      - key: ENVIRONMENT
        value: production
      - key: HOST
        value: 0.0.0.0
      - key: DEBUG
        value: false
      - key: LOG_LEVEL
        value: INFO
      - key: SYMBOLS
        value: EURUSDi,GBPUSDi,USDCHFi,USDJPYi,AUDUSDi,USDCADi
      - key: TIMEFRAMES
        value: M1,M5,M15,M30,H1,H4,D1
      - key: WEBSOCKET_ASYNC_MODE
        value: gevent
      - key: MAX_TICK_HISTORY
        value: 500
      - key: MAX_BAR_HISTORY
        value: 50
    healthCheckPath: /health
    autoDeploy: true
```

Then deploy with:
```bash
git add render.yaml
git commit -m "Add render.yaml config"
git push
```

### **Custom Domain (Optional)**

1. In your Render dashboard, go to your service
2. Click "Settings" → "Custom Domains"
3. Add your domain: `your-domain.com`
4. Update your DNS records as instructed

## 🔄 Connecting Your Local MT4 to Cloud

Since MT4 must run locally, you'll need to forward data to your cloud deployment:

### **Option 1: Webhook Forwarder (Recommended)**

Create `cloud_forwarder.py` on your local machine:

```python
import requests
import json
from web_tick_processor import DWXTickProcessor

class CloudForwarder(DWXTickProcessor):
    def __init__(self, cloud_url):
        super().__init__()
        self.cloud_url = cloud_url
        
    def on_tick_data(self, tick_data):
        try:
            response = requests.post(
                f"{self.cloud_url}/api/forward/tick",
                json=tick_data,
                timeout=5
            )
            if response.status_code == 200:
                print(f"✅ Forwarded tick: {tick_data['symbol']}")
            else:
                print(f"❌ Failed to forward tick: {response.status_code}")
        except Exception as e:
            print(f"❌ Error forwarding tick: {e}")
    
    def on_bar_data(self, bar_data):
        try:
            response = requests.post(
                f"{self.cloud_url}/api/forward/bar",
                json=bar_data,
                timeout=5
            )
            if response.status_code == 200:
                print(f"✅ Forwarded bar: {bar_data['symbol']}")
        except Exception as e:
            print(f"❌ Error forwarding bar: {e}")

if __name__ == "__main__":
    forwarder = CloudForwarder("https://your-app.onrender.com")
    forwarder.run()
```

### **Option 2: WebSocket Bridge**

Create `websocket_bridge.py` on your local machine:

```python
import asyncio
import websockets
import json
from web_tick_processor import DWXTickProcessor

class WebSocketBridge(DWXTickProcessor):
    def __init__(self, websocket_url):
        super().__init__()
        self.websocket_url = websocket_url
        self.websocket = None
        
    async def connect_websocket(self):
        try:
            self.websocket = await websockets.connect(self.websocket_url)
            print("✅ Connected to cloud WebSocket")
        except Exception as e:
            print(f"❌ Failed to connect to WebSocket: {e}")
    
    def on_tick_data(self, tick_data):
        if self.websocket:
            asyncio.create_task(self.websocket.send(json.dumps({
                'type': 'tick',
                'data': tick_data
            })))
    
    def on_bar_data(self, bar_data):
        if self.websocket:
            asyncio.create_task(self.websocket.send(json.dumps({
                'type': 'bar',
                'data': bar_data
            })))

if __name__ == "__main__":
    bridge = WebSocketBridge("wss://your-app.onrender.com/socket.io/")
    asyncio.run(bridge.connect_websocket())
    bridge.run()
```

## 🎛️ Render Dashboard

Access your deployment at: https://dashboard.render.com

### **Useful Commands:**

- **View Logs**: Dashboard → Your Service → Logs
- **Manual Deploy**: Dashboard → Your Service → Manual Deploy
- **Environment Variables**: Dashboard → Your Service → Environment
- **Metrics**: Dashboard → Your Service → Metrics

### **Monitoring:**

```bash
# Health check
curl https://your-app.onrender.com/health

# Tick data API
curl https://your-app.onrender.com/api/tick-data

# Bar data API  
curl https://your-app.onrender.com/api/bar-data
```

## 🔧 Local Development vs Production

### **Local Development**
```bash
# Local
python start.py
# Access: http://localhost:5000
```

### **Production on Render**
```bash
# Automatic from GitHub
git push origin main
# Access: https://your-app.onrender.com
```

## 🐛 Troubleshooting

### **Common Issues:**

1. **Build Failed**
   - Check `requirements.txt` has all dependencies
   - Verify Python version in `runtime.txt`
   - Check build logs in Render dashboard

2. **Service Won't Start**
   - Check start command: `python start.py`
   - Verify environment variables
   - Check application logs

3. **WebSocket Connection Failed**
   - Ensure `gevent` is in requirements.txt
   - Check CORS settings
   - Verify WebSocket endpoint

4. **No Data Showing**
   - Check MT4 connection locally
   - Verify data forwarding setup
   - Check API endpoints

### **Debug Commands:**

```bash
# Check health
curl https://your-app.onrender.com/health

# Check logs
# (Use Render dashboard)

# Test WebSocket
# (Use browser developer tools)
```

## 💡 Tips for Success

1. **Use the free tier efficiently**
   - Render free tier gives you 750 hours/month
   - Your app will sleep after 15 minutes of inactivity
   - First request after sleep takes ~30 seconds

2. **Optimize for cold starts**
   - Use lightweight dependencies
   - Minimize startup time
   - Consider using a keep-alive service

3. **Monitor your usage**
   - Check Render dashboard for hours used
   - Set up alerts for high usage
   - Consider upgrading if needed

4. **Security best practices**
   - Use environment variables for secrets
   - Enable HTTPS (automatic on Render)
   - Validate all inputs

## 📈 Scaling Options

### **Free Tier Limits:**
- 750 hours/month
- 512MB RAM
- 1 CPU
- Apps sleep after 15 minutes

### **Paid Tiers:**
- $7/month - Always on, 512MB RAM
- $25/month - 1GB RAM, faster builds
- $85/month - 2GB RAM, priority support

## 🎉 Next Steps

1. **Deploy your app** using the steps above
2. **Set up local data forwarding** from your MT4 system
3. **Test the WebSocket connection** in your browser
4. **Monitor your app** using the Render dashboard
5. **Share your live trading dashboard** with others!

## 📞 Support

- **Render Documentation**: https://render.com/docs
- **GitHub Issues**: For this project
- **Community**: Render community forums

---

**Happy Trading! 📊🚀** 