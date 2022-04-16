## 手机访问页面，多刷新几次会出现get socket.io.min.js、axios.min.js失败的情况，如果diable cache则正常。
部署上线后，不再复现。


## 如何部署flask + socketio + gunicorn + nginx

#### 步骤
1. nginx配置文件：
```
server {
    listen      80;
    server_name ddmc.remly.xyz;
    location / {
        proxy_pass  http://10.0.16.12:5000;
    }
    location /socket.io {
        proxy_http_version 1.1;
        proxy_buffering off;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_pass http://10.0.16.12:5000/socket.io;
    }
}
```
2. 启动gunicorn
    ```
    gunicorn --worker-class eventlet main:app -b 0.0.0.0:5000
    ```

3. 这样就可以访问了

#### 问题排查
1. 执行python main.py后socketio报错，比如：
    ```
    HTTPS: Hostname is not an accepted origin, even on same-origin requests

    解决方案：
    在main.py里面，把
    socketio = SocketIO(app)
    改成：
    socketio = SocketIO(app, cors_allowed_origins='*')
    ```
    ```
    The WebSocket transport is not available, you must install a WebSocket server that is compatible with your async mode to enable it. 
    See the documentation for details. (further occurrences of this error will be logged with level INFO)

    解决方案：
    pip install eventlet==0.30.2

    注意一定要低版本，否则用gunicorn启动会报：
        Error: class uri 'eventlet' invalid or not found: 

        [Traceback (most recent call last):
        File "/home/lighthouse/.local/lib/python3.8/site-packages/gunicorn/util.py", line 99, in load_class
            mod = importlib.import_module('.'.join(components))
        File "/usr/lib/python3.8/importlib/__init__.py", line 127, in import_module
            return _bootstrap._gcd_import(name[level:], package, level)
        File "<frozen importlib._bootstrap>", line 1014, in _gcd_import
        File "<frozen importlib._bootstrap>", line 991, in _find_and_load
        File "<frozen importlib._bootstrap>", line 975, in _find_and_load_unlocked
        File "<frozen importlib._bootstrap>", line 671, in _load_unlocked
        File "<frozen importlib._bootstrap_external>", line 848, in exec_module
        File "<frozen importlib._bootstrap>", line 219, in _call_with_frames_removed
        File "/home/lighthouse/.local/lib/python3.8/site-packages/gunicorn/workers/geventlet.py", line 20, in <module>
            from eventlet.wsgi import ALREADY_HANDLED as EVENTLET_ALREADY_HANDLED
        ImportError: cannot import name 'ALREADY_HANDLED' from 'eventlet.wsgi' (/home/lighthouse/.local/lib/python3.8/site-packages/eventlet/wsgi.py)
        ]
    ```



