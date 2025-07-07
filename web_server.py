#!/usr/bin/env python3

import json
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room
import threading
import time
from datetime import datetime, timezone
import os
from pathlib import Path

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dwx_tick_data_secret'

# Explicitly configure SocketIO for gevent
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='gevent')

# Global variables for storing tick data
tick_data_cache = {}
bar_data_cache = {}
connected_clients = set()
data_lock = threading.Lock()

class TickDataStreamer:
    def __init__(self):
        self.tick_subscribers = []
        self.bar_subscribers = []
        
    def add_tick_subscriber(self, callback):
        self.tick_subscribers.append(callback)
        
    def add_bar_subscriber(self, callback):
        self.bar_subscribers.append(callback)
        
    def emit_tick(self, symbol, bid, ask, timestamp=None):
        if timestamp is None:
            timestamp = datetime.now(timezone.utc).isoformat()
            
        tick_data = {
            'symbol': symbol,
            'bid': bid,
            'ask': ask,
            'timestamp': timestamp,
            'spread': round(ask - bid, 5)
        }
        
        # Store in cache
        with data_lock:
            tick_data_cache[symbol] = tick_data
            
        # Emit to WebSocket clients
        socketio.emit('tick_data', tick_data, room='tick_room')
        
        # Call subscribers
        for callback in self.tick_subscribers:
            try:
                callback(tick_data)
            except Exception as e:
                print(f"Error in tick subscriber: {e}")
    
    def emit_bar(self, symbol, timeframe, time_bar, open_price, high, low, close_price, volume):
        timestamp = datetime.now(timezone.utc).isoformat()
        
        bar_data = {
            'symbol': symbol,
            'timeframe': timeframe,
            'time': time_bar,
            'open': open_price,
            'high': high,
            'low': low,
            'close': close_price,
            'volume': volume,
            'timestamp': timestamp
        }
        
        # Store in cache
        with data_lock:
            if symbol not in bar_data_cache:
                bar_data_cache[symbol] = {}
            if timeframe not in bar_data_cache[symbol]:
                bar_data_cache[symbol][timeframe] = []
            
            bar_data_cache[symbol][timeframe].append(bar_data)
            # Keep only last 100 bars per symbol/timeframe
            if len(bar_data_cache[symbol][timeframe]) > 100:
                bar_data_cache[symbol][timeframe] = bar_data_cache[symbol][timeframe][-100:]
        
        # Emit to WebSocket clients
        socketio.emit('bar_data', bar_data, room='bar_room')
        
        # Call subscribers
        for callback in self.bar_subscribers:
            try:
                callback(bar_data)
            except Exception as e:
                print(f"Error in bar subscriber: {e}")

# Global streamer instance
streamer = TickDataStreamer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/tick-data')
def get_tick_data():
    """REST API endpoint to get current tick data"""
    with data_lock:
        return json.dumps(tick_data_cache)

@app.route('/api/bar-data')
def get_bar_data():
    """REST API endpoint to get current bar data"""
    with data_lock:
        return json.dumps(bar_data_cache)

@app.route('/health')
def health():
    """Health check endpoint for deployment platforms"""
    return {
        'status': 'healthy',
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'active_connections': len(connected_clients),
        'tick_data_count': len(tick_data_cache),
        'bar_data_count': len(bar_data_cache)
    }

@app.route('/api/forward/tick', methods=['POST'])
def receive_tick_data():
    """API endpoint to receive tick data from local MT4 forwarder"""
    try:
        data = request.get_json()
        if not data:
            return {'error': 'No data provided'}, 400
            
        # Validate required fields
        required_fields = ['symbol', 'bid', 'ask']
        for field in required_fields:
            if field not in data:
                return {'error': f'Missing required field: {field}'}, 400
        
        # Use the streamer to emit the data
        streamer.emit_tick(
            symbol=data['symbol'],
            bid=data['bid'],
            ask=data['ask'],
            timestamp=data.get('timestamp')
        )
        
        return {'status': 'success', 'symbol': data['symbol']}, 200
        
    except Exception as e:
        print(f"Error receiving tick data: {e}")
        return {'error': str(e)}, 500

@app.route('/api/forward/bar', methods=['POST'])
def receive_bar_data():
    """API endpoint to receive bar data from local MT4 forwarder"""
    try:
        data = request.get_json()
        if not data:
            return {'error': 'No data provided'}, 400
            
        # Validate required fields
        required_fields = ['symbol', 'timeframe', 'time', 'open', 'high', 'low', 'close']
        for field in required_fields:
            if field not in data:
                return {'error': f'Missing required field: {field}'}, 400
        
        # Use the streamer to emit the data
        streamer.emit_bar(
            symbol=data['symbol'],
            timeframe=data['timeframe'],
            time_bar=data['time'],
            open_price=data['open'],
            high=data['high'],
            low=data['low'],
            close_price=data['close'],
            volume=data.get('volume', 0)
        )
        
        return {'status': 'success', 'symbol': data['symbol'], 'timeframe': data['timeframe']}, 200
        
    except Exception as e:
        print(f"Error receiving bar data: {e}")
        return {'error': str(e)}, 500

@socketio.on('connect')
def handle_connect():
    print(f'Client connected: {request.sid}')
    connected_clients.add(request.sid)
    
    # Send current tick data to newly connected client
    with data_lock:
        if tick_data_cache:
            emit('initial_tick_data', tick_data_cache)
        if bar_data_cache:
            emit('initial_bar_data', bar_data_cache)

@socketio.on('disconnect')
def handle_disconnect():
    print(f'Client disconnected: {request.sid}')
    connected_clients.discard(request.sid)

@socketio.on('join_ticks')
def handle_join_ticks():
    join_room('tick_room')
    print(f'Client {request.sid} joined tick room')

@socketio.on('leave_ticks')
def handle_leave_ticks():
    leave_room('tick_room')
    print(f'Client {request.sid} left tick room')

@socketio.on('join_bars')
def handle_join_bars():
    join_room('bar_room')
    print(f'Client {request.sid} joined bar room')

@socketio.on('leave_bars')
def handle_leave_bars():
    leave_room('bar_room')
    print(f'Client {request.sid} left bar room')

def create_templates_dir():
    """Create templates directory if it doesn't exist"""
    templates_dir = Path(__file__).parent / 'templates'
    templates_dir.mkdir(exist_ok=True)
    return templates_dir

def create_static_dir():
    """Create static directory if it doesn't exist"""
    static_dir = Path(__file__).parent / 'static'
    static_dir.mkdir(exist_ok=True)
    return static_dir

def get_streamer():
    """Get the global streamer instance"""
    return streamer

if __name__ == '__main__':
    # Get port from environment or default to 5000
    port = int(os.getenv('PORT', 5000))
    
    print(f"🚀 Starting DWX Tick Data Web Server on port {port}...")
    
    # Use SocketIO's web server which is integrated with gevent
    socketio.run(app, host='0.0.0.0', port=port, debug=False) 