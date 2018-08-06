# dianping
from pprint import pprint
from PIL import Image
import cv2
import numpy as np
import pandas as pd
import aircv as ac
from datetime import datetime
import pytesseract

start = datetime.now()
img = Image.open('dianping/p1.png')
img = img.crop((0, 0, 480, 750))
img.save('dianping/p1_new.png')

img = Image.open('dianping/p2.png')
img = img.crop((0, 75, 480, 750))
img.save('dianping/p2_new.png')

# 800 * 480
img1 = cv2.imread('dianping/p1_new.png')
# img1 = img[0:0, 750:480]  # 左上角坐标(0,0)，右下角坐标(480,750)
# # cv2.imwrite('dianping/p1_new.png', img1)
#
img2 = cv2.imread('dianping/p2_new.png')
# img2 = img[0:0, 750:480]
# # cv2.imwrite('dianping/p2_new.png', img2)

# gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
# gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
# ====使用numpy的数组矩阵合并concatenate======

# nox_adb.exe shell input swipe 240 670 240 10 2000
# nox_adb.exe shell screencap -p /sdcard/capture.png
# nox_adb.exe pull /sdcard/capture.png c:\Nox\

# image = np.concatenate((gray1, gray2))
# 纵向连接
img_bg = np.vstack((img1, img2))
cv2.imwrite('dianping/img_bg.png', img_bg)
# img_bg = np.vstack((gray1, gray2))
# # 横向连接
# # image = np.concatenate([gray1, gray2], axis=1)
#
# # ====使用pandas数据集处理的连接concat========
#
# df1 = pd.DataFrame(gray1)
# df2 = pd.DataFrame(gray2)  # ndarray to dataframe
# df = pd.concat([df1, df2])
# # 纵向连接,横向连接
# # df = pd.concat([df1, df2], axis=1)
# image = np.array(df)  # dataframe to ndarray

# 152 * 152
img_border = ac.imread("dianping/border.png")
h, w, _ = img_border.shape
ret = ac.find_all_template(img_bg, img_border, threshold=0.5)
l = []
for r in ret:
    (x, y) = r['result']
    l.append(y)

pprint(l)
min_y = min(l)
print(min_y)

img = Image.open('dianping/img_bg.png')
img = img.crop((0, 180, 480, min_y - h / 2))
img.save('dianping/img_bg_new.png')

image = Image.open('dianping/img_bg_new.png')
code = pytesseract.image_to_string(image, lang='chi_sim')
print(code)

end = datetime.now()
print('times:', (end - start).microseconds / 1000)

# cv2.startWindowThread()
# cv2.imshow('img_bg', img_bg)
# cv2.waitKey(60 * 1000)
# cv2.destroyAllWindows()
# cv2.waitKey(100)
