#!/usr/bin/env python3

"""
Configuration file for DWX Connect Web Server
"""

import os

class Config:
    """Base configuration class."""
    # Default values, can be overridden by subclasses or environment variables
    ENVIRONMENT = 'development'
    DEBUG = True
    HOST = '127.0.0.1'
    PORT = 5001
    LOG_LEVEL = 'INFO'
    
    # MT4 Connection Settings
    MT4_DIRECTORY = '/Users/bopr/Documents/pacific_config/CMC Markets MetaTrader 4'
    
    # DWX Connect Settings - comma-separated strings
    SYMBOLS = 'EURUSDi,GBPUSDi,USDCHFi,USDJPYi,AUDUSDi,USDCADi'
    TIMEFRAMES = 'M1,M5,M15,H1,H4'
    
    # Update frequencies
    TICK_UPDATE_INTERVAL = 0.1
    BAR_UPDATE_INTERVAL = 1.0
    
    # Data storage limits
    MAX_TICK_HISTORY = 1000
    MAX_BAR_HISTORY = 100
    
    # WebSocket Settings
    WEBSOCKET_ASYNC_MODE = 'auto' # gevent, eventlet, threading

class DevelopmentConfig(Config):
    """Configuration for local development."""
    pass # Inherits all defaults from Config

class ProductionConfig(Config):
    """Configuration for production environments like Render."""
    ENVIRONMENT = 'production'
    DEBUG = False
    # Host must be 0.0.0.0 to be reachable in a container
    HOST = '0.0.0.0' 
    # Render provides the port to bind to
    PORT = int(os.getenv('PORT', 10000))
    LOG_LEVEL = 'INFO'
    
    # For production, we get these from environment variables
    # The default values in render.yaml will be used if not overridden in the dashboard
    SYMBOLS = os.getenv('SYMBOLS', Config.SYMBOLS)
    TIMEFRAMES = os.getenv('TIMEFRAMES', Config.TIMEFRAMES)

def get_config():
    """
    Returns the appropriate configuration object based on the ENVIRONMENT variable.
    """
    env = os.getenv('ENVIRONMENT', 'development')
    if env == 'production':
        print("✅ Loading Production Configuration")
        return ProductionConfig()
    else:
        print("🔧 Loading Development Configuration")
        return DevelopmentConfig() 