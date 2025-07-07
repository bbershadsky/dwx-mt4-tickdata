#!/usr/bin/env python3

import json
from time import sleep
from threading import Thread
from os.path import join, exists
from traceback import print_exc
from random import random
from datetime import datetime, timezone, timedelta
import sys
import os

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.dwx_client import dwx_client
from web_server import get_streamer

"""
Web-enabled DWX Connect tick processor

This processor extracts tick data from MT4 via DWX Connect and forwards it
to the web server for real-time display in the browser.

Features:
- Real-time tick data streaming
- Bar data collection
- Web interface integration
- WebSocket real-time updates
- Configurable symbols and timeframes
"""

class WebTickProcessor:
    def __init__(self, MT4_directory_path, 
                 sleep_delay=0.001,             # 1 ms for time.sleep() - much faster updates
                 max_retry_command_seconds=10,  # retry to send the command for 10 seconds if not successful
                 verbose=True,
                 tick_symbols=['EURUSDi', 'GBPUSDi', 'USDCHFi', 'USDJPYi', 'AUDUSDi', 'USDCADi'],
                 bar_symbols_timeframes=[['EURUSDi', 'M1'], ['GBPUSDi', 'M1'], ['USDCHFi', 'M1']]
                 ):
        
        self.verbose = verbose
        self.tick_symbols = tick_symbols
        self.bar_symbols_timeframes = bar_symbols_timeframes
        
        # Statistics
        self.total_ticks_received = 0
        self.total_bars_received = 0
        self.start_time = datetime.now(timezone.utc)
        
        # Get the web streamer instance
        self.streamer = get_streamer()
        
        print(f"🚀 Initializing Web Tick Processor...")
        print(f"📊 Tick symbols: {tick_symbols}")
        print(f"📈 Bar symbols/timeframes: {bar_symbols_timeframes}")
        
        # Initialize DWX client
        self.dwx = dwx_client(self, MT4_directory_path, sleep_delay, 
                             max_retry_command_seconds, verbose=verbose)
        sleep(1)
        
        self.dwx.start()
        
        # Print account information
        if self.verbose:
            print("💼 Account info:", self.dwx.account_info)
        
        # Subscribe to tick data
        print(f"🔔 Subscribing to tick data for {len(tick_symbols)} symbols...")
        self.dwx.subscribe_symbols(tick_symbols)
        
        # Subscribe to bar data
        print(f"📊 Subscribing to bar data for {len(bar_symbols_timeframes)} symbol/timeframe combinations...")
        self.dwx.subscribe_symbols_bar_data(bar_symbols_timeframes)
        
        # Request historic data for initial display
        print("📚 Requesting historic data...")
        end = datetime.now(timezone.utc)
        start = end - timedelta(days=7)  # last 7 days
        
        # Request historic data for the first few symbols
        for symbol in tick_symbols[:3]:  # Limit to first 3 symbols to avoid overwhelming MT4
            self.dwx.get_historic_data(symbol, 'D1', start.timestamp(), end.timestamp())
            sleep(0.5)  # Small delay between requests
        
        print("✅ Web Tick Processor initialized successfully!")
        print("🌐 Web interface available at: http://localhost:5000")

    def on_tick(self, symbol, bid, ask):
        """Handle incoming tick data"""
        now = datetime.now(timezone.utc)
        
        if self.verbose:
            print(f'📈 TICK: {now.strftime("%H:%M:%S")} {symbol} BID:{bid:.5f} ASK:{ask:.5f} SPREAD:{(ask-bid):.5f}')
        
        # Update statistics
        self.total_ticks_received += 1
        
        # Forward to web streamer
        self.streamer.emit_tick(symbol, bid, ask, now.isoformat())
        
        # Print periodic statistics
        if self.total_ticks_received % 100 == 0:
            uptime = now - self.start_time
            print(f"📊 Statistics: {self.total_ticks_received} ticks, {self.total_bars_received} bars, "
                  f"uptime: {uptime.total_seconds():.0f}s")

    def on_bar_data(self, symbol, time_frame, time, open_price, high, low, close_price, tick_volume):
        """Handle incoming bar data"""
        now = datetime.now(timezone.utc)
        
        if self.verbose:
            print(f'📊 BAR: {now.strftime("%H:%M:%S")} {symbol} {time_frame} '
                  f'O:{open_price:.5f} H:{high:.5f} L:{low:.5f} C:{close_price:.5f} V:{tick_volume}')
        
        # Update statistics
        self.total_bars_received += 1
        
        # Forward to web streamer
        self.streamer.emit_bar(symbol, time_frame, time, open_price, high, low, close_price, tick_volume)

    def on_historic_data(self, symbol, time_frame, data):
        """Handle historic data response"""
        if self.verbose:
            print(f'📚 HISTORIC: {symbol} {time_frame} - {len(data)} bars loaded')
        
        # Historic data is accessible via self.dwx.historic_data if needed
        # For now, we just log it

    def on_historic_trades(self):
        """Handle historic trades response"""
        if self.verbose:
            print(f'💼 HISTORIC TRADES: {len(self.dwx.historic_trades)} trades loaded')

    def on_message(self, message):
        """Handle DWX messages"""
        if message['type'] == 'ERROR':
            print(f"❌ ERROR: {message['error_type']} | {message['description']}")
        elif message['type'] == 'INFO':
            print(f"ℹ️  INFO: {message['message']}")
        else:
            print(f"💬 MESSAGE: {message}")

    def on_order_event(self):
        """Handle order events"""
        if self.verbose:
            print(f'📋 ORDER EVENT: {len(self.dwx.open_orders)} open orders')

    def print_status(self):
        """Print current status"""
        now = datetime.now(timezone.utc)
        uptime = now - self.start_time
        
        print(f"\n{'='*60}")
        print(f"📊 WEB TICK PROCESSOR STATUS")
        print(f"{'='*60}")
        print(f"🕐 Uptime: {uptime.total_seconds():.0f} seconds")
        print(f"📈 Total ticks received: {self.total_ticks_received}")
        print(f"📊 Total bars received: {self.total_bars_received}")
        print(f"🔗 WebSocket active: {len(self.streamer.tick_subscribers)} subscribers")
        print(f"💼 Account balance: {self.dwx.account_info.get('balance', 'N/A')}")
        print(f"🎯 Active symbols: {len(self.tick_symbols)}")
        print(f"📡 Connection status: {'🟢 Active' if self.dwx.ACTIVE else '🔴 Inactive'}")
        print(f"{'='*60}\n")

def main():
    """Main function to start the web tick processor"""
    
    # Configuration
    print("🔧 Starting DWX Web Tick Processor...")
    
    # MT4 directory path - Update this to match your MT4 installation
    # Common paths:
    # Windows: 'C:/Users/YourUsername/AppData/Roaming/MetaQuotes/Terminal/TERMINAL_ID/MQL4/Files/'
    # Linux/Wine: '/home/username/.wine/drive_c/users/username/AppData/Roaming/MetaQuotes/Terminal/TERMINAL_ID/MQL4/Files'
    
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
                sleep(30)  # Print status every 30 seconds
                processor.print_status()
        
        status_thread = Thread(target=status_printer)
        status_thread.daemon = True
        status_thread.start()
        
        # Keep the processor running
        print("🏃 Processor running... Press Ctrl+C to stop")
        print("🌐 Open http://localhost:5000 in your browser to view the web interface")
        
        while processor.dwx.ACTIVE:
            sleep(1)
            
    except KeyboardInterrupt:
        print("\n⏹️  Stopping Web Tick Processor...")
        if 'processor' in locals():
            processor.dwx.ACTIVE = False
        print("✅ Web Tick Processor stopped")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print_exc()

if __name__ == "__main__":
    main() 