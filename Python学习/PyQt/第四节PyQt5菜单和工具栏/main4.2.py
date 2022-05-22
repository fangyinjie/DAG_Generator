#!/usr/bin/python3
# -*- coding: utf-8 -*-
# 4.2 状态栏
# 状态栏用于显示状态信息。

"""
Py40 PyQt5 tutorial

This program creates a statusbar.

author: Jan Bodnar
website: py40.com
last edited: January 2015
"""

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication


class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.statusBar().showMessage('Ready')  # 你用QMainWindow创建状态栏的小窗口。
        # QMainWindow类第一次调用statusBar()方法创建一个状态栏。后续调用返回的状态栏对象。showMessage()状态栏上显示一条消息。

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Statusbar')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())