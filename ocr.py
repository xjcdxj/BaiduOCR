from base import aip, ocr_token
from urllib import request, parse
import json, base64


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


def ocr():
    url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic'
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
    # access_token = request.urlopen(url, data=token_data)

    return access_token['access_token']


def token():
    import ssl

    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=17464280&client_secret=【官网获取的SK】'
    rq = request.Request(host)
    rq.add_header('Content-Type', 'application/json; charset=UTF-8')
    response = request.urlopen(request)
    content = response.read()
    if (content):
        print(content)


def ocr_test():
    OcrAip = aip()
    image = get_file_content('C:/Users/XuJiacheng/OneDrive/图片/批注 2019-10-08 161104.png')
    result = OcrAip.basicGeneral(image)['words_result']
    for i in result:
        print(i['words'])


def test2():
    ocr()
    pass


def token_ocr():
    token = ocr_token()
    url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic'
    img_path = 'C:/Users/XuJiacheng/OneDrive/图片/批注 2019-10-08 161104.png'
    with open(img_path, 'rb') as f:
        image = f.read()
    image = base64.b64encode(image)
    data = {
        'access_token': token,
        'image': image
    }
    header = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = parse.urlencode(data).encode('utf-8')
    rq = request.Request(url, headers=header, data=data)
    response = request.urlopen(rq)
    result = response.read().decode()
    print(result)
    result = json.loads(result)['words_result']
    text = []
    for i in result:
        text.append(i['words'])
    print(text)


if __name__ == '__main__':
    token_ocr()
