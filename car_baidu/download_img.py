import os
import redis
import urllib.request
from datetime import datetime
from pprint import pprint
from aip import AipImageClassify

APP_ID = '14131380'
API_KEY = 'KyCbH0iKqkr1usuRAQR5CSga'
SECRET_KEY = 'IkS88smDf5Ab8OGvobIsDzM2x9zWRB7g'

REDIS_SERVER = 'redis://192.168.174.130/11'
img_key = 'weibo_pic_l'
images_path = 'images\\'
conn = redis.StrictRedis.from_url(REDIS_SERVER)


def get_file_content(file_path):
    with open(file_path, 'rb') as fp:
        return fp.read()


def detection(file_path):
    client = AipImageClassify(APP_ID, API_KEY, SECRET_KEY)
    image = get_file_content(file_path)
    client.carDetect(image)
    ret = client.carDetect(image, {'top_num': 10, 'baike_num': 5})  # 带参数调用车辆识别
    pprint(ret)
    return ret


def uploadAPI(request):
    ret = {'img_src': 'error.png'}
    try:
        img_src = str(int(datetime.now().timestamp() * 1000000))
        file_obj = request.FILES.get('file')
        fixed = file_obj.name[file_obj.name.find('.'):]
        img_path = os.path.join(STATIC_ROOT, 'upload', img_src + fixed)
        ret = {'img_src': '/static/upload/{}{}'.format(img_src, fixed)}
        print(img_path)
        f = open(img_path, 'wb')
        # print(file_obj, type(file_obj))
        for chunk in file_obj.chunks():
            f.write(chunk)
        f.close()
        ret.update(detection(img_path))
    except Exception as e:
        print('error:', e)
    finally:
        print('ok')


def dowmload():
    # {
    #     "data_db": "redis:\/\/redis-collectioncache-1.istarshine.net.cn\/3\/sina_data",
    #     "siteName": "\u65b0\u6d6a\u5fae\u535a",
    #     "source_icon_url": "http:\/\/tvax2.sinaimg.cn\/crop.0.0.996.996.50\/0067l5Kxly8fuhwirw34vj30ro0roq4c.jpg",
    #     "mid": "4288906235275900",
    #     "redirect_count": 0,
    #     "device": "OPPO R9s Plus",
    #     "gtime": 1538038491,
    #     "ctime": 1538038393,
    #     "title": "\u51b7\u7684\u817f\u6296 ",
    #     "url": "http:\/\/weibo.com\/5605258337\/GBiR9m8va",
    #     "html": "",
    #     "source": "\u5d14yuting",
    #     "replyCount": 0,
    #     "pic_urls": [
    #         "http:\/\/wx4.sinaimg.cn\/thumbnail\/0067l5Kxly1fvo76gxd10j30qo0zkgsu.jpg"
    #     ]
    # }
    img_info = conn.lpop(img_key)
    conn.lpush(img_key, img_info)
    for url in img_info['pic_urls']:
        urllib.request.urlretrieve(url, images_path)
