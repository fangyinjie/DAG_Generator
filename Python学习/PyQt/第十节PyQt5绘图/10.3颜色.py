# -*- coding: utf-8 -*-
# 10.3颜色
# 颜色是一个对象代表红、绿、蓝(RGB)强度值。
# 有效的RGB值的范围从0到255。
# 我们可以用不同的方法定义了一个颜色。
# 最常见的是RGB十进制或十六进制值的值。
# 我们也可以使用一个RGBA值代表红色,绿色,蓝色,透明度。
# 我们添加一些额外的信息透明度。
# 透明度值255定义了完全不透明,0是完全透明的,例如颜色是无形的。

# 我们为QPainter设置了一个笔刷(Bursh)对象并用它绘制了一个矩形。
# 笔刷是用于绘制形状背景的基本图形对象。drawRect()方法接受四个参数，前两个是起点的x,y坐标，后两个是矩形的宽和高。
# 这个方法使用当前的画笔与笔刷对象进行绘制。
"""
PyQt5 tutorial

This example draws three rectangles in three
#different colours.

author: py40.com
last edited: 2017年3月
"""
import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QBrush


class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 350, 100)
        self.setWindowTitle('Colours')
        self.show()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawRectangles(qp)
        qp.end()

    def drawRectangles(self, qp):
        # 实例中我们绘制了3个不同颜色的矩形；
        col = QColor(0, 0, 0)
        col.setNamedColor('#d4d4d4')
        qp.setPen(col)

        # 在这里,我们定义一个使用十六进制符号颜色。
        qp.setBrush(QColor(200, 0, 0))
        qp.drawRect(10, 15, 90, 60)

        qp.setBrush(QColor(255, 80, 0, 160))
        qp.drawRect(130, 15, 90, 60)

        qp.setBrush(QColor(25, 0, 90, 200))
        qp.drawRect(250, 15, 90, 60)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())