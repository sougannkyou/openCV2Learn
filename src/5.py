# coding:utf8
import sys
import numpy as np
from PIL import Image
import cv2


def test(img):
    ret = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 4))
    print(ret)


if __name__ == '__main__':
    img = cv2.imread('shapes.png')
    test(img)
