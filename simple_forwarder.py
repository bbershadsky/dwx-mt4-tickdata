#!/usr/bin/env python3

import os
import sys
import requests
import json
import time
import threading
from datetime import datetime, timezone
from pathlib import Path

# Add current directory to path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Import the existing tick processor to extend it
try:
    from web_tick_processor import DWXTickProcessor
except ImportError:
    print("❌ web_tick_processor.py not found. Please ensure you're in the correct directory.")
    sys.exit(1)

class CloudForwarder(DWXTickProcessor):
    def __init__(self, cloud_url):
        """
        Initialize the cloud forwarder
        
        Args:
            cloud_url (str): URL of your Render app (e.g., https://your-app.onrender.com)
        """
        super().__init__()
        self.cloud_url = cloud_url.rstrip('/')
        self.session = requests.Session()
        self.session.timeout = 10
        
        # Statistics
        self.ticks_sent = 0
        self.bars_sent = 0
        self.errors = 0
        self.start_time = datetime.now()
        
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
    
    def send_tick_to_cloud(self, symbol, bid, ask, timestamp=None):
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
                if self.ticks_sent % 50 == 0:  # Log every 50th tick
                    print(f"📈 Sent {self.ticks_sent} ticks | Latest: {symbol} {bid}/{ask}")
                return True
            else:
                self.errors += 1
                if self.errors % 10 == 0:  # Log every 10th error
                    print(f"❌ Failed to send tick {symbol}: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.errors += 1
            if self.errors % 10 == 0:  # Log every 10th error
                print(f"❌ Error sending tick {symbol}: {e}")
            return False
    
    def send_bar_to_cloud(self, symbol, timeframe, time_bar, open_price, high, low, close_price, volume=0):
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
    
    def on_tick_data(self, tick_data):
        """Override: Called when new tick data is received from MT4"""
        # Send to cloud
        self.send_tick_to_cloud(
            symbol=tick_data['symbol'],
            bid=tick_data['bid'],
            ask=tick_data['ask'],
            timestamp=tick_data.get('timestamp')
        )
    
    def on_bar_data(self, bar_data):
        """Override: Called when new bar data is received from MT4"""
        # Send to cloud
        self.send_bar_to_cloud(
            symbol=bar_data['symbol'],
            timeframe=bar_data['timeframe'],
            time_bar=bar_data['time'],
            open_price=bar_data['open'],
            high=bar_data['high'],
            low=bar_data['low'],
            close_price=bar_data['close'],
            volume=bar_data.get('volume', 0)
        )
    
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
        if self.ticks_sent > 0 or self.bars_sent > 0:
            total_sent = self.ticks_sent + self.bars_sent
            success_rate = (total_sent / (total_sent + self.errors)) * 100
            print(f"✅ Success rate: {success_rate:.1f}%")
        print("=" * 50)
    
    def run(self):
        """Run the forwarder with connection test"""
        print("🔌 Testing connection to cloud server...")
        if not self.test_connection():
            print("❌ Cannot connect to cloud server. Please check your URL and try again.")
            return
        
        print("📡 Starting data forwarding from MT4 to cloud...")
        print("💡 Press Ctrl+C to stop")
        print("-" * 50)
        
        # Start statistics thread
        stats_thread = threading.Thread(target=self.stats_loop, daemon=True)
        stats_thread.start()
        
        try:
            # Call the parent run method which handles MT4 communication
            super().run()
        except KeyboardInterrupt:
            print("\n⏹️  Stopping forwarder...")
        finally:
            self.print_statistics()
            print("✅ CloudForwarder stopped")
    
    def stats_loop(self):
        """Print statistics periodically"""
        while True:
            time.sleep(60)  # Print stats every minute
            if self.ticks_sent > 0 or self.bars_sent > 0:
                self.print_statistics()

def main():
    """Main function"""
    print("🌐 DWX Cloud Forwarder")
    print("Forwards MT4 data from local machine to cloud dashboard")
    print("=" * 50)
    
    # Get cloud URL
    cloud_url = input("Enter your Render app URL: ").strip()
    if not cloud_url:
        print("❌ Cloud URL is required")
        print("Example: https://your-app-name.onrender.com")
        return
    
    if not cloud_url.startswith('http'):
        cloud_url = 'https://' + cloud_url
    
    print(f"🎯 Target: {cloud_url}")
    
    # Create and run forwarder
    try:
        forwarder = CloudForwarder(cloud_url)
        forwarder.run()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 