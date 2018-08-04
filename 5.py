# coding:utf8
import sys
import cv2
import numpy as np


def GetRowRects(img):
    rows = []
    obj = cv2.imread(img)
    h, w, c = obj.shape
    projection =

    cv2.getRotationMatrix2D()


img = cv2.imread('shapes.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)
