from tabnanny import check
import utils
from utils import config
import requests
import check_stock
import json
from error import RequestError, CrowdedError

class Api:
    def __init__(self) -> None:
        pass

    def is_query_success(self, r):
        """ 检查是否查询成功

        @return: r.json()
        """
        if r.status_code != 200:
            raise RequestError('请求失败')
        r.encoding = 'utf-8'
        res = r.json()
        
        if res.get('code') == -3000 and '拥挤' in res.get('msg', ''):
            raise CrowdedError(json.dumps(res, ensure_ascii=False))
        if res.get('code') != 0:
            raise RequestError('请求异常: ' + str(res.get('message')))
        
        return res

    def send_msg_bark(self, msg):
        """ 发送消息

        """
        bark_msg_url = 'https://api.day.app/' + config['bark_id'] + '/'
        params = {
            'group': '叮咚买菜',
            'sound': 'minuet'
        }
        requests.get(bark_msg_url + msg, params=params)

    def get_address_id(self):
        """ 获取默认收获地址id 需要cookie
        
        """
        headers = {
            'User-Agent': config['ua'],
            'Connection': 'keep-alive',
            'content-type': 'application/x-www-form-urlencoded',
            'Cookie': config['cookie'],
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://servicewechat.com/wx1e113254eda17715/422/page-frame.html'
        }
        param = utils.get_body()
        url = 'https://sunquan.api.ddxq.mobi/api/v1/user/address/'
        try:
            r = requests.get(url, headers=headers, params=param)
        except Exception as e:
            raise RequestError(e)

        res = self.is_query_success(r)

        address_list = res['data']['valid_address']
        for address in address_list:
            if config['location_name'] in address['location']['name']:
                return address['id']
        return None


    def get_cart(self):
        """ 获取购物车可购买的商品信息 需要cookie

        @return: {} or {'products': [], 'total_money': '', ...}
        """
        headers = utils.get_headers()
        headers.pop('Content-Length')
        url = 'https://maicai.api.ddxq.mobi/cart/index'
        params = utils.get_body()
        params['is_load'] = '1'
        try:
            r = requests.get(url, headers=headers, params=params)
        except Exception as e:
            raise RequestError(e)

        res = self.is_query_success(r)

        if not len(res['data']['new_order_product_list']):
            return {}
        products_info = res['data']['new_order_product_list'][0]
        products_info['parent_order_sign'] = res['data']['parent_order_info']['parent_order_sign']
        products = products_info['products']
        effective_product_names = []
        for product in products:
            effective_product_names.append(product['product_name'])
        products_info['effective_product_names'] = effective_product_names

        return products_info

    def check_reserve_time(self, address_id, products_raw):
        """ 检查是否有运力 需要cookie

        @param: address_id: number 默认收获地址id,可通过get_address_id()获取
        @param: products_raw: string 商品信息,可通过get_cart()获取,转为字符串

        @return: {} or {'start_timestamp': '', 'end_timestamp': ''}
        """
        url = 'https://maicai.api.ddxq.mobi/order/getMultiReserveTime'
        headers = utils.get_headers()
        payload = utils.get_body()
        payload['address_id'] = address_id
        payload['products'] = '[' + products_raw + ']'
        payload['group_config_id'] = ''
        payload['isBridge'] = 'false'
        result = {}
        try:
            r = requests.post(url, headers=headers, data=payload)
        except Exception as e:
            raise RequestError(e)

        res = self.is_query_success(r)
  
        reserve_times = res['data'][0]['time'][0]['times']
        for reserve_time in reserve_times:
            if reserve_time['fullFlag'] == False:
                result['start_timestamp'] = reserve_time['start_timestamp']
                result['end_timestamp'] = reserve_time['end_timestamp']
                break
        return result

if __name__ == '__main__':
    api = Api()
    address_id = api.get_address_id()
    cart_info = api.get_cart()
    # cart_info = None
    if cart_info:
        products = cart_info['products']
        effective_product_names = cart_info['effective_product_names']
        res = api.check_reserve_time(address_id, json.dumps(products))
        msg = '购物车有效商品{}件, 运力: {}\n{}'.format(
            len(effective_product_names), 
            '有' if res else '无',
            ','.join([el[:2] for el in effective_product_names])
        )
    else:
        msg = '购物车无有效商品'
    print(msg)