#!/usr/bin/env python3

"""
Main startup script for DWX Connect Web Server

This script launches the complete web-based tick data monitoring solution
using settings from the config.py file.
"""

import os
import sys
import time
import signal
import threading
import logging
from pathlib import Path
from config import get_config
from web_server import app, socketio
from web_tick_processor import DWXTickProcessor

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import configuration
try:
    from config import (
        validate_configuration,
        get_mt4_files_dir,
        get_tick_symbols,
        get_bar_symbols_timeframes,
        get_web_server_config,
        get_processor_config,
        get_historic_data_config
    )
except ImportError as e:
    print(f"❌ Error importing configuration: {e}")
    print("Please ensure config.py is in the same directory")
    sys.exit(1)

# Get configuration
config = get_config()

# Set up logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def print_banner():
    """Print startup banner"""
    print("="*80)
    print("🚀 DWX CONNECT WEB SERVER")
    print("="*80)
    print("📊 Real-time MetaTrader 4 tick data monitoring")
    print("🌐 Modern web interface with WebSocket streaming")
    print("🔧 Self-hosted solution for forex data visualization")
    print("="*80)

def check_dependencies():
    """Check if required Python packages are installed"""
    required_packages = {
        'flask': 'flask',
        'flask_socketio': 'flask_socketio'
    }
    
    optional_packages = {
        'gevent': 'gevent',
        'eventlet': 'eventlet'
    }
    
    missing_packages = []
    
    # Check required packages
    for package_name, import_name in required_packages.items():
        try:
            __import__(import_name)
            print(f"✅ {package_name} is available")
        except ImportError as e:
            print(f"❌ {package_name} import failed: {e}")
            missing_packages.append(package_name)
    
    # Check optional packages
    for package_name, import_name in optional_packages.items():
        try:
            __import__(import_name)
            print(f"✅ {package_name} is available (preferred)")
        except ImportError as e:
            print(f"⚠️  {package_name} not available (will use threading fallback): {e}")
    
    if missing_packages:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        print("Please install them using: pip install -r requirements.txt")
        return False
    
    print("✅ All required packages are installed")
    return True

def start_web_server():
    """Start the Flask web server with WebSocket support"""
    print("🌐 Starting Web Server...")
    
    try:
        # Import and configure the web server
        from web_server import app, socketio, create_templates_dir, create_static_dir
        
        # Create required directories
        create_templates_dir()
        create_static_dir()
        
        # Get configuration
        config = get_web_server_config()
        
        print(f"🚀 Web Server starting on http://{config['host']}:{config['port']}")
        print("📡 WebSocket server ready for real-time data streaming")
        
        # Run the Flask app with SocketIO
        socketio.run(
            app, 
            host=config['host'], 
            port=config['port'], 
            debug=config['debug'], 
            use_reloader=False
        )
        
    except Exception as e:
        print(f"❌ Web Server Error: {str(e)}")
        import traceback
        traceback.print_exc()

def start_tick_processor():
    """Start the tick processor"""
    print("📊 Starting Tick Processor...")
    
    # Wait for web server to initialize
    time.sleep(2)
    
    try:
        # Import the tick processor
        from web_tick_processor import WebTickProcessor
        
        # Get configuration
        mt4_dir = get_mt4_files_dir()
        tick_symbols = get_tick_symbols()
        bar_symbols = get_bar_symbols_timeframes()
        processor_config = get_processor_config()
        historic_config = get_historic_data_config()
        
        # Initialize processor
        processor = WebTickProcessor(
            mt4_dir,
            sleep_delay=processor_config['sleep_delay'],
            max_retry_command_seconds=processor_config['max_retry_command_seconds'],
            verbose=processor_config['verbose'],
            tick_symbols=tick_symbols,
            bar_symbols_timeframes=bar_symbols
        )
        
        # Status printing thread
        def status_printer():
            while processor.dwx.ACTIVE:
                time.sleep(processor_config['status_print_interval'])
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
    print("✅ Goodbye!")
    os._exit(0)

def print_usage_instructions():
    """Print usage instructions"""
    config = get_web_server_config()
    print("\n📋 USAGE INSTRUCTIONS:")
    print("="*50)
    print(f"1. 🌐 Open your web browser")
    print(f"2. 🔗 Navigate to: http://localhost:{config['port']}")
    print(f"3. 📊 View real-time tick data in the web interface")
    print(f"4. ⏹️  Press Ctrl+C to stop the server")
    print("="*50)

def run_tick_processor():
    """Run the tick processor in a separate thread"""
    try:
        logger.info("Starting DWX Tick Processor...")
        processor = DWXTickProcessor()
        processor.run()
    except Exception as e:
        logger.error(f"Error in tick processor: {e}")
        if config.DEBUG:
            import traceback
            traceback.print_exc()

def check_mt4_directory():
    """Check if MT4 directory exists"""
    if not os.path.exists(config.MT4_DIRECTORY):
        logger.warning(f"MT4 directory not found: {config.MT4_DIRECTORY}")
        logger.warning("Data collection will not work without MT4 connection")
        return False
    return True

def main():
    """Main application entry point"""
    logger.info("=" * 50)
    logger.info("DWX Tick Data Web Server")
    logger.info("=" * 50)
    logger.info(f"Environment: {config.ENVIRONMENT}")
    logger.info(f"Host: {config.HOST}")
    logger.info(f"Port: {config.PORT}")
    logger.info(f"Debug: {config.DEBUG}")
    logger.info(f"MT4 Directory: {config.MT4_DIRECTORY}")
    logger.info("=" * 50)
    
    # Check MT4 directory
    mt4_available = check_mt4_directory()
    if not mt4_available:
        logger.warning("MT4 directory not found - running in demo mode")
        logger.warning("To enable data collection, set MT4_DIRECTORY environment variable")
    
    # Start tick processor in separate thread (only if MT4 is available)
    if mt4_available:
        tick_thread = threading.Thread(target=run_tick_processor, daemon=True)
        tick_thread.start()
        logger.info("Tick processor started")
    else:
        logger.info("Tick processor disabled (no MT4 connection)")
    
    # Start web server
    try:
        logger.info(f"Starting web server on {config.HOST}:{config.PORT}")
        socketio.run(
            app,
            host=config.HOST,
            port=config.PORT,
            debug=config.DEBUG,
            allow_unsafe_werkzeug=True  # For development
        )
    except Exception as e:
        logger.error(f"Failed to start web server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 