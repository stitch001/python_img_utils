#coding:utf-8

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys

from Dui.MainWindow import MainWindow

reload(sys)
sys.setdefaultencoding('utf-8')
app = QApplication(sys.argv)
mainWindow = MainWindow()
mainWindow.show()
app.exec_()

