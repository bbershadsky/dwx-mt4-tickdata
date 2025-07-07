# DWX Connect Web Server Solution

A self-hosted web-based solution for real-time MetaTrader 4 tick data visualization and monitoring.

## 🚀 Features

- **Real-time Tick Data**: Live streaming of currency pair prices via WebSocket
- **Bar Data Visualization**: OHLC bar data with configurable timeframes
- **Modern Web Interface**: Beautiful, responsive web UI with real-time updates
- **Statistics Dashboard**: Monitor uptime, tick counts, and active pairs
- **Multi-pair Support**: Monitor multiple currency pairs simultaneously
- **Self-hosted**: Run locally without external dependencies
- **Cross-platform**: Works on Windows, Linux, and macOS

## 📋 Prerequisites

1. **MetaTrader 4** with DWX Connect EA installed and running
2. **Python 3.7+** installed on your system
3. **Active MT4 account** (demo or live) with market data access

## 🔧 Installation

### 1. Install Python Dependencies

```bash
# Navigate to the DWX Connect Python directory
cd dwx/dwxconnect/python

# Install required packages
pip install -r requirements.txt
```

### 2. Configure MT4 Path

Edit the `MT4_files_dir` variable in the following files to match your MT4 installation:

- `launch_web_server.py` (line 40)
- `web_tick_processor.py` (line 166)

**Common MT4 file directory patterns:**

**Windows:**
```
C:/Users/YourUsername/AppData/Roaming/MetaQuotes/Terminal/TERMINAL_ID/MQL4/Files/
```

**Linux/Wine:**
```
/home/username/.wine/drive_c/users/username/AppData/Roaming/MetaQuotes/Terminal/TERMINAL_ID/MQL4/Files
```

**macOS:**
```
/Users/YourUsername/Library/Application Support/MetaQuotes/Terminal/TERMINAL_ID/MQL4/Files/
```

### 3. Configure Symbols (Optional)

Edit the symbol lists in `launch_web_server.py` to match your broker's symbol names:

```python
# Symbols to monitor (adjust as needed)
tick_symbols = ['EURUSDi', 'GBPUSDi', 'USDCHFi', 'USDJPYi', 'AUDUSDi', 'USDCADi']

# Bar data symbols and timeframes
bar_symbols_timeframes = [
    ['EURUSDi', 'M1'],
    ['GBPUSDi', 'M1'],
    ['USDCHFi', 'M1'],
    ['USDJPYi', 'M1']
]
```

## 🏃 Usage

### Start the Complete Solution

Run the launcher script to start both the web server and tick processor:

```bash
python launch_web_server.py
```

### Start Components Individually

**Web Server Only:**
```bash
python web_server.py
```

**Tick Processor Only:**
```bash
python web_tick_processor.py
```

### Access the Web Interface

Open your browser and navigate to:
```
http://localhost:5000
```

## 📊 Web Interface Features

### 1. Tick Data View
- Real-time bid/ask prices
- Spread calculation
- Price update timestamps
- Visual flash effects on price changes

### 2. Bar Data View
- OHLC (Open, High, Low, Close) data
- Volume information
- Multiple timeframes support
- Tabular display of recent bars

### 3. Statistics Dashboard
- Total ticks received
- Total bars processed
- Active currency pairs count
- System uptime
- Real-time updates

## 🔧 Configuration Options

### Web Server Configuration

Edit `web_server.py` to customize:

- **Port**: Change `port=5000` to your desired port
- **Host**: Change `host='0.0.0.0'` to restrict access
- **CORS**: Modify `cors_allowed_origins` for security

### Tick Processor Configuration

Edit `web_tick_processor.py` to customize:

- **Update Frequency**: Modify `sleep_delay` parameter
- **Verbose Logging**: Set `verbose=True/False`
- **Retry Settings**: Adjust `max_retry_command_seconds`

## 🛠️ API Endpoints

### REST API

- `GET /`: Main web interface
- `GET /api/tick-data`: Get current tick data (JSON)
- `GET /api/bar-data`: Get current bar data (JSON)

### WebSocket Events

**Client → Server:**
- `connect`: Establish connection
- `join_ticks`: Subscribe to tick data
- `join_bars`: Subscribe to bar data

**Server → Client:**
- `tick_data`: Real-time tick updates
- `bar_data`: Real-time bar updates
- `initial_tick_data`: Initial data on connection
- `initial_bar_data`: Initial bar data on connection

## 🔍 Troubleshooting

### Common Issues

1. **"MT4 directory not found"**
   - Verify the MT4 installation path
   - Check if DWX Connect EA is running in MT4
   - Ensure the MQL4/Files directory exists

2. **"No tick data received"**
   - Verify MT4 is connected to the broker
   - Check if the symbols are available in Market Watch
   - Ensure DWX Connect EA is active and logging

3. **"Web interface not accessible"**
   - Check if port 5000 is available
   - Verify firewall settings
   - Try accessing via http://127.0.0.1:5000

4. **"Missing dependencies"**
   - Install requirements: `pip install -r requirements.txt`
   - Verify Python version (3.7+)

### Debug Mode

Enable debug mode for detailed logging:

```python
# In web_server.py, change:
socketio.run(app, host='0.0.0.0', port=5000, debug=True)
```

## 📁 File Structure

```
dwx/dwxconnect/python/
├── web_server.py              # Flask web server with WebSocket
├── web_tick_processor.py      # Tick data processor
├── launch_web_server.py       # Complete solution launcher
├── requirements.txt           # Python dependencies
├── templates/
│   └── index.html            # Web interface template
├── static/                   # Static files (CSS, JS)
└── api/
    └── dwx_client.py         # DWX Connect client
```

## 🎯 Performance Tips

1. **Optimize Symbol Count**: Monitor only necessary symbols to reduce load
2. **Adjust Update Frequency**: Increase `sleep_delay` for lower CPU usage
3. **Limit Bar History**: Reduce bar data retention in the web interface
4. **Use Production Mode**: Disable debug mode in production

## 🔒 Security Considerations

- Run on localhost only for security
- Use firewall rules to restrict access
- Consider HTTPS for production deployments
- Implement authentication for public access

## 📈 Extending the Solution

### Adding New Features

1. **Data Persistence**: Store tick data in a database
2. **Chart Visualization**: Add candlestick charts
3. **Alerts**: Implement price alerts and notifications
4. **Analytics**: Add technical indicators and analysis

### Custom Indicators

The solution can be extended to include custom indicators by:

1. Processing tick data in `web_tick_processor.py`
2. Adding calculation functions
3. Sending results via WebSocket
4. Displaying in the web interface

## 🆘 Support

For issues and questions:

1. Check the MT4 Expert Advisors tab for DWX Connect logs
2. Review the Python console output for errors
3. Verify MT4 connection and symbol availability
4. Check the browser console for JavaScript errors

## 📄 License

This solution is provided as-is for educational and personal use. Please ensure compliance with your broker's terms of service when using automated trading solutions.

---

**Made with ❤️ for the trading community** 