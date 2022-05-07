import numpy as np
import networkx as nx
from random import randint, random, uniform
import random as rand
import os
import minmaxplus
import DAG_Set
import Processor
import matplotlib.pyplot as plt
import random


class Dispatcher:
    def __init__(self, DAG_set):
        self.G = DAG_set                # DAG:-networkX结构
        self.DAG_Set_Num = DAG_set.get_dag_num()

    # def Calculation_Priority(self):

    def Scheduling(self):
        # 1.为每个DAG分配优先级（单DAG可忽略）
        # 2.为每个DAG中所有节点分配优先级
        trm_i = 1

        # 返回DAG，其中每个节点都有优先级

    """
    def Mapping(self, Core_num_list):
        # 为每个DAG节点分配core
        # 为每一类核分配一个列表，在每个列表中为每个核确定一个列表，一个列表，具体为每个节点的起始时间，执行时间，和运行在什么核上
        Ready_Dist = {}
        Core_Running_list = []
        Temp_DAG = self.G.copy()
        Current_Time = 0
        # 初始化核心队列
        UN_Ready_Dist = {}
        for x in Temp_DAG.nodes(data=True):
            UN_Ready_Dist[x[0]] = x[1].get('priority')

        for i in range(0, len(Core_num_list)):
            Core_Running_list.append([])
            for j in range(0, Core_num_list[i]):
                Core_Running_list[i].append([])
                Core_Running_list[i][j].append(0)  # 每个core_list的第一个数表示某core最近完工时间
                Core_Running_list[i][j].append(True)  # core的状态，如果core为空闲则为True
        while Temp_DAG.number_of_nodes() > 0:
            # step-1.将Temp_DAG中前驱节点为0的节点加入就绪队列
            for x in Temp_DAG.nodes(data=True):
                if (len(list(Temp_DAG.predecessors(x[0]))) == 0) and (x[0] in UN_Ready_Dist):
                    Ready_Dist[x[0]] = x[1].get('priority')
                    del UN_Ready_Dist[x[0]]  # 在unready中删除
            # step-2.将结合当前core_running_list中，运行时间小于当前时间的核，为其分配就绪队列中优先级最大的任务，
            for i in range(0, len(Core_Running_list)):  # 哪种core
                for j in range(0, len(Core_Running_list[i])):  # 哪个core
                    # if Core_Running_list[i][j][0] <= Current_Time:    # 该核空闲了
                    if Core_Running_list[i][j][1]:  # 该核空闲了
                        if len(Ready_Dist) > 0:
                            Core_Running_list[i][j][1] = False  # 该核心忙碌
                            H_Prio_Node_num = sorted(Ready_Dist.items(), key=lambda x: x[1])[0][0]  # 最高优先级节点号
                            temp_p = Temp_DAG.node[H_Prio_Node_num]
                            H_Prio_Node_WCET = temp_p.get('WCET')  # 最高优先级节点WCET
                            Core_Running_list[i][j][0] = Current_Time + H_Prio_Node_WCET  # 更新节点的最早空闲时间
                            # 添加到就绪队列执行项目。任务号码，任务的起始时间，任务的WCET
                            Core_Running_list[i][j].append((H_Prio_Node_num,
                                                            Current_Time,
                                                            H_Prio_Node_WCET))
                            del Ready_Dist[H_Prio_Node_num]  # 在ready中删除
                        else:  # 就绪队列没有
                            break
            # 直到就绪队列为空，或是所有core的截止时间都大于当前时间

            # step-3.推进系统时间到core的截止时间最小的时间；
            # 搜索截止时间最小的core或是cores
            #   （1）更新当前时间，
            #   （2）更新Temp_DAG
            temp_time_dict = {}
            for i in range(0, len(Core_Running_list)):  # 哪种core
                for j in range(0, len(Core_Running_list[i])):  # 哪个core
                    if (len(Core_Running_list[i][j]) > 2) and (Core_Running_list[i][j][1] == False):
                        temp_n = Core_Running_list[i][j][len(Core_Running_list[i][j]) - 1]
                        # temp_time_dict[temp_n[1] + temp_n[2]] = temp_n[0]
                        temp_time_dict[temp_n[0]] = [temp_n[1] + temp_n[2], i, j]  # {任务节点号：[完成时间,i,j]}
            H_Prio_Node_num = sorted(temp_time_dict.items(), key=lambda x: x[1][0])  # 按照完成时间排序
            # （1）更新时间
            Current_Time = H_Prio_Node_num[0][1][0]  # {}
            # 获取所有最小完成时间的节点列表
            temp_finish_list = [[k, v[1], v[2]] for k, v in temp_time_dict.items() if v[0] == Current_Time]
            for x in temp_finish_list:
                Temp_DAG.remove_node(x[0])  # 在temp-DAG中删除
                Core_Running_list[x[1]][x[2]][1] = True
            # for self_node in self.G.nodes(data=True):
            #     print('node_num=:{0}'.format(self_node))
            #     print('\t前驱节点（predecessors）：{0}'.format(list(self.G.predecessors(self_node[0]))))
            #     print('\t祖先节点（ancestors）：{0}'.format(nx.ancestors(self.get_graph(), self_node[0])))
            #     print('\t后继节点（successors）：{0}'.format(list(self.G.successors(self_node[0]))))
            #     print('\t后代节点（descendants）：{0}'.format(nx.descendants(self.get_graph(), self_node[0])))
            #     print('\t节点的邻居（neighbors）：{0}'.format(list(nx.neighbors(self.G, self_node[0]))))  # 就是后继节点 successors
            #     print('\t节点的度（degree）：{0}'.format(nx.degree(self.G, self_node[0])))  # node 0 with degree 1
            #     print('\t节点的入度（in_degree）：{0}'.format(self.G.in_degree(self_node[0])))
            #     print('\t节点的出度（out_degree）：{0}'.format(self.G.out_degree(self_node[0])))

        return Core_Running_list
    """
    # Processor_list = [4]
    def Mapping(self, Processor_list, DAG_Set):
        # 为每个DAG节点分配core
        # 为每一类核分配一个列表，在每个列表中为每个核确定一个列表，一个列表，具体为每个节点的起始时间，执行时间，和运行在什么核上
        processor = Processor.Processor(Processor_list, 'GD_32')
        processor.Update_Processor_State(0)     # 初始化系统时间为 0

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
    #   自定义 DAG 算法#
    #####################################
    def user_defined_dag(self):
        # 节点号； 节点名； 节点优权重； 节点优先级
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
                 (2, 8), (3, 8), (4, 8), (7, 8)]
        for edge in edges:
            self.G.add_edge(edge[0], edge[1], weight=1)
        # self.G.add_edges_from(edges)
        # # # # # 配置关键路径 # # # # #
        WCET = nx.get_node_attributes(self.G, 'WCET')
        for edge_x in self.G.edges(data=True):
            edge_x[2]['weight'] = WCET[edge_x[1]]
        node_list = nx.dag_longest_path(self.G, weight='weight')  # 关键路径
        for node_xx in self.G.nodes(data=True):
            if node_xx[0] in node_list:  # 判断是否在关键路径里
                node_xx[1]['critic'] = True

    def user_defined_dag_1(self):
        # 节点号； 节点名； 节点优权重； 节点优先级
        HE_2019_nodes = [[1, 'V1', 15120, 0],
                         [2, 'V2', 14861, 2],
                         [3, 'V3', 14824, 5],
                         [4, 'V4', 8848,  1],
                         [5, 'V5', 8153,  3],
                         [6, 'V6', 8315,  7],
                         [7, 'V7', 4546,  4],
                         [8, 'V8', 5667,  6],
                         [9, 'V9', 3320,  8],
                         [10,'V10',24346, 9]]

        for node_x in HE_2019_nodes:
            self.G.add_node(node_x[0], Node_ID=node_x[1], rank=0, critic=False, WCET=node_x[2], priority=node_x[3])

        edges = [(1, 2), (2, 3), (2, 4), (2, 5),
                 (3, 6), (3, 8),
                 (4, 6), (4, 8),(4, 9),
                 (5, 7),
                 (5, 9),
                 (6, 10),
                 (7, 10),
                 (8, 10),
                 (9, 10)
                 ]
        for edge in edges:
            self.G.add_edge(edge[0], edge[1], weight=1)

        # # # # # 配置关键路径 # # # # #
        WCET = nx.get_node_attributes(self.G, 'WCET')
        for edge_x in self.G.edges(data=True):
            edge_x[2]['weight'] = WCET[edge_x[1]]
        node_list = nx.dag_longest_path(self.G, weight='weight')  # 关键路径
        for node_xx in self.G.nodes(data=True):
            if node_xx[0] in node_list:  # 判断是否在关键路径里
                node_xx[1]['critic'] = True

import Processor
if __name__ == "__main__":
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

    # 节点号； 节点名； 节点优权重； 节点优先级
    dagset = DAG_Set.DAG_Set()
    dagset.user_defined_dag()

    plt.subplot()
    # p = Dispatcher()
    # p.user_defined_dag_1()
    p = Dispatcher(dagset)
    process = Processor.Processor(4)
    p.Mapping(process)
    print()
    p.Show_Dag()
    plt.show()
