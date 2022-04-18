from concurrent.futures import thread
from flask import Flask, request, render_template, jsonify
from flask_socketio import SocketIO, emit
from proxy import Proxy
from datetime import timedelta
import config
import gevent
from gevent import monkey

monkey.patch_all()

app = Flask(__name__)
socketio = SocketIO(app,  cors_allowed_origins='*')
proxy = Proxy(socketio)

@socketio.on('connect')
def socket_connect():
    print('socket connected')

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_cart_and_reserve_time', methods=['POST'])
def check_cart_and_reserve_time():
    data = request.get_json()
    proxy.run(data['thread_name'], duration=data.get('duration', config.duration))
    return 'ok'

@app.route('/stop_thread', methods=['POST'])
def stop_thread():
    data = request.get_json()
    proxy.stop(data['thread_name'])
    return 'ok'

@app.route('/stop_all', methods=['POST'])
def stop_all():
    data = request.get_json()
    proxy.stop_all()
    return 'ok'

@app.route('/get_started_thread')
def get_started_thread():
    thread_map = proxy.thread_map
    thread_name_list = list(thread_map.keys())

    return jsonify(thread_name_list)

@app.route('/get_history_msg')
def get_history_msg():
    return jsonify(proxy.history_msg)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
