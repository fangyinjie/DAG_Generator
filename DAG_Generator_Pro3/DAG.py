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
        self.Periodically   = 'APERIODIC'   # 'PERIODIC'：周期任务
                                            # 'SPORADIC'：零星任务
                                            # 'APERIODIC': 非周期任务，一次调用只运行一次，只运行一次
        self.Real_Time      = 'HRT'         # 'HRT', 'SRT', 'FRT'
        self.Cycle_Time     = 0             # 如果periodically是periodic则cycle_time为DAG的周期时间；
                                            # 如果periodically是sporadic则cycle_time为DAG的最小间隔时间；
                                            # 如果periodically是aperiodic则cycle_time为DAG；
        self.Deadline       = 0             # DAG的相对截止时间
        self.Start_Time     = 0             # 默认为0 第一个DAG的到达时间

    #####################################
    #   DAG 基本功能
    #####################################
    def get_graph(self):  # 返回G
        return self.G

    #   获取 DAG 中处于就绪态的节点
    def get_ready_node_list(self):
        return [x for x in self.G.nodes(data=True) if (x[1].get('state') == 'ready')]

    #   获取 DAG 的节点数量
    def get_node_num(self):
        return self.G.number_of_nodes()

    #####################################
    #   DAG 随机生成函数
    #####################################
    def gen(self, algorithm):  # 生成 DAG
        if algorithm == "mine":
            self.gen_mine()
        else:
            return 1
        return 0

    #####################################
    #   DAG generator mine 算法 #
    #####################################
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

    #####################################
    #   Transitive reduction函数
    #   param:      matrix: Adjacency Matrix
    #   return:     A matrix that has been reduced in transitive
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
    #   Show DAG
    #####################################
    def show_dag(self):
        print("DAG_ID:", self.DAG_ID)                       # 1.打印DAG的ID
        print("DAG_Nodes_num:", self.G.number_of_nodes())   # 2.打印节点数量
        print("DAG_Edges_num:", self.G.number_of_edges())   # 打印边的数量

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
        # print(self.G.graph)
        # print(self.G.nodes(data=True))  # 输出所有可能的DAG结果数量；
        print(self.G.nodes.data(data=True))
        print(self.G.edges.data(data=True))

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
        print("pagerank:\n", nx.pagerank(self.G))                  # 返回图中节点的PageRank.
        print("google矩阵:\n", nx.google_matrix(self.G))            # 返回图的google矩阵
        # print("pagerank_numpy:\n", nx.pagerank_numpy(self.G))      # 返回图中节点的PageRank。
        print("pagerank_scipy:\n", nx.pagerank_scipy(self.G))      # 返回图中节点的PageRank。
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
        for z1 in range(0, len(rank_list)):
            for z2 in range(0, len(rank_list[z1])):
                node_ID = rank_list[z1][z2]
                sub_node = self.G.nodes[node_ID]
                n_pos[node_ID] = [(z1 + 0.5) * 120 / len(rank_list), (z2 + 0.5) * 120 / len(rank_list[z1])]
                n_map[node_ID] = "ID:{0} \n WCET:{1} \n prio:{2}".format(
                    sub_node.get('Node_ID'), sub_node.get('WCET'), sub_node.get('priority'))
                if sub_node['critic']:
                    color = 'green'
                else:
                    color = '#1f78b4'
                c_dicy[node_ID] = color
        c_dicy = dict(sorted(c_dicy.items(), key=lambda x: x[0]))
        color_map = [x for x in c_dicy.values()]
        nx.draw_networkx_nodes(self.G, n_pos, node_color=color_map, node_size=800, node_shape='o')    # 绘制节点
        nx.draw_networkx_edges(self.G, n_pos)                                                         # 绘制边
        nx.draw_networkx_labels(self.G, n_pos, labels=n_map, font_size=5, font_color='k')             # 标签

    #####################################
    #   WCET 配置算法#
    #####################################
    def WCET_Config(self, WCET_Config_type):

        if WCET_Config_type == "random":
            self.wcet_random_config()
        else:
            pass

    def wcet_random_config(self):
        for x in self.G.nodes(data=True):
            x[1]['WCET'] = rand.randint(100, 1000)
            # [x for x in self.G.nodes(data=True) if (x[1].get('state') == 'ready')]

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
        if RTA_Type ==  "non-preemptive":
            return self.rta_basics_non_preemptive(core_num)
        elif RTA_Type ==  "preemptive":
            return self.rta_basics_preemptive(core_num)
        else:
            print("RTA_Type input error!")

    def rta_basics_non_preemptive(self, core_num):
        node_list = list(self.G.nodes())
        paths = list(nx.all_simple_paths(self.G, node_list[0], node_list[-1]))

        interference_node_list = []
        # ret_path_and_rta = []
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
    # plt.figure()            # (figsize=(100.0, 100.0))
    plt.subplot(211)
    G = DAG()               # 初始化DAG
    G.parallelism   = 4     # int(Parallelism)      # 输入并行度
    G.Critical_path = 6     # int(Critical_path)    # 输入关键路径长度
    G.gen("mine")
    # G.user_defined_dag()
    G.graph_node_position_determine()   # DAG节点位置确定

    G.dag_param_critical_update()       # 关键数据分析

    # plt.title('DAG generator' +
    #           '\n Is a DAG:{0}'.format(nx.is_directed_acyclic_graph(G.get_graph())) +  # 检测是否是有向无环图
    #           '\n number of nodes for DAG:{0}'.format(G.G.number_of_nodes()) +  # 返回G的节点数量
    #           '\n number of edges for DAG:{0}'.format(G.G.number_of_edges()) +  # 返回G的边数量
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
