#!/usr/bin/python3
# -*- coding: utf-8 -*-

################################################################################
# Dag set
# Fang YJ
# Real-Time Systems Group
# Hunan University HNU
################################################################################

import networkx as nx
import DAG


class DAG_Set:
    def __init__(self):
        self.Dag_Set = []

    #####################################
    #   随机生成一组DAG
    #####################################
    def Random_DAG_Set(self, DAG_count, parallelism_list, critical_path_list):
        for x in range(0, DAG_count):
            Temp_DAG = DAG.DAG()
            Temp_DAG.DAG_ID = "DAG_{}".format(x)
            Temp_DAG.Priority = x + 1
            Temp_DAG.parallelism = parallelism_list[x]
            Temp_DAG.Critical_path = critical_path_list[x]
            Temp_DAG.gen("mine")
            Temp_DAG.WCET_random_config()
            Temp_DAG.priority_random_config()
            Temp_DAG.critical_path_config()
            self.Add_DAG(Temp_DAG)

    def Add_DAG(self, Dag):
        self.Dag_Set.append(Dag)

    #####################################
    #   更新DAG集合中所有DAG节点的状态，
    #   即将所有前驱节点为0，状态为阻塞态的节点
    #   转换为的就绪态状态
    #####################################
    def Status_Dataup(self):
        # step-1.将Temp_DAG_Set中前驱节点为0且未就绪的节点的节点进入就绪队列
        for x in self.Dag_Set:
            for y in x.G.nodes(data=True):
                if (len(list(x.G.predecessors(y[0]))) == 0) and (y[1].get('state') == 'blocked'):
                    y[1]['state'] = 'ready'

    #####################################
    #   获取DAG集合的数量#
    #####################################
    def get_dag_num(self):
        return len(self.Dag_Set)

    #####################################
    #   获取DAG集合中所有节点的数量#
    #####################################
    def get_node_num(self):
        temp_node_num = 0
        for x in self.Dag_Set:
            temp_node_num += x.get_node_num()
        return temp_node_num

    #####################################
    #   获取DAG集合中所有就绪节点
    #####################################
    def get_ready_node(self):
        temp_dict = {}
        for x in self.Dag_Set:
            temp_ready_list = x.get_ready_node_list()
            temp_dict[x.DAG_ID] = temp_ready_list
        return temp_dict

    def get_priorituy_ready_node(self):
        temp_dict = {}
        r_dict = {}
        for x in self.Dag_Set:
            temp_dict[x] = x.Priority
        temp_dict = sorted(temp_dict.items(), key=lambda x: x[1])
        for k, v in temp_dict:
            DAG_ID = k.DAG_ID
            temp_ready_list = k.get_ready_node_list()
            if len(temp_ready_list) > 0:
                run_node = temp_ready_list[0]
                for x in temp_ready_list:
                    if x[1].get('priority') < run_node[1].get('priority'):
                        run_node = x
                return DAG_ID, run_node
        return False, False

    def get_priorituy_ready_node_list(self):
        temp_dict = {}
        r_dict = {}
        for x in self.Dag_Set:
            temp_dict[x] = x.Priority
        temp_dict = sorted(temp_dict.items(), key=lambda x: x[1])
        for k, v in temp_dict:
            DAG_ID = k.DAG_ID
            temp_ready_list = k.get_ready_node_list()
            if len(temp_ready_list) > 0:
                for x in range(0,len(temp_ready_list)):
                    r_dict[x] = temp_ready_list[x][1].get('priority')
                ret = sorted(r_dict.items(), key=lambda x: x[1])
                return DAG_ID, temp_ready_list[ret[0][0]]
        return False, False

    def delet_DAG_Node(self, DAG_ID, Node_ID):
        for x in self.Dag_Set:
            if x.DAG_ID == DAG_ID:
                x.G.remove_node(Node_ID)

    #####################################
    #   Show_DAG_Set
    #####################################
    def Show_DAG_Set(self):
        print("DAG_num:", len(self.Dag_Set))
        print("")
        for x in self.Dag_Set:
            x.show_dag()

    #####################################
    #   自定义 DAG 算法#
    #####################################
    def user_defined_dag(self):
        """
        # 节点号； 节点名； 节点优权重； 节点优先级
        HE_2019_nodes = [[1, 'V1', 1, 1],
                         [2, 'V2', 7, 5],
                         [3, 'V3', 3, 6],
                         [4, 'V4', 3, 7],
                         [5, 'V5', 6, 2],
                         [6, 'V6', 9, 3],
                         [7, 'V7', 2, 4],
                         [8, 'V8', 1, 8]]
        for node_x in HE_2019_nodes:
            self.G.add_node(node_x[0], Node_ID=node_x[1], rank=0, critic=False, WCET=node_x[2], priority=node_x[3])

        edges = [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6),
                 (5, 7), (6, 7), (2, 8), (3, 8), (4, 8), (7, 8)]
        for edge in edges:
            self.G.add_edge(edge[0], edge[1], weight=1)

        HE_2019_nodes = [[1, 'V1', 15120, 0],
                         [2, 'V2', 14861, 2],
                         [3, 'V3', 14824, 5],
                         [4, 'V4', 8848, 1],
                         [5, 'V5', 8153, 3],
                         [6, 'V6', 8315, 7],
                         [7, 'V7', 4546, 4],
                         [8, 'V8', 5667, 6],
                         [9, 'V9', 3320, 8],
                         [10, 'V10', 24346, 9]]
        for node_x in HE_2019_nodes:
            self.G.add_node(node_x[0], Node_ID=node_x[1], rank=0, critic=False, WCET=node_x[2], priority=node_x[3])

        edges = [(1, 2), (2, 3), (2, 4), (2, 5), (3, 6), (3, 8),
                 (4, 6), (4, 8), (4, 9), (5, 7), (5, 9), (6, 10), (7, 10), (8, 10), (9, 10) ]
        for edge in edges:
            self.G.add_edge(edge[0], edge[1], weight=1)
        """

        """
        # 模块1-场景1（2核1流）-情况1 DAG
        # 节点号； 节点名； 节点优权重； 节点优先级
        Temp_Dag1 = nx.DiGraph()
        Temp_Dag1.add_node(1,  Node_ID='Job-29-1', rank=0, critic=False, WCET=1500,   priority=1, state='blocked')
        Temp_Dag1.add_node(2,  Node_ID='Job-29-2', rank=0, critic=False, WCET=23232,  priority=13, state='blocked')
        Temp_Dag1.add_node(3,  Node_ID='Job-36',   rank=0, critic=False, WCET=30000,  priority=12, state='blocked')
        Temp_Dag1.add_node(4,  Node_ID='Job-4-1',  rank=0, critic=False, WCET=45936,  priority=2, state='blocked')
        Temp_Dag1.add_node(5,  Node_ID='Job-35',   rank=0, critic=False, WCET=16772,  priority=14, state='blocked')
        Temp_Dag1.add_node(6,  Node_ID='Job-10',   rank=0, critic=False, WCET=46548,  priority=4, state='blocked')
        Temp_Dag1.add_node(7,  Node_ID='Job-4-2',  rank=0, critic=False, WCET=51348,  priority=3, state='blocked')
        Temp_Dag1.add_node(8,  Node_ID='Job-4-3',  rank=0, critic=False, WCET=269720, priority=5, state='blocked')
        Temp_Dag1.add_node(9,  Node_ID='Job-4-4',  rank=0, critic=False, WCET=123376, priority=6, state='blocked')
        Temp_Dag1.add_node(10, Node_ID='Job-11',   rank=0, critic=False, WCET=117972, priority=7, state='blocked')
        Temp_Dag1.add_node(11, Node_ID='Job-4-5',  rank=0, critic=False, WCET=19316,  priority=8, state='blocked')
        Temp_Dag1.add_node(12, Node_ID='Job-4-6',  rank=0, critic=False, WCET=37048,  priority=9, state='blocked')
        Temp_Dag1.add_node(13, Node_ID='Job-12',   rank=0, critic=False, WCET=33424,  priority=10, state='blocked')
        Temp_Dag1.add_node(14, Node_ID='Job-4-7',  rank=0, critic=False, WCET=31812,  priority=11, state='blocked')

        Temp_Dag1.add_edge(1, 2, weight=1)
        Temp_Dag1.add_edge(1, 3, weight=1)
        Temp_Dag1.add_edge(1, 4, weight=1)
        Temp_Dag1.add_edge(1, 5, weight=1)
        Temp_Dag1.add_edge(4, 6, weight=1)
        Temp_Dag1.add_edge(4, 7, weight=1)
        Temp_Dag1.add_edge(7, 8, weight=1)
        Temp_Dag1.add_edge(6, 8, weight=1)
        Temp_Dag1.add_edge(8, 9, weight=1)
        Temp_Dag1.add_edge(8, 10,weight=1)
        Temp_Dag1.add_edge(9, 11, weight=1)
        Temp_Dag1.add_edge(10,11,weight=1)
        Temp_Dag1.add_edge(11,12,weight=1)
        Temp_Dag1.add_edge(11,13,weight=1)
        Temp_Dag1.add_edge(13,14,weight=1)
        Temp_Dag1.add_edge(12,14,weight=1)

        # 模块1-场景2（3核2流）-情况1
        Temp_Dag2 = nx.DiGraph()
        Temp_Dag2.add_node(1,  Node_ID='Job-29-1',   rank=0, critic=False, WCET=1500,   priority=1, state='blocked')
        Temp_Dag2.add_node(2,  Node_ID='Job-29-2',   rank=0, critic=False, WCET=34276,  priority=26, state='blocked')
        Temp_Dag2.add_node(3,  Node_ID='Job-36(1)',  rank=0, critic=False, WCET=32220,  priority=29, state='blocked')
        Temp_Dag2.add_node(4,  Node_ID='Job-36(2)',  rank=0, critic=False, WCET=32220,  priority=30, state='blocked')
        Temp_Dag2.add_node(5,  Node_ID='Job-4-1(1)', rank=0, critic=False, WCET=40920,  priority=2, state='blocked')
        Temp_Dag2.add_node(6,  Node_ID='Job-4-1(2)', rank=0, critic=False, WCET=40920,  priority=14, state='blocked')
        Temp_Dag2.add_node(7,  Node_ID='Job-35(1)',  rank=0, critic=False, WCET=20000,  priority=31, state='blocked')
        Temp_Dag2.add_node(8,  Node_ID='Job-35(2)',  rank=0, critic=False, WCET=20000,  priority=32, state='blocked')
        Temp_Dag2.add_node(9, Node_ID='Job-10(1)',   rank=0, critic=False, WCET=36392,  priority=4, state='blocked')
        Temp_Dag2.add_node(10, Node_ID='Job-10(2)',  rank=0, critic=False, WCET=36392,  priority=5, state='blocked')
        Temp_Dag2.add_node(11, Node_ID='Job-10(3)',  rank=0, critic=False, WCET=36392,  priority=16, state='blocked')
        Temp_Dag2.add_node(12, Node_ID='Job-10(4)',  rank=0, critic=False, WCET=36392,  priority=17, state='blocked')
        Temp_Dag2.add_node(13, Node_ID='Job-4-2(1)', rank=0, critic=False, WCET=127908, priority=3, state='blocked')
        Temp_Dag2.add_node(14, Node_ID='Job-4-2(2)', rank=0, critic=False, WCET=127908, priority=15, state='blocked')
        Temp_Dag2.add_node(15, Node_ID='Job-4-3(1)', rank=0, critic=False, WCET=292952, priority=6, state='blocked')
        Temp_Dag2.add_node(16, Node_ID='Job-4-3(2)', rank=0, critic=False, WCET=292952, priority=18, state='blocked')
        Temp_Dag2.add_node(17, Node_ID='Job-4-4(1)', rank=0, critic=False, WCET=172964, priority=7, state='blocked')
        Temp_Dag2.add_node(18, Node_ID='Job-4-4(2)', rank=0, critic=False, WCET=172964, priority=19, state='blocked')
        Temp_Dag2.add_node(19, Node_ID='Job-11(1)',  rank=0, critic=False, WCET=90936,  priority=8, state='blocked')
        Temp_Dag2.add_node(20, Node_ID='Job-11(2)',  rank=0, critic=False, WCET=90936,  priority=9, state='blocked')
        Temp_Dag2.add_node(21, Node_ID='Job-11(3)',  rank=0, critic=False, WCET=90936,  priority=20, state='blocked')
        Temp_Dag2.add_node(22, Node_ID='Job-11(4)',  rank=0, critic=False, WCET=90936,  priority=21, state='blocked')
        Temp_Dag2.add_node(23, Node_ID='Job-4-5(1)', rank=0, critic=False, WCET=22264,  priority=10, state='blocked')
        Temp_Dag2.add_node(24, Node_ID='Job-4-5(2)', rank=0, critic=False, WCET=22264,  priority=22, state='blocked')
        Temp_Dag2.add_node(25, Node_ID='Job-4-6(1)', rank=0, critic=False, WCET=126632, priority=11, state='blocked')
        Temp_Dag2.add_node(26, Node_ID='Job-4-6(2)', rank=0, critic=False, WCET=126632, priority=23, state='blocked')
        Temp_Dag2.add_node(27, Node_ID='Job-12(1)',  rank=0, critic=False, WCET=32136,  priority=12, state='blocked')
        Temp_Dag2.add_node(28, Node_ID='Job-12(2)',  rank=0, critic=False, WCET=32136,  priority=13, state='blocked')
        Temp_Dag2.add_node(29, Node_ID='Job-12(3)',  rank=0, critic=False, WCET=32136,  priority=24, state='blocked')
        Temp_Dag2.add_node(30, Node_ID='Job-12(4)',  rank=0, critic=False, WCET=32136,  priority=25, state='blocked')
        Temp_Dag2.add_node(31, Node_ID='Job-4-7(1)', rank=0, critic=False, WCET=34056,  priority=27, state='blocked')
        Temp_Dag2.add_node(32, Node_ID='Job-4-7(2)', rank=0, critic=False, WCET=34056,  priority=28, state='blocked')

        Temp_Dag2.add_edge(1, 2, weight=1)
        Temp_Dag2.add_edge(1, 3, weight=1)
        Temp_Dag2.add_edge(1, 4, weight=1)
        Temp_Dag2.add_edge(1, 5, weight=1)
        Temp_Dag2.add_edge(1, 6, weight=1)
        Temp_Dag2.add_edge(1, 7, weight=1)
        Temp_Dag2.add_edge(1, 8, weight=1)
        Temp_Dag2.add_edge(5, 9, weight=1)
        Temp_Dag2.add_edge(5, 10, weight=1)
        Temp_Dag2.add_edge(5, 13, weight=1)
        Temp_Dag2.add_edge(6, 11, weight=1)
        Temp_Dag2.add_edge(6, 12, weight=1)
        Temp_Dag2.add_edge(6, 14, weight=1)
        Temp_Dag2.add_edge(9, 15, weight=1)
        Temp_Dag2.add_edge(10,15, weight=1)
        Temp_Dag2.add_edge(13,15, weight=1)
        Temp_Dag2.add_edge(11, 16, weight=1)
        Temp_Dag2.add_edge(12, 16, weight=1)
        Temp_Dag2.add_edge(14, 16, weight=1)
        Temp_Dag2.add_edge(15, 17, weight=1)
        Temp_Dag2.add_edge(15, 19, weight=1)
        Temp_Dag2.add_edge(15, 20, weight=1)
        Temp_Dag2.add_edge(16, 18, weight=1)
        Temp_Dag2.add_edge(16, 21, weight=1)
        Temp_Dag2.add_edge(16, 22, weight=1)
        Temp_Dag2.add_edge(17, 23, weight=1)
        Temp_Dag2.add_edge(18, 24, weight=1)
        Temp_Dag2.add_edge(19, 23, weight=1)
        Temp_Dag2.add_edge(20, 23, weight=1)
        Temp_Dag2.add_edge(21, 24, weight=1)
        Temp_Dag2.add_edge(22, 24, weight=1)
        Temp_Dag2.add_edge(23, 25, weight=1)
        Temp_Dag2.add_edge(23, 27, weight=1)
        Temp_Dag2.add_edge(23, 28, weight=1)
        Temp_Dag2.add_edge(24, 26, weight=1)
        Temp_Dag2.add_edge(24, 29, weight=1)
        Temp_Dag2.add_edge(24, 30, weight=1)
        Temp_Dag2.add_edge(25, 31, weight=1)
        Temp_Dag2.add_edge(27, 31, weight=1)
        Temp_Dag2.add_edge(28, 31, weight=1)
        Temp_Dag2.add_edge(26, 32, weight=1)
        Temp_Dag2.add_edge(29, 32, weight=1)
        Temp_Dag2.add_edge(30, 32, weight=1)
        """
        # blocked ready running
        """
         # 模块1-场景1（2核1流）-情况2 DAG
        Temp_Dag1 = nx.DiGraph()
        Temp_Dag1.add_node(1, Node_ID='Job-29-1', rank=0, critic=False, WCET=1500,  priority=1, state='blocked')
        Temp_Dag1.add_node(2, Node_ID='Job-29-2', rank=0, critic=False, WCET=23232, priority=4, state='blocked')
        Temp_Dag1.add_node(3, Node_ID='Job-36',   rank=0, critic=False, WCET=30000, priority=3, state='blocked')
        Temp_Dag1.add_node(4, Node_ID='Job-4',    rank=0, critic=False, WCET=36236, priority=2, state='blocked')
        Temp_Dag1.add_node(5, Node_ID='Job-35',   rank=0, critic=False, WCET=16772, priority=5, state='blocked')

        Temp_Dag1.add_edge(1, 2, weight=1)
        Temp_Dag1.add_edge(1, 3, weight=1)
        Temp_Dag1.add_edge(1, 4, weight=1)
        Temp_Dag1.add_edge(1, 5, weight=1)

        # 模块1-场景2（3核2流）-情况2 DAG
        Temp_Dag2 = nx.DiGraph()
        Temp_Dag2.add_node(1, Node_ID='Job-29-1', rank=0, critic=False, WCET=1500, priority=1, state='blocked')
        Temp_Dag2.add_node(2, Node_ID='Job-29-2', rank=0, critic=False, WCET=34276, priority=4, state='blocked')
        Temp_Dag2.add_node(3, Node_ID='Job-36-1', rank=0, critic=False, WCET=32220, priority=5, state='blocked')
        Temp_Dag2.add_node(4, Node_ID='Job-36-2', rank=0, critic=False, WCET=32220, priority=6, state='blocked')
        Temp_Dag2.add_node(5, Node_ID='Job-35-1', rank=0, critic=False, WCET=20000, priority=7, state='blocked')
        Temp_Dag2.add_node(6, Node_ID='Job-35-2', rank=0, critic=False, WCET=20000, priority=8, state='blocked')
        Temp_Dag2.add_node(7, Node_ID='Job-4-1', rank=0, critic=False, WCET=39716, priority=2, state='blocked')
        Temp_Dag2.add_node(8, Node_ID='Job-4-2', rank=0, critic=False, WCET=39716, priority=3, state='blocked')

        Temp_Dag2.add_edge(1, 2, weight=1)
        Temp_Dag2.add_edge(1, 3, weight=1)
        Temp_Dag2.add_edge(1, 4, weight=1)
        Temp_Dag2.add_edge(1, 5, weight=1)
        Temp_Dag2.add_edge(1, 6, weight=1)
        Temp_Dag2.add_edge(1, 7, weight=1)
        Temp_Dag2.add_edge(1, 8, weight=1)
"""
        # 模块2-场景1（2核1流）-情况1 DAG
        """    """
        Temp_Dag1 = nx.DiGraph()
        node_list = [[1, 'Job-0(1)',    3032,   1],
                     [2, 'Job-1(1)',     196196, 2],
                     [3, 'Job-3-1_1(1)', 89624,  3],
                     [4, 'Job-3-1_2(1)', 89624,  4],
                     [5, 'Job-3-1_3(1)', 89624,  5],
                     [6, 'Job-3-1_4(1)', 89624,  6],
                     [7, 'Job-3-2(1)',   89056,  7],
                     [8, 'Job-7_1(1)',   52492,  8],
                     [9, 'Job-7_2(1)',   52492,  9],
                     [10, 'Job-7_3(1)',  52492,  10],
                     [11, 'Job-7_4(1)',  52492,  11],
                     [12, 'Job-3-3(1)',  39996,  12]]
        for node_x in node_list:
            Temp_Dag1.add_node(node_x[0], Node_ID=node_x[1], rank=0,
                               critic=False, WCET=node_x[2], priority=node_x[3], state='blocked')

        edges = [(1, 2),  (2, 3), (2, 4), (2, 5), (2, 6),
                 (3, 7), (4, 7), (5, 7), (6, 7),
                 (7, 8), (7, 9), (7, 10), (7, 11), (7, 12)]
        for edge in edges:
            Temp_Dag1.add_edge(edge[0], edge[1], weight=1)

        # 模块2-场景2（3核2流）-情况1 DAG
        Temp_Dag2 = nx.DiGraph()
        node_list = [[1,  'Job-0(2)',     6732,   1],
                     [2,  'Job-1_1(2)',   264088, 2],
                     [3,  'Job-1_2(2)',   264088, 8],
                     [4,  'Job-3-1_1(2)', 118764, 3],
                     [5,  'Job-3-1_2(2)', 118764, 4],
                     [6,  'Job-3-1_3(2)', 118764, 5],
                     [7,  'Job-3-1_4(2)', 118764, 6],
                     [8,  'Job-3-1_5(2)', 118764, 9],
                     [9,  'Job-3-1_6(2)', 118764, 10],
                     [10, 'Job-3-1_7(2)', 118764, 11],
                     [11, 'Job-3-1_8(2)', 118764, 12],
                     [12, 'Job-3-2_1(2)', 97020,  7],
                     [13, 'Job-3-2_2(2)', 97020,  13],
                     [14, 'Job-7_1(2)',   75460,  14],
                     [15, 'Job-7_2(2)',   75460,  15],
                     [16, 'Job-7_3(2)',   75460,  15],
                     [17, 'Job-7_4(2)',   75460,  17],
                     [18, 'Job-7_5(2)',   75460,  18],
                     [19, 'Job-7_6(2)',   75460,  19],
                     [20, 'Job-7_7(2)',   75460,  20],
                     [21, 'Job-7_8(2)',   75460,  21],
                     [22, 'Job-3-3_1(2)', 55264,  22],
                     [23, 'Job-3-3_2(2)', 55264,  23] ]
        for node_x in node_list:
            Temp_Dag2.add_node(node_x[0], Node_ID=node_x[1], rank=0,
                               critic=False, WCET=node_x[2], priority=node_x[3], state='blocked')

        edges = [(1, 2),  (1, 3),
                 (2, 4),  (2, 5),  (2, 6),  (2, 7),
                 (3, 8),  (3, 9),  (3, 10), (3, 11),
                 (4, 12), (5, 12), (6, 12), (7, 12),
                 (8, 13), (9, 13), (10, 13), (11, 13),
                 (12, 14), (12, 15), (12, 16), (12, 17), (12, 22),
                 (13, 18), (13, 19), (13, 20), (13, 21), (13, 23)
                 ]
        for edge in edges:
            Temp_Dag2.add_edge(edge[0], edge[1], weight=1)

        # 模块2-场景3（5核6流）-情况1 DAG
        Temp_Dag3 = nx.DiGraph()
        node_list1 = [[1,  'Job-0(3)',      10000,  1],
                      [2,  'Job-1_1(3)',    290488, 2],
                      [3,  'Job-3-1_1(3)',  100000, 3],
                      [4,  'Job-3-1_2(3)',  100000, 4],
                      [5,  'Job-3-1_3(3)',  100000, 5],
                      [6,  'Job-3-1_4(3)',  100000, 6],
                      [7,  'Job-3-2_1(3)',  96008,  7],
                      [8,  'Job-1_2(3)',    290488, 8],
                      [9,  'Job-1_3(3)',    290488, 9],
                      [10, 'Job-1_4(3)',    290488, 10],
                      [11, 'Job-1_5(3)',    290488, 11],
                      [12, 'Job-1_6(3)',    290488, 12],
                      [13, 'Job-3-1_5(3)',  100000, 13],
                      [14, 'Job-3-1_6(3)',  100000, 14],
                      [15, 'Job-3-1_7(3)',  100000, 15],
                      [16, 'Job-3-1_8(3)',  100000, 16],
                      [17, 'Job-3-1_9(3)',  100000, 17],
                      [18, 'Job-3-1_10(3)', 100000, 18],
                      [19, 'Job-3-1_11(3)', 100000, 19],
                      [20, 'Job-3-1_12(3)', 100000, 20],
                      [21, 'Job-3-1_13(3)', 100000, 21],
                      [22, 'Job-3-1_14(3)', 100000, 22],
                      [23, 'Job-3-1_15(3)', 100000, 23],
                      [24, 'Job-3-1_16(3)', 100000, 24],
                      [25, 'Job-3-1_17(3)', 100000, 25],
                      [26, 'Job-3-1_18(3)', 100000, 26],
                      [27, 'Job-3-1_19(3)', 100000, 27],
                      [28, 'Job-3-1_20(3)', 100000, 28],
                      [29, 'Job-3-1_21(3)', 100000, 29],
                      [30, 'Job-3-1_22(3)', 100000, 30],
                      [31, 'Job-3-1_23(3)', 100000, 31],
                      [32, 'Job-3-1_24(3)', 100000, 32],
                      [33, 'Job-3-2_2(3)',  96008,  33],
                      [34, 'Job-3-2_3(3)',  96008,  34],
                      [35, 'Job-3-2_4(3)',  96008,  35],
                      [36, 'Job-3_2_5(3)',  96008,  36],
                      [37, 'Job-3_2_6(3)',  96008,  37],
                      [38, 'Job 7_1(3)',    87560,  38],
                      [39, 'Job 7_2(3)',    87560,  39],
                      [40, 'Job 7_3(3)',    87560,  40],
                      [41, 'Job 7_4(3)',    87560,  41],
                      [42, 'Job 7_5(3)',    87560,  42],
                      [43, 'Job 7_6(3)',    87560,  43],
                      [44, 'Job 7_7(3)',    87560,  44],
                      [45, 'Job 7_8(3)',    87560,  45],
                      [46, 'Job 7_9(3)',    87560,  46],
                      [47, 'Job 7_10(3)',   87560,  47],
                      [48, 'Job 7_11(3)',   87560,  48],
                      [49, 'Job 7_12(3)',   87560,  49],
                      [50, 'Job 7_13(3)',   87560,  50],
                      [51, 'Job 7_14(3)',   87560,  51],
                      [52, 'Job 7_15(3)',   87560,  52],
                      [53, 'Job 7_16(3)',   87560,  53],
                      [54, 'Job 7_17(3)',   87560,  54],
                      [55, 'Job 7_18(3)',   87560,  55],
                      [56, 'Job 7_19(3)',   87560,  56],
                      [57, 'Job 7_20(3)',   87560,  57],
                      [58, 'Job 7_21(3)',   87560,  58],
                      [59, 'Job 7_22(3)',   87560,  59],
                      [60, 'Job 7_23(3)',   87560,  60],
                      [61, 'Job 7_24(3)',   87560,  61],
                      [62, 'Job 3-3_1(3)',  57332,  62],
                      [63, 'Job 3-3_2(3)',  57332,  63],
                      [64, 'Job 3-3_3(3)',  57332,  64],
                      [65, 'Job 3-3_4(3)',  57332,  65],
                      [66, 'Job 3-3_5(3)',  57332,  66],
                      [67, 'Job 3-3_6(3)',  57332,  67]
                         ]
        for node_x in node_list1:
            Temp_Dag3.add_node(node_x[0], Node_ID=node_x[1], rank=0,
                               critic=False, WCET=node_x[2], priority=node_x[3], state='blocked')

        edge1 = [(1, 2),  (1, 8), (1, 9), (1, 10), (1, 11),  (1, 12),
                 (2, 3),  (2, 4), (2, 5), (2, 6),
                 (8, 13), (8, 14), (8, 15), (8, 16),
                 (9, 17), (9, 18), (9, 19), (9, 20),
                 (10, 21), (10, 22), (10, 23), (10, 24),
                 (11, 25), (11, 26), (11, 27), (11, 28),
                 (12, 29), (12, 30), (12, 31), (12, 32),

                 (3, 7), (4, 7), (5, 7), (6, 7),
                 (13, 33), (14, 33), (15, 33), (16, 33),
                 (17, 34), (18, 34), (19, 34), (20, 34),
                 (21, 35), (22, 35), (23, 35), (24, 35),
                 (25, 36), (26, 36), (27, 36), (28, 36),
                 (29, 37), (30, 37), (31, 37), (32, 37),

                 (7,  38), (7, 39), (7, 40), (7, 41), (7, 62),
                 (33, 42), (33, 43), (33, 44), (33, 45), (33, 63),
                 (34, 46), (34, 47), (34, 48), (34, 49), (34, 64),
                 (35, 50), (35, 51), (35, 52), (35, 53), (35, 65),
                 (36, 54), (36, 55), (36, 56), (36, 57), (36, 66),
                 (37, 58), (37, 59), (37, 60), (37, 61),  (37, 67)
                 ]
        for edge in edge1:
            Temp_Dag3.add_edge(edge[0], edge[1], weight=1)
        """   """
        # 模块2-场景1（2核1流）-情况2 DAG
        """
        Temp_Dag1 = nx.DiGraph()
        node_list = [[1, 'Job-0(1)',    3032, 1],
                     [2, 'Job-3-1(1)', 89840, 2] ]
        for node_x in node_list:
            Temp_Dag1.add_node(node_x[0], Node_ID=node_x[1], rank=0,
                               critic=False, WCET=node_x[2], priority=node_x[3], state='blocked')
        edges = [(1, 2)]
        for edge in edges:
            Temp_Dag1.add_edge(edge[0], edge[1], weight=1)
        # 模块2-场景2（3核2流）-情况2 DAG
        Temp_Dag2 = nx.DiGraph()
        node_list = [[1, 'Job-0(2)',    6732,  1],
                     [2, 'Job-1_1(2)', 108328, 2],
                     [3, 'Job-1_2(2)', 108328, 3]]
        for node_x in node_list:
            Temp_Dag2.add_node(node_x[0], Node_ID=node_x[1], rank=0,
                               critic=False, WCET=node_x[2], priority=node_x[3], state='blocked')
        edges = [(1, 2), (1, 3)]
        for edge in edges:
            Temp_Dag2.add_edge(edge[0], edge[1], weight=1)
        # 模块2-场景3（5核6流）-情况2 DAG
        Temp_Dag3 = nx.DiGraph()
        node_list = [[1, 'Job-0(3)',  10000,   1],
                     [2, 'Job-1_1(3)', 120000, 2],
                     [3, 'Job-1_2(3)', 120000, 3],
                     [4, 'Job-1_3(3)', 120000, 4],
                     [5, 'Job-1_4(3)', 120000, 5],
                     [6, 'Job-1_5(3)', 120000, 6],
                     [7, 'Job-1_6(3)', 120000, 7]]
        for node_x in node_list:
            Temp_Dag3.add_node(node_x[0], Node_ID=node_x[1], rank=0,
                               critic=False, WCET=node_x[2], priority=node_x[3], state='blocked')
        edges = [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7)]
        for edge in edges:
            Temp_Dag3.add_edge(edge[0], edge[1], weight=1)
        """
        G1 = DAG.DAG()
        G1.G = Temp_Dag1
        G1.DAG_ID = "DAG_1"
        G1.Priority = 3
        G1.critical_path_config()

        G2 = DAG.DAG()
        G2.G = Temp_Dag2
        G2.DAG_ID = "DAG_2"
        G2.Priority = 2
        G2.critical_path_config()

        G3 = DAG.DAG()
        G3.G = Temp_Dag3
        G3.DAG_ID = "DAG_3"
        G3.Priority = 1
        G3.critical_path_config()
        self.Add_DAG(G1)
        self.Add_DAG(G2)
        # self.Add_DAG(G3)


if __name__ == "__main__":
    dagset = DAG_Set()
    dagset.user_defined_dag()
    dagset.Show_DAG_Set()
    """
    # 字典排序
    a = {'a': 3, 'c': 89, 'b': 0, 'd': 34}
    # 按照字典的值进行排序
    a1 = sorted(a.items(), key=lambda x: x[1])
    # 按照字典的键进行排序
    a2 = sorted(a.items(), key=lambda x: x[0])
    print('按值排序后结果', a1)
    print('按键排序后结果', a2)
    print('结果转为字典格式', dict(a1))
    print('结果转为字典格式', dict(a2))
    # # 节点号； 节点名； 节点优权重； 节点优先级
    # plt.subplot()
    # p = Dispatcher()
    # p.user_defined_dag_1()
    # print(p.Mapping([3]))
    # p.Show_Dag()
    # plt.show()
    """


