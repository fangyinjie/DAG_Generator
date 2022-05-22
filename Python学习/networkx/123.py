import matplotlib.pyplot as plt
import numpy as np
x=["q","w","e","r","t","y"]#不变的依然是x表示标签值
y=[4,6,7,6,3,9]
plt.barh(x,y,align="center",color="green",alpha=0.6,label="barh")
box=dict(fc="red",pad=2,alpha=0.4)
#给坐标轴的标签加上文本框,就是使用bbox函数
plt.xlabel("xaxis",bbox=box)
plt.ylabel("ylabel",bbox=dict(fc="green",ec="black",pad=2,alpha=0.5))
plt.grid(True,color="red",ls="-.",axis="y")#axis表示值显示哪个轴的虚线
plt.legend()
"""
plt.text(0.8, 0.5, "python", size=50, rotation=0.,
         ha="center", va="center",
         bbox=dict(boxstyle="round",
                   ec=(1., 0.5, 0.5),
                   fc=(1., 0.8, 0.8),
                   )
         )
         """
plt.text(0, 0, "beijing", fontsize=50, color="r", style="italic", weight="light",
         verticalalignment='bottom', horizontalalignment='left', rotation=0)
"""
plt.text(0.75, 0.6, "www.jb51.net", size=50, rotation=-30.,
         ha="right", va="top",
         bbox=dict(boxstyle="square",
                   ec=(1., 0.5, 0.5),
                   fc=(1., 0.8, 0.8),
                   )
         )

"""
# n_pos = dict(zip(node_map, np.array(position_map)))         # 构建pos列表
# n_color = dict(zip(node_map, np.array(color_map)))          # 构建color列表
# nx.draw(G.get_graph(), pos=position_map, node_color=color_map, node_size=1000, node_shape='o',
#        with_labels=True)
plt.draw()
plt.show()


