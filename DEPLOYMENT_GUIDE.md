# 🚀 Deployment Guide: DWX Tick Data Web Server

## ⚠️ **Important Architecture Considerations**

Your MT4 tick data application has a specific architecture that affects deployment:

```
MT4 (Local) → DWX Connect → Python Client → WebSocket Server → Browser
```

### **Key Challenge:**
- **MT4 must run locally** on your Debian VM (can't be deployed to cloud)
- **DWX Connect requires file system access** to MT4 directory
- **Web server needs persistent connection** to MT4

## 🏗️ **Deployment Strategies**

### **Option 1: Hybrid Deployment (Recommended)**
Keep MT4 data collection local, deploy web interface to cloud:

```
Local VM:           Cloud:
MT4 + Data Collector ↔ Web Server + Frontend
```

### **Option 2: Full Local with Public Access**
Use tunneling to expose your local server publicly:

```
Local VM:
MT4 + Complete Web Server ↔ Public Internet (via tunnel)
```

### **Option 3: Data Forwarding**
Stream data from local collector to cloud database:

```
Local VM:           Cloud:
MT4 + Data Collector → Database ← Web Server + Frontend
```

---

## 🌐 **Cloud Deployment Options**

### **1. Railway (Recommended - Free)**

**Why Railway?**
- ✅ Free tier: 500 hours/month
- ✅ Supports WebSocket connections
- ✅ Easy GitHub integration
- ✅ Built-in SSL and custom domains

**Setup Steps:**

1. **Create GitHub Repository**
   ```bash
   cd dwx/dwxconnect/python
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/dwx-web-server.git
   git push -u origin main
   ```

2. **Deploy to Railway**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway will automatically detect Python and deploy!

3. **Set Environment Variables**
   ```bash
   ENVIRONMENT=production
   MT4_DIRECTORY=/path/to/your/mt4/directory
   SYMBOLS=EURUSDi,GBPUSDi,USDCHFi,USDJPYi,AUDUSDi,USDCADi
   LOG_LEVEL=INFO
   ```

### **2. Render (Great Alternative)**

**Setup Steps:**

1. **Create Render Account**
   - Go to [render.com](https://render.com)
   - Connect your GitHub account

2. **Create Web Service**
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `python start.py`

3. **Environment Variables**
   ```bash
   ENVIRONMENT=production
   PORT=10000
   HOST=0.0.0.0
   ```

### **3. Heroku (Classic)**

**Setup Steps:**

1. **Install Heroku CLI**
   ```bash
   # On macOS
   brew install heroku/brew/heroku
   
   # On Linux
   sudo snap install heroku --classic
   ```

2. **Deploy**
   ```bash
   cd dwx/dwxconnect/python
   heroku create your-app-name
   heroku config:set ENVIRONMENT=production
   git push heroku main
   ```

---

## 🔧 **Local Tunneling Solutions**

If you want to keep everything local but make it publicly accessible:

### **1. ngrok (Easiest)**
```bash
# Install ngrok
npm install -g ngrok

# Run your local server
python start.py

# In another terminal, expose it
ngrok http 5000
```

### **2. Cloudflare Tunnel**
```bash
# Install cloudflared
curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb -o cloudflared.deb
sudo dpkg -i cloudflared.deb

# Create tunnel
cloudflared tunnel create dwx-server
cloudflared tunnel route dns dwx-server your-domain.com
cloudflared tunnel run dwx-server
```

---

## 📊 **Hybrid Architecture Setup**

**Best approach for your use case:**

### **Step 1: Local Data Collector**
Keep this running on your Debian VM:

```python
# local_collector.py
import requests
import json
from web_tick_processor import DWXTickProcessor

class CloudDataForwarder(DWXTickProcessor):
    def __init__(self):
        super().__init__()
        self.cloud_url = "https://your-app.railway.app"
    
    def on_tick_data(self, tick_data):
        # Send to cloud
        requests.post(f"{self.cloud_url}/api/tick", json=tick_data)
    
    def on_bar_data(self, bar_data):
        # Send to cloud
        requests.post(f"{self.cloud_url}/api/bar", json=bar_data)

if __name__ == "__main__":
    forwarder = CloudDataForwarder()
    forwarder.run()
```

### **Step 2: Cloud Web Server**
Deploy this to Railway/Render:

```python
# cloud_web_server.py
from flask import Flask, request, jsonify
from flask_socketio import SocketIO
import redis  # For data storage

app = Flask(__name__)
socketio = SocketIO(app)
redis_client = redis.Redis()

@app.route('/api/tick', methods=['POST'])
def receive_tick():
    data = request.json
    # Store in Redis
    redis_client.lpush('ticks', json.dumps(data))
    # Broadcast to WebSocket clients
    socketio.emit('tick_data', data)
    return jsonify({'status': 'ok'})

@app.route('/api/bar', methods=['POST'])
def receive_bar():
    data = request.json
    redis_client.lpush('bars', json.dumps(data))
    socketio.emit('bar_data', data)
    return jsonify({'status': 'ok'})
```

---

## 🔐 **Security & Configuration**

### **Environment Variables**
```bash
# Production settings
ENVIRONMENT=production
DEBUG=false
HOST=0.0.0.0
PORT=5000

# MT4 settings (for local deployment)
MT4_DIRECTORY=/path/to/mt4/directory
SYMBOLS=EURUSDi,GBPUSDi,USDCHFi,USDJPYi,AUDUSDi,USDCADi
TIMEFRAMES=M1,M5,M15,M30,H1,H4,D1

# Security
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=https://your-domain.com

# Database (if using cloud storage)
REDIS_URL=redis://localhost:6379
DATABASE_URL=postgresql://user:pass@host:port/db
```

### **Firewall & Security**
```bash
# Open required ports
sudo ufw allow 5000/tcp
sudo ufw enable

# SSL certificate (for production)
sudo certbot --nginx -d your-domain.com
```

---

## 📈 **Monitoring & Scaling**

### **Health Checks**
```python
@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'active_connections': len(socketio.clients),
        'mt4_connected': check_mt4_connection()
    })
```

### **Logging**
```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

---

## 🚀 **Quick Start Commands**

### **Local Development**
```bash
cd dwx/dwxconnect/python
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python start.py
```

### **Railway Deployment**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy
railway login
railway init
railway up
```

### **Docker Deployment**
```bash
# Build image
docker build -t dwx-web-server .

# Run locally
docker run -p 5000:5000 -e ENVIRONMENT=production dwx-web-server

# Deploy to any cloud provider
docker push your-registry/dwx-web-server
```

---

## 🎯 **Recommended Approach**

For your specific use case, I recommend:

1. **Use Railway for the web interface** (free, reliable)
2. **Keep MT4 + data collector on your Debian VM**
3. **Use webhooks/API calls** to send data from VM to Railway
4. **Set up Redis** on Railway for data storage
5. **Use ngrok** for development/testing

This gives you:
- ✅ Scalable web interface
- ✅ Reliable MT4 connection
- ✅ Free hosting
- ✅ Real-time data streaming
- ✅ Global accessibility

Would you like me to help you set up any of these deployment options? 