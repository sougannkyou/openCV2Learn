import cv2
import numpy as np
import matplotlib.pyplot as plt

# pic_path = './jian.png'
pic_path = './ce.png'
# pic_path = './liang.png'

img = cv2.imread(pic_path, 0)
hist = cv2.calcHist([img], [0], None, [256], [0, 256])
plt.subplot(121)
plt.imshow(img, 'gray')
plt.xticks([])
plt.yticks([])
plt.title("Original")
plt.subplot(122)
plt.hist(img.ravel(), 256, [0, 256])
plt.show()