#coding:utf-8
import cv2
import numpy as np

def xy_cut(filename):
    img = cv2.imread(filename.decode("utf-8").encode("gbk"))
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img_inv = cv2.threshold(img_gray, 100, 255, cv2.THRESH_BINARY_INV)
    width_sum = np.sum(img_inv, axis=1)
    # 找到跳变值大于30的点 跳变值不大于30 证明是平滑的统计，不是文本行
    # 竖直投影找到文本行 该函数的方法，把0到非0的边界提取出来
    def get_edge_from_projection(sum):
        edge_array, = np.where(sum > 0)  # 找到投影中和大于0的点 的下标  numpy的where方法
        edge_array_2 = edge_array[np.where(np.gradient(edge_array) > 1)]  # 使用gradient求梯度，找到梯度不为0的点即为分界点
        edge_array_edge_2 = np.append(np.append(edge_array[0], edge_array_2), edge_array[-1])  # 将首，末相互结合成一个新的数组
        return zip(edge_array_edge_2[::2], edge_array_edge_2[1::2])  # 配成对儿

    edges = get_edge_from_projection(width_sum)
    # 水平投影 找子块儿
    for w1, w2 in edges:
        data = img_inv[w1:w2, :]
        cv2.line(img, (0, w1), (img_inv.shape[1] - 1, w1), (255, 0, 0))  # 水平画直线
        cv2.line(img, (0, w2), (img_inv.shape[1] - 1, w2), (255, 0, 0))  # 水平画直线
        height_sum = np.sum(data, axis=0)  # numpy 的sum方法 默认求数组中总和，axis=0 竖直 axis=1水平
        height_sum_edge = get_edge_from_projection(height_sum)
        for h1, h2 in height_sum_edge:
            cv2.line(img, (h1, w1), (h1, w2), (255, 0, 0))  # 竖直画线
            cv2.line(img, (h2, w1), (h2, w2), (255, 0, 0))  # 竖直画线

    img_2 = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    return img_2