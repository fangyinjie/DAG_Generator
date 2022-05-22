# -*- coding: utf-8 -*-
# 6.5 日历控件 QCalendarWidget
# QCalendarWidget提供了一个基于月份的日历控件。它使用户以一种简单直观的方式来选择日期。
# 我们检索所选日期通过调用selectedDate()方法。然后我们将date对象转换为字符串,并将其设置为小部件的标签。
"""
PyQt5 tutorial

This example shows a QCalendarWidget widget.

author: py40.com
last edited: 2017年3月
"""
import sys
from PyQt5.QtWidgets import (QWidget, QCalendarWidget,
                             QLabel, QApplication)
from PyQt5.QtCore import QDate


class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # QCalendarWidget提供了一个基于月份的日历控件。它使用户以一种简单直观的方式来选择日期。
        cal = QCalendarWidget(self)
        cal.setGridVisible(True)
        cal.move(20, 20)
        cal.clicked[QDate].connect(self.showDate)   # QCalendarWidget被创建

        self.lbl = QLabel(self)
        date = cal.selectedDate()
        self.lbl.setText(date.toString())
        self.lbl.move(130, 260)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Calendar')
        self.show()

    # 如果我们从部件选择一个日期,点击[QDate]发出信号。我们将这个信号连接到用户定义的showDate()方法。
    def showDate(self, date):
        self.lbl.setText(date.toString())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())