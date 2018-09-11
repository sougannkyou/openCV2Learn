import cv2
import matplotlib.pyplot as plt
import numpy as np


def draw_contours(axes, img, contours):
    from matplotlib.patches import Polygon
    axes.imshow(img)
    axes.axis('off')
    for i, cnt in enumerate(contours):
        cnt = np.squeeze(cnt)
        # 点同士を結ぶ線を描画する。
        axes.add_patch(Polygon(cnt, fill=None, lw=2., color='b'))
        # 点を描画する。
        axes.plot(cnt[:, 0], cnt[:, 1],
                  marker='o', ms=4., mfc='red', mew=0., lw=0.)
        # 輪郭の番号を描画する。
        axes.text(cnt[0][0], cnt[0][1], i, color='orange', size='20')


if __name__ == '__main__':
    # 画像を読み込む。
    img = cv2.imread('test_image/findcontours_01.png')
    img = cv2.flip(img, 1)

    # 画像を表示する。
    fig, axes = plt.subplots(figsize=(6, 6))
    axes.imshow(img)
    axes.axis('off')
    plt.show()

    # 輪郭抽出する。
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, contours, hierarchy = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    fig, axes = plt.subplots(figsize=(6, 6))
    draw_contours(axes, img, contours)
    plt.show()
