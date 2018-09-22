# encoding:utf-8
import json
import base64
import urllib.parse
import urllib.request

'''
车型识别
'''
AK = 'KyCbH0iKqkr1usuRAQR5CSga'
SK = 'IkS88smDf5Ab8OGvobIsDzM2x9zWRB7g'

# client_id 为官网获取的AK， client_secret 为官网获取的SK
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(
    AK, SK)
request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/car"

try:
    request = urllib.request.Request(host)
    request.add_header('Content-Type', 'application/json; charset=UTF-8')
    response = urllib.request.urlopen(request)
    token = response.read()
    if token:
        print('token:', token)
        # {
        #   "refresh_token": "25.b55fe1d287227ca97aab219bb249b8ab.315360000.1798284651.282335-8574074",
        #   "expires_in": 2592000,
        #   "scope": "public wise_adapt",
        #   "session_key": "9mzdDZXu3dENdFZQurfg0Vz8slgSgvvOAUebNFzyzcpQ5EnbxbF+hfG9DQkpUVQdh4p6HbQcAiz5RmuBAja1JJGgIdJI",
        #   "access_token": "24.6c5e1ff107f0e8bcef8c46d3424a0e78.2592000.1485516651.282335-8574074",
        #   "session_secret": "dfac94a3489fe9fca7c3221cbf7525ff"
        # }

        f = open('./images/A4L1.jpg', 'rb')
        img = base64.b64encode(f.read())
        print('img size:', len(img))
        params = {"image": img, "top_num": 5}
        params = urllib.parse.urlencode(params)

        b = token.decode('utf-8')
        t = json.loads(b)
        access_token = t['access_token']  # '[调用鉴权接口获取的token]'
        print('access_token:', access_token)
        request_url = request_url + "?access_token=" + access_token
        request = urllib.request.Request(url=request_url, data=params)
        request.add_header('Content-Type', 'application/x-www-form-urlencoded')
        response = urllib.request.urlopen(request)
        content = response.read()
        if content:
            print('content:', content)

except Exception as e:
    print('error:', e)
finally:
    print('end.')
