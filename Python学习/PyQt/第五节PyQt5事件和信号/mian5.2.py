#!/usr/bin/python3
# -*- coding: utf-8 -*-
# 5.2 重新实现事件处理器
# 在PyQt5中常通过重新实现事件处理器来处理事件。
# 我们按下Escape(esc)键会使程序退出。
"""
pyu40 PyQt5 tutorial

In this example, we reimplement an
event handler.

author: Jan Bodnar
website: py40.com
last edited: January 2015
"""

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Event handler')
        self.show()

    # 在示例中我们重新实现了keyPressEvent()事件处理器。
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())