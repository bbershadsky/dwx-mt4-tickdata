#!/usr/bin/env python3

"""
Configuration file for DWX Connect Web Server

Modify these settings to customize the behavior of the web server
and tick processor according to your needs.
"""

import os
from pathlib import Path

# =============================================================================
# DWX Tick Data Web Server Configuration
# =============================================================================

class Config:
    # Web Server Settings
    HOST = os.getenv('HOST', '0.0.0.0')  # Changed to 0.0.0.0 for deployment
    PORT = int(os.getenv('PORT', 5000))   # Use PORT env var for deployment
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # MT4 Connection Settings
    MT4_DIRECTORY = os.getenv('MT4_DIRECTORY', '/Users/bopr/Documents/pacific_config/CMC Markets MetaTrader 4')
    
    # DWX Connect Settings
    SYMBOLS = os.getenv('SYMBOLS', 'EURUSDi,GBPUSDi,USDCHFi,USDJPYi,AUDUSDi,USDCADi').split(',')
    TIMEFRAMES = os.getenv('TIMEFRAMES', 'M1,M5,M15,M30,H1,H4,D1').split(',')
    
    # Update frequencies (in seconds)
    TICK_UPDATE_INTERVAL = float(os.getenv('TICK_UPDATE_INTERVAL', '0.1'))
    BAR_UPDATE_INTERVAL = float(os.getenv('BAR_UPDATE_INTERVAL', '1.0'))
    
    # Data storage limits
    MAX_TICK_HISTORY = int(os.getenv('MAX_TICK_HISTORY', '1000'))
    MAX_BAR_HISTORY = int(os.getenv('MAX_BAR_HISTORY', '100'))
    
    # WebSocket Settings
    WEBSOCKET_ASYNC_MODE = os.getenv('WEBSOCKET_ASYNC_MODE', 'auto')  # auto, gevent, eventlet, threading
    
    # Deployment Settings
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')  # development, production
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Deployment-specific configurations
class ProductionConfig(Config):
    DEBUG = False
    ENVIRONMENT = 'production'
    
class DevelopmentConfig(Config):
    DEBUG = True
    ENVIRONMENT = 'development'
    HOST = '127.0.0.1'  # Local development

# Choose config based on environment
def get_config():
    env = os.getenv('ENVIRONMENT', 'development')
    if env == 'production':
        return ProductionConfig()
    else:
        return DevelopmentConfig()

# Default config instance
config = get_config()

# =============================================================================
# Broker-specific Symbol Mappings
# =============================================================================

BROKER_SYMBOLS = {
    'cmc': {
        'EURUSD': 'EURUSDi',
        'GBPUSD': 'GBPUSDi', 
        'USDCHF': 'USDCHFi',
        'USDJPY': 'USDJPYi',
        'AUDUSD': 'AUDUSDi',
        'USDCAD': 'USDCADi'
    },
    'standard': {
        'EURUSD': 'EURUSD',
        'GBPUSD': 'GBPUSD',
        'USDCHF': 'USDCHF', 
        'USDJPY': 'USDJPY',
        'AUDUSD': 'AUDUSD',
        'USDCAD': 'USDCAD'
    }
}

# =============================================================================
# Helper Functions
# =============================================================================

def get_mt4_directory():
    """Get MT4 directory from environment or default"""
    return config.MT4_DIRECTORY

def get_symbols():
    """Get trading symbols list"""
    return config.SYMBOLS

def get_timeframes():
    """Get timeframes list"""
    return config.TIMEFRAMES

def is_production():
    """Check if running in production"""
    return config.ENVIRONMENT == 'production'

def get_websocket_mode():
    """Get WebSocket async mode"""
    return config.WEBSOCKET_ASYNC_MODE

# ====================================
# MT4 CONFIGURATION
# ====================================

# MT4 Files Directory Path
# Update this path to match your MT4 installation
# The path should point to: MT4_DATA_FOLDER/MQL4/Files/

# Example paths:
# Windows: r'C:\Users\YourUsername\AppData\Roaming\MetaQuotes\Terminal\TERMINAL_ID\MQL4\Files'
# Linux/Wine: '/home/username/.wine/drive_c/users/username/AppData/Roaming/MetaQuotes/Terminal/TERMINAL_ID/MQL4/Files'
# macOS: '/Users/YourUsername/Library/Application Support/MetaQuotes/Terminal/TERMINAL_ID/MQL4/Files'

MT4_FILES_DIR = '/home/mt4/.wine/drive_c/users/mt4/AppData/Roaming/MetaQuotes/Terminal/46A834A4BD020127C05B0DA2582F8F5C/MQL4/Files'

# ====================================
# SYMBOL CONFIGURATION
# ====================================

# Currency pairs to monitor for tick data
# Adjust these symbol names to match your broker's naming convention
# Common suffixes: 'i' (CMC), 'm' (FXCM), '.z' (OANDA), etc.
TICK_SYMBOLS = [
    'EURUSDi',
    'GBPUSDi', 
    'USDCHFi',
    'USDJPYi',
    'AUDUSDi',
    'USDCADi',
    'EURGBPi',
    'EURJPYi'
]

# Bar data symbols and timeframes
# Format: [['SYMBOL', 'TIMEFRAME'], ...]
# Available timeframes: M1, M5, M15, M30, H1, H4, D1, W1, MN1
BAR_SYMBOLS_TIMEFRAMES = [
    ['EURUSDi', 'M1'],
    ['GBPUSDi', 'M1'],
    ['USDCHFi', 'M1'],
    ['USDJPYi', 'M1'],
    ['AUDUSDi', 'M1'],
    ['USDCADi', 'M1']
]

# ====================================
# WEB SERVER CONFIGURATION
# ====================================

# Web server settings
WEB_SERVER_HOST = config.HOST
WEB_SERVER_PORT = config.PORT
WEB_SERVER_DEBUG = config.DEBUG

# CORS settings (Cross-Origin Resource Sharing)
CORS_ALLOWED_ORIGINS = "*"  # "*" for all origins, or specify specific URLs

# ====================================
# TICK PROCESSOR CONFIGURATION
# ====================================

# Processing settings
SLEEP_DELAY = config.TICK_UPDATE_INTERVAL
MAX_RETRY_COMMAND_SECONDS = 10  # Retry failed commands for this many seconds
VERBOSE_LOGGING = True  # Enable detailed logging output

# Data retention settings
MAX_BARS_PER_SYMBOL = config.MAX_BAR_HISTORY
MAX_TICK_HISTORY = config.MAX_TICK_HISTORY

# Status reporting
STATUS_PRINT_INTERVAL = 30  # Print status every N seconds

# ====================================
# HISTORIC DATA CONFIGURATION
# ====================================

# Historic data settings
HISTORIC_DATA_DAYS = 7  # Number of days of historic data to request
HISTORIC_DATA_TIMEFRAME = 'D1'  # Timeframe for historic data
MAX_HISTORIC_REQUESTS = 3  # Limit historic requests to avoid overwhelming MT4

# ====================================
# ADVANCED SETTINGS
# ====================================

# WebSocket settings
WEBSOCKET_PING_TIMEOUT = 60
WEBSOCKET_PING_INTERVAL = 25

# Buffer sizes
TICK_BUFFER_SIZE = 1000
BAR_BUFFER_SIZE = 500

# Performance settings
ENABLE_TICK_BATCHING = False  # Batch tick updates (reduces WebSocket traffic)
TICK_BATCH_SIZE = 10  # Number of ticks to batch together
TICK_BATCH_TIMEOUT = 0.1  # Maximum time to wait for batch completion (seconds)

# ====================================
# HELPER FUNCTIONS
# ====================================

def validate_mt4_path():
    """Validate that the MT4 files directory exists"""
    path = Path(MT4_FILES_DIR)
    if not path.exists():
        print(f"❌ WARNING: MT4 files directory not found: {MT4_FILES_DIR}")
        print("Please update the MT4_FILES_DIR in config.py")
        return False
    return True

def get_mt4_files_dir():
    """Get the MT4 files directory path"""
    return MT4_FILES_DIR

def get_tick_symbols():
    """Get the list of symbols to monitor for tick data"""
    return TICK_SYMBOLS

def get_bar_symbols_timeframes():
    """Get the list of symbol/timeframe combinations for bar data"""
    return BAR_SYMBOLS_TIMEFRAMES

def get_web_server_config():
    """Get web server configuration"""
    return {
        'host': WEB_SERVER_HOST,
        'port': WEB_SERVER_PORT,
        'debug': WEB_SERVER_DEBUG,
        'cors_allowed_origins': CORS_ALLOWED_ORIGINS
    }

def get_processor_config():
    """Get tick processor configuration"""
    return {
        'sleep_delay': SLEEP_DELAY,
        'max_retry_command_seconds': MAX_RETRY_COMMAND_SECONDS,
        'verbose': VERBOSE_LOGGING,
        'max_bars_per_symbol': MAX_BARS_PER_SYMBOL,
        'max_tick_history': MAX_TICK_HISTORY,
        'status_print_interval': STATUS_PRINT_INTERVAL
    }

def get_historic_data_config():
    """Get historic data configuration"""
    return {
        'days': HISTORIC_DATA_DAYS,
        'timeframe': HISTORIC_DATA_TIMEFRAME,
        'max_requests': MAX_HISTORIC_REQUESTS
    }

# ====================================
# CONFIGURATION VALIDATION
# ====================================

def validate_configuration():
    """Validate the configuration settings"""
    errors = []
    
    # Check MT4 path
    if not validate_mt4_path():
        errors.append("MT4 files directory not found")
    
    # Check symbols
    if not TICK_SYMBOLS:
        errors.append("No tick symbols configured")
    
    if not BAR_SYMBOLS_TIMEFRAMES:
        errors.append("No bar symbols/timeframes configured")
    
    # Check port
    if not (1 <= WEB_SERVER_PORT <= 65535):
        errors.append(f"Invalid port number: {WEB_SERVER_PORT}")
    
    # Check delays
    if SLEEP_DELAY <= 0:
        errors.append("Sleep delay must be positive")
    
    return errors

if __name__ == "__main__":
    """Test the configuration"""
    print("🔧 DWX Connect Web Server Configuration")
    print("=" * 50)
    
    # Validate configuration
    errors = validate_configuration()
    if errors:
        print("❌ Configuration errors found:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("✅ Configuration is valid")
    
    # Display current settings
    print(f"\n📊 Current Configuration:")
    print(f"MT4 Files Directory: {MT4_FILES_DIR}")
    print(f"Tick Symbols: {len(TICK_SYMBOLS)} symbols")
    print(f"Bar Symbols: {len(BAR_SYMBOLS_TIMEFRAMES)} combinations")
    print(f"Web Server: {WEB_SERVER_HOST}:{WEB_SERVER_PORT}")
    print(f"Verbose Logging: {VERBOSE_LOGGING}")
    print(f"Sleep Delay: {SLEEP_DELAY}s")
    print("=" * 50) 