# 🔧 Troubleshooting Guide

## Common Issues and Solutions

### 1. Python 3.12+ Compatibility Issues

**Problem**: `eventlet` fails with `ModuleNotFoundError: No module named 'distutils'`
```
❌ Missing required packages: eventlet
ModuleNotFoundError: No module named 'distutils'
```

**Cause**: Python 3.12+ removed the `distutils` module that eventlet depends on.

**Solutions**:

#### Option A: Use gevent (Recommended for Python 3.12+)
The solution now uses `gevent` instead of `eventlet` for Python 3.12+ compatibility:
```bash
pip install gevent==23.9.1
```

#### Option B: Use Threading Mode (Always Works)
The web server automatically falls back to threading mode if neither gevent nor eventlet are available:
```bash
python start.py
```

You'll see:
```
⚠️  Using threading mode (gevent/eventlet not available)
```

#### Option C: For Python < 3.12, use eventlet
If you're using Python 3.11 or earlier:
```bash
pip install eventlet==0.33.3
```

#### Option D: Install setuptools for distutils compatibility
```bash
pip install setuptools  # Provides distutils compatibility
pip install eventlet==0.33.3
```

### 2. MT4 Directory Not Found

**Problem**: 
```
❌ ERROR: MT4 directory not found: /path/to/mt4
```

**Solutions**:

1. **Find your MT4 directory**:
   - Windows: `C:\Users\YourName\AppData\Roaming\MetaQuotes\Terminal\TERMINAL_ID\MQL4\Files`
   - Linux/Wine: `/home/user/.wine/drive_c/users/user/AppData/Roaming/MetaQuotes/Terminal/TERMINAL_ID/MQL4/Files`
   - macOS: `/Users/YourName/Library/Application Support/MetaQuotes/Terminal/TERMINAL_ID/MQL4/Files`

2. **Update config.py**:
   ```python
   MT4_FILES_DIR = '/your/actual/path/here'
   ```

3. **Check if DWX folder exists**:
   The path should contain a `DWX` folder created by the DWX Connect EA

### 3. No Tick Data Received

**Problem**: Web interface shows "Waiting for tick data..."

**Solutions**:

1. **Check MT4 Connection**:
   - Ensure MT4 is connected to your broker
   - Check internet connection
   - Verify account login

2. **Check DWX Connect EA**:
   - EA should be running and show green smiley face
   - Check MT4 Expert Advisors tab for errors
   - Ensure "Allow DLL imports" is enabled

3. **Check Symbol Names**:
   - Verify symbol names in `config.py` match your broker
   - Common suffixes: `i` (CMC), `m` (FXCM), `.z` (OANDA)

4. **Check Market Hours**:
   - Forex markets are closed on weekends
   - Some pairs may be inactive during holidays

### 4. Web Interface Not Accessible

**Problem**: Cannot access http://localhost:5000

**Solutions**:

1. **Check Port Availability**:
   ```bash
   netstat -an | grep 5000  # Check if port is in use
   ```

2. **Try Different Port**:
   Edit `config.py`:
   ```python
   WEB_SERVER_PORT = 8080  # Change to different port
   ```

3. **Check Firewall**:
   - Allow Python/Flask through firewall
   - Temporarily disable antivirus/firewall to test

4. **Try Different Address**:
   - `http://127.0.0.1:5000`
   - `http://localhost:5000`

### 5. High CPU Usage

**Problem**: High CPU usage when running

**Solutions**:

1. **Reduce Update Frequency**:
   Edit `config.py`:
   ```python
   SLEEP_DELAY = 0.01  # Increase from 0.005
   ```

2. **Monitor Fewer Symbols**:
   ```python
   TICK_SYMBOLS = ['EURUSDi', 'GBPUSDi']  # Reduce list
   ```

3. **Disable Verbose Logging**:
   ```python
   VERBOSE_LOGGING = False
   ```

### 6. WebSocket Connection Issues

**Problem**: Browser shows "Disconnected" status

**Solutions**:

1. **Check Browser Console**:
   - Press F12 in browser
   - Look for WebSocket errors in Console tab

2. **Try Different Browser**:
   - Chrome, Firefox, Safari, Edge
   - Disable browser extensions

3. **Check Network**:
   - Ensure no proxy/VPN interference
   - Try from different network

### 7. Python Version Issues

**Problem**: Import errors or compatibility issues

**Solutions**:

1. **Check Python Version**:
   ```bash
   python --version  # Should be 3.7+
   ```

2. **Use Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   pip install -r requirements.txt
   ```

### 8. Permission Errors

**Problem**: Permission denied when accessing files

**Solutions**:

1. **Run as Administrator/Root** (if necessary):
   ```bash
   sudo python start.py  # Linux/Mac
   ```

2. **Check File Permissions**:
   ```bash
   ls -la dwx/dwxconnect/python/
   ```

3. **Fix Permissions**:
   ```bash
   chmod +x start.py
   ```

## 🆘 Getting Help

### Debug Steps:

1. **Enable Verbose Logging**:
   Set `VERBOSE_LOGGING = True` in `config.py`

2. **Check All Logs**:
   - Python console output
   - MT4 Expert Advisors tab
   - Browser console (F12)

3. **Test Configuration**:
   ```bash
   python config.py
   ```

4. **Test Individual Components**:
   ```bash
   python web_server.py  # Test web server only
   python web_tick_processor.py  # Test tick processor only
   ```

### System Information to Gather:

- Operating System and version
- Python version
- MT4 version and broker
- Error messages (exact text)
- What was happening when error occurred

### Alternative Solutions:

1. **Use Demo Account**: Test with demo data first
2. **Start Small**: Begin with 1-2 symbols, add more gradually
3. **Check Logs**: Always check MT4 and Python logs
4. **Restart Services**: Sometimes a fresh start helps

## 🔧 Advanced Troubleshooting

### Performance Optimization:

1. **Optimize Symbol Count**: Start with 2-3 symbols
2. **Adjust Sleep Delays**: Balance responsiveness vs CPU usage
3. **Use SSD**: Faster disk access for file operations
4. **Monitor Resources**: Watch CPU, memory, and disk usage

### Network Issues:

1. **Check Firewall**: Allow Python through firewall
2. **Test Localhost**: Try 127.0.0.1 instead of localhost
3. **Check Ports**: Ensure port 5000 is available

### MT4 Integration:

1. **EA Settings**: Verify DWX Connect EA settings
2. **File Permissions**: Check MQL4/Files directory permissions
3. **Symbol Availability**: Verify symbols in Market Watch

## 🐍 Python 3.12+ Quick Fix

If you're using **Python 3.12 or newer**, here's the fastest solution:

```bash
# Remove eventlet and install gevent instead
pip uninstall eventlet -y
pip install gevent==23.9.1

# Run the server
python start.py
```

You should see:
```
🔧 Using gevent for WebSocket support (Python 3.12+ compatible)
```

---

**Still having issues?** The web server now works with gevent, eventlet, or pure threading, so it should run successfully on any Python version! 