# 🚀 DWX Connect Web Server - Quick Start Guide

Get your MT4 tick data streaming to a beautiful web interface in just 3 steps!

## ⚡ Quick Setup (3 Steps)

### Step 1: Install Dependencies
```bash
cd dwx/dwxconnect/python
pip install -r requirements.txt
```

**🐍 Python 3.12+ Users:** If you get a `distutils` error, run this instead:
```bash
pip uninstall eventlet -y
pip install -r requirements.txt
```

### Step 2: Configure MT4 Path
Edit `config.py` and update the `MT4_FILES_DIR` variable:

```python
# Find this line in config.py and update it:
MT4_FILES_DIR = '/path/to/your/mt4/MQL4/Files'
```

**Common paths:**
- **Windows:** `C:\Users\YourName\AppData\Roaming\MetaQuotes\Terminal\TERMINAL_ID\MQL4\Files`
- **Linux/Wine:** `/home/user/.wine/drive_c/users/user/AppData/Roaming/MetaQuotes/Terminal/TERMINAL_ID/MQL4/Files`

### Step 3: Start the Server
```bash
python start.py
```

That's it! 🎉 Open `http://localhost:5000` in your browser to view real-time tick data.

## 📊 What You Get

### 🔄 Real-time Tick Data
- Live bid/ask prices
- Spread calculations
- Visual price updates
- Multi-currency support

### 📈 Bar Data Visualization
- OHLC (Open, High, Low, Close) data
- Volume information
- Multiple timeframes
- Historical data

### 📋 Statistics Dashboard
- Total ticks processed
- Active currency pairs
- System uptime
- Performance metrics

## 🛠️ Customization

### Change Currency Pairs
Edit the `TICK_SYMBOLS` list in `config.py`:
```python
TICK_SYMBOLS = [
    'EURUSDi',  # Your broker's symbol names
    'GBPUSDi',
    'USDCHFi',
    # Add more symbols here
]
```

### Change Web Server Port
Edit `config.py`:
```python
WEB_SERVER_PORT = 8080  # Change to your preferred port
```

### Adjust Update Speed
Edit `config.py`:
```python
SLEEP_DELAY = 0.01  # Higher = less CPU usage, lower = more responsive
```

## 🔧 Troubleshooting

### "MT4 directory not found"
- Verify your MT4 installation path
- Make sure DWX Connect EA is installed and running
- Check that the MQL4/Files directory exists

### "No tick data received"
- Ensure MT4 is connected to your broker
- Check that symbols are in Market Watch
- Verify DWX Connect EA is active

### "Cannot access web interface"
- Check if port 5000 is available
- Try `http://127.0.0.1:5000` instead
- Disable firewall/antivirus temporarily

## 🎯 Pro Tips

1. **Monitor CPU Usage**: Start with fewer symbols, add more as needed
2. **Use Demo Account**: Test with demo data before going live
3. **Bookmark the Page**: Add `http://localhost:5000` to your bookmarks
4. **Multiple Browsers**: Open multiple tabs to monitor different views
5. **Mobile Friendly**: The interface works great on mobile devices

## 📁 File Overview

```
dwx/dwxconnect/python/
├── start.py                  # 🚀 Main startup script (use this!)
├── config.py                 # 🔧 Configuration file
├── web_server.py             # 🌐 Web server backend
├── web_tick_processor.py     # 📊 Tick data processor
├── requirements.txt          # 📦 Dependencies
└── templates/index.html      # 🎨 Web interface
```

## 🆘 Need Help?

1. **Check the logs**: The terminal will show detailed error messages
2. **Verify MT4 connection**: Look for DWX Connect messages in MT4
3. **Test configuration**: Run `python config.py` to validate settings
4. **Restart everything**: Sometimes a fresh start helps

## 🎉 Success!

If you see this in your terminal:
```
✅ Configuration is valid
🚀 Web Server starting on http://0.0.0.0:5000
📡 WebSocket server ready for real-time data streaming
🏃 Tick Processor running...
```

**You're all set!** Open your browser and enjoy real-time forex data visualization.

---

**Happy Trading! 📈💰** 