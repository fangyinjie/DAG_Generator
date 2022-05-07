#!/usr/bin/python3
# -*- coding: utf-8 -*-

################################################################################
# Randomized DAG Generator
# Fang YJ
# Real-Time Systems Group
# Hunan University HNU
################################################################################

import matplotlib.pyplot as plt
from DAG import DAG

if __name__ == "__main__":

    # plt.figure()          # (figsize=(100.0, 100.0))
    plt.subplot(211)

    # # # # # 步骤1 DAG生成 # # # # #

    G = DAG()               # 初始化DAG
    G.parallelism  = 4      # int(input("请输入DAG的并行度："))
    print("你输入的内容是: ", G.parallelism)
    G.Critical_path = 8     # int(input("请输入DAG的关键路径长度："))
    print("你输入的内容是: ", G.Critical_path)
    G.gen("mine")           # 生成DAG(1)随机
    # G.user_defined_dag()  # 生成DAG(2)设定

    # # # # # 步骤2 DAG赋值 # # # # #

    G.wcet_config()       # 分配WCET

    # # # # # 步骤3 DAG分析 # # # # #

    G.dag_param_critical_update()       # 关键数据分析
    G.graph_node_position_determine()   # DAG节点位置确定

    # plt.title('DAG generator' +
    #           '\n Is a DAG:{0}'.format(nx.is_directed_acyclic_graph(G.get_graph())) +     # 检测是否是有向无环图
    #           '\n number of nodes for DAG:{0}'.format(G.G.number_of_nodes()) +            # 返回G的节点数量
    #           '\n number of edges for DAG:{0}'.format(G.G.number_of_edges()) +            # 返回G的边数量
    #           '',
    #           fontsize=10, color="black", weight="light", ha='left', x=0)  # style="italic",

    plt.xlabel('crirical={}'.format(G.Critical_path))
    plt.ylabel('param={}'.format(G.parallelism))
    plt.show()
    # G.save(basefolder="data/")

    # 传递闭包***
    # 有向图的 transitive closure；
    # nx.transitive_closure(G, reflexive=False)
    # 如果有向无环形图的transitive closure；
    # nx.transitive_closure_dag(G.get_graph(), topo_order=None)
    # print('1', np.array(nx.adjacency_matrix(G.get_graph()).todense()))
    # print('2', np.array(nx.adjacency_matrix(G1).todense()))
