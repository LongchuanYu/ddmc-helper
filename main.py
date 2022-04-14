import requests
import json
import time
import sys
import config
from check_stock import check_stock, send_msg_bark
from api import Api


class Resolve():
    def __init__(self) -> None:
        self.api = Api()
        self.msg = ''

    def check_cart_and_reserve_time(self):
        print('开始检查购物车和运力...')
        address_id = self.api.get_address_id()
        while True:
            cart_info = self.api.get_cart()
            if cart_info:
                products = cart_info['products']
                effective_product_names = cart_info['effective_product_names']
                res = self.api.check_reserve_time(address_id, json.dumps(products))
                if len(effective_product_names):
                    msg = '购物车有效商品{}件, 运力: {} \n {}'.format(
                        len(effective_product_names), 
                        '有' if res else '无',
                        ','.join(effective_product_names)
                        
                    )
                    print(msg)
                    if self.msg != msg:
                        send_msg_bark(msg)
                        self.msg = msg
            time.sleep(config.duration)


if __name__ == '__main__':
    # 给在服务器后台执行使用
    if len(sys.argv) > 1:
        run_type = int(sys.argv[1])
        if run_type in [1, 2, 3]:
            config.run_type = run_type
    resolve = Resolve()
    if config.run_type == 1:
        resolve.check_cart_and_reserve_time()
        
    else:
        check_stock()

