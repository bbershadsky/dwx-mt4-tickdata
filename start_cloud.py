#!/usr/bin/env python3

import os
import sys
import time
import threading
import logging
from config import get_config
from web_server import app, socketio

# Get configuration
config = get_config()

# Set up logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main application entry point for cloud deployment"""
    logger.info("=" * 60)
    logger.info("DWX Tick Data Web Server - CLOUD MODE")
    logger.info("=" * 60)
    logger.info(f"Environment: {config.ENVIRONMENT}")
    logger.info(f"Host: {config.HOST}")
    logger.info(f"Port: {config.PORT}")
    logger.info(f"Debug: {config.DEBUG}")
    logger.info("Mode: Cloud Backend (waiting for data from local MT4)")
    logger.info("=" * 60)
    
    logger.info("🌐 Cloud backend started - ready to receive data")
    logger.info("📡 Send data from your local MT4 to this URL")
    logger.info("💡 Use the provided forwarder script on your local machine")
    
    # Start web server
    try:
        logger.info(f"🚀 Starting web server on {config.HOST}:{config.PORT}")
        socketio.run(
            app,
            host=config.HOST,
            port=config.PORT,
            debug=config.DEBUG,
            allow_unsafe_werkzeug=True  # For development
        )
    except Exception as e:
        logger.error(f"❌ Failed to start web server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 