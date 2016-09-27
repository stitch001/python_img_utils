#coding:utf-8

import cv2
import numpy as np

def get_theshold_num_data(theshold,file_path):
    img = cv2.imread(file_path.decode("utf-8").encode("gbk"),0)
    _,img = cv2.threshold(img,theshold,255,cv2.THRESH_BINARY)
    img_2 =  cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
    return img_2