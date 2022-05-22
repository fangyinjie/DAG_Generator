# -*- coding: utf-8 -*-
# 6.3滑动条 QSlider
# QSlider是一个带有简单滑块的控件。滑块可以前后拖动。我们可以通过拖动选择一个特定的值。有时使用滑动条比直接输入数字或使用旋转框更加自然。
# 在下面的例子中，我们会显示一个滑动条与一个标签，标签用于显示图片，并通过滑动条控件图片的显示 。
# 注意这里图片只能用ico格式的，png格式图片会显示不了。
# 创建一个水平滑块
"""
PyQt5 tutorial

This example shows a QSlider widget.

author: py40.com
last edited: 2017年3月
"""
import sys
from PyQt5.QtWidgets import (QWidget, QSlider,
                             QLabel, QApplication)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        # 例子中我们模拟了一个音量控制。通过拖动滑块来改变标签上的图像。
        sld = QSlider(Qt.Horizontal, self)
        sld.setFocusPolicy(Qt.NoFocus)
        sld.setGeometry(30, 40, 100, 30)
        sld.valueChanged[int].connect(self.changeValue)  # 创建了一个QLabel控件并为它设置了一个初始音量图像。

        self.label = QLabel(self)
        self.label.setPixmap(QPixmap('audio.ico'))
        self.label.setGeometry(160, 40, 80, 30)

        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('QSlider')
        self.show()

    def changeValue(self, value):

        # 我们将valueChanged信号连接到自定义的changeValue()方法。
        # 我们根据滑动条的值来设置标签的图像。在上面的代码中，当滑动条的值为0时我们为标签设置audio.ico图像。
        if value == 0:
            self.label.setPixmap(QPixmap('audio.ico'))
        elif value > 0 and value <= 30:
            self.label.setPixmap(QPixmap('min.ico'))
        elif value > 30 and value < 80:
            self.label.setPixmap(QPixmap('med.ico'))
        else:
            self.label.setPixmap(QPixmap('max.ico'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())