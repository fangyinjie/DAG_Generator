# -*- coding: utf-8 -*-
# 5.4 发出信号
# 通过QObject创建的对象可以发出信号。下面的示例演示了如何发出自定义信号
# 当在窗体上点击鼠标时会触发closeApp信号，使程序退出。
"""
PyQt5 tutorial

In this example, we determine the event sender
object.

author: py40.com
last edited: 2017年3月
"""

import sys
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QMainWindow, QApplication


# 我们创建了一个名为closeApp的信号。这个信号会在按下鼠标时触发，它连接着QMainWindow的close()插槽。
class Communicate(QObject):
    closeApp = pyqtSignal()


class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # 信号closeApp是Communicate的类属性，它由pyqtSignal()创建。
        self.c = Communicate()
        self.c.closeApp.connect(self.close)

        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Emit signal')
        self.show()

    # 自定义closeApp信号连接到QMainWindow的close槽
    def mousePressEvent(self, event):
        self.c.closeApp.emit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())