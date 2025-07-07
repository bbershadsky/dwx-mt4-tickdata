#!/usr/bin/env python3

import os
import sys
import requests
import json
import time
import threading
from datetime import datetime, timezone
from pathlib import Path

# Add current directory to path so we can import local modules
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

try:
    from dwx_client import DWXClient
except ImportError:
    print("❌ DWX Client not found. Please ensure dwx_client.py is in the same directory.")
    sys.exit(1)

class CloudForwarder:
    def __init__(self, cloud_url, mt4_directory):
        """
        Initialize the cloud forwarder
        
        Args:
            cloud_url (str): URL of your Render app (e.g., https://your-app.onrender.com)
            mt4_directory (str): Path to your MT4 directory
        """
        self.cloud_url = cloud_url.rstrip('/')
        self.mt4_directory = mt4_directory
        self.session = requests.Session()
        self.session.timeout = 10
        
        # Statistics
        self.ticks_sent = 0
        self.bars_sent = 0
        self.errors = 0
        self.start_time = datetime.now()
        
        # Initialize DWX Client
        self.dwx_client = DWXClient(self.mt4_directory)
        
        print("🚀 CloudForwarder initialized")
        print(f"📍 Cloud URL: {self.cloud_url}")
        print(f"📂 MT4 Directory: {self.mt4_directory}")
        print("=" * 50)
    
    def test_connection(self):
        """Test connection to cloud server"""
        try:
            response = self.session.get(f"{self.cloud_url}/health")
            if response.status_code == 200:
                print("✅ Successfully connected to cloud server")
                health_data = response.json()
                print(f"   Server status: {health_data.get('status', 'unknown')}")
                print(f"   Active connections: {health_data.get('active_connections', 0)}")
                return True
            else:
                print(f"❌ Cloud server returned status: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Failed to connect to cloud server: {e}")
            return False
    
    def send_tick_data(self, symbol, bid, ask, timestamp=None):
        """Send tick data to cloud server"""
        if timestamp is None:
            timestamp = datetime.now(timezone.utc).isoformat()
        
        tick_data = {
            'symbol': symbol,
            'bid': bid,
            'ask': ask,
            'timestamp': timestamp,
            'spread': round(ask - bid, 5)
        }
        
        try:
            response = self.session.post(
                f"{self.cloud_url}/api/forward/tick",
                json=tick_data,
                timeout=5
            )
            
            if response.status_code == 200:
                self.ticks_sent += 1
                if self.ticks_sent % 10 == 0:  # Log every 10th tick
                    print(f"📈 Sent {self.ticks_sent} ticks | Latest: {symbol} {bid}/{ask}")
                return True
            else:
                self.errors += 1
                print(f"❌ Failed to send tick {symbol}: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.errors += 1
            print(f"❌ Error sending tick {symbol}: {e}")
            return False
    
    def send_bar_data(self, symbol, timeframe, time_bar, open_price, high, low, close_price, volume=0):
        """Send bar data to cloud server"""
        bar_data = {
            'symbol': symbol,
            'timeframe': timeframe,
            'time': time_bar,
            'open': open_price,
            'high': high,
            'low': low,
            'close': close_price,
            'volume': volume
        }
        
        try:
            response = self.session.post(
                f"{self.cloud_url}/api/forward/bar",
                json=bar_data,
                timeout=5
            )
            
            if response.status_code == 200:
                self.bars_sent += 1
                print(f"📊 Sent bar: {symbol} {timeframe} | OHLC: {open_price}/{high}/{low}/{close_price}")
                return True
            else:
                self.errors += 1
                print(f"❌ Failed to send bar {symbol} {timeframe}: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.errors += 1
            print(f"❌ Error sending bar {symbol} {timeframe}: {e}")
            return False
    
    def print_statistics(self):
        """Print forwarding statistics"""
        runtime = datetime.now() - self.start_time
        hours, remainder = divmod(runtime.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        
        print("\n" + "=" * 50)
        print("📊 FORWARDING STATISTICS")
        print("=" * 50)
        print(f"⏱️  Runtime: {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}")
        print(f"📈 Ticks sent: {self.ticks_sent}")
        print(f"📊 Bars sent: {self.bars_sent}")
        print(f"❌ Errors: {self.errors}")
        if self.ticks_sent > 0:
            success_rate = ((self.ticks_sent + self.bars_sent) / (self.ticks_sent + self.bars_sent + self.errors)) * 100
            print(f"✅ Success rate: {success_rate:.1f}%")
        print("=" * 50)
    
    def run(self):
        """Main run loop"""
        print("🔌 Testing connection to cloud server...")
        if not self.test_connection():
            print("❌ Cannot connect to cloud server. Please check your URL and try again.")
            return
        
        print("📡 Starting data forwarding...")
        print("💡 Press Ctrl+C to stop")
        print("-" * 50)
        
        try:
            # Start statistics thread
            stats_thread = threading.Thread(target=self.stats_loop, daemon=True)
            stats_thread.start()
            
            # Main forwarding loop
            last_tick_time = {}
            
            while True:
                try:
                    # Get tick data
                    tick_data = self.dwx_client.get_latest_ticks()
                    for symbol, data in tick_data.items():
                        if symbol not in last_tick_time or data['timestamp'] > last_tick_time[symbol]:
                            self.send_tick_data(symbol, data['bid'], data['ask'], data['timestamp'])
                            last_tick_time[symbol] = data['timestamp']
                    
                    # Get bar data (less frequently)
                    if self.ticks_sent % 50 == 0:  # Every 50 ticks, check for new bars
                        bar_data = self.dwx_client.get_latest_bars()
                        for symbol_tf, data in bar_data.items():
                            parts = symbol_tf.split('_')
                            if len(parts) == 2:
                                symbol, timeframe = parts
                                self.send_bar_data(
                                    symbol, timeframe, data['time'],
                                    data['open'], data['high'], data['low'], data['close'],
                                    data.get('volume', 0)
                                )
                    
                    time.sleep(0.1)  # 100ms delay
                    
                except KeyboardInterrupt:
                    print("\n⏹️  Stopping forwarder...")
                    break
                except Exception as e:
                    print(f"❌ Error in main loop: {e}")
                    time.sleep(1)  # Wait before retrying
                    
        except Exception as e:
            print(f"❌ Fatal error: {e}")
        finally:
            self.print_statistics()
            print("✅ CloudForwarder stopped")
    
    def stats_loop(self):
        """Print statistics periodically"""
        while True:
            time.sleep(30)  # Print stats every 30 seconds
            if self.ticks_sent > 0 or self.bars_sent > 0:
                self.print_statistics()

def main():
    """Main function"""
    print("🌐 DWX Cloud Forwarder")
    print("=" * 50)
    
    # Configuration
    CLOUD_URL = input("Enter your Render app URL (e.g., https://your-app.onrender.com): ").strip()
    if not CLOUD_URL:
        print("❌ Cloud URL is required")
        return
    
    # Use default MT4 directory or ask user
    default_mt4 = "/Users/bopr/Documents/pacific_config/CMC Markets MetaTrader 4"
    if os.path.exists(default_mt4):
        MT4_DIRECTORY = default_mt4
        print(f"✅ Using MT4 directory: {MT4_DIRECTORY}")
    else:
        MT4_DIRECTORY = input("Enter your MT4 directory path: ").strip()
        if not MT4_DIRECTORY or not os.path.exists(MT4_DIRECTORY):
            print("❌ Invalid MT4 directory")
            return
    
    # Create and run forwarder
    forwarder = CloudForwarder(CLOUD_URL, MT4_DIRECTORY)
    forwarder.run()

if __name__ == "__main__":
    main() 