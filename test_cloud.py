#!/usr/bin/env python3

import requests
import json
import time
from datetime import datetime, timezone

def test_cloud_server(cloud_url):
    """Test the cloud server endpoints"""
    print(f"🧪 Testing cloud server: {cloud_url}")
    print("=" * 50)
    
    try:
        # Test health endpoint
        print("1. Testing health endpoint...")
        response = requests.get(f"{cloud_url}/health", timeout=10)
        if response.status_code == 200:
            health_data = response.json()
            print(f"   ✅ Health check passed")
            print(f"   📊 Status: {health_data.get('status')}")
            print(f"   🔗 Active connections: {health_data.get('active_connections', 0)}")
        else:
            print(f"   ❌ Health check failed: HTTP {response.status_code}")
            return False
        
        # Test tick forwarding endpoint
        print("\n2. Testing tick data forwarding...")
        test_tick = {
            'symbol': 'EURUSD_TEST',
            'bid': 1.17698,
            'ask': 1.17702,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        
        response = requests.post(
            f"{cloud_url}/api/forward/tick",
            json=test_tick,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Tick forwarding works")
            print(f"   📈 Sent test tick for {result.get('symbol')}")
        else:
            print(f"   ❌ Tick forwarding failed: HTTP {response.status_code}")
            return False
        
        # Test bar forwarding endpoint
        print("\n3. Testing bar data forwarding...")
        test_bar = {
            'symbol': 'EURUSD_TEST',
            'timeframe': 'M15',
            'time': '2024-01-01T12:00:00',
            'open': 1.17650,
            'high': 1.17720,
            'low': 1.17640,
            'close': 1.17698,
            'volume': 100
        }
        
        response = requests.post(
            f"{cloud_url}/api/forward/bar",
            json=test_bar,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Bar forwarding works")
            print(f"   📊 Sent test bar for {result.get('symbol')} {result.get('timeframe')}")
        else:
            print(f"   ❌ Bar forwarding failed: HTTP {response.status_code}")
            return False
        
        print("\n4. Testing web interface...")
        response = requests.get(cloud_url, timeout=10)
        if response.status_code == 200:
            print(f"   ✅ Web interface accessible")
            print(f"   🌐 Dashboard ready at: {cloud_url}")
        else:
            print(f"   ❌ Web interface failed: HTTP {response.status_code}")
            return False
        
        print("\n" + "=" * 50)
        print("🎉 ALL TESTS PASSED!")
        print("=" * 50)
        print("Your cloud setup is working perfectly!")
        print(f"Dashboard: {cloud_url}")
        print("Ready to start forwarding real MT4 data!")
        return True
        
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to {cloud_url}")
        print("   Check if the URL is correct and the server is running")
        return False
    except requests.exceptions.Timeout:
        print(f"❌ Timeout connecting to {cloud_url}")
        print("   Server might be sleeping (Render free tier)")
        print("   Try again in 30 seconds...")
        return False
    except Exception as e:
        print(f"❌ Error testing server: {e}")
        return False

def main():
    """Main function"""
    print("🧪 Cloud Server Test Utility")
    print("=" * 50)
    
    cloud_url = input("Enter your Render app URL: ").strip()
    if not cloud_url:
        print("❌ URL is required")
        return
    
    if not cloud_url.startswith('http'):
        cloud_url = 'https://' + cloud_url
    
    success = test_cloud_server(cloud_url)
    
    if success:
        print("\n💡 Next steps:")
        print("1. Run 'python simple_forwarder.py' on your local machine")
        print("2. Enter the same URL when prompted")
        print("3. Watch your real-time MT4 data appear in the cloud!")
    else:
        print("\n🔧 Troubleshooting:")
        print("1. Check if your Render app is deployed correctly")
        print("2. Verify the URL is correct")
        print("3. Wait 30 seconds if the app was sleeping")
        print("4. Check Render logs at dashboard.render.com")

if __name__ == "__main__":
    main() 