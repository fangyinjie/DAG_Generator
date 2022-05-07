import networkx as nx
import matplotlib.pyplot as plt
import DAG

from random import randint, random, uniform
import random
import random as rand
import numpy as np
import os
import minmaxplus


class DAG_Set:
    def __init__(self):
        self.Dag_Set = []

    def Add_DAG(self, DAG):
        self.Dag_Set.append(DAG)

    def Self_Construct(self):
        self.DagSetNum  = len(self.Dag_Set)

    def Show_Dag(self):
        color_map = []
        n_pos = {}
        n_map = {}
        rank_list = [sorted(generation) for generation in nx.topological_generations(self.G)]
        # print('拓扑分层：{0}'.format(rank_list))
        for z1 in range(0, len(rank_list)):
            for z2 in range(0, len(rank_list[z1])):
                node_ID = rank_list[z1][z2]
                sub_node = self.G.node[node_ID]
                n_pos[node_ID] = [(z1 + 0.5) * 120 / len(rank_list), (z2 + 0.5) * 120 / len(rank_list[z1])]
                n_map[node_ID] = 'ID:{0} \n WCET:{1}'.format(
                    sub_node.get('Node_ID'),
                    sub_node.get('WCET'))
                if sub_node['critic']:
                    color = 'green'
                else:
                    color = '#1f78b4'
                color_map.append(color)
        nx.draw_networkx_nodes(self.G, n_pos, node_color=color_map, node_size=2500, node_shape='o')  # 绘制节点
        nx.draw_networkx_edges(self.G, n_pos)  # 绘制边
        nx.draw_networkx_labels(self.G, n_pos, labels=n_map, font_size=10, font_color='k')  # 标签

    #####################################
    #   关键路径配置
    #####################################
    def critical_path_config(self, cp_Dag):
        WCET = nx.get_node_attributes(cp_Dag, 'WCET')
        for edge_x in cp_Dag.edges(data=True):
            edge_x[2]['weight'] = WCET[edge_x[1]]
        node_list = nx.dag_longest_path(cp_Dag, weight='weight')  # 关键路径
        for node_xx in cp_Dag.nodes(data=True):
            if node_xx[0] in node_list:  # 判断是否在关键路径里
                node_xx[1]['critic'] = True

    #####################################
    #   获取DAG集合的数量#
    #####################################
    def get_dag_num(self):
        return len(self.Dag_Set)

    #####################################
    #   Show_DAG_Set
    #####################################
    def Show_DAG_Set(self):
        return len(self.Dag_Set)

    #####################################
    #   自定义 DAG 算法#
    #####################################
    def user_defined_dag(self):
        # 节点号； 节点名； 节点优权重； 节点优先级
        # 模块1-场景1（2核1流）-情况1 DAG
        # Temp_Dag1 = nx.DiGraph()
        #
        # Temp_Dag1.add_node(1,  Node_ID='Job-29-1', rank=0, critic=False, WCET=1500, priority=0)
        # Temp_Dag1.add_node(2,  Node_ID='Job-29-2', rank=0, critic=False, WCET=23232, priority=0)
        # Temp_Dag1.add_node(3,  Node_ID='Job-36',   rank=0, critic=False, WCET=30000, priority=0)
        # Temp_Dag1.add_node(4,  Node_ID='Job-4-1',  rank=0, critic=False, WCET=45936, priority=0)
        # Temp_Dag1.add_node(5,  Node_ID='Job-35',   rank=0, critic=False, WCET=16772, priority=0)
        # Temp_Dag1.add_node(6,  Node_ID='Job-10',   rank=0, critic=False, WCET=46548, priority=0)
        # Temp_Dag1.add_node(7,  Node_ID='Job-4-2',  rank=0, critic=False, WCET=51348, priority=0)
        # Temp_Dag1.add_node(8,  Node_ID='Job-4-3',  rank=0, critic=False, WCET=269720, priority=0)
        # Temp_Dag1.add_node(9,  Node_ID='Job-4-4',  rank=0, critic=False, WCET=123376, priority=0)
        # Temp_Dag1.add_node(10, Node_ID='Job-11',   rank=0, critic=False, WCET=117972, priority=0)
        # Temp_Dag1.add_node(11, Node_ID='Job-4-5',  rank=0, critic=False, WCET=19316, priority=0)
        # Temp_Dag1.add_node(12, Node_ID='Job-4-6',  rank=0, critic=False, WCET=37048, priority=0)
        # Temp_Dag1.add_node(13, Node_ID='Job-12',   rank=0, critic=False, WCET=33424, priority=0)
        # Temp_Dag1.add_node(14, Node_ID='Job-4-7',  rank=0, critic=False, WCET=31812, priority=0)
        #
        # Temp_Dag1.add_edge(1, 2, weight=1)
        # Temp_Dag1.add_edge(1, 3, weight=1)
        # Temp_Dag1.add_edge(1, 4, weight=1)
        # Temp_Dag1.add_edge(1, 5, weight=1)
        # Temp_Dag1.add_edge(4, 6, weight=1)
        # Temp_Dag1.add_edge(4, 7, weight=1)
        # Temp_Dag1.add_edge(7, 8, weight=1)
        # Temp_Dag1.add_edge(6, 8, weight=1)
        # Temp_Dag1.add_edge(8, 9, weight=1)
        # Temp_Dag1.add_edge(8, 10,weight=1)
        # Temp_Dag1.add_edge(9, 11, weight=1)
        # Temp_Dag1.add_edge(10,11,weight=1)
        # Temp_Dag1.add_edge(11,12,weight=1)
        # Temp_Dag1.add_edge(11,13,weight=1)
        # Temp_Dag1.add_edge(13,14,weight=1)
        # Temp_Dag1.add_edge(12,14,weight=1)
        #
        # # 模块1-场景2（3核2流）-情况1
        # Temp_Dag2 = nx.DiGraph()
        # Temp_Dag2.add_node(1,  Node_ID='Job-29-1', rank=0, critic=False, WCET=1500, priority=0)
        # Temp_Dag2.add_node(2,  Node_ID='Job-29-2', rank=0, critic=False, WCET=23232, priority=0)
        # Temp_Dag2.add_node(3,  Node_ID='Job-36',   rank=0, critic=False, WCET=30000, priority=0)
        # Temp_Dag2.add_node(4,  Node_ID='Job-4-1',  rank=0, critic=False, WCET=45936, priority=0)
        # Temp_Dag2.add_node(5,  Node_ID='Job-35',   rank=0, critic=False, WCET=16772, priority=0)
        # Temp_Dag2.add_node(6,  Node_ID='Job-10',   rank=0, critic=False, WCET=46548, priority=0)
        # Temp_Dag2.add_node(7,  Node_ID='Job-4-2',  rank=0, critic=False, WCET=51348, priority=0)
        # Temp_Dag2.add_node(8,  Node_ID='Job-4-3',  rank=0, critic=False, WCET=269720, priority=0)
        # Temp_Dag2.add_node(9,  Node_ID='Job-4-4',  rank=0, critic=False, WCET=123376, priority=0)
        # Temp_Dag2.add_node(10, Node_ID='Job-11',   rank=0, critic=False, WCET=117972, priority=0)
        # Temp_Dag2.add_node(11, Node_ID='Job-4-5',  rank=0, critic=False, WCET=19316, priority=0)
        # Temp_Dag2.add_node(12, Node_ID='Job-4-6',  rank=0, critic=False, WCET=37048, priority=0)
        # Temp_Dag2.add_node(13, Node_ID='Job-12',   rank=0, critic=False, WCET=33424, priority=0)
        # Temp_Dag2.add_node(14, Node_ID='Job-4-7',  rank=0, critic=False, WCET=31812, priority=0)

        # ready running finish
        # 模块1-场景1（2核1流）-情况2 DAG
        Temp_Dag1 = nx.DiGraph()
        Temp_Dag1.add_node(1,  Node_ID='Job-29-1', rank=0, critic=False, WCET=1500, priority=0, state='ready')
        Temp_Dag1.add_node(2,  Node_ID='Job-29-2', rank=0, critic=False, WCET=23232, priority=0, state='ready')
        Temp_Dag1.add_node(3,  Node_ID='Job-36',   rank=0, critic=False, WCET=30000, priority=0, state='ready')
        Temp_Dag1.add_node(4,  Node_ID='Job-4',    rank=0, critic=False, WCET=36236, priority=0, state='ready')
        Temp_Dag1.add_node(5,  Node_ID='Job-35',   rank=0, critic=False, WCET=16772, priority=0, state='ready')

        Temp_Dag1.add_edge(1, 2, weight=1)
        Temp_Dag1.add_edge(1, 3, weight=1)
        Temp_Dag1.add_edge(1, 4, weight=1)
        Temp_Dag1.add_edge(1, 5, weight=1)
        self.critical_path_config(Temp_Dag1)

        # 模块1-场景2（3核2流）-情况2 DAG
        Temp_Dag2 = nx.DiGraph()
        Temp_Dag2.add_node(1,  Node_ID='Job-29-1', rank=0, critic=False, WCET=1500, priority=0, state='ready')
        Temp_Dag2.add_node(2,  Node_ID='Job-29-2', rank=0, critic=False, WCET=34276, priority=0, state='ready')
        Temp_Dag2.add_node(3,  Node_ID='Job-36-1', rank=0, critic=False, WCET=32220, priority=0, state='ready')
        Temp_Dag2.add_node(4,  Node_ID='Job-36-2', rank=0, critic=False, WCET=32220, priority=0, state='ready')
        Temp_Dag2.add_node(5,  Node_ID='Job-35-1', rank=0, critic=False, WCET=20000, priority=0, state='ready')
        Temp_Dag2.add_node(6,  Node_ID='Job-35-2', rank=0, critic=False, WCET=20000, priority=0, state='ready')
        Temp_Dag2.add_node(7,  Node_ID='Job-4-1',  rank=0, critic=False, WCET=39716, priority=0, state='ready')
        Temp_Dag2.add_node(8,  Node_ID='Job-4-2',  rank=0, critic=False, WCET=39716, priority=0, state='ready')

        Temp_Dag2.add_edge(1, 2, weight=1)
        Temp_Dag2.add_edge(1, 3, weight=1)
        Temp_Dag2.add_edge(1, 4, weight=1)
        Temp_Dag2.add_edge(1, 5, weight=1)
        Temp_Dag2.add_edge(1, 6, weight=1)
        Temp_Dag2.add_edge(1, 7, weight=1)
        Temp_Dag2.add_edge(1, 8, weight=1)

        self.critical_path_config(Temp_Dag2)

        G1 = DAG.DAG(Temp_Dag1)
        G2 = DAG.DAG(Temp_Dag2)
        self.Add_DAG(G1)
        self.Add_DAG(G2)


if __name__ == "__main__":
    dagset = DAG_Set()
    dagset.user_defined_dag()
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
