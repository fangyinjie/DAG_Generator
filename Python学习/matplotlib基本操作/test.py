import matplotlib.pyplot as plt
import numpy as np

# 1.1 Figure
# 在任何绘图之前，我们需要一个Figure对象，可以理解成我们需要一张画板才能开始绘图。
fig = plt.figure()

# 1.2 Axes
# 作画还需要轴，没有轴的话就没有绘图基准，所以需要添加Axes。也可以理解成为真正可以作画的纸。
ax1 = fig.add_subplot(221)  # 两行两列中的第一行第一列
ax2 = fig.add_subplot(222)  # 两行两列中的第一行第二列
ax3 = fig.add_subplot(212)  # 两行一列中的第二行第一列

ax1.set(xlim=[0.5, 4.5],            # x轴的区间
        ylim=[-2, 8],               # y轴的区间
        title='An Example Axes',    # 图的名字
        ylabel='Y-Axis',            # y轴坐标
        xlabel='X-Axis')            # x轴坐标

# 1.3 Multiple Axes
# 可以发现我们上面添加 Axes 似乎有点弱鸡，所以提供了下面的方式一次性生成所有 Axes：
fig, axes = plt.subplots(nrows=2, ncols=2)
axes[0, 0].set(title='Upper Left')
axes[0, 1].set(title='Upper Right')
axes[1, 0].set(title='Lower Left')
axes[1, 1].set(title='Lower Right')

# 1.4 Axes Vs .pyplot
# 下面的作画方式适合简单的绘图，快速的将图绘出。在处理复杂的绘图工作时，还是需要使用 Axes 来完成作画的。

plt.plot([1, 2, 3, 4], [10, 20, 25, 30], color='lightblue', linewidth=3)        # 绘制线
plt.xlim(0.5, 4.5)      # plt.xlim(xmin, xmax) xmin：x轴上的最小值 x轴上的最大值
plt.ylim(10.0, 50)      # plt.ylim(ymin, ymax) ymin：y轴上的最小值 x轴上的最大值
plt.show()