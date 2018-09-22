from pprint import pprint
from aip import AipImageClassify

APP_ID = '14131380'
API_KEY = 'KyCbH0iKqkr1usuRAQR5CSga'
SECRET_KEY = 'IkS88smDf5Ab8OGvobIsDzM2x9zWRB7g'

client = AipImageClassify(APP_ID, API_KEY, SECRET_KEY)

""" 读取图片 """


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


image = get_file_content('./images/A4L1.jpg')

""" 调用车辆识别 """
client.carDetect(image)

""" 如果有可选参数 """
options = {
    'top_num': 3,
    'baike_num': 5
}

""" 带参数调用车辆识别 """
pprint(client.carDetect(image, options))
