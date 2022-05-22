# -*- coding: utf-8 -*-
# 8.2 文本框 QLineEdit
# QLineEdit是用于输入或编辑单行文本的控件。它还有撤销重做、剪切复制和拖拽功能。
# 在onChanged()方法中我们将QLabel控件的文本设置为输入的内容。通过调用adjustSize()方法将QLabel控件的尺寸调整为文本的长度。
"""
PyQt5 tutorial

This example shows text which
is entered in a QLineEdit
in a QLabel widget.

author: py40.com
last edited: 2017年3月
"""
import sys
from PyQt5.QtWidgets import (QWidget, QLabel,
                             QLineEdit, QApplication)


class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.lbl = QLabel(self)
        qle = QLineEdit(self)   # 示例中展示了一个QLineEdit与一个QLabel。我们在QLineEdit中输入的文字会实时显示在QLabel控件中。

        qle.move(60, 100)
        self.lbl.move(60, 40)

        qle.textChanged[str].connect(self.onChanged)  # 创建QLineEdit

        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('QLineEdit')
        self.show()

    # 文本框的内容发生改变的时候，会调用onChanged方法
    def onChanged(self, text):
        self.lbl.setText(text)
        self.lbl.adjustSize()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())