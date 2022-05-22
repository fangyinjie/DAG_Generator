# -*- coding: utf-8 -*-
# 9.1 简单拖放
# 在第一个示例中,我们有一个QLineEdit QPushButton。我们拖着纯文本的行编辑窗口小部件,然后放到按钮部件。按钮的标签会改变。
# QLineEdit内置了对drag(拖动)操作的支持。我们只需要调用setDragEnabled()方法就可以了。
"""
PyQt5 tutorial

This is a simple drag and
drop example.

author: py40.com
last edited: 2017年3月
"""
import sys
from PyQt5.QtWidgets import (QPushButton, QWidget,
                             QLineEdit, QApplication)

# 这个列子演示了一个简单的拖拽操作
class Button(QPushButton):
    def __init__(self, title, parent):
        super().__init__(title, parent)

        # 我们需要重新实现某些方法才能使QPushButton接受拖放操作。因此我们创建了继承自QPushButton的Button类。
        self.setAcceptDrops(True)

    # 使该控件接受drop(放下)事件。
    def dragEnterEvent(self, e):

        if e.mimeData().hasFormat('text/plain'):
            e.accept()
        else:
            e.ignore()

    # 首先我们重新实现了dragEnterEvent()方法，并设置可接受的数据类型(在这里是普通文本)。
    def dropEvent(self, e):

        self.setText(e.mimeData().text())


class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # 通过重新实现dropEvent()方法，我们定义了在drop事件发生时的行为。这里我们改变了按钮的文字。
        edit = QLineEdit('', self)
        edit.setDragEnabled(True)
        edit.move(30, 65)

        button = Button("Button", self)
        button.move(190, 65)

        self.setWindowTitle('Simple drag & drop')
        self.setGeometry(300, 300, 300, 150)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    app.exec_()