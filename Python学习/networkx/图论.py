import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()

G.add_edge('A', 'B', weight=4, cc=12)
G.add_edge('B', 'D', weight=2, cc=12)
G.add_edge('A', 'C', weight=3, cc=12)
G.add_edge('C', 'D', weight=5, cc=12)
G.add_edge('A', 'D', weight=6, cc=12)
G.add_edge('C', 'F', weight=7, cc=12)
G.add_edge('A', 'G', weight=1, cc=12)
G.add_edge('B', 'H', weight=2, cc=12)
G.add_edge('F', 'D', weight=2, cc=12)
G.add_edge('G', 'D', weight=3, cc=12)
G.add_edge('H', 'D', weight=1, cc=0)

for u, v, d in G.edges(data=True):
    print(u, v, d['weight'])
edge_labels = dict([((u, v,), d['weight']) for u, v, d, c in G.edges(data=True) if (c > 10)])
# fixed_position = {'A':[ 1.,  2.], 'B': [ 1.,  0.], 'D': [ 5., 5.], 'C': [ 0.,6.]} # 每个点在坐标轴中的位置
# pos=nx.spring_layout(G,pos = fixed_position)                                      # 获取结点的位置,每次点的位置都是随机的
# pos = nx.spring_layout(G)  # 也可以不固定点
# nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=14)  # 绘制图中边的权重
# nx.draw_networkx_edge_labels(G, edge_labels=edge_labels, font_size=14)  # 绘制图中边的权重
print("edge_labels:", edge_labels)
print("nodes:", G.nodes(data=True))             # 输出全部的节点：
print("edges:", G.edges(data=True))             # 输出全部的边：
print("number of edges:", G.number_of_edges())  # 输出边的数量

# 生成邻接矩阵
mat = nx.to_numpy_matrix(G)
print(mat)

# 计算两点间的最短路
# dijkstra_path
print('dijkstra方法寻找最短路径：')
path = nx.dijkstra_path(G, source='A', target='D')
print('节点A到D的路径：', path)
print('dijkstra方法寻找最短距离：')
distance = nx.dijkstra_path_length(G, source='A', target='D')
print('节点A到D的距离为：', distance)

# 一点到所有点的最短路
p = nx.shortest_path(G, source='A', method="dijkstra")  # target not specified # method='bellman-ford'.
d = nx.shortest_path_length(G, source='A', method="dijkstra")
for node in G.nodes():
    print("A 到", node, "的最短路径为:", p[node])
    print("A 到", node, "的最短距离为:", d[node])

# 所有点到一点的最短距离
p = nx.shortest_path(G, target='D')  # target not specified
d = nx.shortest_path_length(G, target='D')
for node in G.nodes():
    print(node, "到 D 的最短路径为:", p[node])
    print(node, "到 D 的最短距离为:", d[node])

"""
# 任意两点间的最短距离
p = nx.shortest_path_length(G)
p = dict(p)
d = nx.shortest_path_length(G)
d = dict(d)
for node1 in G.nodes():
    for node2 in G.nodes():
        print(node1, "到", node2, "的最短距离为:", d[node1][node2])
"""

"""
# 最小生成树
T = nx.minimum_spanning_tree(G)  # 边有权重 无向图
print(sorted(T.edges(data=True)))
mst = nx.minimum_spanning_edges(G, data=False)  # a generator of MST edges
edgelist = list(mst)  # make a list of the edges
print(sorted(edgelist))
"""

# 使用A *算法的最短路径和路径长度
p = nx.astar_path(G, source='A', target='D')
print('节点H到F的路径：', path)
d = nx.astar_path_length(G, source='A', target='D')
print('节点H到F的距离为：', distance)

# 找回路
hl = nx.algorithms.find_cycle(G, orientation='ignore')
print('回路包括：', hl)

"""
# 二分图匹配
G = nx.complete_bipartite_graph(2, 3)
nx.draw_networkx(G)
left, right = nx.bipartite.sets(G)
list(left)  # [0, 1]
list(right)  # [2, 3, 4]
p = nx.bipartite.maximum_matching(G)
print("输出匹配：", p)
"""

"""
# 最大流
# graph's maximum flow
# flow is computed between vertex 0 and vertex n-1
# expected input format:    # n # m
# g = nx.DiGraph()
# n, m = int(input()), int(input())
# for i in range(n):
#    g.add_node(i)
# for _ in range(m):
#    a, b, c = [ int(i) for i in input().split(' ') ]
#    g.add_edge(a, b, capacity=c)
# max_flow = nx.algorithms.flow.maxflow.maximum_flow(g, 0, n-1)[0]
# print(max_flow)
g = nx.DiGraph()
n, m = 4, 5
for i in range(n):
    g.add_node(i)
edge = ["0 1 3", "1 3 2", "0 2 2", "2 3 3", "0 3 1"]
for x in edge:
    a, b, c = [int(i) for i in x.split(' ')]
    g.add_edge(a, b, capacity=c)
nx.draw(g)
max_flow = nx.algorithms.flow.maxflow.maximum_flow(g, 0, n - 1)[0]
print('最大流：', max_flow)
"""

nx.draw_networkx(G, node_size=400)
plt.savefig("DAG.png")
plt.show()
