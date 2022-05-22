import networkx as nx

if __name__ == "__main__":
    g_2 = nx.Graph()      # 创建空的无向图
    g_1 = nx.DiGraph()    # 创建空的有向图
# 1，向图中增加顶点
# 向图中增加顶点时，可以一次增加一个顶点，也可以一次性增加多个顶点，顶点的ID属性是必需的。
# 可通过g.nodes()函数获得图的所有顶点的视图，返回的实际上NodeView对象；
# 如果为g.nodes(data=True)的data参数设置为true，
# 那么返回的是NodeDataView对象，该对象不仅包含每个顶点的ID属性，还包括顶点的其他属性。
    g_1.add_node(1)
    g_1.add_nodes_from([2,3,4])
    g_2.add_node(1)
    g_2.add_nodes_from([2,3,4])
    print(g_1.nodes())
    print(g_2.nodes())
# NodeView((1, 2,3,4))
# 在向图中添加顶点时，除ID属性之外，也可以向顶点中增加自定义的属性，例如，名称属性，权重属性：
    g_1.add_node(1, name='n1', weight=1)
    g_1.add_node(2, name='n2', weight=1.2)
    print(g_1.nodes(data=True))
    print(g_1.node[1])
    # g_2.add_node(1, name='n1', weight=1)
    # g_2.add_node(2, name='n2', weight=1.2)
    # print(g_2.nodes(data=True))
    # print(g_2.node[1])
# 通过g.nodes()，按照特定的条件来查看顶点：
    l1 = list(g_1.nodes(data=True))
    print(l1)
    # l2 = list(g_2.nodes(data=True))
    # print(l1)
# 3，删除顶点
# 通过remove函数删除图的顶点，删除顶点通过传递ID属性作为参数。
    # g_1.remove_node(node_ID)
    # g_1.remove_nodes_from(nodes_list)
# 4，更新顶点
# 更新图的顶点，有两种方式，第一种方式使用字典结构的_update函数，第二种方式是通过索引来设置新值：
    # g_1._node[1].update({'name':'n1_new'})
    g_1.node[1]['name'] = 'n1_new'
    print(g_1.nodes(data=True))
# 5，删除顶点的属性:使用del命令删除顶点的属性
    del g_1.nodes[1]['name']
    print(g_1.nodes(data=True))
# 6，检查是否存在顶点:检查一个顶点是否存在于图中，可以使用 n in g方式来判断，也可以使用函数：
    print(g_1.has_node(1))
# 三，图的边
# 图的边用于表示两个顶点之间的关系，因此，边是由两个顶点唯一确定的。
# 为了表示复杂的关系，通常会为边增加一个权重weight属性；
# 为了表示关系的类型，也会设置为边设置一个关系属性。
# 1，向图中增加边
# 边是由对应顶点的名称构成的，
# 例如，顶点2和3之间有一条边，记作e=(2,3)，通过add_edge(node1,node2)向图中添加一条边，
# 也可以通过add_edges_from(list)向图中添加多条边；在添加边时，如果顶点不存在，那么networkx会自动把相应的顶点加入到图中。
    g_1.add_edge(2, 3)
    g_1.add_edges_from([(1, 2), (1, 3)])
# 可以向边中增加属性，例如，权重，关系等：
    # g_1.add_edge(1, 2, weight=4.7, relationship='renew')
    # print(g_1.edges(data=True))
# 由于在图中，边的权重weight是非常有用和常用的属性，因此，networkx模块内置以一个函数，专门用于在添加边时设置边的权重，
# 该函数的参数是三元组，前两个字段是顶点的ID属性，用于标识一个边，第三个字段是边的权重：
    g_1.add_weighted_edges_from([
        (1, 2, 0.125),
        (1, 3, 0.75),
        (2, 4, 1.2),
        (3, 4, 0.375)])
# 在增加边时，也可以一次增加多条边，为不同的边设置不同的属性：
    g_1.add_edges_from([
        (1, 2, {'color': 'blue'}),
        (2, 3, {'weight': 8})])
    print(g_1.edges(data=True))
# 2，查看边的属性：即查看边的数据(data)，查看所有边及其属性：
# g_1.edges(data=True)
    print(g_1.get_edge_data(1,2))
# 3，删除边
# 边是两个顶点的ID属性构成的元组，通过 edge=(node1,node2) 来标识边，进而从图中找到边：
    g_1.remove_edge(1, 2)
    # g_1.remove_edges_from(edges_list)
    print(g_1.edges(data=True))
# 4，更新边的属性
# 通过边来更新边的属性，由两种方式，一种是使用update函数，一种是通过属性赋值来实现：
    # g_1[1][2]['weight'] = 4.7                            # (1)
    # g_1.edge[1][2]['weight'] = 4                         # (2)
    # g_1[1][2].update({"weight": 4.7})                    # (3)
    # g_1.edges[1, 2].update({"weight": 4.7})              # (4)
# 5，删除边的属性：通过 del命令来删除边的属性
    del g_1[1][3]['weight']
    print(g_1.edges(data=True))
# 6，检查边是否存在:检查一条边是否存在于图中
    print(g_1.has_edge(1, 3))
# 四，图的属性
# 图的属性主要是指相邻数据，节点和边。
# 1，adj
# adj返回的是一个AdjacencyView视图，该视图是顶点的相邻的顶点和顶点的属性，
# 用于显示用于存储与顶点相邻的顶点的数据，这是一个只读的字典结构，
# Key是顶点，Value是顶点的属性数据。
    print(g_1.adj[2][3])
    print(g_1.adj[2])       # 直接后继节点（）
# 2，edges
# 图的边是由边的两个顶点唯一确定的，边还有一定的属性，因此，边是由两个顶点和边的属性构成的：
    print(g_1.edges)            # 返回边的信息
    print(g_1.edges.data())     # 返回边的信息与属性
# EdgeView仅仅提供边的信息，可以通过属性g.edges或函数g.edges()来获得图的边视图。
# EdgeDataView提供图的边和边的属性，可以通过EdgeView对象来调用data()函数获得。
# 3，nodes
# 图的顶点是顶点和顶点的属性构成的
    print(g_1.nodes())
    print(g_1.nodes.data())
# NodeView 通过属性g.nodes或函数g.nodes()来获得。
# NodeDataView提供图的边和边的属性，可以通过NodeView对象来调用data()函数获得。
# 4，degree
# 对于无向图，顶点的度是指跟顶点相连的边的数量；对于有向图，顶点的图分为入度和出度，朝向顶点的边称作入度；背向顶点的边称作出度。
    print('123')
    print(g_1.in_degree)
    print(g_1.out_degree)
    print(g_1.degree)
# 五，图的遍历:图的遍历是指按照图中各顶点之间的边，从图中的任一顶点出发，对图中的所有顶点访问一次且只访问一次。
# 图的遍历按照优先顺序的不同，通常分为深度优先搜索（DFS）和广度优先搜索（BFS）两种方式。
# 1，查看顶点的相邻顶点
# 查看顶点的相邻顶点，有多种方式:
    print(g_1[3])              # 返回顶点1的相邻顶点，g[n]表示图g中，与顶点n相邻的所有顶点：
    print(g_1.adj[3])          # 返回顶点1的相邻顶点，g[n]表示图g中，与顶点n相邻的所有顶点：
    print(g_1.neighbors(3))    # g.neighbors(n)是g.adj[n]的迭代器版本。：
# 2，查看图的相邻
# 该函数返回顶点n和相邻的节点信息：
    for n, nbrs in g_1.adjacency():     # 后继节点
        print(n)
        print(nbrs)
# 3，图的遍历
# （1）深度优先遍历的算法DFS：
# （2）广度优先遍历的算法BFS：
# 在进行图遍历时，需要访问顶点的相邻顶点，这需要用到adjacency()函数，
# 例如，g是一个无向图，n是顶点，nbrs是顶点n的相邻顶点，是一个字典结构
    for n, nbrs in g_1.adjacency():
        print(n, nbrs)
        for nbr, attr in nbrs.items():
            # nbr表示跟n连接的顶点，attr表示这两个点连边的属性集合
            print(nbr, attr)
# 六，绘制Graph
# 使用networkx模块draw()函数构造graph，使用matplotlib把图显示出来：
    import matplotlib.pyplot as plt
    # 修改顶点和边的颜色：
    g_1 = nx.cubical_graph()
    # nx.draw(g_1, pos=nx.spectral_layout(g_1), nodecolor='r', edge_color='b')
    nx.draw(g_1, pos=nx.spectral_layout(g_1), edge_color='b')
    plt.show()

