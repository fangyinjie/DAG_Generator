# -*- coding: utf-8 -*-
"""
@File    : test.py
@Time    : 2020/5/26 18:09
@Author  : Dontla
@Email   : sxana@qq.com
@Software: PyCharm
"""
from matplotlib import pyplot as plt  # 用来绘制图形
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

X1 = X2 = np.arange(-5, 15, 1)
X1, X2 = np.meshgrid(X1, X2)

Z = 1 / 2 * X1 ** 2

# 绘制三维图初始角度
azim = -60
elev = 30

# 创建绘制实时损失的动态窗口
plt.ion()
for i in range(30000):
    plt.clf()  # 清除之前画的图
    fig = plt.gcf()  # 获取当前图
    ax = fig.gca(projection='3d')  # 获取当前轴

    ax.view_init(elev, azim)  # 设定角度

    ax.plot_surface(X1, X2, Z, cmap='rainbow')
    plt.pause(0.001)  # 暂停一段时间，不然画的太快会卡住显示不出来

    elev, azim = ax.elev, ax.azim  # 将当前绘制的三维图角度记录下来，用于下一次绘制（放在ioff()函数前后都可以，但放在其他地方就不行）
    # elev, azim = ax.elev, ax.azim - 1 # 可自动旋转角度，不需要人去拖动

    plt.ioff()  # 关闭画图窗口Z

    Z = Z - X1 + 2 * X2  # 变换Z值

# 加这个的目的是绘制完后不让窗口关闭
plt.show()

