#!/usr/bin/python3
# -*- coding: utf-8 -*-

################################################################################
# Randomized DAG Generator
# Fang YJ
# Real-Time Systems Group
# Hunan University HNU
################################################################################

from random import randint, random, uniform
import random as rand
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import math
# import rta
# Class: DAG (Directed Acyclic Graph Task)


class DAG:
    #####################################
    #   DAG 参数
    #   param0  DAG name        ：标注DAG，方便存储及调用
    #
    #   param1.1* periodically  ：DAG的周期性质包括 {周期性任务(periodic)； 零星任务(sporadic)； 非周期性任务(aperiodic)}
    #   param1.2* real_time     ：DAG的实时性包括   {HRT(Hard); SRT(Soft); FRT(Firm)}
    #   param1.3* cycle_time    ：(1)if periodically == periodic:   cycle_time = DAG的周期时间；
    #                             (2)if periodically == sporadic:   cycle_time = DAG的最小间隔时间；
    #                             (3)if periodically == aperiodic:  cycle_time = DAG的释放时间；
    #   param2* Deadline        ：DAG的相对截止时间#
    #   param3  DAG G
    #       param3.1    node的属性 ：
    #           param3.1.1  Node_num        ：Node_ID    节点号码(自然ID)；
    #           param3.1.2  rank(level)     ：rank       节点所在层；
    #           param3.1.3  critic          ：critic     节点是否是关键节点
    #           param3.1.4* process_costs   ：WCET       可以是节点的执行时间或最差执行时间（WCET）；
    #           e.g.:self.G.add_node(self_Node_num, Node_ID='job{}'.format(self_Node_num), rank=x, critic=False, WCET=1)
    #       param3.2    edge的属性 ：
    #           param3.2.1  communication time：或者可以通过（节点间通信数据量/core间通信带宽）获取；
    #
    #   param4  其他参数(输入生成)：
    #       param4.1    task_num            ： DAG中的节点数量
    #       param4.2*   parallelism         ： DAG的并行度，生成时的输入 ≥ 最终计算的结果
    #       param4.3*   Critical_path       ： DAG的关键路径的节点长度（输入）
    #   param5 其他参数(后期计算)：
    #       param5.1
    #####################################

    def __init__(self):
        self.name           = 'Tau_{null}'  # DAG save的名称
        self.DAG_ID         = '0'           # DAG的名称
        self.G              = nx.DiGraph()  # DAG:-networkX结构
        self.task_num       = 0             # DAG中节点（job）的数量
        self.Priority       = 1             # 越小等级越高
        # generator mine
        self.parallelism    = 0             # 并行度
        self.Critical_path  = 0             # 关键路径长度

    # def __init__(self, Dag, Dag_ID, Priority):
    #     self.name           = 'Tau_{null}'  # DAG的名称
    #     self.DAG_ID         = Dag_ID        # DAG的名称
    #     self.G              = Dag           # DAG:-networkX结构
    #     self.task_num       = 0             # DAG中节点（job）的数量
    #     self.Priority       = Priority      # 越小等级越高
    #     # generator mine
    #     self.parallelism    = 0             # 并行度
    #     self.Critical_path  = 0             # 关键路径长度

    #   param1.1*                   三种任务的周期属性；
    Periodically = list(enumerate(['PERIODIC', 'SPORADIC', 'APERIODIC'], start=1))
    #   param1.2* real_time         三种DAG的实时性包括   {HRT(Hard); SRT(Soft); FRT(Firm)}
    Real_Time = list(enumerate(['HRT', 'SRT', 'FRT'], start=1))

    def get_graph(self):  # 返回G
        return self.G

    def gen(self, algorithm):  # 生成 DAG
        if algorithm == "mine":
            self.gen_mine()
        else:
            return 1
        return 0

    def get_ready_node_list(self):
        return [x for x in self.G.nodes(data=True) if (x[1].get('state') == 'ready')]

    # #####################################
    # #   分配DAG节点的WCET
    # #   wcet_config
    # #####################################
    # def wcet_config(self):
    #     Max_WCET    = 10
    #     for node_x in self.G.nodes(data=True):
    #         node_x[1]['WCET'] = randint(1, Max_WCET)

    #####################################
    #   关键路径配置
    #####################################
    def critical_path_config(self):
        # # # # # （1）配置关键路径 # # # # #
        WCET = nx.get_node_attributes(self.G, 'WCET')
        for edge_x in self.G.edges(data=True):
            edge_x[2]['weight'] = WCET[edge_x[1]]
        node_list = nx.dag_longest_path(self.G, weight='weight')  # 关键路径
        for node_xx in self.G.nodes(data=True):
            if node_xx[0] in node_list:  # 判断是否在关键路径里
                node_xx[1]['critic'] = True
        # print('关键路径：{0}'.format(node_list))

    #####################################
    #   获取DAG的并行度和关键路径长度
    #   DAG generator 算法4#
    #####################################
    def dag_param_critical_update(self):
        # # # # # （1）配置关键路径 # # # # #
        node_list = nx.dag_longest_path(self.G, weight='weight')  # 关键路径
        print('关键路径：{0}'.format(node_list))
        # # # # # （1.2）配置最短路径 # # # # #
        shortest_path = list(nx.all_shortest_paths(self.G, 0, self.G.number_of_nodes() - 1, weight='weight'))
        print('DAG的最短路径{0}条：'.format(len(shortest_path)))
        for path in shortest_path:
            print(path)
        # # # # # （3）获取拓扑分层 shape # # # # #
        # # # # # （3.1）正向shape # # # # #
        rank_list = [sorted(generation) for generation in nx.topological_generations(self.G)]
        print('拓扑分层：{0}'.format(rank_list))
        print('节点的拓扑排序:{}'.format(list(nx.topological_sort(self.G))))
        print('边的拓扑排序:{}'.format(list(nx.topological_sort(nx.line_graph(self.G)))))
        # # # # # （3.2）反向shape # # # # #
        re_rank_list = [sorted(generation) for generation in nx.topological_generations(nx.DiGraph.reverse(self.G))]
        re_rank_list.reverse()
        print('反向拓扑分层：{0}'.format(re_rank_list))
        app = []
        for rank_x in rank_list:
            app.append(len(rank_x))
        self.parallelism = max(app)
        # # # # # （4）antichains # # # # #
        print("antichains", list(nx.antichains(self.G, topo_order=None)))    # 从DAG中生成antichains；
        """Find the k-cores of a graph."""
        print("每个vertex的core数:", nx.core_number(self.G))                   # Returns the core number for each vertex.
        # k-core是包含k度(degree k)或k度(degree k)以上节点的最大子图。
        print("图G的k-core:", nx.k_core(self.G).edges(data=True))             # Returns the k-core of G.
        # k-shell是由core数为k的节点生成的子图，即，节点在nodes in the k-core中且不在(k+1)-core中.
        print("图G的k_shell:", nx.k_shell(self.G).edges(data=True))           # Returns the k-shell of G.
        # k-crust是带有k-core删除的边的图G(去掉边后的孤立节点也一并去掉)。
        print("图G的k_crust:", nx.k_crust(self.G).edges(data=True))           # Returns the k-crust of G.
        # k-corona是k-core中节点的子图，这些节点在k核中正好有k个邻居。
        print("图G的k_corona:", nx.k_corona(self.G, None).edges(data=True))   # Returns the k-corona of G.
        """Routines to find the boundary of a set of nodes."""
        print("edge_boundary:", list(nx.edge_boundary(self.G, [1])))
        print("node_boundary:", list(nx.node_boundary(self.G, [1])))
        """Dominance algorithms."""
        print("直接支配节点:", nx.immediate_dominators(self.G, 0))     # 返回有向图中所有节点的直接支配节点。
        print("直接支配边界:", nx.dominance_frontiers(self.G, 0))      # 返回有向图中所有节点的支配边界。
        """Flow Hierarchy."""   # 返回有向网络的流层次结构(恒为1.0不知道为什么？)。
        # print("flow_hierarchy:", nx.flow_hierarchy(self.G, weight='weight'))
        """搜索最低共同祖先（DAGs）的算法."""
        # lcas: 元组((u, v), lca)的生成器，其中'u'和'v'是对儿中节点，lca是他们的最低共同祖先，但要求必须需是树！！！
        print("all_pairs_lowest_common_ancestor:", list(nx.all_pairs_lowest_common_ancestor(self.G)))
        """用于计算和验证规则图(regular graphs)的功能 """
        # 定义（regular graph）：图中每个节点都有相同的度。regular有向图是指每个顶点的入度和出度相等的图。
        print("图是否是规则图:", nx.is_regular(self.G))   # 判断图G是否是规则图.
        # 定义（k-regular graph）：每个节点都具有k度，a graph where each vertex has degree k.不支持有向图；is_k_regular # 检测是否图G是一个k-regular图
        """图结构的Hubs（中心）以及authorities（权限）分析."""
        print("节点的HITS hubs和authorities值:\n", nx.hits(self.G))  # h,a=hits(G)返回节点的HITS hubs和authorities值.
        print("authority矩阵:\n", nx.authority_matrix(self.G))      # 返回HITS authority矩阵.
        print("hub矩阵:\n", nx.hub_matrix(self.G))                  # 返回HITS hub矩阵.
        """图结构的PageRank分析."""
        # print("pagerank:\n", nx.pagerank(self.G))                  # 返回图中节点的PageRank.
        # print("google矩阵:\n", nx.google_matrix(self.G))            # 返回图的google矩阵
        #  # print("pagerank_numpy:\n", nx.pagerank_numpy(self.G))      # 返回图中节点的PageRank。
        # print("pagerank_scipy:\n", nx.pagerank_scipy(self.G))      # 返回图中节点的PageRank。
        """宽度优先搜索(BFS)图节点的基本算法"""
        print("BFS_edges:\n", list(nx.bfs_edges(self.G, 0)))       # 从source开始的宽度优先搜索中对边进行迭代。
        print("edge_bfs:\n", list(nx.edge_bfs(self.G, source=0)))  # 一种直接的在图G中边的宽度优先搜索, 起始于`source`.
        print("BFS_tree:\n", list(nx.bfs_tree(self.G, 0)))         # 返回一个从source开始的宽度优先搜索构造的面向方向的树。
        print("BFS_predecessors:\n", list(nx.bfs_predecessors(self.G, 0)))  # 从source中返回宽度优先搜索(BFS)的前驱的迭代器。
        print("BFS_successors:\n", list(nx.bfs_successors(self.G, 0)))      # 从source中返回宽度优先搜索(BFS)的后继的迭代器。
        # 返回“G”中距“source”固定“distance”的所有节点。
        print("descendants_at_distance:\n", list(nx.descendants_at_distance(self.G, 0, self.Critical_path - 2)))
        """深度优先搜索(DFS)图节点的基本算法"""
        print("Dfs_edges:\n", list(nx.dfs_edges(self.G, source=0)))    # 从source开始的深度优先搜索(DFS)中对边进行迭代。
        print("edge_dfs:\n", list(nx.edge_dfs(self.G, source=0)))      # 一种直接的在图G中边的深度优先搜索, 起始于`source`.
        print("dfs_tree:\n", list(nx.dfs_tree(self.G, source=0)))      # 返回基于深度优先搜索的树。
        print("dfs_predecessors:\n", list(nx.dfs_predecessors(self.G, source=0)))        # 返回在source中深度优先搜索中的前驱的字典。
        print("dfs_successors:\n", list(nx.dfs_successors(self.G, source=0)))            # 返回在source中深度优先搜索中的后继的字典。
        print("dfs_postorder_nodes:\n", list(nx.dfs_postorder_nodes(self.G, source=0)))  # 从source开始，以深度优先搜索后排序的方式生成节点。
        print("dfs_labeled_edges:\n", list(nx.dfs_labeled_edges(self.G, source=0)))      # 在按类型标记的深度优先搜索(DFS)中迭代边。
        """用于识别孤立(零度)节点的函数"""
        print("isolates:\n", list(nx.isolates(self.G)))                    # 判断是否有孤立节点，图中孤立节点的迭代器
        print("number_of_isolates:\n", nx.number_of_isolates(self.G))      # 返回图中鼓励节点的数量
        # 3.node_num节点的前驱、后继、祖先、后代
        for self_node in self.G.nodes(data=True):
            print('node_num=:{0}'.format(self_node))
            print('\t前驱节点（predecessors）：{0}'.format(list(self.G.predecessors(self_node[0]))))
            print('\t祖先节点（ancestors）：{0}'.format(nx.ancestors(self.get_graph(), self_node[0])))
            print('\t后继节点（successors）：{0}'.format(list(self.G.successors(self_node[0]))))
            print('\t后代节点（descendants）：{0}'.format(nx.descendants(self.get_graph(), self_node[0])))
            print('\t节点的邻居（neighbors）：{0}'.format(list(nx.neighbors(self.G, self_node[0]))))  # 就是后继节点 successors
            print('\t节点的度（degree）：{0}'.format(nx.degree(self.G, self_node[0])))  # node 0 with degree 1
            print('\t节点的入度（in_degree）：{0}'.format(self.G.in_degree(self_node[0])))

        # pp1 = nx.dag_to_branching(self.G)
        # sources = defaultdict(set)
        # for v, source in pp1.nodes(data="source"):
        #     sources[source].add(v)
        # print("sources", sources)

        # """Algorithms to calculate reciprocity in a directed graph."""
        # print("reciprocity:", nx.reciprocity(self.G))  # 计算有向图中的互反性（reciprocity）,DAG不允许自反！！！。
        # print("overall_reciprocity:", nx.overall_reciprocity(self.G))  #计算全图的自反性

    #####################################
    #   Show DAG
    #####################################
    def show_dag(self):
        # 1.打印DAG的ID
        print("DAG_ID:", self.DAG_ID)
        # 2.打印节点数量
        print("DAG_Nodes_num:", self.G.number_of_nodes())
        # 打印边的数量
        print("DAG_Edges_num:", self.G.number_of_edges())

    def node_property(self, node_number):
        # for node_x in self.G.nodes(data=True):
        node_x = self.G.nodes[node_number]
        assert (node_number == node_x[0])
        print("node_id", node_x[0], node_number)
        print("node_Node_ID", node_x[1].get('Node_ID'))
        print("node_rank", node_x[1].get('rank'))
        print("node_critic", node_x[1].get('critic'))
        # self.G.node[0]['critic'] == True

    def print_data(self):
        # print(self.G.graph)
        # print(self.G.nodes(data=True))  # 输出所有可能的DAG结果数量；
        print(self.G.nodes.data(data=True))
        print(self.G.edges.data(data=True))

    #####################################
    #   get DAG parameter
    #####################################
    def get_node_num(self):
        return self.G.number_of_nodes()

    #####################################
    #   Transitive reduction函数
    #   param:
    #       matrix: Adjacency Matrix
    #   return:
    #       A matrix that has been reduced in transitive
    #####################################
    def transitive_reduction_matrix(self):
        matrix = np.array(nx.adjacency_matrix(self.G).todense())
        row, columns = matrix.shape
        assert (row == self.task_num)
        assert (columns == self.task_num)
        print("matrix shape is ({0},{1})".format(row, columns))
        i_test = np.eye(self.task_num).astype(bool)
        i_matrix = matrix.astype(bool)
        D = np.power((i_matrix | i_test), self.task_num)  # (M | I)^n
        D = D.astype(bool) & (~i_test)
        TR = matrix & (~(np.dot(i_matrix, D)))  # Tr = T ∩ （-（T . D））
        return nx.DiGraph(TR)

    #########################################
    #   DAG graph_node_position_determine
    #   参数：
    #       G：一个DAG；
    #   注：更新self.pos,方便作图
    #       pos = nx.spring_layout(G.get_graph())               #- spring_layout：    用Fruchterman - Reingold算法排列节点
    #       pos = nx.random_layout(G.get_graph())               #- random_layout：    节点随机分布
    #       pos = nx.circular_layout(G.get_graph())             #- circular_layout：  节点在一个圆环上均匀分布
    #       pos = nx.shell_layout(G.get_graph())                #- shell_layout：     节点在同心圆上分布
    #       pos = nx.spectral_layout(G.get_graph(), scale=15)   #- spectral_layout：  根据图的拉普拉斯特征向量排列节
    #########################################
    def graph_node_position_determine(self):
        color_map       = []
        n_pos           = {}
        n_map           = {}
        c_dicy          = {}
        rank_list = [sorted(generation) for generation in nx.topological_generations(self.G)]
        # print('拓扑分层：{0}'.format(rank_list))
        for z1 in range(0, len(rank_list)):
            for z2 in range(0, len(rank_list[z1])):
                node_ID = rank_list[z1][z2]
                sub_node = self.G.nodes[node_ID]
                n_pos[node_ID] = [(z1 + 0.5) * 120 / len(rank_list), (z2 + 0.5) * 120 / len(rank_list[z1])]
                n_map[node_ID] = 'ID:{0} \n WCET:{1}\n prio:{2}'.format(sub_node.get('Node_ID'), sub_node.get('WCET'), sub_node.get('priority'))
                if sub_node['critic']:
                    color = 'green'
                else:
                    color = '#1f78b4'
                # color_map.append(color)
                c_dicy[node_ID] = color
        # n_pos = dict(sorted(n_pos.items(), key=lambda x: x[0]))
        # n_map = dict(sorted(n_map.items(), key=lambda x: x[0]))
        c_dicy = dict(sorted(c_dicy.items(), key=lambda x: x[0]))
        color_map = [x for x in c_dicy.values()]
        nx.draw_networkx_nodes(self.G, n_pos, node_color=color_map, node_size=800, node_shape='o')    # 绘制节点
        nx.draw_networkx_edges(self.G, n_pos, arrows=True,arrowstyle='-|>',  arrowsize=20)                                     # 绘制边
        nx.draw_networkx_labels(self.G, n_pos, labels=n_map, font_size=5, font_color='k')             # 标签

    #####################################
    #   DAG generator 算法3#
    #####################################
    def gen_mine(self):
        assert (self.parallelism >= 1)
        assert (self.Critical_path >= 3)
        # 步骤一：initial a new graph G               # e.g. G = nx.DiGraph(Index=self.task_num)
        #   添加节点；确定rank的节点
        self_critical_path  = self.Critical_path    # 关键路径长度
        self_parallelism    = self.parallelism      # 图的并行度
        self_Node_num       = 0                     # DAG的节点数量
        self.G.add_node(0, Node_ID='souce', rank=0, critic=False, WCET=1, priority=0)  # 起始节点（1）；rank=0
        for x in range(1, self_critical_path - 1):
            m = randint(1, self_parallelism)        # 随机每层的节点数量（不能大于并行度）
            for y in range(1, m + 1):
                self_Node_num += 1
                self.G.add_node(self_Node_num, Node_ID='job{}'.format(self_Node_num), rank=x, critic=False, WCET=1, priority=0)
        self.G.add_node(self_Node_num + 1, Node_ID='sink', rank=self_critical_path - 1, critic=False, WCET=1, priority=0)
        self.task_num = self_Node_num + 2  # +2算上source和sink
        self.G.add_edge(0, 1)
        for x in range(1, self_critical_path - 1):  # 从第2层开始到倒数第二层
            ancestors_list   = [node_x for node_x in self.G.nodes(data=True) if (node_x[1].get('rank') < x)]
            descendants_list = [node_x for node_x in self.G.nodes(data=True) if (node_x[1].get('rank') > x)]
            self_list        = [node_x for node_x in self.G.nodes(data=True) if (node_x[1].get('rank') == x)]
            successors_list  = [node_x for node_x in self.G.nodes(data=True) if (node_x[1].get('rank') == (x + 1))]
            for y in self_list:
                k1 = randint(1, len(ancestors_list))                    # 在祖先节点中随机几个节点作为前驱
                ancestors_group = rand.sample(ancestors_list, k1)
                k2 = randint(1, len(descendants_list))                  # 在后代节点中随机几个节点作为后继
                descendants_group = rand.sample(descendants_list, k2)
                for z in ancestors_group:
                    self.G.add_edge(z[0], y[0])
                for z in descendants_group:
                    self.G.add_edge(y[0], z[0])
            self.G.add_edge(self_list[0][0], successors_list[0][0])
        self.name = 'Tau_{:d}'.format(self.task_num)
        # self.G = nx.DiGraph(self.Matrix)                  # 邻接矩阵生成一个有向图netWorkX；属性全无；
        # ## transitive reduction 传递约简； ## #
        # lp = list(nx.DiGraph(self.transitive_reduction_matrix()).edges())     # 1.networkx包
        lp = list(nx.transitive_reduction(self.G).edges())                  # 2.networkx包
        self.G.clear_edges()
        self.G.add_edges_from(lp)
        # print(np.array(nx.adjacency_matrix(self.G).todense()))

    #####################################
    #   自定义 DAG 算法#
    #####################################
    def user_defined_dag(self):
        # 节点号； 节点名； 节点优权重； 节点优先级
        self.parallelism = 4
        self.Critical_path = 4
        HE_2019_nodes = [[1, 'V1', 1, 1],
                         [2, 'V2', 7, 5],
                         [3, 'V3', 3, 6],
                         [4, 'V4', 3, 7],
                         [5, 'V5', 6, 2],
                         [6, 'V6', 9, 3],
                         [7, 'V7', 2, 4],
                         [8, 'V8', 1, 8]]
        # for x in self_list:
        # self.G.add_node(0, Node_ID='souce_node', rank=0, critic=False, WCET=1)  # 起始节点（1）；rank=0
        for node_x in HE_2019_nodes:
            self.G.add_node(node_x[0], Node_ID=node_x[1], rank=0, critic=False, WCET=node_x[2], priority=node_x[3])
        edges = [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6),
                 (5, 7), (6, 7),
                 (2, 8), (3, 8), (4, 8), (7, 8) ]
        for edge in edges:
            self.G.add_edge(edge[0], edge[1], weight=1)

    def response_time_analysis(self, core_num):
        node_list = list(self.G.nodes())
        paths = list(nx.all_simple_paths(self.G, node_list[0], node_list[-1]))

        interference_node_list = []
        ret_path_and_rta = [0, 0, 0, [], []]
        for x in paths:
            # print(x)
            temp_interference_node_list = []
            temp_path_weight = 0
            temp_WCET = []
            for y in x:
                temp_all_node = self.G.nodes(data=True)
                temp_ance = list(nx.ancestors(self.G, y))
                temp_desc = list(nx.descendants(self.G, y))
                temp_self = x
                sub_node = self.G.nodes[y]
                temp_path_weight += sub_node.get('WCET')
                temp_WCET.append(sub_node.get('WCET'))
                for z in temp_all_node:
                    if (z[0] not in temp_ance) and (z[0] not in temp_desc) and (z[0] not in temp_self):  # 判断z是否是干扰节点
                        # if z[1]['priority'] < sub_node.get('priority'):             # 判断此z的优先级是否大于y
                        if z not in temp_interference_node_list:            # 判断此z是否已经加入
                            temp_interference_node_list.append(z)

                # 每个节点的非前驱和非后继节点
            temp_inter_weight = 0
            for y in temp_interference_node_list:
                temp_inter_weight += y[1]['WCET']
            interference_node_list.append(temp_interference_node_list)
            temp_rta = temp_path_weight + temp_inter_weight/core_num
            # 计算此路径的RTA

            if temp_rta > ret_path_and_rta[0]:
                ret_path_and_rta[0] = temp_rta
                ret_path_and_rta[1] = temp_path_weight
                ret_path_and_rta[2] = temp_inter_weight
                ret_path_and_rta[3] = x
                ret_path_and_rta[4] = temp_interference_node_list
            print((temp_rta, temp_path_weight, temp_inter_weight, x, temp_interference_node_list))
            print(temp_WCET)
            # ret_path_and_rta.append((temp_rta, temp_path_weight, temp_inter_weight, x, temp_interference_node_list))
        return ret_path_and_rta

    def WCET_random_config(self):
        for x in self.G.nodes(data=True):
            x[1]['WCET'] = rand.randint(1, 10)
            # [x for x in self.G.nodes(data=True) if (x[1].get('state') == 'ready')]

    def priority_random_config(self):
        priority_random_list = list(range(0, self.G.number_of_nodes()))
        np.random.shuffle(priority_random_list)
        for x in self.G.nodes(data=True):
            x[1]['priority'] = priority_random_list.pop()

    def DAG_config(self, input_G, input_C, input_prio):  # 关键路径分析
        self.parallelism = 4
        self.Critical_path = 4
        for key, value in input_C.items():
            self.G.add_node(key, Node_ID=key, rank=0, critic=False, WCET=value, priority=input_prio[key])
        for key, value in input_G.items():
            for x in value:
                self.G.add_edge(key, x, weight=1)

    def rev_DAG_config(self):  # 关键路径分析
        self.parallelism = 4
        self.Critical_path = 4
        input_G = {}
        input_C = {}
        input_prio = {}
        for x in self.G.nodes(data=True):
            # input_G[x[0]] = list(nx.bfs_successors(self.G, x[0]))
            input_G[x[0]] = list(nx.neighbors(self.G, x[0]))
            input_C[x[0]] = x[1]['WCET']
            input_prio[x[0]] = x[1]['priority']
        return input_G, input_C, input_prio

    def rev_DAG_config2(self):  # 关键路径分析
        self.parallelism = 4
        self.Critical_path = 4
        input_G = {}
        input_C = {}
        # input_prio = {}
        for x in self.G.nodes(data=True):
            # input_G[x[0]] = list(nx.bfs_successors(self.G, x[0]))
            input_G[x[0]] = list(nx.neighbors(self.G, x[0]))
            input_C[x[0]] = x[1]['WCET']
        return input_G, input_C





def rta_alphabeta_new(G_, C_, prio_, m, overide_prio=0, EOPA=False, TPDS=False):
    """ Response time analysis using alpha_beta
    """
    # --------------------------------------------------------------------------
    # I. load the DAG task
    # G_dict, C_dict, C_array, lamda, VN_array, L, W = load_task(task_idx)

    # << load DAG task <<
    G_dict = G_
    C_dict = C_
    V_array = []

    for key in G_dict:
        V_array.append(key)

    # formulate the c list (c[0] is c for v1!!)
    C_array = []
    for key in sorted(C_dict):
        C_array.append(C_dict[key])

    V_array.sort()
    L, lamda = find_longest_path_dfs(G_dict, V_array[0], V_array[-1], C_array)
    W = sum(C_array)

    VN_array = V_array.copy()

    for i in lamda:
        if i in VN_array:
            VN_array.remove(i)
    # >> end of load DAG task >>

    # --------------------------------------------------------------------------
    # II. providers and consumers
    # iterative all critical nodes
    # after this, all provides and consumers will be collected
    providers, consumers = find_providers_consumers(G_dict, lamda, VN_array)
    print_debug("Providers:", providers)
    print_debug("Consumers:", consumers)

    # --------------------------------------------------------------------------
    # III. calculate the finish times of each provider, and the consumers within
    f_dict = {}        # the set of all finish times
    I_dict = {}        # interference workload
    I_e_dict = {}      # interference workload (for EO)
    R_i_minus_one = 0  # the response time of the previous provider theta^*_(i - 1)

    alpha_arr = []
    beta_arr = []

    # if EOPA:
    #     Prio = Eligiblity_Ordering_PA(G_dict, C_dict)
    #     print_debug("Prioirties", Prio)
    # elif TPDS:
    #     Prio = TPDS_Ordering_PA(G_dict, C_dict)
    #     # reverse the order
    #     for i in Prio:
    #         Prio[i] = A_VERY_LARGE_NUMBER - Prio[i]
    #     print_debug("Prioirties", Prio)
    # else:
    #     Prio = prio_

    if overide_prio == 1:
        Prio = prio_
    else:
        # remove the sink node first; to comptatible with EOPA
        G_dict_cp = copy.deepcopy(G_dict)
        C_dict_cp = copy.deepcopy(C_dict)
        sink_node_idx = V_array[-1]
        G_dict_cp.pop(sink_node_idx)
        C_dict_cp.pop(sink_node_idx)

        # assign prioirties
        Prio = Eligiblity_Ordering_PA(G_dict_cp, C_dict_cp)

        Prio[sink_node_idx] = A_VERY_LARGE_NUMBER

        for key in sorted(Prio.keys()):
            print("{0}:{1}".format(key, Prio[key]), end=',')
        print("")

    # ==========================================================================
    # iteratives all providers (first time, to get all finish times)
    for i, theta_i_star in enumerate(providers):
        print_debug("- - - - - - - - - - - - - - - - - - - -")
        print_debug("theta(*)", i, ":", theta_i_star)
        print_debug("theta", i, ":", consumers[i])

        # get the finish time of all provider nodes (in provider i)
        for _, provi_i in enumerate(theta_i_star):
            # (skipped) sort with topoligical order, skipped because guaranteed by the generator
            # find the max finish time of all its predecences
            f_provider_i_pre_max = 0

            predecsor_of_ij = find_predecesor(G_dict, provi_i)
            for pre_i in predecsor_of_ij:
                if f_dict[pre_i] > f_provider_i_pre_max:
                    f_provider_i_pre_max = f_dict[pre_i]

            f_i = C_dict[provi_i] + f_provider_i_pre_max

            f_dict[provi_i] = f_i
            f_theta_i_star = f_i # finish time of theta_i_star. every loop refreshes this

        # iteratives all consumers
        # (skipped) topoligical order, skipped because guaranteed by the generator
        # note: consumer can be empty
        theta_i = consumers[i]
        f_v_j_max = 0; f_v_j_max_idx = -1
        for _, theta_ij in enumerate(theta_i):
            # the interference term
            con_nc_ij = find_concurrent_nodes(G_dict, theta_ij)
            remove_nodes_in_list(con_nc_ij, lamda)
            if test_parallelism(G_dict, con_nc_ij, m - 1):
                # sufficient parallism
                interference = 0
                I_dict[theta_ij] = []
                I_e_dict[theta_ij] = []
            else:
                # not enough cores
                # start to search interference nodes >>>
                # concurrent nodes of ij. Can be empty.
                con_ij = find_concurrent_nodes(G_dict, theta_ij)
                #print_debug("Con nodes:", con_ij)

                int_ij = con_ij.copy()
                remove_nodes_in_list(int_ij, lamda)

                ans_ij = find_ancestors(G_dict, theta_ij, path=[])
                remove_nodes_in_list(ans_ij, lamda)
                #print_debug("Ans nodes:", ans_ij)

                for ij in ans_ij:
                    ans_int = I_dict[ij]
                    for ijij in ans_int:
                        if ijij in int_ij:
                            int_ij.remove(ijij)
                #print_debug("Int nodes:", int_ij)

                I_dict[theta_ij] = int_ij


                if EOPA or TPDS:
                    # for EOPA, only the (m - 1) longest lower priority interference node is kept
                    int_ij_EO = []
                    int_ij_EO_less_candidates = []
                    int_ij_EO_less_candidates_C = []

                    if int_ij:
                        for int_ij_k in int_ij:
                            if Prio[int_ij_k] > Prio[theta_ij]:
                                # E_k > E_i, add with confidence
                                int_ij_EO.append(int_ij_k)
                            else:
                                # E_k < E_i, put into a list and later will only get longest m - 1
                                int_ij_EO_less_candidates.append( int_ij_k )
                                int_ij_EO_less_candidates_C.append( C_dict[int_ij_k] )

                        # sort nodes by C (if it exists), and append (m-1) longest to int_ij_EO
                        if int_ij_EO_less_candidates:
                            list_of_less_EO_nodes_C = int_ij_EO_less_candidates_C
                            indices, _ = zip(*sorted(enumerate(list_of_less_EO_nodes_C), key=itemgetter(1), reverse=True))
                            #indices = [i[0] for i in sorted(enumerate(list_of_less_EO_nodes_C), key=lambda x:x[1])]
                            int_ij_EO_less_candidates_sorted = []

                            for idx_ in range(len(list_of_less_EO_nodes_C)):
                                int_ij_EO_less_candidates_sorted.append(int_ij_EO_less_candidates[indices[idx_]])

                            # adding (m - 1) lower EO nodes
                            for xxx in range(1, m):
                                if len(int_ij_EO_less_candidates) >= xxx:
                                    int_ij_EO.append( int_ij_EO_less_candidates_sorted[xxx - 1] )

                        int_ij = int_ij_EO.copy()

                    I_e_dict[theta_ij] = int_ij
                # >>> end of searching interference nodes

                int_c_sum = sum(C_dict[ij] for ij in int_ij)
                interference = math.ceil(1.0 / (m-1) * int_c_sum)

            # find the max finish time of all its predecences
            f_ij_pre_max = 0

            predecsor_of_ij = find_predecesor(G_dict, theta_ij)
            for pre_i in predecsor_of_ij:
                if f_dict[pre_i] > f_ij_pre_max:
                    f_ij_pre_max = f_dict[pre_i]

            # calculate the finish time
            f_ij = C_dict[theta_ij] + f_ij_pre_max + interference
            f_dict[theta_ij] = f_ij
            print_debug("f_theta({}) : {}".format(theta_ij, f_dict[theta_ij]))



    # ==========================================================================
    # iteratives all providers (2nd time)
    # the finish times of provider nodes have to be calculated again to get f_theta_i_star
    # the finish times of consumer nodes have to be calculated again to get lambda_ve
    for i, theta_i_star in enumerate(providers):
        print_debug("- - - - - - - - - - - - - - - - - - - -")
        print_debug("theta(*)", i, ":", theta_i_star)
        print_debug("theta", i, ":", consumers[i])

        # get the finish time of all provider nodes (in provider i)
        for _, provi_i in enumerate(theta_i_star):
            # (skipped) sort with topoligical order, skipped because guaranteed by the generator
            # find the max finish time of all its predecences
            f_provider_i_pre_max = 0

            predecsor_of_ij = find_predecesor(G_dict, provi_i)
            for pre_i in predecsor_of_ij:
                if f_dict[pre_i] > f_provider_i_pre_max:
                    f_provider_i_pre_max = f_dict[pre_i]

            f_i = C_dict[provi_i] + f_provider_i_pre_max

            f_dict[provi_i] = f_i
            f_theta_i_star = f_i # finish time of theta_i_star. every loop refreshes this

        print_debug("finish time of theta(*)", f_theta_i_star)

        # iteratives all consumers
        # (skipped) topoligical order, skipped because guaranteed by the generator
        # note: consumer can be empty
        theta_i = consumers[i]
        f_v_j_max = 0; f_v_j_max_idx = -1
        for _, theta_ij in enumerate(theta_i):
            print_debug(theta_ij, ":", C_dict[theta_ij])

            # the interference term
            con_nc_ij = find_concurrent_nodes(G_dict, theta_ij)
            remove_nodes_in_list(con_nc_ij, lamda)
            if test_parallelism(G_dict, con_nc_ij, m - 1):
                # sufficient parallism
                interference = 0
                I_dict[theta_ij] = []
                I_e_dict[theta_ij] = []
            else:
                # not enough cores
                # start to search interference nodes >>>
                # concurrent nodes of ij. Can be empty.
                con_ij = find_concurrent_nodes(G_dict, theta_ij)
                #print_debug("Con nodes:", con_ij)

                int_ij = con_ij.copy()
                remove_nodes_in_list(int_ij, lamda)

                ans_ij = find_ancestors(G_dict, theta_ij, path=[])
                remove_nodes_in_list(ans_ij, lamda)
                #print_debug("Ans nodes:", ans_ij)

                for ij in ans_ij:
                    ans_int = I_dict[ij]
                    for ijij in ans_int:
                        if ijij in int_ij:
                            int_ij.remove(ijij)
                #print_debug("Int nodes:", int_ij)

                I_dict[theta_ij] = int_ij


                if EOPA or TPDS:
                    # for EOPA, only the (m - 1) longest lower priority interference node is kept
                    int_ij_EO = []
                    int_ij_EO_less_candidates = []
                    int_ij_EO_less_candidates_C = []

                    if int_ij:
                        for int_ij_k in int_ij:
                            if Prio[int_ij_k] > Prio[theta_ij]:
                                # E_k > E_i, add with confidence
                                int_ij_EO.append(int_ij_k)
                            else:
                                # E_k < E_i, put into a list and later will only get longest m - 1
                                int_ij_EO_less_candidates.append( int_ij_k )
                                int_ij_EO_less_candidates_C.append( C_dict[int_ij_k] )

                        # sort nodes by C (if it exists), and append (m-1) longest to int_ij_EO
                        if int_ij_EO_less_candidates:
                            list_of_less_EO_nodes_C = int_ij_EO_less_candidates_C
                            indices, _ = zip(*sorted(enumerate(list_of_less_EO_nodes_C), key=itemgetter(1), reverse=True))
                            #indices = [i[0] for i in sorted(enumerate(list_of_less_EO_nodes_C), key=lambda x:x[1])]
                            int_ij_EO_less_candidates_sorted = []

                            for idx_ in range(len(list_of_less_EO_nodes_C)):
                                int_ij_EO_less_candidates_sorted.append(int_ij_EO_less_candidates[indices[idx_]])

                            # adding (m - 1) lower EO nodes
                            for xxx in range(1, m):
                                if len(int_ij_EO_less_candidates) >= xxx:
                                    int_ij_EO.append( int_ij_EO_less_candidates_sorted[xxx - 1] )

                        int_ij = int_ij_EO.copy()

                    I_e_dict[theta_ij] = int_ij
                # >>> end of searching interference nodes

                int_c_sum = sum(C_dict[ij] for ij in int_ij)
                interference = math.ceil(1.0 / (m-1) * int_c_sum)

            # find the max finish time of all its predecences
            f_ij_pre_max = 0

            predecsor_of_ij = find_predecesor(G_dict, theta_ij)
            for pre_i in predecsor_of_ij:
                if f_dict[pre_i] > f_ij_pre_max:
                    f_ij_pre_max = f_dict[pre_i]

            # calculate the finish time
            f_ij = C_dict[theta_ij] + f_ij_pre_max + interference
            f_dict[theta_ij] = f_ij
            print_debug("f_theta({}) : {}".format(theta_ij, f_dict[theta_ij]))

            # find max(f_vj)
            if f_ij > f_v_j_max:
                f_v_j_max = f_ij
                f_v_j_max_idx = theta_ij

        # --------------------------------------------------------------------------
        # start to calculate the response time of provider i
        Wi_nc = sum(C_dict[ij] for ij in theta_i)
        Li = sum(C_dict[ij] for ij in theta_i_star)
        Wi = Wi_nc + Li


        if not EOPA and not TPDS:
            # G(theta_i^*) needs to be added for random
            # Wi and Wi_nc will be updated
            G_theta_i_star = find_G_theta_i_star(G_dict, providers, consumers, i)

            Wi_G = sum(C_dict[ij] for ij in G_theta_i_star)
            Wi_nc = Wi_nc + Wi_G
            Wi = Wi_nc + Li

        # --------------------------------------------------------------------------
        # IV. bound alpha and beta
        # For Case A (has no delay to the critical path):
        if (f_theta_i_star >= f_v_j_max):
            print_debug("** Case A **")
            alpha_i = Wi_nc
            beta_i = 0
        # For Case B (has delay to the critical path):
        else:
            print_debug("** Case B **")
            # search for lamda_ve
            ve = f_v_j_max_idx  # end node & backward search
            lamda_ve = [ve]
            len_lamda_ve = 0

            while True:
                # find pre of ve
                pre_of_ve = find_predecesor(G_dict, ve)  # pre_of_ve can be empty!

                # only care about those within this provider
                for ij in pre_of_ve.copy():
                    if ij not in theta_i:
                        pre_of_ve.remove(ij)

                if pre_of_ve:
                    # calculate the finish times, and the maximum
                    f_pre_of_ve = []
                    for ij in pre_of_ve:
                        f_pre_of_ve.append(f_dict[ij])

                    max_value = max(f_pre_of_ve)
                    max_index = f_pre_of_ve.index(max_value)

                    if max_value > f_theta_i_star:
                        ve = pre_of_ve[max_index]
                        lamda_ve.append(ve)
                    else:
                        break
                else:
                    break

            # calculate accmulative intererence
            for ve_i in lamda_ve:
                if f_dict[ve_i] - C_dict[ve_i] >= f_theta_i_star:
                    len_lamda_ve = len_lamda_ve + C_dict[ve_i]
                else:
                    len_lamda_ve = len_lamda_ve + max((f_dict[ve_i] - f_theta_i_star), 0)

            print_debug("lamda_ve:", lamda_ve, "len:", len_lamda_ve)

            # beta_i
            beta_i = len_lamda_ve

            # alpha (a): find alpha by estimation of finish times
            alpha_hat_class_a = []
            alpha_hat_class_b = []

            for _, theta_ij in enumerate(theta_i):
                if f_dict[theta_ij] <= f_theta_i_star:
                    if theta_ij not in alpha_hat_class_a:
                        alpha_hat_class_a.append(theta_ij)
                elif f_dict[theta_ij] < f_theta_i_star + C_dict[theta_ij]:
                    if theta_ij not in alpha_hat_class_b:
                        alpha_hat_class_b.append(theta_ij)
                else:
                    pass

            if not EOPA and not TPDS:
                # for random, the alpha_i is different
                for _, theta_ij in enumerate(G_theta_i_star):
                    if f_dict[theta_ij] <= f_theta_i_star:
                        if theta_ij not in alpha_hat_class_a:
                            alpha_hat_class_a.append(theta_ij)
                    elif f_dict[theta_ij] < f_theta_i_star + C_dict[theta_ij]:
                        if theta_ij not in alpha_hat_class_b:
                            alpha_hat_class_b.append(theta_ij)
                    else:
                        pass

            print_debug("A:", alpha_hat_class_a, "B:", alpha_hat_class_b)

            alpha_i_hat = sum(C_dict[ij] for ij in alpha_hat_class_a) + \
                            sum(f_theta_i_star - (f_dict[ij] - C_dict[ij]) for ij in alpha_hat_class_b)


            # # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            # # alpha case (b): find alpha by approximation
            # theta_i_llen = theta_i.copy()
            # llen_i = {}
            # len_llen_i = {}

            # # find the m - 1 longest path and their finish times within the provider
            # # n = 1, m - 1
            # for n in range(1, m):
            #     # no more candidates, searching is finished
            #     if theta_i_llen == []:
            #         llen_i[n] = []
            #         len_llen_i[n] = 0
            #         continue

            #     f_theta_i_llen = []

            #     for ij in theta_i_llen:
            #         f_theta_i_llen.append(f_dict[ij])

            #     max_value = max(f_theta_i_llen)
            #     max_index = f_theta_i_llen.index(max_value)
            #     ve = theta_i_llen[max_index]

            #     # find the path (backward search)
            #     llen_ij = [ve]
            #     len_llen_ij = C_dict[ve]

            #     while(True):
            #         pre_of_ij = find_predecesor(G_dict, ve)
            #         for ij in pre_of_ij:
            #             if ij not in theta_i:
            #                 pre_of_ij.remove(ij)

            #         if pre_of_ij:
            #             # find the maximum finish time, within the provider
            #             f_pre_of_ij = []
            #             for ij in pre_of_ij:
            #                 f_pre_of_ij.append(f_dict[ij])

            #             max_value = max(f_pre_of_ij)
            #             max_index = f_pre_of_ij.index(max_value)

            #             if max_value > f_theta_i_star:
            #                 ve = pre_of_ij[max_index]
            #                 llen_ij.append(ve)
            #                 len_llen_ij = len_llen_ij + C_dict[ve]
            #             else:
            #                 break
            #         else:
            #             break

            #     # remove the nodes in the path from theta_i_llen
            #     for ij in llen_ij:
            #         if ij in theta_i_llen:
            #             theta_i_llen.remove(ij)

            #     # save the llen_ij
            #     llen_i[n] = llen_ij
            #     len_llen_i[n] = len_llen_ij

            # # update the finish time of nodes in len_i
            # U_llen = []
            # for key in llen_i:
            #     if llen_i[key]:
            #         # topological sort, to ensure finish time is calculated in the right order
            #         llen_i[key].sort()

            #         # update the UNION(llen(k))
            #         for theta_ij in llen_i[key]:
            #             U_llen.append(theta_ij)

            #         # iterative all nodes in the (key)th longest path
            #         for theta_ij in llen_i[key]:
            #             # the interference term
            #             con_nc_ij = find_concurrent_nodes(G_dict, theta_ij)
            #             remove_nodes_in_list(con_nc_ij, lamda)
            #             if test_parallelism(G_dict, con_nc_ij, m - 1):
            #                 # sufficient parallism
            #                 interference = 0
            #             else:
            #                 # not enough cores
            #                 # start to search interference nodes >>>
            #                 # concurrent nodes of ij. Can be empty.
            #                 con_ij = find_concurrent_nodes(G_dict, theta_ij)
            #                 #print_debug("Con nodes:", con_ij)

            #                 int_ij = con_ij.copy()
            #                 remove_nodes_in_list(int_ij, lamda)

            #                 ans_ij = find_ancestors(G_dict, theta_ij, path=[])
            #                 remove_nodes_in_list(ans_ij, lamda)
            #                 #print_debug("Ans nodes:", ans_ij)

            #                 for ij in ans_ij:
            #                     ans_int = I_dict[ij]
            #                     for ijij in ans_int:
            #                         if ijij in int_ij:
            #                             int_ij.remove(ijij)
            #                 #print_debug("Int nodes:", int_ij)

            #                 I_dict[theta_ij] = int_ij
            #                 # >>> end of searching interference nodes

            #                 # one more step: remove all Union(llen(k))
            #                 for ij in U_llen:
            #                     if ij in int_ij:
            #                         int_ij.remove(ij)

            #                 int_c_sum = sum(C_dict[ij] for ij in int_ij)
            #                 interference = math.ceil(1.0 / (m-1) * int_c_sum)

            #             # find the max finish time of all its predecences
            #             f_ij_pre_max = 0

            #             predecsor_of_ij = find_predecesor(G_dict, theta_ij)
            #             for pre_i in predecsor_of_ij:
            #                 if f_dict[pre_i] > f_ij_pre_max:
            #                     f_ij_pre_max = f_dict[pre_i]

            #             # calculate the finish time
            #             f_ij = C_dict[theta_ij] + f_ij_pre_max + interference

            #             print_debug("Finish time of {:} updated from {:} to {:}".format(theta_ij, f_dict[theta_ij], f_ij))
            #             f_dict[theta_ij] = f_ij

            # # calculate f_delta = sum[(f_ve - f_theta_i_star)]0
            # f_delta_sum = 0
            # for iii_f in range(1, m):
            #     if llen_i[iii_f]:
            #         llen_i_ve = llen_i[iii_f][-1]
            #         f_delta = max(f_dict[llen_i_ve] - f_theta_i_star, 0)
            #         f_delta_sum = f_delta_sum + f_delta
            #     else:
            #         pass
            # # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

            # approxiation of alpha
            # (!) note: alpha_i_new is removed as it is unsafe
            #alpha_i_new = Wi - Li - f_delta_sum
            alpha_i_new = 0

            # alpha_i is the max of the two
            alpha_i = max(alpha_i_hat, alpha_i_new)

        if not EOPA and not TPDS:
            # RTA-CFP
            # calculate the response time based on alpha_i and beta_i
            Ri = Li + beta_i + math.ceil(1.0 / m * (Wi - Li - alpha_i - beta_i))
            # this improved is to bound Ri to be better than classic bound
            #Ri = Li + math.ceil(1.0 / m * (Wi - Li - max(alpha_i - (m-1) * beta_i, 0)))
        else:
            # RTA-CFP + EOPA
            if beta_i == 0:
                Ri = Li
            else:
                I_e_lambda_ve = []
                I_e_lambda_ve_candidates = []
                I_e_lambda_ve_candidates_I = []

                len_I_lambda_ve = {}

                # I_lambda_ve calculation
                for v_k in lamda_ve:
                    I_v_k = I_dict[v_k]

                    for v_j in I_v_k:
                        if f_dict[v_j] > f_theta_i_star:
                            if Prio[v_j] > Prio[v_k]:
                                # E_k > E_i, add with confidence
                                I_e_lambda_ve.append(v_j)

                                if f_dict[v_j] - C_dict[v_j] >= f_theta_i_star:
                                    I_lambda_ve_j = C_dict[v_j]
                                else:
                                    I_lambda_ve_j = f_dict[v_j] - f_theta_i_star

                                len_I_lambda_ve[v_j] = I_lambda_ve_j
                            else:
                                # E_k < E_i, put into a list and later will only get longest m - 1
                                I_e_lambda_ve_candidates.append(v_j)

                                # get I_lambda_ve_j
                                if f_dict[v_j] - C_dict[v_j] >= f_theta_i_star:
                                    I_lambda_ve_j = C_dict[v_j]
                                else:
                                    I_lambda_ve_j = f_dict[v_j] - f_theta_i_star

                                I_e_lambda_ve_candidates_I.append(I_lambda_ve_j)

                                len_I_lambda_ve[v_j] = I_lambda_ve_j

                # sort nodes by I (if it exists), and append (m-1) longest to int_ij_EO
                if I_e_lambda_ve_candidates:
                    indices, _ = zip(*sorted(enumerate(I_e_lambda_ve_candidates_I), key=itemgetter(1), reverse=True))
                    I_e_lambda_ve_candidates_sorted = []

                    for idx_ in range(len(I_e_lambda_ve_candidates_I)):
                        I_e_lambda_ve_candidates_sorted.append(I_e_lambda_ve_candidates[indices[idx_]])

                    # adding (m) lower EO nodes
                    for xxx in range(1, m+1):
                        if len(I_e_lambda_ve_candidates) >= xxx:
                            I_e_lambda_ve.append(I_e_lambda_ve_candidates_sorted[xxx - 1])

                # test parallelism of I_lambda_ve
                if test_parallelism(G_dict, I_e_lambda_ve, m):
                    I_term_for_EO = 0
                else:
                    # calculate I_ve
                    I_ve = 0

                    for v_j in I_e_lambda_ve:
                        len_I_lambda_ve_j = len_I_lambda_ve[v_j]
                        I_ve = I_ve + len_I_lambda_ve_j


                    I_term_for_EO = math.ceil(1.0 / m * I_ve)

                    # check: I_ve should <= (Wi - Li - alpha_i - beta_i)
                    #print_debug("(DEBUG) Wi - Li - alpha_i - beta_i: {}".format( Wi - Li - alpha_i - beta_i ))
                    #print_debug("(DEBUG) I_ve: {}".format( I_ve ))

                Ri = Li + beta_i + I_term_for_EO

        # print_debug("R_i:", Ri)
        R_i_minus_one = R_i_minus_one + Ri
        # print_debug("R_sum: ", R_i_minus_one)

        alpha_arr.append(alpha_i)
        beta_arr.append(beta_i)

    R = R_i_minus_one

    return R, alpha_arr, beta_arr


if __name__ == "__main__":
    plt.figure()
    G = DAG()           # 初始化DAG

    """     """
    G.parallelism = 4  # int(Parallelism)      # 输入并行度
    G.Critical_path = 4  # int(Critical_path)    # 输入关键路径长度 30 * 7 将近一分钟
    # G.gen("mine")
    # G.user_defined_dag()    # 自定义DAG
    # G.WCET_random_config()  # WCET 配置//

    # input_G, input_C = G.rev_DAG_config2()

    # input_prio = rta.TPDS_Ordering_PA(input_G, input_C)
    # G.priority_random_config()  # 优先级配置
    # print(input_G)
    # print(input_C)
    # print(input_prio)

    # for x in G.G.nodes(data=True):
    #     x[1]['priority'] = input_prio[x[0]]

    # input_G, input_C, input_prio = G.rev_DAG_config()
    """ """

    """ """
    input_G = {1: [2, 3, 4, 5, 9], 2: [9], 3: [6, 7, 8], 4: [7], 5: [7, 8], 6: [9], 7: [9], 8: [9], 9: []}
    input_C = {1: 4581, 2: 17559, 3: 9352, 4: 7826, 5: 8589, 6: 12215, 7: 9543, 8: 15078, 9: 11261}
    # input_prio = {1: 9, 2: 8, 3: 7, 4: 6, 5: 5, 6: 4, 7: 3, 8: 2, 9: 1}
    input_prio = {1: 0, 3: 1, 5: 2, 8: 3, 6: 4, 2: 5, 4: 6, 7: 7, 9: 8}
    G.DAG_config(input_G, input_C, input_prio)
    """ """
    input_n_cores = 2
    input_overide_prio = 0
    G.critical_path_config()                  # 关键路径分析
    G.graph_node_position_determine()         # DAG节点位置确定
    # G.dag_param_critical_update()           # DAG数据分析
    #################
    # 响应时间分析
    #################
    print('\n')
    print(G.G.nodes(data=True))

    # 1.zhao 2020 方法
    print('zhao 2020 方法')
    R, alpha_arr, beta_arr = rta_alphabeta_new(input_G, input_C, input_prio, input_n_cores, input_overide_prio)

    print(R)
    print(alpha_arr)
    print(beta_arr)
    print('\n')
    # 2.he 2019 方法
    print('he 2019 方法')
    he_r = TPDS_rta_new(input_G, input_C, input_prio, input_n_cores)    # 自备优先级算法
    print(he_r)
    # he_r = rta.TPDS_rta_new_pro(input_G, input_C, input_n_cores)          # 使用其他的优先级
    # print(he_r)
    print('\n')
    # 3.基础方法
    print('基础方法')
    x = G.response_time_analysis(input_n_cores)
    print(x)


    # plt.title('DAG generator' +
    #           '\n Is a DAG:{0}'.format(nx.is_directed_acyclic_graph(G.get_graph())) +  # 检测是否是有向无环图
    #           '\n number of nodes for DAG:{0}'.format(G.G.number_of_nodes()) +  # 返回G的节点数量
    #           '\n number of edges for DAG:{0}'.format(G.G.number_of_edges()) +  # 返回G的边数量
    #           '',
    #           fontsize=10, color="black", weight="light", ha='left', x=0)  # style="italic",
    # plt.xlabel('crirical={}'.format(G.Critical_path))
    # plt.ylabel('param={}'.format(G.parallelism))
    plt.show()




    # 传递闭包***
    # 有向图的 transitive closure；
    # nx.transitive_closure(G, reflexive=False)
    # 如果有向无环形图的transitive closure；
    # nx.transitive_closure_dag(G.get_graph(), topo_order=None)
    # print('1', np.array(nx.adjacency_matrix(G.get_graph()).todense()))
    # print('2', np.array(nx.adjacency_matrix(G1).todense()))

