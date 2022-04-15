import signal
import requests
import json
import time
import sys
import config
from check_stock import check_stock, send_msg_bark
from api import Api
from logger import log_print
import threading


class Proxy():
    def __init__(self) -> None:
        self.api = Api()
        self.msg = ''
        self.thread_map = {}


    def stop_all(self):
        thread_list = list(self.thread_map.keys())
        for thread in thread_list:
            self.stop(thread)

    def check_cart_and_reserve_time_thread(self):
        log_print('开始检查购物车和运力...')
        try:
            fun_name = sys._getframe().f_code.co_name
            address_id = self.api.get_address_id()
            while fun_name in self.thread_map:
                print(time.time(), self.thread_map)
                # cart_info = self.api.get_cart()
                # if cart_info:
                #     products = cart_info['products']
                #     effective_product_names = cart_info['effective_product_names']
                #     res = self.api.check_reserve_time(address_id, json.dumps(products))
                #     if len(effective_product_names):
                #         msg = '购物车有效商品{}件, 运力: {} \n {}'.format(
                #             len(effective_product_names), 
                #             '有' if res else '无',
                #             ','.join(effective_product_names)
                            
                #         )
                #         print(msg)
                #         if self.msg != msg:
                #             # send_msg_bark(msg)
                #             self.msg = msg
                time.sleep(config.duration)
        except Exception as e:
            log_print(e)
            self.thread_running = False
            
    def run(self, thread_name):
        fun = getattr(self, thread_name)
        if not fun:
            log_print('{} is not a function'.format(thread_name))
            return False

        if thread_name not in self.thread_map:
            thread = threading.Thread(target=fun)
            thread.start()
            self.thread_map[thread_name] = thread

        return True

    def stop(self, thread_name):
        if thread_name in self.thread_map:
            thread = self.thread_map.pop(thread_name)
            thread.join()
            log_print('{} is stopped'.format(thread_name))


proxy = Proxy()


if __name__ == '__main__':
    proxy.run('check_cart_and_reserve_time_thread')
    # time.sleep(5)
    # proxy.stop_all()

