import json
import time
from urllib import request, parse
import pickle

from aip import AipOcr


def aip():
    """ 你的 APPID AK SK """
    APP_ID = '17464280'
    API_KEY = 'DRbVzkC2vgG7i6QcW3mPkqef'
    SECRET_KEY = 'TU6ixTndecAlLHPznPVpqzewU3whQTwu'

    return AipOcr(APP_ID, API_KEY, SECRET_KEY)


def ocr_token():
    try:
        with open('token', 'rb') as f:
            f = f.read()
            token = pickle.loads(f)
            access_token = token['token']
            validity = token['validity']
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
    try:
        access_token = request.urlopen(rq)

    except:
        return 1, '访问token失败'
    access_token = access_token.read().decode('utf-8')
    access_token = json.loads(access_token)
    try:
        if access_token['access_token'] and access_token['expires_in']:
            token = {
                'token': access_token['access_token'],
                'validity': access_token['expires_in']
            }
            with open('token', 'wb') as f:
                pickle.dump(token, f)
            return 0, access_token['access_token']
    except:
        if access_token['error'] and access_token['error_description']:
            return 1, access_token['error'] + '\n' + access_token['error_description']
        else:
            return 1, '未知错误'
