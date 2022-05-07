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
import os
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


# Class: DAG (Directed Acyclic Graph Task)
class DAG:
    #####################################
    #   DAG 参数
    #   param0  DAG name        ：标注DAG，方便存储及调用
    #
    #   param1.1* periodically   ：DAG的周期性质包括{周期性任务； 零星任务； 非周期性任务}
    #       {periodic; sporadic; aperiodic}
    #   param1.2* real_time      ：DAG的实时性包括{Hard Real-time Task； Soft Real-time Task； Firm Real-time Task}
    #       {HRT; SRT; FRT}
    #   param1.3* cycle_time     ： (1)periodically == periodic;  cycle_time = DAG的周期时间
    #                               (2)periodically == sporadic;  cycle_time = DAG的最小间隔时间
    #                               (3)periodically == aperiodic; cycle_time = DAG的释放时间
    #
    #   param2* Deadline        ：DAG的相对截止时间
    #
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
        self.name = 'Tau_{null}'  # DAG的名称
        self.G = nx.DiGraph()  # DAG:-networkX结构
        self.task_num = 0  # DAG中节点（job）的数量
        # generator mine
        self.parallelism = 3  # 并行度
        self.Critical_path = 5  # 关键路径长度

    def get_graph(self):  # 返回G
        return self.G

    def save(self, basefolder="data/"):
        # create base folder (if not exists)
        if not os.path.exists(basefolder):
            os.makedirs(basefolder)
        nx.write_gpickle(self.G, basefolder + self.name + '.gpickle')  # save graph (gpickle)
        nx.write_gml(self.G, basefolder + self.name + '.gml')  # save graph (gml)

    def load(self, basefolder="./data/"):
        pass

    def gen(self, algorithm):  # 生成 DAG
        if algorithm == "mine":
            self.gen_mine()
        else:
            return 1
        return 0

    #####################################
    #   获取DAG的并行度和关键路径长度
    #   DAG generator 算法4#
    #####################################
    def dag_param_critical_update(self):
        # 关键路径
        node_list = nx.dag_longest_path(self.G)
        # 获取拓扑分层
        rank_list = [sorted(generation) for generation in nx.topological_generations(self.G)]
        app = []
        for rank_x in rank_list:
            app.append(len(rank_x))
        self.Critical_path = len(node_list)  # 关键路径长度
        self.parallelism = max(app)
        print('关键路径：{0}'.format(node_list))
        print('拓扑分层：{0}'.format(rank_list))

    #####################################
    #   根据DAG的节点num打印节点的属性；
    #   def node_property
    #   param：
    #       node_number;
    #####################################
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
        node_map        = []
        position_map    = []
        color_map       = []
        str_map         = []

        WCET = nx.get_node_attributes(self.G, 'WCET')
        for edge_xx in self.G.edges(data=True):
            edge_xx[2]['weight'] = WCET[edge_xx[1]]     # WCET[edge_xx[1]]
        node_list       = nx.dag_longest_path(G.get_graph(), weight='weight')  # 关键路径
        # assert self.Critical_path == len(node_list), (self.Critical_path, len(node_list))
        p_list = np.zeros(self.Critical_path, dtype=int)
        for node_xx in self.G.nodes(data=True):
            node_rank = node_xx[1].get('rank')
            if node_xx[0] in node_list:  # 判断是否在关键路径里
                node_xx[1]['critic'] = True
                k = 0
                color = 'green'
            else:
                p_list[node_rank] += 1
                k = p_list[node_rank]
                color = '#1f78b4'
            node_map.append(node_xx[0])
            position_map.append([100 * node_rank / self.Critical_path , 100 * k / self.parallelism])
            str_map.append('ID={0} \n rank={1} \n critic={2} \n WCET={3}'.format(node_xx[1].get('Node_ID'),
                                                                                       node_xx[1].get('rank'),
                                                                                       node_xx[1].get('critic'),
                                                                                       node_xx[1].get('WCET') ))
            color_map.append(color)
        n_pos = dict(zip(node_map, np.array(position_map)))  # 构建pos列表
        n_str = dict(zip(node_map, np.array(str_map)))  # 构建pos列表
        nx.draw_networkx_nodes(self.G, n_pos,
                               nodelist=node_map, node_color=color_map,
                               node_size=5000, node_shape='s')  # 绘制节点
        nx.draw_networkx_edges(self.G, n_pos)  # 绘制边
        nx.draw_networkx_labels(self.G, n_pos, labels=n_str, font_size=10, font_color='k')  # 标签

    #####################################
    #   DAG generator 算法3#
    #####################################
    def gen_mine(self):
        assert (self.parallelism >= 1)
        assert (self.Critical_path >= 3)
        # 步骤一：initial a new graph G               # e.g. G = nx.DiGraph(Index=self.task_num)
        #   添加节点；确定rank的节点
        self_critical_path = self.Critical_path  # 关键路径长度
        self_parallelism = self.parallelism  # 图的并行度
        self_Node_num = 0  # DAG的节点数量
        self.G.add_node(0, Node_ID='souce', rank=0, critic=False, WCET=1)  # 起始节点（1）；rank=0
        for x in range(1, self_critical_path - 1):
            m = randint(1, self_parallelism)  # 随机每层的节点数量（不能大于并行度）
            for y in range(1, m + 1):
                self_Node_num += 1
                self.G.add_node(self_Node_num, Node_ID='job{}'.format(self_Node_num), rank=x, critic=False, WCET=1)
        self.G.add_node(self_Node_num + 1, Node_ID='sink', rank=self_critical_path - 1, critic=False, WCET=1)
        self.task_num = self_Node_num + 2  # +2算上source和sink
        self.G.add_edge(0, 1)
        for x in range(1, self_critical_path - 1):  # 从第2层开始到倒数第二层
            ancestors_list = [node_x for node_x in self.G.nodes(data=True) if (node_x[1].get('rank') < x)]
            descendants_list = [node_x for node_x in self.G.nodes(data=True) if (node_x[1].get('rank') > x)]
            self_list = [node_x for node_x in self.G.nodes(data=True) if (node_x[1].get('rank') == x)]
            successors_list = [node_x for node_x in self.G.nodes(data=True) if (node_x[1].get('rank') == (x + 1))]
            for y in self_list:
                k1 = randint(1, len(ancestors_list))
                k2 = randint(1, len(descendants_list))
                ancestors_group = rand.sample(ancestors_list, k1)
                descendants_group = rand.sample(descendants_list, k2)
                for z in ancestors_group:
                    self.G.add_edge(z[0], y[0])
                for z in descendants_group:
                    self.G.add_edge(y[0], z[0])
            self.G.add_edge(self_list[0][0], successors_list[0][0])
        self.name = 'Tau_{:d}'.format(self.task_num)
        # self.G = nx.DiGraph(self.Matrix)                  # 邻接矩阵生成一个有向图netWorkX；属性全无；
        # ## transitive reduction 传递约简； ## #
        self.transitive_reduction_matrix()  # 更新graph
        # print(np.array(nx.adjacency_matrix(self.G).todense()))
        # self_G = nx.DiGraph(self.transitive_reduction_matrix())     # 1.自己写的方法，
        # lp = list(self_G.edges())                                   # 1.networkx包
        lp = list(nx.transitive_reduction(self.G).edges())  # 2.networkx包
        self.G.clear_edges()
        self.G.add_edges_from(lp)
        # print(np.array(nx.adjacency_matrix(self.G).todense()))

    #####################################
    #   自定义 DAG 算法#
    #####################################
    def user_defined_dag(self):
        # 节点号； 节点名； 节点优权重； 节点优先级
        HE_2019_nodes = [[1, 'V1', 1, 1, 1],
                         [2, 'V2', 3, 7, 5],
                         [3, 'V3', 3,  3, 6],
                         [4, 'V4', 3, 3, 7],
                         [5, 'V5', 2, 6, 2],
                         [6, 'V6', 2, 9, 3],
                         [7, 'V7', 3, 2, 4],
                         [8, 'V8', 4, 1, 8]]
        # for x in self_list:
        # self.G.add_node(0, Node_ID='souce_node', rank=0, critic=False, WCET=1)  # 起始节点（1）；rank=0
        for node_x in HE_2019_nodes:
            self.G.add_node(node_x[0], Node_ID=node_x[1], rank=node_x[2], critic=False, WCET=node_x[3], priority=node_x[4])

        edges = [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6),
                 (5, 7), (6, 7),
                 (2, 8), (3, 8), (4, 8), (7, 8) ]
        for edge in edges:
            self.G.add_edge(edge[0], edge[1], weight=1)
        # self.G.add_edges_from(edges)


if __name__ == "__main__":
    # Parallelism = input("请输入DAG的并行度：")
    # print("你输入的内容是: ", Parallelism)
    # Critical_path = input("请输入DAG的关键路径长度：")
    # print("你输入的内容是: ", Critical_path)
    plt.figure()            # (figsize=(100.0, 100.0))
    G = DAG()               # 初始化DAG
    G.parallelism = 4       # int(Parallelism)      # 输入并行度
    G.Critical_path = 6     # int(Critical_path)    # 输入关键路径长度
    G.gen("mine")
    # G.user_defined_dag()

    G.graph_node_position_determine()

    # G.dag_param_critical_update()

    plt.title('DAG generator' +
              '\n Is a DAG:{0}'.format(nx.is_directed_acyclic_graph(G.get_graph())) +  # 检测是否是有向无环图
              '\n number of nodes for DAG:{0}'.format(G.G.number_of_nodes()) +  # 返回G的节点数量
              '\n number of edges for DAG:{0}'.format(G.G.number_of_edges()) +  # 返回G的边数量
              '',
              fontsize=10, color="black", weight="light", ha='left', x=0)  # style="italic",
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
