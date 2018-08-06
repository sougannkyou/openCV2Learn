# dianping
from pprint import pprint
import cv2
import aircv as ac

img_obj = ac.imread("dianping/photo.png")
# img_bg = ac.imread("dianping/2_2.png")
img_bg = ac.imread("dianping/2_2.png")


def debug(x, y):
    cv2.circle(img=img_bg, center=(int(x), int(y)), radius=40, color=(0, 255, 0), thickness=1)
    cv2.putText(img=img_bg, text='match', org=(int(x) - 50, int(y) + 10),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 255, 0), thickness=1)
    cv2.startWindowThread()
    cv2.imshow('Debugger', img_bg)
    cv2.waitKey(5 * 1000)
    cv2.destroyAllWindows()
    cv2.waitKey(100)


def test():
    # pos = ac.find_template(img_bg, img_obj, threshold=0.7)
    # print(pos)
    ret = ac.find_all_template(img_bg, img_obj, threshold=0.5)
    pprint(ret)
    return ret


if __name__ == '__main__':
    ret = test()
    # (x, y) = ret['result']
    for result in ret:
        x, y = result['result']
        debug(x, y)
    print(cv2.getBuildInformation())
