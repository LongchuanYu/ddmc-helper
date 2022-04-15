import signal
from socket import timeout
from tokenize import Funny
import requests
import json
import time
import sys
import config
from check_stock import check_stock, send_msg_bark
from api import Api
import threading
from threading import Lock


class Proxy():
    def __init__(self, socket) -> None:
        self.api = Api()
        self.msg = ''
        self.thread_map = {}
        self.socket = socket
        self.recycle_times = {
            'check_cart_and_reserve_time_thread': 0
        }
        self.thread_map_lock = Lock()

    def log_print(self, msg, type='INFO', do_emit=True, channel='common'):
        formatted_msg = '{} {} {}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
            type, 
            str(msg))
        print(formatted_msg)
        if do_emit:
            self.socket.emit(channel, {
                'msg': str(formatted_msg)
            })

    def check_cart_and_reserve_time_thread(self):
        self.log_print('开始检查购物车和运力...')
        fun_name = sys._getframe().f_code.co_name
        try:
            address_id = self.api.get_address_id()
            while fun_name in self.thread_map:
                cart_info = self.api.get_cart()
                # cart_info = None
                if cart_info:
                    products = cart_info['products']
                    effective_product_names = cart_info['effective_product_names']
                    res = self.api.check_reserve_time(address_id, json.dumps(products))
                    msg = '购物车有效商品{}件, 运力: {}'.format(
                        len(effective_product_names), 
                        '有' if res else '无'
                    )
                    if len(effective_product_names) and self.msg != msg:
                        send_msg_bark(msg)
                        self.msg = msg
                else:
                    msg = '购物车无有效商品'
                self.log_print(msg, do_emit=True)
                self.recycle_times['check_cart_and_reserve_time_thread'] += 1
                time.sleep(config.duration)
        except Exception as e:
            self.log_print('检查购物车和运力因为错误已停止：' + str(e), type='ERROR')
            if fun_name in self.thread_map:
                self.thread_map.pop(fun_name)
            
    def run(self, thread_name):
        fun = getattr(self, thread_name)
        if not fun:
            self.log_print('{} is not a function'.format(thread_name))
            return False

        if thread_name not in self.thread_map:
            thread = threading.Thread(target=fun)
            thread.start()
            self.thread_map[thread_name] = thread

        return True

    def stop(self, thread_name):
        if thread_name in self.thread_map:
            thread = self.thread_map.pop(thread_name)
            thread.join(timeout=2)
            self.log_print('{}已停止，共运行{}次'.format(thread_name, self.recycle_times[thread_name]))
            self.recycle_times[thread_name] = 0

    def stop_all(self):
        thread_list = list(self.thread_map.keys())
        for thread_name in thread_list:
            self.stop(thread_name)