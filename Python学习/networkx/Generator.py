import networkx as nx
import matplotlib.pyplot as plt

# 1. 应用经典的图操作，例如：
# subgraph（G，nbunch）                  返回在 nbunch 中的节点上诱导的子图。
# union（G，H[，重命名，名称]）             返回图 G 和 H 的并集。
# disjoint_union(G, H)                  返回图 G 和 H 的不相交并集。
# cartesian_product(G, H)               返回 G 和 H 的笛卡尔积。
# compose(G, H)                         返回由 H 组成的 G 的新图。
# complement（G）                        返回 G 的图补集。
# create_empty_copy(G[, with_data])     返回删除所有边的图 G 的副本。
# to_undirected（图形）                   返回图的无向视图graph。
# to_directed（图形）                     返回图形的有向视图graph。

# 2. 使用对经典小图之一的调用，例如，
# petersen_graph（[创建_使用]）             返回彼得森图。
# tutte_graph（[创建_使用]）                返回 Tutte 图。
# sedgewick_maze_graph（[创建_使用]）       返回一个带循环的小迷宫。
# tetrahedral_graph（[创建_使用]）          返回 3 正则柏拉图四面体图。

# 3. 为经典图使用（建设性）生成器，例如，
# complete_graph(n[, create_using])                 返回K_n具有 n 个节点的完整图。
# complete_bipartite_graph(n1, n2[, create_using])  返回完整的二分图K_{n_1,n_2}。
# barbell_graph(m1, m2[, create_using])             返回杠铃图：通过路径连接的两个完整图。
# lollipop_graph(m, n[, create_using])              返回棒棒糖图；K_m连接到P_n.

# 4. 使用随机图生成器，例如
# erdos_renyi_graph(n, p[, 种子, 定向])                 返回一个随机图，也称为 Erdős-Rényi 图或二项式图。
# watts_strogatz_graph(n, k, p[, 种子])                返回 Watts-Strogatz 小世界图。
# barabasi_albert_graph(n, m[, 种子, ...])             使用 Barabási–Albert 优先附件返回一个随机图
# random_lobster(n, p1, p2[, 种子])                    返回一个随机龙虾图。

G = nx.DiGraph()

# 一个图中的节点可以合并到另一个图中：
# H = nx.path_graph(10)
# G.add_nodes_from(H)
# G现在包含 的节点H作为 的节点G。相反，您可以将图形H用作 中的节点G。
# G.add_node(H)

# K_5 = nx.complete_graph(5)
# K_3_5 = nx.complete_bipartite_graph(3, 5)
# barbell = nx.barbell_graph(10, 10)
# lollipop = nx.lollipop_graph(10, 20)

# er = nx.erdos_renyi_graph(10, 0.1)        # G_{n,p}
# ws = nx.watts_strogatz_graph(30, 3, 0.1)    # Watts–Strogatz small-world graph.
# ba = nx.barabasi_albert_graph(10, 5)
red = nx.random_lobster(10, 0.9, 0.9)

print(red.nodes(data=True))
print(red.edges(data=True))
nx.draw_networkx(red, node_size=400)
plt.show()
