import os
import json
import redis
import urllib.request
from datetime import datetime
from pprint import pprint

REDIS_SERVER = 'redis://192.168.174.130/10'
img_key = 'weibo_pic_l'
img_detection_key = 'weibo_pic_detector_h'
conn = redis.Redis(host='192.168.174.130', port='6379', db=10, decode_responses=True)
local_conn = redis.Redis(host='172.16.253.37', port='6379', db=10, decode_responses=True)

def download():
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
    #     ],
    #     "detect":[{},{},{}]
    # }
    for _ in range(min(conn.llen(img_key), 10)):
        v = conn.lpop(img_key)
        conn.rpush(img_key, v)
        local_conn.rpush(img_key, v)  # backup
        img_info = json.loads(v)
        if not conn.hexists(img_detection_key, img_info['mid']):
            img_info.update({"detect": [{} for _ in range(len(img_info['pic_urls']))]})
            conn.hset(img_detection_key, img_info['mid'], img_info)
            # pprint(img_info)
            i = 0
            for url in img_info['pic_urls']:
                urllib.request.urlretrieve(
                    url.replace('thumbnail', 'large'),
                    os.path.join(os.getcwd(), 'images', '{}_{}.jpg'.format(img_info['mid'], i))
                )
                i += 1


if __name__ == '__main__':
    download()
