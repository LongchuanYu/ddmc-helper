# 基本配置
bark_id = ''  # bark app通知id
duration = 10  # 执行间隔时间秒
run_type = 1  # 监控类型 1检查配送时间

# 首页get参数
station_id = ''  # 站点id

# 购物车post参数
longitude = ''  # ddmc-longitude 上海的经度
latitude = ''  # ddmc-latitude 上海的纬度
city_number = '0101'  # ddmc-city-number 0101上海
api_version = '9.49.2'  # ddmc-api-version
build_version = '2.82.0'    # ddmc-build-version

ua = ''
cookie = '='  # 账号cookie 类似:DDXQSESSID=XXXXX
device_id = ''  # ddmc-device-id
uid = ''  # ddmc-uid

# 然后raw_body填Fiddler里面请求信息的Raw tab最下面的一串url格式的字符串(类似uid=xxx&longitude=xxx，购物车点结算-预约时间就有了)
raw_body = ''

name_of_all_categories = [
    "预制菜", "蔬菜豆制品", "肉禽蛋", "水产海鲜", "水果鲜花", "叮咚特供", "乳品烘焙", "速食冻品", "粮油调味", "酒水饮料", "火锅到家", "熟食卤味",
    "休闲零食", "日用百货", "方便食品", "营养早餐", "宝妈严选", "轻养星球", "在家烧烤", "云仓快送"
]
name_of_categories_i_care = [
    '酒水饮料'
]

def get_headers():
    headers = { 
        'User-Agent': ua,
        'Connection': 'keep-alive',
        'Content-Length': '2249',
        'content-type': 'application/x-www-form-urlencoded',
        'ddmc-city-number': city_number,
        'ddmc-build-version': build_version,
        'ddmc-device-id': device_id,
        'ddmc-station-id': station_id,
        'ddmc-channel': 'applet',
        'ddmc-os-version': '[object Undefined]',
        'ddmc-app-client-id': '4',
        'Cookie': cookie,
        'ddmc-ip': '',
        'ddmc-longitude': longitude,
        'ddmc-latitude': latitude,
        'ddmc-api-version': api_version,
        'ddmc-uid': uid,
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://servicewechat.com/wx1e113254eda17715/422/page-frame.html'
    }
    return headers

def get_body(build_from_raw_body=False):
    body = {
        "uid": uid,
        "longitude": longitude,
        "latitude": latitude,
        "station_id": station_id,
        "city_number": '0101',
        "api_version": api_version,
        "app_version": build_version,
        "applet_source": '',
        "channel": 'applet',
        "app_client_id": '4',
        "sharer_uid": '',
        "openid": device_id,
        "h5_source": '',
        "device_token": ''
    }

    if build_from_raw_body:
        raw_body_dict = build_from_raw_body(raw_body)
        for key in raw_body_dict:
            if key in body:
                body[key] = raw_body_dict[key]
    return body
    
def build_from_raw_body(raw_body):
    body = []
    key_value = raw_body.split('&')
    for kv in key_value:
        k, v = kv.split('=')
        body[k] = v
    return body