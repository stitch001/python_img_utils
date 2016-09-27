#coding:utf-8

import numpy as np
import cv2

#点标记类
class Label_Pnt:
    """
    点标记类
    """
    def __init__(self,x,y,label=0):
        self.x = x
        self.y = y
        self.label = label

    def __str__(self):
        return str(self.x) + "," +str(self.y) + "," + str(self.label)

#获取邻域内的连通标记
def get_neighbor_label(point,img,plist):
    '''
    获取邻域内的连通标记 上 左 标记，有上标记取上标记(两个的话取第一个，然后把两个标记建立相等关系)
    :param point: Label_pnt
    :param img: 图像 numpy array
    :param plist: 标记点集合
    :return: 可能有两个
    '''
    x = pnt.x
    y = pnt.y
    neighbor_labels = []
    if y > 0 and x > 0:
        #获取上，左方面的邻域的标记值 label
        if img[x,y-1] > 0:
            neighbor_labels.append(plist[str(x)+","+str(y-1)].label)
        if img[x-1,y] >0:
            neighbor_labels.append(plist[str(x-1)+","+str(y)].label)
    elif y > 0 and x ==0:
        if img[x,y-1] > 0:
            neighbor_labels.append(plist[str(x) + "," + str(y - 1)].label)
    elif x > 0 and y == 0:
        if img[x - 1, y] > 0:
            neighbor_labels.append(plist[str(x - 1) + "," + str(y)].label)
    return neighbor_labels

#合并相等的 标签点 注意，此处需要使用无向图
# 例如 x = [(1,3),(3,7),(2,4)]
# 合并为 [[1, 3, 7], [2, 4]]
# 利用图的深度优先遍历实现边的合并
def get_lincked_field(x):
    #x = sorted(x)
    node_num = len(np.unique(x))
    visited = np.zeros(node_num)
    print visited
    #建立邻接表
    neighbor_list = {}
    for item in x:
        node1 ,node2  = item
        l = neighbor_list.get(node1)
        if not l is None:
            if node2 not in l:
                l.append(node2)
        else:
            neighbor_list[node1] = [node2]
    #print neighbor_list

    #使用list当成数据结构 栈
    #append --> push 入栈
    #pop --> pop 出栈  pop(0)出队列
    v_stack = []
    v_list = []#所有同一类的边在这个列表中
    for k,v in neighbor_list.items(): #循环访问邻接表中的数据
        if not visited[k - 1]: #访问过的表数据跳过
            visited[k-1] = 1
            v_sublist = [k]
        else:
            continue
        if v : #将邻接表中边集合入栈
            for node in v:
                v_stack.append(node)

        while len(v_stack) > 0: #深度优先遍历
            #node = v_stack.pop(0)
            node = v_stack.pop()
            if not visited[node-1]:
                v_sublist.append(node) #相同关系的边归为一类，在一个列表中存储
                #print node
                visited[node-1] = 1
            else:
                continue
            l = neighbor_list.get(node)
            if l : #将 l 邻接表入栈
                for node in l:
                    v_stack.append(node)
        #栈空则表示一个连通区域结束，一次深度优先遍历结束
        v_list.append(v_sublist)
        if np.sum(visited) == node_num:
            break

    return v_list

img = cv2.imread("cc3.png")
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#blur = cv2.blur(gray,(5,5))
#_,img_bin = cv2.threshold(gray,200,1,cv2.THRESH_BINARY_INV)
_,img_bin = cv2.threshold(gray,200,1,cv2.THRESH_BINARY)
#print gray
h,w = img_bin.shape
#print w,h
#two-pass 算法
plist = {}
eq_labels = []
label_gen = 1
for i in xrange(h):
    for j in xrange(w):
        if img_bin[i,j] > 0:
            pnt = Label_Pnt(i,j)
            labels = get_neighbor_label(pnt,img_bin,plist)
            if len(labels) > 0: #附近点有标记
                pnt.label = labels[0] #采取上方连通标记
                if len(labels) > 1 and labels[0] !=labels[1]:
                    pnt.label = labels[1] #建立相等关系
                    eq_labels.append((labels[1],labels[0]))
            else:
                pnt.label = label_gen #建立自己相等关系 主要用于孤立点
                eq_labels.append((label_gen, label_gen))
                label_gen += 1 #标记加一

            plist[str(i)+","+str(j)] = pnt

print eq_labels
eq_labels_unique = []
#变为简单图，无向图
for item in eq_labels:
    if not item in eq_labels_unique:
        eq_labels_unique.append(item)
        if item[1] != item[0]:
            eq_labels_unique.append((item[1],item[0]))
print eq_labels_unique
#获取图的连通分量
merged_labes = get_lincked_field(eq_labels_unique)
print merged_labes
#重新标记，标记为最小的标记
for pnt in plist.values():
    for l in merged_labes:
        if pnt.label in l:
            pnt.label = min(l)

print(len(merged_labes))
#颜色
# START FIXME 颜色数量不够，应该和连通区域的数量一样
c = {}
color = [
    [255, 0, 0],
    [0, 255, 255],
    [255, 0, 255],
    [255, 255, 0],
    [0, 255, 0],
    [0,0,255],
    [128,0,128],
    [128,179,200],
]
#END FIXME

for i,v in enumerate(merged_labes):
    c[v[0]] = color[i]
for item in plist.values():

    img[item.x,item.y] = c[item.label]
cv2.imwrite("ccout.png",img)