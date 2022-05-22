# -*- coding: utf-8 -*-
# 10.1 绘制文本
# 我们先以窗体内Unicode文本的绘制为例。
# drawText()方法将文本绘制在窗体，显示在中心
"""
PyQt5 tutorial

In this example, we draw text in Russian azbuka.

author: py40.com
last edited: 2017年3月
"""
import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt


class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.text = u'\u041b\u0435\u0432 \u041d\u0438\u043a\u043e\u043b\u0430\
\u0435\u0432\u0438\u0447 \u0422\u043e\u043b\u0441\u0442\u043e\u0439: \n\
\u0410\u043d\u043d\u0430 \u041a\u0430\u0440\u0435\u043d\u0438\u043d\u0430'

        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('Draw text')
        self.show()

    # 在我们的示例中,我们绘制一些Cylliric文本。文本垂直和水平对齐。
    def paintEvent(self, event):
        # 绘制工作在paintEvent的方法内部完成。
        qp = QPainter()
        qp.begin(self)
        self.drawText(event, qp)
        qp.end()

    def drawText(self, event, qp):
        # QPainter类负责所有的初级绘制。之间的所有绘画方法去start()和end()方法。实际的绘画被委托给drawText()方法。
        qp.setPen(QColor(168, 34, 3))
        qp.setFont(QFont('Decorative', 10))
        # 在这里, 我们定义一个画笔和一个字体用于绘制文本。
        qp.drawText(event.rect(), Qt.AlignCenter, self.text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())