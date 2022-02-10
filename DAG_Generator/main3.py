import numpy as np
import DAG
import networkx as nx
import matplotlib.pyplot as plt

dag_class = DAG.DAG_class()
# test = dag_class.make_struct(0, 0)  # 定义并初始化


def node_edge_trans(Metrix, node):
    edge=[]
    for x in range(0,len(node)):
        for y in range(1, len(node)):
            if Metrix[x][y]:
                edge.append(('{}'.format(node[x]),'{}'.format(node[y])))
    return edge

123123
while 1:
    Parallelism = input("请输入DAG的并行度：")
    print("你输入的内容是: ", Parallelism)
    Critical_path = input("请输入DAG的关键路径长度：")
    print("你输入的内容是: ", Critical_path)

    # ###################### #
    #   生成DAG图的邻接矩阵     #
    # ###################### #
    test = dag_class.make_struct(int(Parallelism), int(Critical_path))
    ret = dag_class.DAG_generator(test)

    # ########################
    #   显示DAG图
    # ########################
    # for x in range(0, len(ret[0])):           # x 代表分布种类

    x = 0
    dist = ret[1][x]                            # dist = ret[1][x]
    node = []
    for y in range(0, len(ret[1][x])):          # y 代表层号
        for z in range(0, len(ret[1][x][y])):
            node.append('{0}_{1}'.format(y, ret[1][x][y][z]))
    for y in range(0, len(ret[0])):          # y 代表分布的总体矩阵数量
        Metrix = ret[0][y]
        edge = node_edge_trans(Metrix, node)
        G = nx.DiGraph()
        for z1 in range(0,len(dist)):
            for z2 in range(0, len(dist[z1])):
                G.add_node('{0}_{1}'.format(z1, dist[z1][z2]), pos=((z1+0.5) * 120/len(dist),  (z2 + 0.5) * 120/len(dist[z1])))
                # G.add_node('{0}_{1}'.format(z1, dist[z1][z2]))
        r = G.add_edges_from(edge)

    pos = nx.spring_layout(G)
    nx.draw(G, nx.get_node_attributes(G, 'pos'), with_labels=True, node_color='y')
    plt.show()


