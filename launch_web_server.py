#!/usr/bin/env python3

import os
import sys
import time
import signal
import threading
from pathlib import Path

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def start_web_server():
    """Start the Flask web server with WebSocket support"""
    print("🌐 Starting Web Server...")
    
    # Import and run the web server
    from web_server import app, socketio, create_templates_dir, create_static_dir
    
    # Create required directories
    create_templates_dir()
    create_static_dir()
    
    print("🚀 Web Server starting on http://localhost:5000")
    print("📡 WebSocket server ready for real-time data streaming")
    
    # Run the Flask app with SocketIO
    socketio.run(app, host='0.0.0.0', port=5000, debug=False, use_reloader=False)

def start_tick_processor():
    """Start the tick processor"""
    print("📊 Starting Tick Processor...")
    
    # Wait a moment for web server to initialize
    time.sleep(2)
    
    # Import and run the tick processor
    from web_tick_processor import WebTickProcessor
    from os.path import exists
    
    # MT4 directory path - Update this to match your MT4 installation
    MT4_files_dir = '/home/mt4/.wine/drive_c/users/mt4/AppData/Roaming/MetaQuotes/Terminal/46A834A4BD020127C05B0DA2582F8F5C/MQL4/Files'
    
    # Check if directory exists
    if not exists(MT4_files_dir):
        print(f"❌ ERROR: MT4 directory not found: {MT4_files_dir}")
        print("Please update the MT4_files_dir variable in this script with the correct path.")
        print("\nCommon MT4 file directory patterns:")
        print("- Windows: C:/Users/YourUsername/AppData/Roaming/MetaQuotes/Terminal/TERMINAL_ID/MQL4/Files/")
        print("- Linux/Wine: /home/username/.wine/drive_c/users/username/AppData/Roaming/MetaQuotes/Terminal/TERMINAL_ID/MQL4/Files")
        return
    
    # Symbols to monitor (adjust as needed)
    tick_symbols = ['EURUSDi', 'GBPUSDi', 'USDCHFi', 'USDJPYi', 'AUDUSDi', 'USDCADi']
    
    # Bar data symbols and timeframes
    bar_symbols_timeframes = [
        ['EURUSDi', 'M1'],
        ['GBPUSDi', 'M1'],
        ['USDCHFi', 'M1'],
        ['USDJPYi', 'M1']
    ]
    
    try:
        # Initialize processor
        processor = WebTickProcessor(
            MT4_files_dir,
            verbose=True,
            tick_symbols=tick_symbols,
            bar_symbols_timeframes=bar_symbols_timeframes
        )
        
        # Status printing thread
        def status_printer():
            while processor.dwx.ACTIVE:
                time.sleep(30)  # Print status every 30 seconds
                processor.print_status()
        
        status_thread = threading.Thread(target=status_printer)
        status_thread.daemon = True
        status_thread.start()
        
        # Keep the processor running
        print("🏃 Tick Processor running...")
        
        while processor.dwx.ACTIVE:
            time.sleep(1)
            
    except Exception as e:
        print(f"❌ Tick Processor Error: {str(e)}")
        import traceback
        traceback.print_exc()

def signal_handler(signum, frame):
    """Handle shutdown signals"""
    print("\n⏹️  Shutting down DWX Web Server...")
    os._exit(0)

def main():
    """Main function to start the complete solution"""
    
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("="*80)
    print("🚀 DWX CONNECT WEB SERVER LAUNCHER")
    print("="*80)
    print("📊 This will start both the web server and tick processor")
    print("🌐 Web interface will be available at: http://localhost:5000")
    print("📡 Real-time tick data will be streamed via WebSocket")
    print("="*80)
    
    # Check if required dependencies are available
    try:
        import flask
        import flask_socketio
        print("✅ Flask and Flask-SocketIO are available")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install requirements: pip install -r requirements.txt")
        return
    
    # Check async mode support (optional)
    async_mode = None
    try:
        import gevent
        print("✅ gevent is available (Python 3.12+ compatible)")
        async_mode = 'gevent'
    except ImportError:
        try:
            import eventlet
            print("✅ eventlet is available")
            async_mode = 'eventlet'
        except ImportError:
            print("⚠️  Using threading mode (gevent/eventlet not available)")
            async_mode = 'threading'
    
    # Start web server in a separate thread
    web_server_thread = threading.Thread(target=start_web_server)
    web_server_thread.daemon = True
    web_server_thread.start()
    
    # Give web server time to start
    time.sleep(3)
    
    # Start tick processor in main thread
    print("🎯 Starting Tick Processor...")
    print("📋 Press Ctrl+C to stop both services")
    print("="*80)
    
    try:
        start_tick_processor()
    except KeyboardInterrupt:
        print("\n⏹️  Stopping services...")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        print("✅ DWX Web Server shutdown complete")

if __name__ == "__main__":
    main() 