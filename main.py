import requests
import json
import time
import sys
import config
from check_stock import check_stock, send_msg_bark
from api import Api


def run():
    apis = Apis()
    if config.run_type == 1:
        api.check_reserve_time()
    else:
        check_stock()
    # time.sleep(config.duration)


if __name__ == '__main__':
    # 给在服务器后台执行使用
    if len(sys.argv) > 1:
        run_type = int(sys.argv[1])
        if run_type in [1, 2, 3]:
            config.run_type = run_type
    api = Api()
    if config.run_type == 1:
        address_id = api.get_address_id()
        cart_info = api.get_cart()
        products = cart_info['products']
        res = api.check_reserve_time(address_id, json.dumps(products))
        
    else:
        check_stock()

