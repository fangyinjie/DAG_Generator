# -*- coding: utf-8 -*-
# 11 PyQt5自定义控件
# PyQt5包含种类丰富的控件。但能满足所有需求的控件库是不存在的。
# 通常控件库只提供了像按钮、文本控件、滑块等最常用的控件。
# 但如果需要某种特殊的控件，我们只能自己动手来实现。
# 自定义控件需要使用工具库提供的绘图工具，可能有两种方式：
#       在已有的控件上进行拓展或从头开始创建自定义控件。
# 11.1 Burning widget(烧录控件)
# 这个控件可能会在Nero，K3B或其他CD/DVD烧录软件中见到。

# 当滑块发生移动时，changeValue()方法会被调用。
# 在方法内我们触发了一个自定义的updateBW信号，其参数是当前滚动条的值。
# 该值被用于计算Burning widget的容量值。然后对控件进行重绘。
"""
PyQt5 tutorial

In this example, we create a custom widget.

author: py40.com
last edited: 2017年3月
"""
import sys
from PyQt5.QtWidgets import (QWidget, QSlider, QApplication,
                             QHBoxLayout, QVBoxLayout)
from PyQt5.QtCore import QObject, Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QFont, QColor, QPen


class Communicate(QObject):
    updateBW = pyqtSignal(int)


# 在示例中我们使用了滑块与一个自定义控件。自定义控件受滑块控制。控件显示了媒体介质的容量和剩余空间。
# 该控件的最小值为1,最大值为750。在值超过700时颜色变为红色。
# 这通常意味着超刻(即实际写入光盘的容量超过刻录盘片官方标称容量的一种操作)。

# BurningWidget控件通过QHBoxLayout与QVBoxLayout置于窗体的底部。
class BurningWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        # 烧录的控件,它基于QWidget
        self.setMinimumSize(1, 30)
        self.value = 75
        self.num = [75, 150, 225, 300, 375, 450, 525, 600, 675]

    def setValue(self, value):

        self.value = value

    def paintEvent(self, e):

        qp = QPainter()
        qp.begin(self)
        self.drawWidget(qp)
        qp.end()

    def drawWidget(self, qp):

        # 我们改变了控件的最小大小(高度),默认值为有点小。
        font = QFont('Serif', 7, QFont.Light)
        qp.setFont(font)

        # 我们使用一个比默认要小的字体。
        size = self.size()
        w = size.width()
        h = size.height()

        step = int(round(w / 10.0))

        till = int(((w / 750.0) * self.value))
        full = int(((w / 750.0) * 700))

        if self.value >= 700:

            qp.setPen(QColor(255, 255, 255))
            qp.setBrush(QColor(255, 255, 184))
            qp.drawRect(0, 0, full, h)
            qp.setPen(QColor(255, 175, 175))
            qp.setBrush(QColor(255, 175, 175))
            qp.drawRect(full, 0, till - full, h)

        else:

            qp.setPen(QColor(255, 255, 255))
            qp.setBrush(QColor(255, 255, 184))
            qp.drawRect(0, 0, till, h)

        pen = QPen(QColor(20, 20, 20), 1,
                   Qt.SolidLine)

        qp.setPen(pen)
        qp.setBrush(Qt.NoBrush)
        qp.drawRect(0, 0, w - 1, h - 1)

        j = 0

        for i in range(step, 10 * step, step):
            qp.drawLine(i, 0, i, 5)
            # 控件采用了动态绘制技术。窗体越大，控件也随之变大；反之亦然。这也是我们需要计算自定义控件的载体控件(即窗体)尺寸的原因。
            # till参数定义了需要绘制的总尺寸，它根据slider控件计算得出，是整体区域的比例值。
            # full参数定义了红色区域的绘制起点。注意在绘制时为取得较大精度而使用的浮点数运算。

            # 实际的绘制分三个步骤。黄色或红黄矩形的绘制，然后是刻度线的绘制，最后是刻度值的绘制。
            metrics = qp.fontMetrics()
            fw = metrics.width(str(self.num[j]))
            qp.drawText(i - fw / 2, h / 2, str(self.num[j]))
            j = j + 1


class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        sld = QSlider(Qt.Horizontal, self)
        sld.setFocusPolicy(Qt.NoFocus)
        sld.setRange(1, 750)
        sld.setValue(75)
        sld.setGeometry(30, 40, 150, 30)

        self.c = Communicate()
        self.wid = BurningWidget()
        self.c.updateBW[int].connect(self.wid.setValue)

        sld.valueChanged[int].connect(self.changeValue)
        hbox = QHBoxLayout()
        hbox.addWidget(self.wid)
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        self.setGeometry(300, 300, 390, 210)
        self.setWindowTitle('Burning widget')
        self.show()

    # 我们使用字体度量来绘制文本。我们必须知道文本的宽度,以中心垂直线。
    def changeValue(self, value):
        self.c.updateBW.emit(value)
        self.wid.repaint()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())