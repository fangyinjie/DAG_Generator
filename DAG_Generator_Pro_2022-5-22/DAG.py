#!/usr/bin/python3
# -*- coding: utf-8 -*-

################################################################################
# Randomized DAG Generator
# Fang YJ
# Real-Time Systems Group
# Hunan University HNU
################################################################################
import math
from random import randint, random, uniform
import random as rand
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
# Class: DAG (Directed Acyclic Graph Task)


class DAG:
    def __init__(self):
        self.name           = 'Tau_{null}'  # DAG save的名称
        self.DAG_ID         = '0'           # DAG的名称
        self.G              = nx.DiGraph()  # DAG:-networkX结构
        self.task_num       = 0             # DAG中节点（job）的数量
        self.Priority       = 1             # 越小等级越高
        # generator mine
        self.parallelism    = 0             # 并行度
        self.Critical_path  = 0             # 关键路径长度
        # 'PERIODIC'：周期任务；'SPORADIC'：零星任务；'APERIODIC'：非周期任务(只运行一次)
        self.Periodically   = 'APERIODIC'
        # 'HRT'：硬实时, 'SRT'：软实时, 'FRT'：固实时
        self.Real_Time      = 'HRT'
        # 周期DAG的循环时间、零散DAG的最短时间间隔
        self.Cycle_Time     = 0
        self.Deadline       = 0             # DAG的相对截止时间
        self.Start_Time     = 0             # 第一个DAG的到达时间（默认为0）

    #####################################
    #   Section_0: DAG 基本功能
    #####################################
    #   获取 DAG 中处于就绪态的节点
    def get_ready_node_list(self):
        return [x for x in self.G.nodes(data=True) if (x[1].get('state') == 'ready')]

    #   获取 DAG 的节点数量
    def get_node_num(self):
        return self.G.number_of_nodes()

    #####################################
    #   Section_1: DAG 随机生成函数
    #####################################
    def DAG_Generator(self, DAG_Generator_algorithm):
        if DAG_Generator_algorithm == "mine":
            self.gen_mine()
        elif DAG_Generator_algorithm == "GNM":
            self.gen_gnm(n=12, m=20)
            pass
        elif DAG_Generator_algorithm == "GNP":
            self.gen_gnp(n=12, p=0.2)       # 将所有前驱为0的和source连接，后继为0的和sink连接
        elif DAG_Generator_algorithm == "Layer_By_Layer":
            pass
        elif DAG_Generator_algorithm == "Fan_in_Fan_out":
            pass
        elif DAG_Generator_algorithm == "Random_Order":
            pass
        else:
            return False
        return 0

    # #### DAG generator mine 算法  #### #
    def gen_mine(self):
        assert (self.parallelism >= 1)
        assert (self.Critical_path >= 3)
        # 步骤一：initial a new graph G               # e.g. G = nx.DiGraph(Index=self.task_num)
        #   添加节点；确定rank的节点
        self_critical_path  = self.Critical_path    # 关键路径长度
        self_parallelism    = self.parallelism      # 图的并行度
        self_Node_num       = 0                     # DAG的节点数量
        self.G.add_node(0, Node_ID='souce', rank=0, critic=False, WCET=1, priority=1, state='blocked')  # 起始节点（1）；rank=0

        for x in range(1, self_critical_path - 1):
            m = randint(1, self_parallelism)        # 随机每层的节点数量（不能大于并行度）
            for y in range(1, m + 1):
                self_Node_num += 1
                self.G.add_node(self_Node_num, Node_ID='job{}'.format(self_Node_num), rank=x, critic=False, WCET=1, priority=1, state='blocked')
        self.G.add_node(self_Node_num + 1, Node_ID='sink', rank=self_critical_path - 1, critic=False, WCET=1, priority=1, state='blocked')
        self.task_num = self_Node_num + 2  # +2算上source和sink
        self.G.add_edge(0, 1)
        for x in range(1, self_critical_path - 1):  # 从第2层开始到倒数第二层
            ancestors_list      = [node_x for node_x in self.G.nodes(data=True) if (node_x[1].get('rank') <  x)]
            descendants_list    = [node_x for node_x in self.G.nodes(data=True) if (node_x[1].get('rank') >  x)]
            self_list           = [node_x for node_x in self.G.nodes(data=True) if (node_x[1].get('rank') == x)]
            successors_list     = [node_x for node_x in self.G.nodes(data=True) if (node_x[1].get('rank') == (x + 1))]
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

    # #### DAG generator GNP 算法  #### #
    def gen_gnp(self, n, p):
        Temp_Matrix = np.zeros((n, n), dtype=bool)
        for x in range(1, n-1):
            for y in range(x+1, n-1):
                if random() < p:
                    Temp_Matrix[x][y] = True
        self.G = nx.from_numpy_matrix(np.array(Temp_Matrix), create_using=nx.DiGraph)
        while True:
            # self.G = nx.fast_gnp_random_graph(n=n, p=p, seed=None, directed=True)
            for x in self.G.nodes(data=True):
                x[1]['Node_ID']     = 'Job_{0}'.format(x[0])
                x[1]['rank']        = 0
                x[1]['critic']      = False
                x[1]['WCET']        = 1
                x[1]['priority']    = 1
                x[1]['state']       = 'blocked'
                # 无前驱节点的连接到0
                if len(list(self.G.predecessors(x[0]))) == 0:
                    if x[0] != 0:
                        self.G.add_edge(0, x[0])
                # 无前后继点的连接到n-1
                if len(list(self.G.successors(x[0]))) == 0:
                    if x[0] != n-1:
                        self.G.add_edge(x[0], n-1)
            if nx.is_directed_acyclic_graph(self.G):
                break
            else:
                print("GNP Failed")

    # #### DAG generator GNM 算法  #### #
    def gen_gnm(self, n, m):
        assert n * (n - 1) >= m >= n - 1
        All_edges_list = []
        for x in range(n):
            for y in range(x + 1, n):
                All_edges_list.append((x, y))
        Temp_edges_list = rand.sample(All_edges_list, m)
        self.G.add_edges_from(Temp_edges_list)
        for x in self.G.nodes(data=True):
            x[1]['Node_ID']     = 'Job_{0}'.format(x[0])
            x[1]['rank']        = 0
            x[1]['critic']      = False
            x[1]['WCET']        = 1
            x[1]['priority']    = 1
            x[1]['state']       = 'blocked'
            if (len(list(self.G.predecessors(x[0]))) == 0) and (x[0] != 0):
                self.G.add_edge(0, x[0])
            if (len(list(self.G.successors(x[0]))) == 0) and (x[0] != n-1):
                self.G.add_edge(x[0], n-1)
        assert nx.is_directed_acyclic_graph(self.G)

    # #### DAG generator Layer_By_Layer 算法  #### #
    def gen_layer_by_layer(self, n, m):
        pass

    # #### DAG generator Fan_in_Fan_out 算法  #### #
    def gen_fan_in_fan_out(self, n, m):
        pass

    # #### DAG generator Random_Order 算法  #### #
    def gen_random_order(self, n, m):
        pass

    # ######################################################################
    #   Transitive reduction函数
    #   param:      matrix: Adjacency Matrix
    #   return:     A matrix that has been reduced in transitive
    # ######################################################################
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

    #####################################
    #   关键路径配置
    #####################################
    def critical_path_config(self):
        WCET = nx.get_node_attributes(self.G, 'WCET')
        for edge_x in self.G.edges(data=True):
            edge_x[2]['weight'] = WCET[edge_x[1]]
        node_list = nx.dag_longest_path(self.G, weight='weight')  # 关键路径
        for node_xx in self.G.nodes(data=True):
            if node_xx[0] in node_list:  # 判断是否在关键路径里
                node_xx[1]['critic'] = True
        # print('关键路径：{0}'.format(node_list))

    #####################################
    #   获取DAG的关键参数分析
    #####################################
    def dag_param_critical_update(self):
        # #### 0.DAG检测及基本参数 #### #
        assert format(nx.is_directed_acyclic_graph(self.G))      # 检测是否是有向无环图
        print("DAG_ID:", self.DAG_ID)  # 1.打印DAG的ID
        print('DAG中的节点数量：{0}'.format(self.G.number_of_nodes()))
        print('DAG中的边的数量：{0}'.format(self.G.number_of_edges()))

        #####################################
        #   获取DAG的结构相关参数
        #####################################
        # #### 1.关键路径 #### #
        node_list = nx.dag_longest_path(self.G, weight='weight')  # 关键路径
        print('关键路径：{0}'.format(node_list))

        # #### 2.最短路径 #### #
        shortest_path = list(nx.all_shortest_paths(self.G, 0, self.G.number_of_nodes() - 1, weight='weight'))
        print('DAG的最短路径{0}条：'.format(len(shortest_path)))
        [print(path) for path in shortest_path]

        # #### 3.获取拓扑分层 shape #### #
        # 3.1 正向shape
        rank_list = [sorted(generation) for generation in nx.topological_generations(self.G)]
        rank_num_list = [len(x) for x in rank_list]
        print('拓扑分层：{0}'.format(rank_list))
        print('拓扑分层节点数量分布：{0}'.format(rank_num_list))
        print("最大shape:{0}、最小shape:{1}、平均shape:{2:2f}、shape标准差:{3:2f}".format(
            max(rank_num_list), min(rank_num_list), np.mean(rank_num_list), np.std(rank_num_list)))
        # 3.2 反向shape
        re_rank_list = [sorted(generation) for generation in nx.topological_generations(nx.DiGraph.reverse(self.G))]
        re_rank_list.reverse()
        re_rank_num_list = [len(x) for x in re_rank_list]
        print('反向拓扑分层：{0}'.format(re_rank_list))
        print('反向拓扑分层节点数量分布：{0}'.format(re_rank_num_list))
        print("最大re_shape:{0}、最小re_shape:{1}、平均re_shape:{2:2f}、re_shape标准差:{3:2f}".format(
            max(re_rank_num_list), min(re_rank_num_list), np.mean(re_rank_num_list), np.std(re_rank_num_list)))

        # #### 4.DAG并行度数据更新 #### #
        self.parallelism = max([len(rank_x) for rank_x in rank_list])
        print('DAG的并行度：{0}'.format(self.parallelism))

        # #### 5.antichains #### #
        print("anti-chains", list(nx.antichains(self.G, topo_order=None)))  # 从DAG中生成antichains；

        # #### 6.degree #### #
        degree_list = [nx.degree(self.G, self_node[0]) for self_node in self.G.nodes(data=True)]
        degree_in_list = [self.G.in_degree(self_node[0]) for self_node in self.G.nodes(data=True)]
        degree_out_list = [self.G.out_degree(self_node[0]) for self_node in self.G.nodes(data=True)]
        print("最大度:{0}、最小度:{1}、平均度{2:2f}、度标准差{3:2f}".format(
            max(degree_list), min(degree_list), np.mean(degree_list), np.std(degree_list)))
        print("最大入度:{0}、最小入度:{1}、平均入度{2:2f}、入度标准差{3:2f}".format(
            max(degree_in_list), min(degree_in_list), np.mean(degree_in_list), np.std(degree_in_list)))
        print("最大出度:{0}、最小出度:{1}、平均出度{2:2f}、出度标准差{3:2f}".format(
            max(degree_out_list), min(degree_out_list), np.mean(degree_out_list), np.std(degree_out_list)))

        # #### 7.DAG的稠密度 Density  #### #
        Dag_density = (2 * self.G.number_of_edges()) / (self.G.number_of_nodes() * (self.G.number_of_nodes()-1))
        print("稠密度：{0:2f}".format(Dag_density))

        #####################################
        #   获取DAG的时间相关参数
        #####################################
        # #### 1.DAG最差执行时间list  #### #
        WCET_list = [x[1]['WCET'] for x in self.G.nodes.data(data=True)]
        print("WCET_list：{0}".format(WCET_list))
        print("WCET的顺序执行时间：{0}, WCET的均值：{1:2f}, WCET的标准差：{2:2f}".format(
            np.sum(WCET_list), np.mean(WCET_list), np.std(WCET_list)))

    def dag_param_critical_update_other(self):
        print('节点的拓扑排序:{}'.format(list(nx.topological_sort(self.G))))
        print('边的拓扑排序:{}'.format(list(nx.topological_sort(nx.line_graph(self.G)))))
        """搜索最低共同祖先（DAGs）的算法."""
        # lcas: 元组((u, v), lca)的生成器，其中'u'和'v'是对儿中节点，lca是他们的最低共同祖先，但要求必须需是树！！！
        print("all_pairs_lowest_common_ancestor:")
        for x in list(nx.all_pairs_lowest_common_ancestor(self.G)):
            print(x)
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
        """Flow Hierarchy."""   # 返回有向网络的流层次结构(恒为1.0不知道为什么？)。
        # print("flow_hierarchy:", nx.flow_hierarchy(self.G, weight='weight'))
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
        # print("pagerank_numpy:\n", nx.pagerank_numpy(self.G))      # 返回图中节点的PageRank。
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
        print("isolates:\n", list(nx.isolates(self.G)))  # 判断是否有孤立节点，图中孤立节点的迭代器
        print("number_of_isolates:\n", nx.number_of_isolates(self.G))  # 返回图中鼓励节点的数量
        # #### 6.Dominance algorithms #### #
        print("直接支配节点:", nx.immediate_dominators(self.G, 0))  # 返回有向图中所有节点的直接支配节点。
        print("直接支配边界:", nx.dominance_frontiers(self.G, 0))  # 返回有向图中所有节点的支配边界。

        # pp1 = nx.dag_to_branching(self.G)
        # sources = defaultdict(set)
        # for v, source in pp1.nodes(data="source"):
        #     sources[source].add(v)
        # print("sources", sources)
        # """Algorithms to calculate reciprocity in a directed graph."""
        # print("reciprocity:", nx.reciprocity(self.G))  # 计算有向图中的互反性（reciprocity）,DAG不允许自反！！！。
        # print("overall_reciprocity:", nx.overall_reciprocity(self.G))  #计算全图的自反性

    def node_property(self, node_number):
        # for node_x in self.G.nodes(data=True):
        node_x = self.G.node[node_number]
        assert (node_number == node_x[0])
        print("node_id", node_x[0], node_number)
        print("node_Node_ID", node_x[1].get('Node_ID'))
        print("node_rank", node_x[1].get('rank'))
        print("node_critic", node_x[1].get('critic'))
        # self.G.node[0]['critic'] == True

    def print_data(self):
        # print(self.G.nodes.data(data=False))
        # print(self.G.edges.data(data=False))
        print(self.G.nodes.data(data=True))
        print(self.G.edges.data(data=True))

    #########################################
    #   DAG graph_node_position_determine
    #########################################
    def graph_node_position_determine(self):
        n_pos           = {}
        n_map           = {}
        rank_list = [sorted(generation) for generation in nx.topological_generations(self.G)]
        for z1 in range(0, len(rank_list)):
            for z2 in range(0, len(rank_list[z1])):
                node_ID = rank_list[z1][z2]
                sub_node = self.G.nodes[node_ID]
                n_pos[node_ID] = [(z1 + 0.5) * 120 / len(rank_list), (z2 + 0.5) * 120 / len(rank_list[z1])]
                n_map[node_ID] = "ID:{0} \n WCET:{1} \n prio:{2} \n Cri:{3}".format(
                    sub_node.get('Node_ID'), sub_node.get('WCET'), sub_node.get('priority'), sub_node.get('critic'))
        nx.draw(self.G, n_pos, node_size=800, with_labels=True, labels=n_map, font_size=5, font_color='k')

    #####################################
    #   WCET 配置算法#
    #   参数a： 均匀分布的最小值、高斯分布的均值
    #   参数b： 均匀分布的最大值、高斯分布的方差
    #####################################
    def WCET_Config(self, WCET_Config_type, a, b):
        # 方式1（均匀分布）：在区间[a, b]中均匀分布方式生成 WCET
        if WCET_Config_type == "random":
            for x in self.G.nodes(data=True):
                x[1]['WCET'] = math.ceil(np.random.uniform(a, b))
                # x[1]['WCET'] = rand.randint(a, b)
            # [x for x in self.G.nodes(data=True) if (x[1].get('state') == 'ready')]

        # 方式2（正态分布）：以loc=a为均值，以scale=b为方差 # size:输出形式 / 维度
        elif WCET_Config_type == "normal":
            for x in self.G.nodes(data=True):
                while True:
                    x[1]['WCET'] = math.ceil(np.random.normal(loc=a, scale=b, size=None))
                    if x[1]['WCET'] > 0:
                        break

        # 方式3（高斯分布，gauss）以均值为mu=a，标准偏差为sigma=b的方式生成 WCET
        elif WCET_Config_type == "gauss":
            for x in self.G.nodes(data=True):
                while True:
                    x[1]['WCET'] = math.ceil(rand.gauss(a, b))
                    if x[1]['WCET'] > 0:
                        break
        else:
            pass


    #####################################
    #   优先级 配置算法#
    #####################################
    def Priority_Config(self, Priority_Config_type):
        if Priority_Config_type == "random":
            self.priority_random_config()
        elif Priority_Config_type == "Zhao":
            self.priority_Zhao_config()
        elif Priority_Config_type == "He2019":
            self.priority_He2019_config()
        elif Priority_Config_type == "He2021":
            self.priority_He2021_config()
        elif Priority_Config_type == "Chen":
            self.priority_Chen_config()
        elif Priority_Config_type == "Mine":
            self.priority_Mine_config()
        else:
            print("priority config error!\n")

    def priority_random_config(self):
        priority_random_list = list(range(0, self.G.number_of_nodes()))
        np.random.shuffle(priority_random_list)
        for x in self.G.nodes(data=True):
            x[1]['priority'] = priority_random_list.pop()

    def priority_Zhao_config(self):
        pass

    def priority_He2019_config(self):
        pass

    def priority_He2021_config(self):
        pass

    def priority_Chen_config(self):
        pass

    def priority_Mine_config(self):
        pass

    #####################################
    #   响应时间分析算法#
    #####################################
    def Response_Time_analysis(self, RTA_Type, core_num):
        if RTA_Type == "non-preemptive":
            return self.rta_basics_non_preemptive(core_num)
        elif RTA_Type == "preemptive":
            return self.rta_basics_preemptive(core_num)
        else:
            print("RTA_Type input error!")

    def rta_basics_non_preemptive(self, core_num):
        node_list = list(self.G.nodes())
        paths = list(nx.all_simple_paths(self.G, node_list[0], node_list[-1]))

        interference_node_list = []
        ret_path_and_rta = [0, 0, 0, [], []]
        for x in paths:
            temp_interference_node_list = []
            temp_path_weight = 0
            for y in x:
                temp_all_node = self.G.nodes(data=True)
                temp_ance = list(nx.ancestors(self.G, y))
                temp_desc = list(nx.descendants(self.G, y))
                temp_self = x
                sub_node = self.G.node[y]
                for z in temp_all_node:
                    if (z[0] not in temp_ance) and (z[0] not in temp_desc) and (z[0] not in temp_self):  # 判断z是否是干扰节点
                        if z[1]['priority'] < sub_node.get('priority'):             # 判断此z的优先级是否大于y
                            if z not in temp_interference_node_list:            # 判断此z是否已经加入
                                temp_interference_node_list.append(z)
                temp_path_weight += sub_node.get('WCET')
                # 每个节点的非前驱和非后继节点
            temp_inter_weight = 0
            for y in temp_interference_node_list:
                temp_inter_weight += y[1]['WCET']
            interference_node_list.append(temp_interference_node_list)
            temp_rta = temp_path_weight + temp_inter_weight/core_num
            # 计算此路径的RTA
            # ret_path_and_rta.append((temp_rta, temp_path_weight, temp_inter_weight, x, temp_interference_node_list))
            if temp_rta > ret_path_and_rta[0]:
                ret_path_and_rta[0] = temp_rta
                ret_path_and_rta[1] = temp_path_weight
                ret_path_and_rta[2] = temp_inter_weight
                ret_path_and_rta[3] = x
                ret_path_and_rta[4] = temp_interference_node_list
        return math.ceil(ret_path_and_rta[0])

    def rta_basics_preemptive(self, core_num):
        node_list = list(self.G.nodes())
        paths = list(nx.all_simple_paths(self.G, node_list[0], node_list[-1]))

        interference_node_list = []
        ret_path_and_rta = [0, 0, 0, [], []]
        for x in paths:
            temp_interference_node_list = []
            reserve_node_list = {}
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
                        if z[1]['priority'] < sub_node.get('priority'):   # 判断此z的优先级是否大于y
                            if z not in temp_interference_node_list:            # 判断此z是否已经加入
                                temp_interference_node_list.append(z)
                        else:
                            reserve_node_list[z[0]] = z[1]['WCET']
            t_reserve_list = sorted(reserve_node_list.items(), key=lambda x: x[1])
            add_reserve = 0
            for y in range(0, min(core_num, len(t_reserve_list))):
                add_reserve += t_reserve_list[y][1]
            temp_inter_weight = 0
            for y in temp_interference_node_list:
                temp_inter_weight += y[1]['WCET']
            interference_node_list.append(temp_interference_node_list)
            temp_rta = temp_path_weight + (temp_inter_weight+add_reserve)/core_num
            # 计算此路径的RTA
            if temp_rta > ret_path_and_rta[0]:
                ret_path_and_rta[0] = temp_rta
                ret_path_and_rta[1] = temp_path_weight
                ret_path_and_rta[2] = temp_inter_weight
                ret_path_and_rta[3] = x
                ret_path_and_rta[4] = temp_interference_node_list
        return math.ceil(ret_path_and_rta[0])


if __name__ == "__main__":
    # Parallelism = input("请输入DAG的并行度：")
    # print("你输入的内容是: ", Parallelism)
    # Critical_path = input("请输入DAG的关键路径长度：")
    # print("你输入的内容是: ", Critical_path)
    plt.figure()            # (figsize=(100.0, 100.0))
    # plt.subplot(211)
    G = DAG()               # 初始化DAG
    # （1）手动生成DAG
    # G.user_defined_dag()
    # （2）随机生成DAG
    G.DAG_ID = "DAG_{0}".format("4_6")  # 配置DAG的ID
    G.Priority = 1                      # 配置DAG的优先级
    G.parallelism   = 4                 # 输入并行度 int(Parallelism)
    G.Critical_path = 6                 # 输入关键路径长度 int(Critical_path)
    # step1.DAG结构生成
    # G.DAG_Generator("mine")
    # G.DAG_Generator("GNP")
    G.DAG_Generator("GNM")
    # step2. DAG WCET配置；
    G.WCET_Config("gauss", 10, 100)  # gauss # random # normal
    # step3. DAG 优先级配置；
    G.Priority_Config("random")
    # step4. DAG 关键路径配置；
    G.critical_path_config()
    # step5. DAG节点位置确定
    G.graph_node_position_determine()

    # #### DAG 关键数据分析；#### #
    G.print_data()
    G.dag_param_critical_update()       # 关键数据分析

    plt.xlabel('crirical={}'.format(G.Critical_path))
    plt.ylabel('param={}'.format(G.parallelism))
    plt.show()
    # G.save(basefolder="data/")
