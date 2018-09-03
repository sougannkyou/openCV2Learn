# coding:utf8
import sys
import cv2
import numpy as np
from pprint import pprint

FONT_SIZE = 18
LINE_MIN_SIZE = 5


def preprocess(gray):
    # 1. Sobel算子，x方向求梯度
    sobel = cv2.Sobel(gray, cv2.CV_8U, 1, 0, ksize=3)

    # 2. 二值化
    ret, binary = cv2.threshold(sobel, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)

    # binary = cv2.GaussianBlur(binary, (7, 7), 0)
    binary = cv2.medianBlur(binary, 3)
    binary = cv2.medianBlur(binary, 1)
    binary = cv2.medianBlur(binary, 1)

    # 3. 膨胀和腐蚀操作的核函数
    # FONT_SIZE = 24
    # erosion_rect = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 9))
    # dilation_rect = cv2.getStructuringElement(cv2.MORPH_RECT, (24, 6))
    # dilation2_rect = cv2.getStructuringElement(cv2.MORPH_RECT, (24, 6))

    # FONT_SIZE = 18
    erosion_rect = cv2.getStructuringElement(cv2.MORPH_RECT, (24, 7))
    dilation_rect = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 4))
    dilation2_rect = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 4))

    # 4. 膨胀一次，让轮廓突出
    dilation = cv2.dilate(binary, dilation_rect, iterations=1)

    # 5. 腐蚀一次，去掉细节，如表格线等。注意这里去掉的是竖直的线
    erosion = cv2.erode(dilation, erosion_rect, iterations=1)

    # 6. 再次膨胀，让轮廓明显一些
    dilation2 = cv2.dilate(erosion, dilation2_rect, iterations=3)

    # 7. 存储中间图片
    cv2.namedWindow("binary", cv2.WINDOW_NORMAL)
    cv2.imshow("binary", binary)
    cv2.imwrite("binary.png", binary)

    cv2.namedWindow("dilation", cv2.WINDOW_NORMAL)
    cv2.imshow("dilation", dilation)
    cv2.imwrite("dilation.png", dilation)

    cv2.namedWindow("erosion", cv2.WINDOW_NORMAL)
    cv2.imshow("erosion", erosion)
    cv2.imwrite("erosion.png", erosion)

    # cv2.namedWindow("dilation2", cv2.WINDOW_NORMAL)
    # cv2.imshow("dilation2", dilation2)
    # cv2.imwrite("dilation2.png", dilation2)

    return erosion


def findTextRegion(img):
    region = []

    # 1. 查找轮廓
    image, contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 2. 筛选
    for i in range(len(contours)):
        cnt = contours[i]
        # 计算该轮廓的面积
        area = cv2.contourArea(cnt)

        # 筛选掉面积太小的
        if area < FONT_SIZE * FONT_SIZE * LINE_MIN_SIZE / 10:
            continue

        # 轮廓近似，作用很小
        epsilon = 0.001 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)

        # 找到最小的矩形，该矩形可能有方向
        rect = cv2.minAreaRect(cnt)
        print("rect is: ", rect)

        # box是四个点的坐标
        box = cv2.boxPoints(rect)
        box = np.int0(box)

        # 计算高和宽
        height = abs(box[0][1] - box[2][1])
        width = abs(box[0][0] - box[2][0])

        # 筛选掉宽度小于3个字宽
        if width < LINE_MIN_SIZE * FONT_SIZE:
            continue

        # 筛选掉瘦高的矩形，留下矮宽的
        if height > width:
            continue

        # 筛选掉太矮的
        if height < FONT_SIZE / 2:
            continue

        # 筛选掉太矮的
        if height * LINE_MIN_SIZE > width:
            continue

        region.append(box)

    return region


def detect(img):
    # 1.  转化成灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 2. 形态学变换的预处理，得到可以查找矩形的图片
    dilation = preprocess(gray)

    # 3. 查找和筛选文字区域
    region = findTextRegion(dilation)

    # 4. 用绿线画出这些找到的轮廓
    for box in region:
        cv2.drawContours(img, [box], 0, (0, 255, 0), 2)

    cv2.namedWindow("img", cv2.WINDOW_NORMAL)
    cv2.imshow("img", img)

    # 带轮廓的图片
    cv2.imwrite("contours.png", img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    # 读取文件
    # imagePath = sys.argv[1]
    # image_path = 'test_image/text_line/tenxun{}.png'.format(18)
    # image_path = 'test_image/text_line/shouhu{}.png'.format(7)
    # image_path = 'test_image/text_line/sina{}.png'.format(5)  # bug:4
    # image_path = 'test_image/text_line/163_{}.png'.format(7)  # bug:1 6 7
    image_path = 'test_image/text_line/ifeng{}.png'.format(3)  # bug:3
    img = cv2.imread(image_path)
    detect(img)
