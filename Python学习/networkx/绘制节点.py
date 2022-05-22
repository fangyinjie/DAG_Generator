import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

plt.figure()                #(figsize=(10.0, 10.0))
G = nx.Graph()              # 创建一个空的无向图
num = 6                     # 节点的个数
nodes = list(range(num))    # [0,1,2,3,4,5]
G.add_nodes_from(nodes)     # 将节点添加到网络中
edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)]
G.add_edges_from(edges)     # 将所有边加入网络
# 每个节点对应坐标坐标
coordinates = [[1, 2], [2, 2], [3, 2], [3, 1], [2, 1], [1, 1]]
# 可导入自己所需的数据            # np.loadtxt()
v_node = np.array(coordinates)
n_pos = dict(zip(nodes, v_node))    # 获取节点与坐标之间的映射关系，用字典表示(节点号，（节点坐标）)
n_labels = dict(zip(nodes, nodes))  # 标志字典，构建节点与标识点之间的关系(节点号，节点号)
nx.draw_networkx_nodes(G, n_pos, node_size=400, node_color="#6CB6FF")   # 绘制节点
nx.draw_networkx_edges(G, n_pos, edges)                                 # 绘制边
nx.draw_networkx_labels(G, n_pos, n_labels)                             # 标签

# 若显示多个图，可将所有节点放入该列表中
# pos = {}
# pos.update(n_pos)
# nx.draw_networkx_nodes(G, pos,
#   nodelist=None,
#   node_size=300,
#   node_color='r',
#   node_shape='o',
#   alpha=1.0,
#   cmap=None,
#   vmin=None,
#   vmax=None,
#   ax=None,
#   linewidths=None,
#   label=None,**kwds):


# 在任何绘图之前，我们需要一个Figure对象，可以理解成我们需要一张画板才能开始绘图。
# plt.figure()


# ax1 = fig.add_subplot(111)  # 1行1列中的第一个（行+行*列）
# ax1.set(xlim=[0.5, 4.5],            # x轴的区间
#         ylim=[-2, 8],               # y轴的区间
#         title='An Example Axes',    # 图的名字
#         ylabel='Y-Axis',            # y轴坐标
#         xlabel='X-Axis')            # x轴坐标

x_max, y_max    = v_node.max(axis=0)           # 获取每一列的最大值，axis=1表示每一行的最大值
x_min, y_min    = v_node.min(axis=0)           # 获取每一列最小值
x_num           = (x_max - x_min) / 10
y_num           = (y_max - y_min) / 10
# print(x_max, y_max, x_min, y_min)
# plt.xlim(x_min - x_num, x_max + x_num)           # plt.xlim(xmin, xmax) xmin：x轴上的最小值 x轴上的最大值
# plt.ylim(y_min - y_num, y_max + y_num)
plt.title('DAG generator\n'+
            'beijing',fontsize=10, color="r", style="italic", weight="light",)
plt.xlabel('crirical')
plt.ylabel('param')

plt.show()
