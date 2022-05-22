#!/usr/bin/python3
# -*- coding: utf-8 -*-
# 5.1 信号槽 Signals & slots
# 这个例子中展示了一个QtGui.QLCDNumber和QtGui.QSlider。lcd的值会随着滑块的拖动而改变
# 在这里我们将滚动条的valueChanged信号连接到lcd的display插槽。
# sender是发出信号的对象。receiver是接收信号的对象。slot(插槽)是对信号做出反应的方法。
"""
Py40 PyQt5 tutorial

In this example, we connect a signal
of a QSlider to a slot of a QLCDNumber.

author: Jan Bodnar
website: py40.com
last edited: January 2015
"""

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QLCDNumber, QSlider,
                             QVBoxLayout, QApplication)


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        lcd = QLCDNumber(self)
        sld = QSlider(Qt.Horizontal, self)

        vbox = QVBoxLayout()
        vbox.addWidget(lcd)
        vbox.addWidget(sld)

        self.setLayout(vbox)
        sld.valueChanged.connect(lcd.display)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Signal & slot')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())