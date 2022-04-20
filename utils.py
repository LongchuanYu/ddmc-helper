import yaml


with open('config.yml', 'r', encoding='utf-8') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

def get_headers():
    headers = { 
        'User-Agent': config['ua'],
        'Connection': 'keep-alive',
        'Content-Length': '2249',
        'content-type': 'application/x-www-form-urlencoded',
        'ddmc-city-number': config['city_number'],
        'ddmc-build-version': config['build_version'],
        'ddmc-device-id': config['device_id'],
        'ddmc-station-id': config['station_id'],
        'ddmc-channel': 'applet',
        'ddmc-os-version': '[object Undefined]',
        'ddmc-app-client-id': '4',
        'Cookie': config['cookie'],
        'ddmc-ip': '',
        'ddmc-longitude': config['longitude'],
        'ddmc-latitude': config['latitude'],
        'ddmc-api-version': config['api_version'],
        'ddmc-uid': config['uid'],
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://servicewechat.com/wx1e113254eda17715/422/page-frame.html'
    }
    return headers

def get_body(is_build_from_raw_body=False):
    body = {
        "uid": config['uid'],
        "longitude": config['longitude'],
        "latitude": config['latitude'],
        "station_id": config['station_id'],
        "city_number": '0101',
        "api_version": config['api_version'],
        "app_version": config['build_version'],
        "applet_source": '',
        "channel": 'applet',
        "app_client_id": '4',
        "sharer_uid": '',
        "openid": config['device_id'],
        "h5_source": '',
        "device_token": config['device_token']
    }

    if is_build_from_raw_body:
        raw_body_dict = build_from_raw_body('')
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