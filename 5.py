# coding:utf8
import sys
import numpy as np
from  PIL import Image
import cv2


def GetRowRects(img):
    rows = []
    obj = cv2.imread(img)
    h, w, c = obj.shape
    # 用于存储投影值
    projection = [0 for _ in range(h)]

    # 遍历每一行计算投影值
    for y in range(h):
        for x in range(w):
            im = Image.open('image.gif')
            rgb_im = im.convert('RGB')
            r, g, b = rgb_im.getpixel((1, 1))
        {
            var
        s = Cv.Get2D(source, y, x);
        if (s.Val0 == 255)
        projection[y]++;


if __name__ == '__main__':
    img = cv2.imread('shapes.png')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)
