#coding:utf-8

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys

class MainWindow(QDialog):
    def __init__(self,parent=None):
        super(MainWindow, self).__init__()

        gridLayout = QGridLayout(self)
        self.btn_open_file = QPushButton(u"打开文件")
        gridLayout.addWidget(self.btn_open_file,0,0)
        self.label = QLabel(u"文件路径")
        gridLayout.addWidget(self.label,0,1)
        self.btn_info = QPushButton(u"信息")
        gridLayout.addWidget(self.btn_info,1,0)


        self.connect(self.btn_open_file,SIGNAL("clicked()"),self.openfile)
        self.connect(self.btn_info,SIGNAL("clicked()"),self.show_info)

    def openfile(self):
        s = QFileDialog.getOpenFileName(self, "Open file dialog", "/", u"图片文件(*.png *.bmp *.jpg);;文本文档(*.txt *.c)")
        if s != "":
            self.label.setText(s)

    def show_info(self):
        QMessageBox.information(self,u"信息标题",u"信息内容")
        QMessageBox.critical(self, u"信息标题", u"信息内容")
        s = QMessageBox.question(self, u"信息标题", u"信息内容",QMessageBox.Ok|QMessageBox.Cancel,QMessageBox.Ok)
        if s == QMessageBox.Ok:
            self.label.setText("OK")
        elif s == QMessageBox.Cancel:
            self.label.setText("Cancel")
        else:
            self.label.setText(u"未选择")


app = QApplication(sys.argv)
mainWindow = MainWindow()
mainWindow.show()
app.exec_()