#!/usr/bin/python3
# -*- coding: utf-8 -*-
# 3.2 框布局
# 使用QHBoxLayout和QVBoxLayout，来分别创建横向布局和纵向布局。
# 在这个例子中，我们使用HBoxLayout和QVBoxLayout并添加伸展因子，在窗口的右下角显示两个按钮。
"""
Py40 PyQt5 tutorial

In this example, we position two push
buttons in the bottom-right corner
of the window.

author: Jan Bodnar
website: py40.com
last edited: January 2015
"""

import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QHBoxLayout, QVBoxLayout, QApplication)


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        okButton = QPushButton("OK")
        cancelButton = QPushButton("Cancel")

        # 建立一个OK的按钮
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(okButton)
        hbox.addWidget(cancelButton)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox) # 创建一个垂直布局，并添加伸展因子，让水平布局显示在窗口底部

        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Buttons')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())