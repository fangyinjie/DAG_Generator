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
import rta
import math
import ast
import sys
# Class: DAG (Directed Acyclic Graph Task)


class DAG:
    def __init__(self):
        self.name           = 'Tau_{null}'  #
        self.DAG_ID         = '0'           # 
        self.G              = nx.DiGraph()  #
        self.task_num       = 0             # 
        self.Priority       = 1             #
        # generator mine
        self.parallelism    = 0             # 
        self.Critical_path  = 0             # 

    Periodically = list(enumerate(['PERIODIC', 'SPORADIC', 'APERIODIC'], start=1))
    Real_Time = list(enumerate(['HRT', 'SRT', 'FRT'], start=1))

    def get_graph(self):  
        return self.G

    def gen(self, algorithm):  
        if algorithm == "mine":
            self.gen_mine()
        else:
            return 1
        return 0

    def get_ready_node_list(self):
        return [x for x in self.G.nodes(data=True) if (x[1].get('state') == 'ready')]

    def critical_path_config(self):
        WCET = nx.get_node_attributes(self.G, 'WCET')
        for edge_x in self.G.edges(data=True):
            edge_x[2]['weight'] = WCET[edge_x[1]]
        node_list = nx.dag_longest_path(self.G, weight='weight')  
        for node_xx in self.G.nodes(data=True):
            if node_xx[0] in node_list:  
                node_xx[1]['critic'] = True

    #####################################
    #   Show DAG
    #####################################
    def show_dag(self):
        print("DAG_ID:", self.DAG_ID)
        print("DAG_Nodes_num:", self.G.number_of_nodes())
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
        print(self.G.nodes.data(data=True))
        print(self.G.edges.data(data=True))

    #####################################
    #   get DAG parameter
    #####################################
    def get_node_num(self):
        return self.G.number_of_nodes()

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
        TR = matrix & (~(np.dot(i_matrix, D)))  
        return nx.DiGraph(TR)

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
        nx.draw_networkx_nodes(self.G, n_pos, node_color=color_map, node_size=800, node_shape='o')     
        nx.draw_networkx_edges(self.G, n_pos, arrows=True,arrowstyle='-|>',  arrowsize=20)           
        nx.draw_networkx_labels(self.G, n_pos, labels=n_map, font_size=5, font_color='k')              

    def gen_mine(self):
        assert (self.parallelism >= 1)
        assert (self.Critical_path >= 3)

        self_critical_path  = self.Critical_path    # 
        self_parallelism    = self.parallelism      # 
        self_Node_num       = 0                     # 
        self.G.add_node(0, Node_ID='souce', rank=0, critic=False, WCET=1, priority=0)  # 
        for x in range(1, self_critical_path - 1):
            m = randint(1, self_parallelism)        # 
            for y in range(1, m + 1):
                self_Node_num += 1
                self.G.add_node(self_Node_num, Node_ID='job{}'.format(self_Node_num), rank=x, critic=False, WCET=1, priority=0)
        self.G.add_node(self_Node_num + 1, Node_ID='sink', rank=self_critical_path - 1, critic=False, WCET=1, priority=0)
        self.task_num = self_Node_num + 2  
        self.G.add_edge(0, 1)
        for x in range(1, self_critical_path - 1):  #
            ancestors_list   = [node_x for node_x in self.G.nodes(data=True) if (node_x[1].get('rank') < x)]
            descendants_list = [node_x for node_x in self.G.nodes(data=True) if (node_x[1].get('rank') > x)]
            self_list        = [node_x for node_x in self.G.nodes(data=True) if (node_x[1].get('rank') == x)]
            successors_list  = [node_x for node_x in self.G.nodes(data=True) if (node_x[1].get('rank') == (x + 1))]
            for y in self_list:
                k1 = randint(1, len(ancestors_list))                    
                ancestors_group = rand.sample(ancestors_list, k1)
                k2 = randint(1, len(descendants_list))              
                descendants_group = rand.sample(descendants_list, k2)
                for z in ancestors_group:
                    self.G.add_edge(z[0], y[0])
                for z in descendants_group:
                    self.G.add_edge(y[0], z[0])
            self.G.add_edge(self_list[0][0], successors_list[0][0])
        self.name = 'Tau_{:d}'.format(self.task_num)

        lp = list(nx.transitive_reduction(self.G).edges())                  
        self.G.clear_edges()
        self.G.add_edges_from(lp)

    #####################################
    def user_defined_dag(self):
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
            temp_interference_node_list = []
            reserve_node_list = []
            temp_path_weight = 0
            temp_WCET = []
            add_reserve = 0
            for y in x:  # x表示完全路径，遍历每个路径节点y
                temp_all_node = self.G.nodes(data=True)
                temp_ance = list(nx.ancestors(self.G, y))
                temp_desc = list(nx.descendants(self.G, y))
                temp_self = x
                sub_node = self.G.nodes[y]
                temp_path_weight += sub_node.get('WCET')
                temp_WCET.append(sub_node.get('WCET'))
                reserve_node_buff = {}
                for z in temp_all_node:  # dag中所有节点与本路径上的节点之间的关系
                    if (z[0] not in temp_ance) and (z[0] not in temp_desc) and (z[0] not in temp_self):
                        if z[1]['priority'] < sub_node.get('priority'):
                            if z not in temp_interference_node_list:
                                temp_interference_node_list.append(z)
                        else:
                            if z[0] not in reserve_node_list:
                                reserve_node_buff[z[0]] = z[1]['WCET']
                t_reserve_list = sorted(reserve_node_buff.items(), key=lambda x: x[1])
                if len(t_reserve_list) > 0:
                    for z in range(0, min(core_num - 1, len(t_reserve_list))):
                        reserve_node_list.append(t_reserve_list[len(t_reserve_list) - z - 1][0])
            for y in range(0, len(reserve_node_list)):
                t_node = self.G.nodes[reserve_node_list[y]]
                add_reserve += t_node.get('WCET')
            # for y in range(1, min(core_num, len(t_reserve_list))):
            #     add_reserve += t_reserve_list[len(t_reserve_list)-y][1]
            temp_inter_weight = 0
            for y in temp_interference_node_list:
                temp_inter_weight += y[1]['WCET']
            interference_node_list.append(temp_interference_node_list)
            temp_rta = temp_path_weight + (temp_inter_weight + add_reserve) / core_num

            if temp_rta > ret_path_and_rta[0]:
                ret_path_and_rta[0] = temp_rta
                ret_path_and_rta[1] = temp_path_weight
                ret_path_and_rta[2] = temp_inter_weight
                ret_path_and_rta[3] = x
                ret_path_and_rta[4] = temp_interference_node_list
        return ret_path_and_rta

    def WCET_random_config(self):
        for x in self.G.nodes(data=True):
            x[1]['WCET'] = rand.randint(1, 10)

    def priority_random_config(self):
        priority_random_list = list(range(0, self.G.number_of_nodes()))
        np.random.shuffle(priority_random_list)
        for x in self.G.nodes(data=True):
            x[1]['priority'] = priority_random_list.pop()

    def DAG_config(self, input_G, input_C, input_prio): 
        self.parallelism = 4
        self.Critical_path = 4
        for key, value in input_C.items():
            self.G.add_node(key, Node_ID=key, rank=0, critic=False, WCET=value, priority=input_prio[key])
        for key, value in input_G.items():
            for x in value:
                self.G.add_edge(key, x, weight=1)

    def rev_DAG_config(self):
        self.parallelism = 4
        self.Critical_path = 4
        input_G = {}
        input_C = {}
        input_prio = {}
        for x in self.G.nodes(data=True):
            input_G[x[0]] = list(nx.neighbors(self.G, x[0]))
            input_C[x[0]] = x[1]['WCET']
            input_prio[x[0]] = x[1]['priority']
        return input_G, input_C, input_prio

    def rev_DAG_config2(self):  
        self.parallelism = 4
        self.Critical_path = 4
        input_G = {}
        input_C = {}
        # input_prio = {}
        for x in self.G.nodes(data=True):
            input_G[x[0]] = list(nx.neighbors(self.G, x[0]))
            input_C[x[0]] = x[1]['WCET']
        return input_G, input_C


if __name__ == "__main__":

  
    G = DAG()  

    input_G = ast.literal_eval(sys.argv[1])
    input_C = ast.literal_eval(sys.argv[2])
    input_prio = ast.literal_eval(sys.argv[3])
    input_n_cores = ast.literal_eval(sys.argv[4])
    overide_prio = ast.literal_eval(sys.argv[5])

    G.DAG_config(input_G, input_C, input_prio)
    G.critical_path_config()

    # 1.he 2019

    x = G.response_time_analysis(input_n_cores)
    print(math.ceil(x[0]))      #  HE RTA

    # 2.zhao 2020
  # Prio = rta.Eligiblity_Ordering_PA(input_G, input_C) # ZHAO PRIO
    # R = rta.rta_alphabeta_new(input_G, input_C, input_prio, input_n_cores, overide_prio=0, EOPA=False, TPDS=False)   # ZHAO RTA
    # print(R)
   # print(Prio)

