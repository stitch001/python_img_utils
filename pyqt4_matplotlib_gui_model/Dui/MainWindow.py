#coding:utf-8

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import Pic_proc
import numpy
import cv2

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt


class MainWindow(QMainWindow):
    def __init__(self,parent=None):
        super(MainWindow, self).__init__(parent)

        self.file_path=""
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas,self)
        self.setMenus()

        layout = QBoxLayout(QBoxLayout.TopToBottom)
        layout.addWidget(self.canvas)
        layout.addWidget(self.toolbar)
        self.centerWidget = QWidget()
        self.centerWidget.setLayout(layout)
        self.setCentralWidget(self.centerWidget)



    #设置菜单
    def setMenus(self):
        menubar = self.menuBar()
        self_inner = self
        ax = self.figure.add_subplot(111)
        # 文件
        #  > 打开
        #  > 关闭
        #  > 保存
        #  > -----
        #  > 退出
        menu_file = menubar.addMenu(u"文件")
        menu_file_open_action = QAction(u"打开",menu_file)
        #文件 > 打开  绑定事件
        def get_open_file_name():
            file_name_str = QFileDialog.getOpenFileName(self_inner, u"打开文件","/", u"图片文件(*.jpg *.bmp *.png)")
            img = plt.imread(unicode(file_name_str))
            self_inner.figure.hold(False)
            ax.imshow(img)
            self_inner.canvas.draw()
            self_inner.file_path = file_name_str
        self.connect(menu_file_open_action,SIGNAL("triggered()"),get_open_file_name)
        menu_file.addAction(menu_file_open_action)

        menu_file_close_action = QAction(u"关闭",menu_file)
        #文件 > 关闭 绑定事件
        def close_open_file():
            self_inner.file_path = ""
            plt.plot()
        self.connect(menu_file_close_action, SIGNAL("triggered()"), close_open_file)
        menu_file.addAction(menu_file_close_action)

        menu_file.addSeparator()
        menu_file_exit_action = QAction(u"退出",menu_file)
        # 文件 > 退出 绑定事件
        def exit_program():
            sys.exit(0)
        self.connect(menu_file_exit_action, SIGNAL("triggered()"), exit_program)
        menu_file.addAction(menu_file_exit_action)



        # Todo 添加基础处理操作方法
        # 操作
        #  > 切分
        #  > 二值化
        #  > ...
        menu_operate = menubar.addMenu(u"操作")
        menu_operate_threshold = QAction(u"二值化",menu_file)
        def menu_operate_threshold_action():
            threshold_num,ok = QInputDialog.getInteger(self_inner,u"阈值",u"请输入阈值",75,1,255)
            data = Pic_proc.get_theshold_num_data(threshold_num,str(self_inner.file_path))
            ax.imshow(data)
            self_inner.canvas.draw()
        menu_operate.addAction(menu_operate_threshold)
        self.connect(menu_operate_threshold,SIGNAL("triggered()"),menu_operate_threshold_action)

        ##文本行切分
        menu_operate_xy_cut = QAction(u"xy投影切分", menu_file)
        def menu_operate_xy_cut_action():
            data = Pic_proc.xy_cut(unicode(self_inner.file_path))
            ax.imshow(data)
            self_inner.canvas.draw()
        menu_operate.addAction(menu_operate_xy_cut)
        self.connect(menu_operate_xy_cut, SIGNAL("triggered()"), menu_operate_xy_cut_action)




