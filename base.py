from aip import AipOcr
from urllib import request, parse
import json, time


def aip():
    """ 你的 APPID AK SK """
    APP_ID = '17464280'
    API_KEY = 'DRbVzkC2vgG7i6QcW3mPkqef'
    SECRET_KEY = 'TU6ixTndecAlLHPznPVpqzewU3whQTwu'

    return AipOcr(APP_ID, API_KEY, SECRET_KEY)


def ocr_token():
    try:
        with open('token', 'r') as f:
            access_token = f.readline().rstrip()
            validity = f.readline()
            if access_token and validity:
                if time.time() < float(validity):
                    return access_token
    except FileNotFoundError:
        pass
    token_url = 'https://aip.baidubce.com/oauth/2.0/token'
    data = {
        'grant_type': 'client_credentials',
        'client_id': 'DRbVzkC2vgG7i6QcW3mPkqef',
        'client_secret': 'TU6ixTndecAlLHPznPVpqzewU3whQTwu'
    }

    token_data = parse.urlencode(data).encode('utf-8')
    rq = request.Request(token_url, data=token_data)
    rq.add_header('Content-Type', 'application/json; charset=UTF-8')
    access_token = request.urlopen(rq).read().decode('utf-8')
    access_token = json.loads(access_token)
    with open('token', 'w') as f:
        f.write(access_token['access_token'] + '\n%s' % str(time.time() + int(access_token['expires_in'])))
    return access_token['access_token']
