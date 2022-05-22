import networkx as nx
import matplotlib.pyplot as plt

if __name__ == "__main__":
    G = nx.DiGraph()    # 创建空的有向图
    # G = nx.Graph()  # 创建空的无向图
# 一 图的顶点
# 向图中增加顶点
# g.nodes(data=True)的data参数设置为true，获得图的所有顶点的视图，那么返回的是NodeDataView对象，该对象不仅包含每个顶点的ID属性，还包括顶点的其他属性。
# 在向图中添加顶点时，除ID属性之外，也可以向顶点中增加自定义的属性，例如，名称属性，权重属性：
    G.add_node(5)
    G.add_nodes_from([3, 4, 6])
    G.add_node(1, name='n1', weight=1)
    G.add_node(2, name='n2', weight=1.2)
    print(G.nodes(data=True))
    print(G.node[1])
    l1 = list(G.nodes(data=True))
    print(l1)
# 删除顶点:remove()，删除顶点通过传递ID属性作为参数。
    # g_1.remove_node(node_ID)
    # g_1.remove_nodes_from(nodes_list)
# 更新顶点属性
    G.node[1]['name'] = 'n1_new'
# 删除顶点的属性
    del G.nodes[1]['name']
    print(G.nodes(data=True))
# 检查顶点是否存在:检查一个顶点是否存在于图中
    print(G.has_node(1))
# 二 图的边：表一般具有：权重weight属性；关系类型属性。
# 向图中增加边：例如，顶点2和3之间有一条边，记作e=(2,3)，通过add_edge(node1,node2)向图中添加一条边，
# 也可以通过add_edges_from(list)向图中添加多条边；在添加边时，如果顶点不存在，那么networkx会自动把相应的顶点加入到图中。
# 可以向边中增加属性，例如，权重，关系等：
    G.add_edge(2, 3)
    G.add_edge(1, 2, weight=4.7, relationship='renew')
    G.add_edges_from([(1, 2), (1, 3)])
# 在增加边时，也可以一次增加多条边，为不同的边设置不同的属性：
    G.add_edges_from([(1, 2, {'color': 'blue'}),
                      (2, 3, {'weight': 8})])
# 该函数的参数是三元组，前两个字段是顶点的ID属性，用于标识一个边，第三个字段是边的权重：
    G.add_weighted_edges_from([(1, 2, 0.125),
                               (1, 3, 0.75),
                               (2, 4, 1.2),
                               (3, 4, 0.375)])
# 查看边的属性：即查看边的数据(data)，查看所有边及其属性：
# g_1.edges(data=True)
    print(G.get_edge_data(1, 2))
# 删除边
    G.remove_edge(1, 2)
    # g_1.remove_edges_from(edges_list)
# 更新边的属性，有两种方式，一种是使用update函数，一种是通过属性赋值来实现：
    # g_1[1][2]['weight'] = 4.7                            # (1)
    # g_1.edge[1][2]['weight'] = 4                         # (2)
    # g_1[1][2].update({"weight": 4.7})                    # (3)
    # g_1.edges[1, 2].update({"weight": 4.7})              # (4)
# 删除边的属性：通过 del命令来删除边的属性
    del G[1][3]['weight']
    print(G.edges(data=True))
# 检查边是否存在:检查一条边是否存在于图中
    print(G.has_edge(1, 3))
# 三，图的属性：图的属性主要是指相邻数据，节点和边。
# 1，adj： adj返回的是一个AdjacencyView视图，该视图是顶点的相邻的顶点和顶点的属性，
# 用于显示用于存储与顶点相邻的顶点的数据，是一个只读的字典结构，
# Key是顶点，Value是顶点的属性数据。
    print(G.adj[2][3])
    print(G.adj[2])       # 直接后继节点（）
# 2，edges: 图的边是由边的两个顶点唯一确定的，边还有一定的属性，因此，边是由两个顶点和边的属性构成的：
    print(G.edges)            # 返回边的信息,EdgeView仅提供边的信息，可以通过g.edges()来获得图的边视图。
    print(G.edges.data())     # 返回边的信息与属性,EdgeDataView提供图的边和边的属性，可以通过EdgeView对象来调用data()函数获得。
# 3，nodes：图的顶点是顶点和顶点的属性构成的
    print(G.nodes())          # NodeView 通过属性g.nodes或函数g.nodes()来获得。
    print(G.nodes.data())     # NodeDataView提供图的边和边的属性，可以通过NodeView对象来调用data()函数获得。
# 4，degree：
    print('123')
    print(G.in_degree)        # G的入度
    print(G.out_degree)       # G的出度
    print(G.degree)           # G的度
# 四，图的遍历:   通常分为深度优先搜索（DFS）和广度优先搜索（BFS）两种方式。
# 1，查看顶点的相邻顶点
# 查看顶点的相邻顶点，有多种方式:
    print(G[3])              # 返回顶点1的相邻顶点，g[n]表示图g中，与顶点n相邻的所有顶点：
    print(G.adj[3])          # 返回顶点1的相邻顶点，g[n]表示图g中，与顶点n相邻的所有顶点：
    print(G.neighbors(3))    # g.neighbors(n)是g.adj[n]的迭代器版本。：
# 2，查看图的相邻
# 该函数返回顶点n和相邻的节点信息：
# 进行图遍历需要使用adjacency()函数，访问顶点的相邻顶点，、
# n是顶点，nbr_s是顶点n的相邻顶点，是一个字典结构
    for n, nbr_s in G.adjacency():          # 后继节点
        print(n, nbr_s)
        for nbr, attr in nbr_s.items():     # nbr表示跟n连接的顶点，attr表示这两个点连边的属性集合
            print(nbr, attr)
    print(G.nodes(data=True))
    print(G.edges(data=True))
# 五，绘制Graph
# 使用networkx模块draw()函数构造graph，使用matplotlib把图显示出来：
    # G = nx.cubical_graph()    # 修改顶点和边的颜色：
    # nx.draw(g_1, pos=nx.spectral_layout(g_1), nodecolor='r', edge_color='b')
    # nx.draw(G, pos=nx.spectral_layout(G), edge_color='r')
    nx.draw(G, edge_color='r')
    plt.show()

