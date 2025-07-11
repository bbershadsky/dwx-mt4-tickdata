~/pacific_config/dwx/dwxconnect/python$ python start.py 
================================================================================
🚀 DWX CONNECT WEB SERVER
================================================================================
📊 Real-time MetaTrader 4 tick data monitoring
🌐 Modern web interface with WebSocket streaming
🔧 Self-hosted solution for forex data visualization
================================================================================
🔧 Validating configuration...
✅ Configuration is valid
✅ flask is available
✅ flask_socketio is available
✅ gevent is available (preferred)
⚠️  eventlet not available (will use threading fallback): No module named 'eventlet'
✅ All required packages are installed

📊 Current Configuration:
MT4 Directory: /home/mt4/.wine/drive_c/users/mt4/AppData/Roaming/MetaQuotes/Terminal/46A834A4BD020127C05B0DA2582F8F5C/MQL4/Files
Tick Symbols: 8 symbols
Bar Symbols: 6 combinations
Web Server: 0.0.0.0:5000

📋 USAGE INSTRUCTIONS:
==================================================
1. 🌐 Open your web browser
2. 🔗 Navigate to: http://localhost:5000
3. 📊 View real-time tick data in the web interface
4. ⏹️  Press Ctrl+C to stop the server
==================================================

🚀 Starting services...
🌐 Starting Web Server...
🔧 Using gevent for WebSocket support (Python 3.12+ compatible)
🚀 Web Server starting on http://0.0.0.0:5000
📡 WebSocket server ready for real-time data streaming
[2025-07-06 22:27:47,188] WARNING in __init__: WebSocket transport not available. Install gevent-websocket for improved performance.
Client connected: _Ko6H02IJ-Uq88LLAAAB
Client _Ko6H02IJ-Uq88LLAAAB joined tick room
Client _Ko6H02IJ-Uq88LLAAAB joined bar room
📡 Services are now running...
📊 Starting Tick Processor...
🚀 Initializing Web Tick Processor...
📊 Tick symbols: ['EURUSDi', 'GBPUSDi', 'USDCHFi', 'USDJPYi', 'AUDUSDi', 'USDCADi', 'EURGBPi', 'EURJPYi']
📈 Bar symbols/timeframes: [['EURUSDi', 'M1'], ['GBPUSDi', 'M1'], ['USDCHFi', 'M1'], ['USDJPYi', 'M1'], ['AUDUSDi', 'M1'], ['USDCADi', 'M1']]
💼 Account info: {'name': 'Boris Bershadsky', 'number': 2047987, 'currency': 'USD', 'leverage': 200, 'free_margin': 51199.079925, 'balance': 52379.64, 'equity': 51938.43}
🔔 Subscribing to tick data for 8 symbols...
📊 Subscribing to bar data for 6 symbol/timeframe combinations...
📚 Requesting historic data...
📊 BAR: 02:27:53 USDCHFi M1 O:0.79432 H:0.79439 L:0.79430 C:0.79436 V:105
📈 TICK: 02:27:53 EURUSDi BID:1.17726 ASK:1.17730 SPREAD:0.00004
📈 TICK: 02:27:53 GBPUSDi BID:1.36349 ASK:1.36354 SPREAD:0.00005
📈 TICK: 02:27:53 USDCHFi BID:0.79436 ASK:0.79446 SPREAD:0.00010
📈 TICK: 02:27:53 USDJPYi BID:144.68300 ASK:144.69100 SPREAD:0.00800
📈 TICK: 02:27:53 AUDUSDi BID:0.65300 ASK:0.65305 SPREAD:0.00005
📈 TICK: 02:27:53 USDCADi BID:1.36157 ASK:1.36165 SPREAD:0.00008
📈 TICK: 02:27:53 EURGBPi BID:0.86338 ASK:0.86344 SPREAD:0.00006
📈 TICK: 02:27:53 EURJPYi BID:170.32800 ASK:170.33800 SPREAD:0.01000
ℹ️  INFO: Successfully subscribed to: EURUSDi, GBPUSDi, USDCHFi, USDJPYi, AUDUSDi, USDCADi, EURGBPi, EURJPYi
✅ Web Tick Processor initialized successfully!
🌐 Web interface available at: http://localhost:5000
🏃 Tick Processor running...
Client disconnected: _Ko6H02IJ-Uq88LLAAAB
Client connected: uO6WML4HPyp_a2LKAAAD
ℹ️  INFO: Successfully subscribed to bar data: EURUSDi,M1,GBPUSDi,M1,USDCHFi,M1,USDJPYi,M1,AUDUSDi,M1,USDCADi,M1
📊 BAR: 02:27:59 EURUSDi M1 O:1.17732 H:1.17734 L:1.17724 C:1.17727 V:57
📊 BAR: 02:27:59 GBPUSDi M1 O:1.36351 H:1.36352 L:1.36346 C:1.36347 V:66
📊 BAR: 02:27:59 USDJPYi M1 O:144.64700 H:144.68800 L:144.64500 C:144.68000 V:125
📊 BAR: 02:27:59 AUDUSDi M1 O:0.65299 H:0.65307 L:0.65297 C:0.65297 V:48
📊 BAR: 02:27:59 USDCADi M1 O:1.36153 H:1.36156 L:1.36148 C:1.36155 V:86
📚 HISTORIC: EURUSDi D1 - 5 bars loaded
ℹ️  INFO: Successfully read historic data for EURUSDi_D1.
📈 TICK: 02:28:00 EURUSDi BID:1.17727 ASK:1.17730 SPREAD:0.00003
📈 TICK: 02:28:00 GBPUSDi BID:1.36350 ASK:1.36357 SPREAD:0.00007
📈 TICK: 02:28:00 USDCHFi BID:0.79434 ASK:0.79444 SPREAD:0.00010
📈 TICK: 02:28:00 USDJPYi BID:144.68100 ASK:144.68900 SPREAD:0.00800
📈 TICK: 02:28:00 AUDUSDi BID:0.65301 ASK:0.65306 SPREAD:0.00005
📈 TICK: 02:28:00 USDCADi BID:1.36155 ASK:1.36163 SPREAD:0.00008
📈 TICK: 02:28:00 EURGBPi BID:0.86338 ASK:0.86343 SPREAD:0.00005
📈 TICK: 02:28:00 EURJPYi BID:170.32600 ASK:170.33500 SPREAD:0.00900
📚 HISTORIC: GBPUSDi D1 - 5 bars loaded
ℹ️  INFO: Successfully read historic data for GBPUSDi_D1.
📚 HISTORIC: USDCHFi D1 - 5 bars loaded
ℹ️  INFO: Successfully read historic data for USDCHFi_D1.
📈 TICK: 02:28:00 EURJPYi BID:170.32700 ASK:170.33500 SPREAD:0.00800
📊 BAR: 02:28:00 USDJPYi M1 O:144.67900 H:144.68300 L:144.67000 C:144.68100 V:87
📈 TICK: 02:28:01 EURJPYi BID:170.32700 ASK:170.33600 SPREAD:0.00900
📈 TICK: 02:28:01 GBPUSDi BID:1.36350 ASK:1.36356 SPREAD:0.00006
📊 BAR: 02:28:01 GBPUSDi M1 O:1.36346 H:1.36351 L:1.36346 C:1.36350 V:46
📈 TICK: 02:28:01 USDJPYi BID:144.68000 ASK:144.68900 SPREAD:0.00900
📈 TICK: 02:28:01 USDJPYi BID:144.68100 ASK:144.68900 SPREAD:0.00800
📈 TICK: 02:28:01 EURJPYi BID:170.32600 ASK:170.33600 SPREAD:0.01000
📈 TICK: 02:28:02 USDJPYi BID:144.68000 ASK:144.68900 SPREAD:0.00900
📈 TICK: 02:28:02 EURJPYi BID:170.32600 ASK:170.33500 SPREAD:0.00900
📈 TICK: 02:28:02 EURJPYi BID:170.32500 ASK:170.33500 SPREAD:0.01000
📈 TICK: 02:28:02 EURUSDi BID:1.17726 ASK:1.17729 SPREAD:0.00003
📈 TICK: 02:28:02 GBPUSDi BID:1.36349 ASK:1.36356 SPREAD:0.00007
📈 TICK: 02:28:02 USDCHFi BID:0.79435 ASK:0.79444 SPREAD:0.00009
📈 TICK: 02:28:02 EURGBPi BID:0.86338 ASK:0.86343 SPREAD:0.00005
📈 TICK: 02:28:02 EURJPYi BID:170.32500 ASK:170.33400 SPREAD:0.00900
📊 BAR: 02:28:02 EURUSDi M1 O:1.17727 H:1.17730 L:1.17724 C:1.17727 V:56
📊 BAR: 02:28:02 USDCHFi M1 O:0.79436 H:0.79437 L:0.79432 C:0.79434 V:60
📈 TICK: 02:28:02 EURUSDi BID:1.17726 ASK:1.17730 SPREAD:0.00004
📈 TICK: 02:28:02 USDCHFi BID:0.79434 ASK:0.79444 SPREAD:0.00010
📊 BAR: 02:28:02 USDCADi M1 O:1.36156 H:1.36159 L:1.36155 C:1.36155 V:64
📈 TICK: 02:28:02 USDCADi BID:1.36156 ASK:1.36163 SPREAD:0.00007
📈 TICK: 02:28:02 EURJPYi BID:170.32600 ASK:170.33500 SPREAD:0.00900
📈 TICK: 02:28:02 USDCHFi BID:0.79435 ASK:0.79444 SPREAD:0.00009
📈 TICK: 02:28:02 EURGBPi BID:0.86338 ASK:0.86344 SPREAD:0.00006
📈 TICK: 02:28:02 EURJPYi BID:170.32500 ASK:170.33600 SPREAD:0.01100
📈 TICK: 02:28:02 EURUSDi BID:1.17725 ASK:1.17729 SPREAD:0.00004
📈 TICK: 02:28:02 USDCHFi BID:0.79436 ASK:0.79446 SPREAD:0.00010
📈 TICK: 02:28:02 USDJPYi BID:144.68400 ASK:144.69300 SPREAD:0.00900
📈 TICK: 02:28:02 USDCADi BID:1.36156 ASK:1.36164 SPREAD:0.00008
📈 TICK: 02:28:02 EURJPYi BID:170.32600 ASK:170.33600 SPREAD:0.01000
📈 TICK: 02:28:02 EURUSDi BID:1.17725 ASK:1.17728 SPREAD:0.00003
📈 TICK: 02:28:02 GBPUSDi BID:1.36348 ASK:1.36355 SPREAD:0.00007
📈 TICK: 02:28:02 USDJPYi BID:144.68400 ASK:144.69200 SPREAD:0.00800
📈 TICK: 02:28:02 AUDUSDi BID:0.65300 ASK:0.65305 SPREAD:0.00005
📈 TICK: 02:28:02 USDCADi BID:1.36157 ASK:1.36164 SPREAD:0.00007
📈 TICK: 02:28:02 EURGBPi BID:0.86337 ASK:0.86342 SPREAD:0.00005
📈 TICK: 02:28:02 EURJPYi BID:170.32600 ASK:170.33500 SPREAD:0.00900
📊 BAR: 02:28:02 AUDUSDi M1 O:0.65297 H:0.65301 L:0.65293 C:0.65301 V:35
📈 TICK: 02:28:03 EURUSDi BID:1.17723 ASK:1.17727 SPREAD:0.00004
📈 TICK: 02:28:03 USDJPYi BID:144.68400 ASK:144.69300 SPREAD:0.00900
📈 TICK: 02:28:03 EURJPYi BID:170.32500 ASK:170.33500 SPREAD:0.01000
📈 TICK: 02:28:04 GBPUSDi BID:1.36348 ASK:1.36354 SPREAD:0.00006
📈 TICK: 02:28:04 AUDUSDi BID:0.65297 ASK:0.65302 SPREAD:0.00005
📈 TICK: 02:28:04 USDCADi BID:1.36157 ASK:1.36165 SPREAD:0.00008
📈 TICK: 02:28:04 EURJPYi BID:170.32600 ASK:170.33600 SPREAD:0.01000
📈 TICK: 02:28:04 GBPUSDi BID:1.36348 ASK:1.36355 SPREAD:0.00007
📈 TICK: 02:28:04 USDJPYi BID:144.68500 ASK:144.69300 SPREAD:0.00800
📈 TICK: 02:28:04 EURJPYi BID:170.32700 ASK:170.33600 SPREAD:0.00900
📈 TICK: 02:28:04 EURJPYi BID:170.32600 ASK:170.33600 SPREAD:0.01000
📈 TICK: 02:28:05 EURUSDi BID:1.17722 ASK:1.17725 SPREAD:0.00003
📈 TICK: 02:28:05 GBPUSDi BID:1.36348 ASK:1.36354 SPREAD:0.00006
📈 TICK: 02:28:05 USDCHFi BID:0.79437 ASK:0.79447 SPREAD:0.00010
📈 TICK: 02:28:05 USDJPYi BID:144.69200 ASK:144.70000 SPREAD:0.00800
📈 TICK: 02:28:05 AUDUSDi BID:0.65294 ASK:0.65299 SPREAD:0.00005
📈 TICK: 02:28:05 USDCADi BID:1.36159 ASK:1.36166 SPREAD:0.00007
📈 TICK: 02:28:05 EURGBPi BID:0.86336 ASK:0.86342 SPREAD:0.00006
📈 TICK: 02:28:05 EURJPYi BID:170.33200 ASK:170.34200 SPREAD:0.01000
📈 TICK: 02:28:05 EURUSDi BID:1.17722 ASK:1.17726 SPREAD:0.00004
📈 TICK: 02:28:05 USDCADi BID:1.36158 ASK:1.36166 SPREAD:0.00008
📈 TICK: 02:28:05 EURJPYi BID:170.33300 ASK:170.34200 SPREAD:0.00900
📈 TICK: 02:28:05 USDCHFi BID:0.79438 ASK:0.79447 SPREAD:0.00009
📈 TICK: 02:28:05 USDJPYi BID:144.69100 ASK:144.70000 SPREAD:0.00900
📈 TICK: 02:28:05 USDCADi BID:1.36159 ASK:1.36166 SPREAD:0.00007
📈 TICK: 02:28:05 EURJPYi BID:170.33200 ASK:170.34200 SPREAD:0.01000
📈 TICK: 02:28:05 USDJPYi BID:144.69200 ASK:144.70000 SPREAD:0.00800
📈 TICK: 02:28:05 EURJPYi BID:170.33300 ASK:170.34200 SPREAD:0.00900
📈 TICK: 02:28:05 USDJPYi BID:144.69100 ASK:144.69900 SPREAD:0.00800
📈 TICK: 02:28:05 EURJPYi BID:170.33300 ASK:170.34200 SPREAD:0.00900
📈 TICK: 02:28:05 EURJPYi BID:170.33200 ASK:170.34200 SPREAD:0.01000
📈 TICK: 02:28:05 USDCHFi BID:0.79437 ASK:0.79447 SPREAD:0.00010
📈 TICK: 02:28:05 EURGBPi BID:0.86337 ASK:0.86342 SPREAD:0.00005
📈 TICK: 02:28:05 USDJPYi BID:144.69000 ASK:144.69900 SPREAD:0.00900
📈 TICK: 02:28:05 AUDUSDi BID:0.65292 ASK:0.65297 SPREAD:0.00005
📈 TICK: 02:28:05 USDCADi BID:1.36159 ASK:1.36167 SPREAD:0.00008
📈 TICK: 02:28:05 EURJPYi BID:170.33100 ASK:170.34100 SPREAD:0.01000
📈 TICK: 02:28:06 EURUSDi BID:1.17722 ASK:1.17725 SPREAD:0.00003
📈 TICK: 02:28:06 USDCHFi BID:0.79436 ASK:0.79446 SPREAD:0.00010
📈 TICK: 02:28:06 USDJPYi BID:144.69000 ASK:144.69800 SPREAD:0.00800
📈 TICK: 02:28:06 USDCADi BID:1.36160 ASK:1.36167 SPREAD:0.00007
📈 TICK: 02:28:06 EURGBPi BID:0.86336 ASK:0.86342 SPREAD:0.00006
📈 TICK: 02:28:06 EURJPYi BID:170.33000 ASK:170.34000 SPREAD:0.01000
📈 TICK: 02:28:06 EURUSDi BID:1.17722 ASK:1.17726 SPREAD:0.00004
📈 TICK: 02:28:06 USDCADi BID:1.36159 ASK:1.36167 SPREAD:0.00008
📈 TICK: 02:28:06 EURGBPi BID:0.86335 ASK:0.86342 SPREAD:0.00007
📈 TICK: 02:28:06 EURJPYi BID:170.33100 ASK:170.34000 SPREAD:0.00900
📈 TICK: 02:28:06 AUDUSDi BID:0.65293 ASK:0.65297 SPREAD:0.00004
📈 TICK: 02:28:06 USDCADi BID:1.36159 ASK:1.36166 SPREAD:0.00007
📈 TICK: 02:28:06 AUDUSDi BID:0.65292 ASK:0.65297 SPREAD:0.00005
📈 TICK: 02:28:07 USDCHFi BID:0.79437 ASK:0.79446 SPREAD:0.00009
📊 Statistics: 100 ticks, 12 bars, uptime: 15s
📈 TICK: 02:28:07 USDJPYi BID:144.69100 ASK:144.69900 SPREAD:0.00800
📈 TICK: 02:28:07 AUDUSDi BID:0.65292 ASK:0.65298 SPREAD:0.00006
📈 TICK: 02:28:07 EURGBPi BID:0.86336 ASK:0.86342 SPREAD:0.00006
📈 TICK: 02:28:07 EURJPYi BID:170.33200 ASK:170.34200 SPREAD:0.01000
📈 TICK: 02:28:07 USDJPYi BID:144.69000 ASK:144.69900 SPREAD:0.00900
📈 TICK: 02:28:07 USDCADi BID:1.36159 ASK:1.36167 SPREAD:0.00008
📈 TICK: 02:28:07 EURJPYi BID:170.33100 ASK:170.34200 SPREAD:0.01100
📈 TICK: 02:28:07 EURJPYi BID:170.33200 ASK:170.34200 SPREAD:0.01000
Client disconnected: uO6WML4HPyp_a2LKAAAD
📈 TICK: 02:28:08 USDCHFi BID:0.79437 ASK:0.79447 SPREAD:0.00010
📈 TICK: 02:28:08 USDJPYi BID:144.69100 ASK:144.69900 SPREAD:0.00800
📈 TICK: 02:28:08 EURJPYi BID:170.33100 ASK:170.34200 SPREAD:0.01100
📈 TICK: 02:28:08 USDCHFi BID:0.79436 ASK:0.79446 SPREAD:0.00010
📈 TICK: 02:28:08 USDJPYi BID:144.69000 ASK:144.69900 SPREAD:0.00900
Client connected: Stitu1-XnKyaBmkKAAAF
