from flask import Flask, request, render_template, redirect, url_for, jsonify
# from proxy import Proxy

app = Flask(__name__)

# proxy = Proxy()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_cart_and_reserve_time', methods=['POST'])
def check_cart_and_reserve_time():
    # proxy.run('check_cart_and_reserve_time_thread')
    print('check_cart_and_reserve_time')
    return {'status': 'ok'}

@app.route('/stop_thread', methods=['POST', 'GET'])
def stop_thread():
    # data = request.get_json()
    print('stopped')
    # proxy.stop(data['thread_name'])
    return jsonify('okk')

@app.route('/stop_all', methods=['POST'])
def stop_all():
    # proxy.stop_all()
    return {'status': 'ok'}

if __name__ == '__main__':
    app.run(debug=True)