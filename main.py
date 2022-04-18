from gevent import monkey  # 放在最开头，否则可能造成无限递归
monkey.patch_all()  # 放在最开头，否则可能造成无限递归

from flask import Flask, request, render_template, jsonify
from proxy import Proxy
import config


app = Flask(__name__)
proxy = Proxy()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_cart_and_reserve_time', methods=['POST'])
def check_cart_and_reserve_time():
    data = request.get_json()
    proxy.run(data['thread_name'], duration=data.get('duration'))
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

@app.route('/get_proxy_params')
def get_proxy_params():
    data = {
        'thread_name_list': list(proxy.thread_map.keys()),
        'history_msg': proxy.history_msg,
        'duration': proxy.duration
    }

    return jsonify(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
