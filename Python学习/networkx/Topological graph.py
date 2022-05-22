import networkx as nx
import matplotlib.pyplot as plt

# 简单例子
# G = nx.Graph()
# G.add_node('Hamburg', pos=(10, 10))
# G.add_node('Berlin', pos=(10, 20))
# nx.draw(G, nx.get_node_attributes(G, 'pos'), with_labels=True, node_size=0)
# plt.show()

nodes = ['A',    'B',    'C',    'D',    'E',    'F',    'G']

G = nx.Graph()      # 图
# G=nx.DiGraph()    # 有向图
# G=nx.MultiGraph() #

for node in nodes:
    G.add_node(node)

edges = [('A', 'B'),    ('A', 'C'),    ('B', 'C'),    ('D', 'B'),
         ('B', 'D'),    ('D', 'C'),    ('E', 'B'),    ('E', 'A'),
         ('F', 'B'),    ('F', 'A'),    ('G', 'C'),    ('G', 'A')]

r = G.add_edges_from(edges)

# 计算最短路径。
shortest_way = nx.shortest_path(G, "F", "D")
print(shortest_way)

nx.draw(G, with_labels=True, node_color='y', )
plt.show()