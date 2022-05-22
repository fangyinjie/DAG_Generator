# -*- coding: utf-8 -*-
# QPixmap
# QPixmap是用于处理图像的控件。是优化的显示图像在屏幕上。在我们的代码示例中,我们将使用QPixmap窗口显示一个图像。
# 我们将这个pixmap放到QLabel控件中。
"""
PyQt5 tutorial

In this example, we dispay an image
on the window.

author: py40.com
last edited: 2017年3月
"""
import sys
from PyQt5.QtWidgets import (QWidget, QHBoxLayout,
                             QLabel, QApplication)
from PyQt5.QtGui import QPixmap


class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        hbox = QHBoxLayout(self)
        # 在窗口上显示一个图片
        pixmap = QPixmap("icon.png")

        # 创建一个QPixmap 对象，它将传入的文件名作为参数。
        lbl = QLabel(self)
        lbl.setPixmap(pixmap)

        hbox.addWidget(lbl)
        self.setLayout(hbox)

        self.move(300, 200)
        self.setWindowTitle('Red Rock')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())