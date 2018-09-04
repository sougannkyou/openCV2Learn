import sys
import cv2
import numpy as np
from datetime import datetime
from pprint import pprint


# FONT_SIZE = 24
# FONT_SIZE = 15
# FONT_SIZE = 18


class Detect(object):
    def __init__(self, font_size=18, region=(0, 0, 480, 800)):
        self._DEBUG = False
        self.LINE_WORD_MIN = 5  # 5个字
        self.window_flags = cv2.WINDOW_NORMAL  # WINDOW_AUTOSIZE | WINDOW_KEEPRATIO | WINDOW_GUI_EXPANDED
        self._SHOW_TOP_X = 60
        self._SHOW_TOP_Y = 100
        self._font_size = font_size
        self._spacing = font_size
        self._region = region
        self._img_obj = None

    def preprocess(self, gray):
        # Sobel算子，x方向求梯度
        sobel = cv2.Sobel(gray, cv2.CV_8U, 1, 0, ksize=3)

        # 二值化
        ret, binary = cv2.threshold(sobel, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)

        # binary = cv2.GaussianBlur(binary, (7, 7), 0)
        if self._font_size == 15:
            binary = cv2.medianBlur(binary, 3)
        elif self._font_size == 18:
            binary = cv2.medianBlur(binary, 3)
            binary = cv2.medianBlur(binary, 1)
            binary = cv2.medianBlur(binary, 1)
        else:  # self._font_size = 24
            binary = cv2.medianBlur(binary, 3)
            binary = cv2.medianBlur(binary, 3)
            binary = cv2.medianBlur(binary, 3)

        # 膨胀和腐蚀操作的核函数
        if self._font_size == 15:
            erosion_rect = cv2.getStructuringElement(cv2.MORPH_RECT, (24, 7))
            dilation_rect = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 4))
            dilation2_rect = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 4))
        elif self._font_size == 18:
            erosion_rect = cv2.getStructuringElement(cv2.MORPH_RECT, (24, 7))
            dilation_rect = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 4))
            dilation2_rect = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 4))
        else:  # self._font_size == 24:
            erosion_rect = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 9))
            dilation_rect = cv2.getStructuringElement(cv2.MORPH_RECT, (24, 6))
            dilation2_rect = cv2.getStructuringElement(cv2.MORPH_RECT, (24, 6))

        # 膨胀一次，让轮廓突出
        dilation = cv2.dilate(binary, dilation_rect, iterations=1)

        # 腐蚀一次，去掉细节，如表格线等。注意这里去掉的是竖直的线
        erosion = cv2.erode(dilation, erosion_rect, iterations=1)

        # 再次膨胀，让轮廓明显一些
        dilation2 = cv2.dilate(erosion, dilation2_rect, iterations=3)

        if self._DEBUG:
            cv2.namedWindow("binary", self.window_flags)
            cv2.resizeWindow("binary", 300, 500)
            cv2.imshow("binary", binary)
            cv2.moveWindow("binary", self._SHOW_TOP_X, self._SHOW_TOP_Y)
            cv2.imwrite("test_image/text_line/binary.png", binary)

            cv2.namedWindow("dilation", self.window_flags)
            cv2.resizeWindow("dilation", 300, 500)
            cv2.imshow("dilation", dilation)
            cv2.moveWindow("dilation", 300 + self._SHOW_TOP_X, self._SHOW_TOP_Y)
            cv2.imwrite("test_image/text_line/dilation.png", dilation)

            cv2.namedWindow("erosion", self.window_flags)
            cv2.resizeWindow("erosion", 300, 500)
            cv2.imshow("erosion", erosion)
            cv2.moveWindow("erosion", 600 + self._SHOW_TOP_X, self._SHOW_TOP_Y)
            cv2.imwrite("test_image/text_line/erosion.png", erosion)

            # cv2.namedWindow("dilation2", cv2.WINDOW_NORMAL)
            # cv2.imshow("dilation2", dilation2)
            # cv2.imwrite("dilation2.png", dilation2)

        return erosion

    def find_text_region(self, img):
        '''
        查找和筛选文字区域
        '''
        region = []
        image, contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            # 面积
            area = cv2.contourArea(contour)

            # 筛选掉面积太小的
            if area < self._font_size * self._font_size * self.LINE_WORD_MIN / 10:
                continue

            # # 近似多边形
            # epsilon = 0.01 * cv2.arcLength(contour, True)
            # approx = cv2.approxPolyDP(contour, epsilon, True)
            # print('approx:', len(approx))
            # cv2.drawContours(img, [contour], 0, 255, -1)
            # cv2.imshow('img', img)

            # 找到最小的矩形，该矩形可能有方向
            rect = cv2.minAreaRect(contour)
            a, b, c = rect

            # box是四个点的坐标
            box = cv2.boxPoints(rect)
            box = np.int0(box)

            top_y = box[2][1]
            bottom_y = box[0][1]
            top_x = box[0][0]
            bottom_x = box[2][0]

            # 筛选限定范围内的
            (_top_x, _top_y, _bottom_x, _bottom_y) = self._region
            if top_x < _top_x or top_y < _top_y or bottom_x > _bottom_x or bottom_y > _bottom_y:
                continue

            # 靠近顶端的可能是wifi、4G和电池
            if top_y < 100:
                continue

            height = abs(bottom_y - top_y)
            width = abs(top_x - bottom_x)

            # 筛选掉宽度小于5个字宽
            if width < self.LINE_WORD_MIN * self._font_size:
                continue

            # 筛选掉瘦高，留下矮宽的
            if height > width:
                continue

            # 筛选掉太矮的
            if height < self._font_size * 0.6:
                continue

            # 筛选掉文字宽度不够的
            if height * self.LINE_WORD_MIN > width:
                continue

            # print("rect is: ", a, b)
            print('top_x:{} top_y:{} bottom_x:{} bottom_y:{}'.format(top_x, top_y, bottom_x, bottom_y))
            region.append(box)

        return region

    def find_paragraph(self, region):
        focus = []
        done = []
        for i in range(len(region)):
            print(len(region), done)
            if i in done:
                continue

            r1 = region[i]
            top_x1 = r1[0][0]
            top_y1 = r1[2][1]
            bottom_x1 = max(r1[2][0], r1[3][0])
            bottom_y1 = r1[0][1]

            for j in range(len(region)):
                if j in done or j == i:
                    continue

                r2 = region[j]
                top_x2 = r2[0][0]
                top_y2 = r2[2][1]
                bottom_x2 = max(r2[2][0], r2[3][0])
                bottom_y2 = r2[0][1]

                # 小于行间距
                if abs((bottom_y1 + top_y1) / 2 - (bottom_y2 + top_y2) / 2) < self._spacing * 2:
                    print(top_x1, top_y1, bottom_x1, bottom_y1, 'VS', top_x2, top_y2, bottom_x2, bottom_y2)
                    focus.append((min(top_x1, top_x2), min(top_y1, top_y2),
                                  max(bottom_x1, bottom_x2), max(bottom_y1, bottom_y2)))
                    done.append(i)
                    done.append(j)
                else:
                    focus.append((top_x1, top_y1, bottom_x1, bottom_y1))

        if self._DEBUG:
            for f in focus:
                (top_x, top_y, bottom_x, bottom_y) = f
                cv2.rectangle(self._img_obj, (top_x, top_y), (bottom_x, bottom_y), (0, 0, 255), 2)

            cv2.namedWindow("paragraph", self.window_flags)
            cv2.resizeWindow("paragraph", 480, 800)
            cv2.imshow("paragraph", self._img_obj)
            cv2.moveWindow("paragraph", 1200 + self._SHOW_TOP_X, self._SHOW_TOP_Y)
            cv2.imwrite("test_image/text_line/paragraph.png", self._img_obj)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    def merger(self, r1, r2):
        pass

    def detect(self, image_path):
        self._img_obj = cv2.imread(image_path)
        gray = cv2.cvtColor(self._img_obj, cv2.COLOR_BGR2GRAY)
        dilation = self.preprocess(gray)
        region = self.find_text_region(dilation)
        # 画轮廓（绿） (蓝,绿,红)
        for box in region:
            cv2.drawContours(self._img_obj, [box], 0, (0, 255, 0), 2)

        if self._DEBUG:
            cv2.namedWindow("contours", self.window_flags)
            cv2.resizeWindow("contours", 300, 500)
            cv2.imshow("contours", self._img_obj)
            cv2.moveWindow("contours", 900 + self._SHOW_TOP_X, self._SHOW_TOP_Y)
            cv2.imwrite("test_image/text_line/contours.png", self._img_obj)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

        self.find_paragraph(region)


if __name__ == '__main__':
    # image_path = 'test_image/text_line/news{}.png'.format(17)  # qq bug 18 17
    image_path = 'test_image/text_line/qq{}.png'.format(6)  # bug: 6
    # image_path = 'test_image/text_line/baidu{}.png'.format(4)  # bug: 6
    # image_path = 'test_image/text_line/shouhu{}.png'.format(7)
    # image_path = 'test_image/text_line/sina{}.png'.format(4)  # bug:4
    # image_path = 'test_image/text_line/163_{}.png'.format(7)  # bug: 6 7
    # image_path = 'test_image/text_line/ifeng{}.png'.format(3)  # bug:3
    start = datetime.now()
    d = Detect(font_size=18)
    d._DEBUG = True
    d.detect(image_path)
    end = datetime.now()
    print('spend times:{}'.format(end - start))
