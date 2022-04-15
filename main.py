from concurrent.futures import thread
from flask import Flask, request, render_template, redirect, url_for, jsonify
from flask_socketio import SocketIO, emit
from proxy import Proxy

app = Flask(__name__)
socketio = SocketIO(app)
proxy = Proxy(socketio)

@socketio.on('connect')
def socket_connect():
    proxy.log_print('socket connected', do_emit=False)

@socketio.on('disconnect')
def test_disconnect():
    proxy.log_print('Client disconnected', do_emit=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_cart_and_reserve_time', methods=['POST'])
def check_cart_and_reserve_time():
    data = request.get_json()
    proxy.run(data['thread_name'])
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

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True)