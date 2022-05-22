# -*- coding: utf-8 -*-
# 6.1 QCheckBox
# QCheckBox复选框控件，它有两个状态:打开和关闭，他是一个带有文本标签（Label）的控件。复选框常用于表示程序中可以启用或禁用的功能。
# 复选框的状态经由state参数传入changeTitle()方法。在勾选复选框时设置窗体标题，取消勾选时就将标题设为空字符串。
"""
PyQt5 tutorial

In this example, we determine the event sender
object.

author: py40.com
last edited: 2017年3月
"""
import sys
from PyQt5.QtWidgets import QWidget, QCheckBox, QApplication
from PyQt5.QtCore import Qt


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # 在我们的示例中,我们将创建一个复选框,将切换窗口标题。
        cb = QCheckBox('Show title', self)
        cb.move(20, 20)
        # 这是QCheckBox的构造行数
        cb.toggle()
        # 我们有设置窗口标题, 所以我们也必须检查复选框。默认情况下, 没有设置窗口标题和也没有勾选复选框。
        cb.stateChanged.connect(self.changeTitle)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('QCheckBox')
        self.show()

    # 我们将自定义的changeTitle()方法连接到stateChanged信号。这个方法会切换窗体的标题。
    def changeTitle(self, state):

        if state == Qt.Checked:
            self.setWindowTitle('QCheckBox')
        else:
            self.setWindowTitle('')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())