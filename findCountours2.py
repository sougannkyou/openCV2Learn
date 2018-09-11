import cv2
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx


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
    img = cv2.imread('test_image/findcontours_02.png')

    fig, axes = plt.subplots(figsize=(6, 6))

    # 輪郭を抽出する。
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, contours, hierarchy = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 抽出した輪郭を表示する。
    axes.set_title('cv2.RETR_EXTERNAL')
    draw_contours(axes, img, contours)
    plt.show()

    # 階層構造をグラフで作成する。
    graph = nx.DiGraph()
    for my_no, info in enumerate(hierarchy[0]):
        next_no, prev_no, first_child_no, parent_no = info
        if parent_no == -1:
            graph.add_edge('root', my_no)
        else:
            graph.add_edge(parent_no, my_no)
        print('contour {} (next: {}, previous: {}, first_child: {}, parent: {})'.format(my_no, *info))

    pos = nx.spring_layout(graph)
    nx.draw_networkx_nodes(graph, pos, node_size=400, node_color='#3ddb94')
    nx.draw_networkx_edge_labels(graph, pos)
    nx.draw_networkx_labels(graph, pos)
    nx.draw_networkx_edges(graph, pos)
    plt.axis('off')
    plt.show()
