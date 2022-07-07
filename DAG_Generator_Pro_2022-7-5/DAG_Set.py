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
import simpy


#####################################
#   自定义 DAG 数据
#   节点号； 节点名； 节点优权重； 节点优先级
#####################################


# 一.何庆强 2019 测试数据
# 1.1 测试数据1(简单数据)
def he_2019_DAG1():
    HE_2019_DAG = nx.DiGraph()
    HE_2019_nodes = [[1, 'V1', 1, 1],
                     [2, 'V2', 7, 5],
                     [3, 'V3', 3, 6],
                     [4, 'V4', 3, 7],
                     [5, 'V5', 6, 2],
                     [6, 'V6', 9, 3],
                     [7, 'V7', 2, 4],
                     [8, 'V8', 1, 8]]

    for node_x in HE_2019_nodes:
        HE_2019_DAG.add_node(
            node_x[0], Node_ID=node_x[1], critic=False, WCET=node_x[2], priority=node_x[3])

    HE_2019_edges = [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (5, 7), (6, 7), (2, 8), (3, 8), (4, 8), (7, 8)]
    for edge_x in HE_2019_edges:
        HE_2019_DAG.add_edge(edge_x[0], edge_x[1], weight=1)
    G = DAG.DAG()
    G.G = HE_2019_DAG
    G.DAG_ID = "he_2019_DAG1"
    G.critical_path_config()
    return G


# 1.2 测试数据2(复杂数据)
def he_2019_DAG2():
    HE_2019_DAG = nx.DiGraph()
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
        HE_2019_DAG.add_node(
            node_x[0], Node_ID=node_x[1], rank=0, critic=False, WCET=node_x[2], priority=node_x[3])

    HE_2019_edges = [(1, 2), (2, 3), (2, 4), (2, 5), (3, 6), (3, 8),
             (4, 6), (4, 8), (4, 9), (5, 7), (5, 9), (6, 10), (7, 10), (8, 10), (9, 10) ]
    for edge_x in HE_2019_edges:
        HE_2019_DAG.add_edge(edge_x[0], edge_x[1], weight=1)
    G = DAG.DAG()
    G.G = HE_2019_DAG
    G.DAG_ID = "he_2019_DAG2"
    G.critical_path_config()
    return G

# 二.华为无线测试数据
# 2.1 模块1
# 2.1.1 情况1
# (1_1) 场景1——2核1流:(华为原有)
# def mode1_case1_scene1_2c1f_huawei():


# (1) 场景1——2核1流:
def mode1_case1_scene1_2c1f():
    Temp_Dag = nx.DiGraph()
    # [0] node_num; [1]node_ID; [2]AVET; [3]BCET; [4]WCET; [5]priority;
    node_list = [[1,  'Job-29-1', 569,       50,         1500,   1 ],
                 [2,  'Job-29-2', 13507,     10000,      23232,  13],
                 [3,  'Job-36',   14110,     6732,       30000,  12],
                 [4,  'Job-4-1',  36169,     29656,      45936,  2 ],
                 [5,  'Job-35',   3619,      572,        16772,  14],
                 [6,  'Job-10',   40229,     37752,      46548,  4 ],
                 [7,  'Job-4-2',  45409,     42724,      51348,  3 ],
                 [8,  'Job-4-3',  252370,    240724,     269720, 5 ],
                 [9,  'Job-4-4',  103897,    95612,      123376, 6 ],
                 [10, 'Job-11',   99335,     89976,      117972, 7 ],
                 [11, 'Job-4-5',  17699,     16676,      19316,  8 ],
                 [12, 'Job-4-6',  32609,     30008,      37048,  9 ],
                 [13, 'Job-12',  29889,      27672,      33424,  10],
                 [14, 'Job-4-7',   24250,    19712,      31812,  11] ]
    for node_x in node_list:
        Temp_Dag.add_node(node_x[0], Node_ID=node_x[1], critic=False, AVET=node_x[2], BCET=node_x[3], WCET=node_x[4],
                          priority=node_x[5], state='blocked')

    edge_list = [(1, 2), (1, 3), (1, 4), (1, 5), (4, 6), (4, 7), (7, 8), (6, 8), (8, 9), (8, 10), (9, 11), (10, 11),
                 (11, 12), (11, 13), (13, 14), (12, 14)]
    for edge_x in edge_list:
        Temp_Dag.add_edge(edge_x[0], edge_x[1], weight=1)
    G = DAG.DAG()
    G.G = Temp_Dag
    G.DAG_ID = "M1_C1_S1"
    G.critical_path_config()
    return G


# (2) 场景2——3核2流:
def mode1_case1_scene2_3c2f():
    Temp_Dag = nx.DiGraph()
    # [0] node_num; [1]node_ID; [2]AVET; [3]BCET; [4]WCET; [5]priority;
    node_list = [[1, 'Job-29-1',     569,       50,        1500,     1],
                 [2, 'Job-29-2',     23226,     20000,     34276,    26],
                 [3, 'Job-36(1)',    13730,     5744,      32220,    29],
                 [4, 'Job-36(2)',    13730,     5744,      32220,    30],
                 [5, 'Job-4-1(1)',   34908,     29348,     40920,    2],
                 [6, 'Job-4-1(2)',   34908,     29348,     40920,    14],
                 [7, 'Job-35(1)',    5066,      624,       20000,    31],
                 [8, 'Job-35(2)',    5066,      624,       20000,    32],
                 [9, 'Job-10(1)',    26492,     23088,     36392,    4],
                 [10, 'Job-10(2)',   26492,     23088,     36392,    5],
                 [11, 'Job-10(3)',   26492,     23088,     36392,    16],
                 [12, 'Job-10(4)',   26492,     23088,     36392,    17],
                 [13, 'Job-4-2(1)',  76423,     56672,     127908,   3],
                 [14, 'Job-4-2(2)',  76423,     56672,     127908,   15],
                 [15, 'Job-4-3(1)',  275809,    255508,    292952,   6],
                 [16, 'Job-4-3(2)',  275809,    255508,    292952,   18],
                 [17, 'Job-4-4(1)',  144060,    129390,    172964,   7],
                 [18, 'Job-4-4(2)',  144060,    129390,    172964,   19],
                 [19, 'Job-11(1)',   67942,     55300,     90936,    8],
                 [20, 'Job-11(2)',   67942,     55300,     90936,    9],
                 [21, 'Job-11(3)',   67942,     55300,     90936,    20],
                 [22, 'Job-11(4)',   67942,     55300,     90936,    21],
                 [23, 'Job-4-5(1)',  18491,     17116,     22264,    10],
                 [24, 'Job-4-5(2)',  18491,     17116,     22264,    22],
                 [25, 'Job-4-6(1)',  94332,     24288,     126632,   11],
                 [26, 'Job-4-6(2)',  94332,     24288,     126632,   23],
                 [27, 'Job-12(1)',   18484,     11624,     32136,    12],
                 [28, 'Job-12(2)',   18484,     11624,     32136,    13],
                 [29, 'Job-12(3)',   18484,     11624,     32136,    24],
                 [30, 'Job-12(4)',   18484,     11624,     32136,    25],
                 [31, 'Job-4-7(1)',  24471,     8712,      34056,    27],
                 [32, 'Job-4-7(2)',  24471,     8712,      34056,    28]]

    for node_x in node_list:
        Temp_Dag.add_node(node_x[0], Node_ID=node_x[1], critic=False, AVET=node_x[2], BCET=node_x[3], WCET=node_x[4],
                          priority=node_x[5], state='blocked')


    .(1, 2, weight=1)
    .(1, 3, weight=1)
    .(1, 4, weight=1)
    .(1, 5, weight=1)
    .(1, 6, weight=1)
    .(1, 7, weight=1)
    .(1, 8, weight=1)
    .(5, 9, weight=1)
    .(5, 10, weight=1)
    .(5, 13, weight=1)
    .(6, 11, weight=1)
    .(6, 12, weight=1)
    .(6, 14, weight=1)
    .(9, 15, weight=1)
    .(10, 15, weight=1)
    .(13, 15, weight=1)
    .(11, 16, weight=1)
    .(12, 16, weight=1)
    .(14, 16, weight=1)
    .(15, 17, weight=1)
    .(15, 19, weight=1)
    .(15, 20, weight=1)
    .(16, 18, weight=1)
    .(16, 21, weight=1)
    .(16, 22, weight=1)
    .(17, 23, weight=1)
    .(18, 24, weight=1)
    .(19, 23, weight=1)
    .(20, 23, weight=1)
    .(21, 24, weight=1)
    .(22, 24, weight=1)
    .(23, 25, weight=1)
    .(23, 27, weight=1)
    .(23, 28, weight=1)
    .(24, 26, weight=1)
    .(24, 29, weight=1)
    .add_edge(24, 30, weight=1)
    Temp_Dag2.add_edge(25, 31, weight=1)
    Temp_Dag2.add_edge(27, 31, weight=1)
    Temp_Dag2.add_edge(28, 31, weight=1)
    Temp_Dag2.add_edge(26, 32, weight=1)
    Temp_Dag2.add_edge(29, 32, weight=1)
    Temp_Dag2.add_edge(30, 32, weight=1)
    G = DAG.DAG()
    G.G = Temp_Dag2
    G.DAG_ID = "M1_C1_S2"
    G.critical_path_config()
    return G


# 2.1.2 情况2
# (1) 场景1——2核1流:
def mode1_case2_scene1_2c1f():
    Temp_Dag = nx.DiGraph()
    Temp_Dag.add_node(1, Node_ID='Job-29-1', rank=0, critic=False, WCET=1500, priority=1, state='blocked')
    Temp_Dag.add_node(2, Node_ID='Job-29-2', rank=0, critic=False, WCET=23232, priority=4, state='blocked')
    Temp_Dag.add_node(3, Node_ID='Job-36', rank=0, critic=False, WCET=30000, priority=3, state='blocked')
    Temp_Dag.add_node(4, Node_ID='Job-4', rank=0, critic=False, WCET=36236, priority=2, state='blocked')
    Temp_Dag.add_node(5, Node_ID='Job-35', rank=0, critic=False, WCET=16772, priority=5, state='blocked')

    Temp_Dag.add_edge(1, 2, weight=1)
    Temp_Dag.add_edge(1, 3, weight=1)
    Temp_Dag.add_edge(1, 4, weight=1)
    Temp_Dag.add_edge(1, 5, weight=1)

    G = DAG.DAG()
    G.G = Temp_Dag
    G.DAG_ID = "M1_C2_S1"
    G.critical_path_config()
    return G


# (2) 场景2——3核2流:
def mode1_case2_scene2_3c2f():
    Temp_Dag = nx.DiGraph()
    Temp_Dag.add_node(1, Node_ID='Job-29-1', rank=0, critic=False, WCET=1500, priority=1, state='blocked')
    Temp_Dag.add_node(2, Node_ID='Job-29-2', rank=0, critic=False, WCET=34276, priority=4, state='blocked')
    Temp_Dag.add_node(3, Node_ID='Job-36-1', rank=0, critic=False, WCET=32220, priority=5, state='blocked')
    Temp_Dag.add_node(4, Node_ID='Job-36-2', rank=0, critic=False, WCET=32220, priority=6, state='blocked')
    Temp_Dag.add_node(5, Node_ID='Job-35-1', rank=0, critic=False, WCET=20000, priority=7, state='blocked')
    Temp_Dag.add_node(6, Node_ID='Job-35-2', rank=0, critic=False, WCET=20000, priority=8, state='blocked')
    Temp_Dag.add_node(7, Node_ID='Job-4-1', rank=0, critic=False, WCET=39716, priority=2, state='blocked')
    Temp_Dag.add_node(8, Node_ID='Job-4-2', rank=0, critic=False, WCET=39716, priority=3, state='blocked')

    Temp_Dag.add_edge(1, 2, weight=1)
    Temp_Dag.add_edge(1, 3, weight=1)
    Temp_Dag.add_edge(1, 4, weight=1)
    Temp_Dag.add_edge(1, 5, weight=1)
    Temp_Dag.add_edge(1, 6, weight=1)
    Temp_Dag.add_edge(1, 7, weight=1)
    Temp_Dag.add_edge(1, 8, weight=1)

    G = DAG.DAG()
    G.G = Temp_Dag
    G.DAG_ID = "M1_C2_S2"
    G.critical_path_config()
    return G


# 2.2 模块2
# 2.2.1 情况1
# (1) 场景1——2核1流:
def mode2_case1_scene1_2c1f():
    Temp_Dag = nx.DiGraph()
    node_list = [[1, 'Job-0(1)',     3032,   1],
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
        Temp_Dag.add_node(node_x[0], Node_ID=node_x[1], rank=0, critic=False, WCET=node_x[2], priority=node_x[3], state='blocked')

    edge_list = [(1, 2), (2, 3), (2, 4), (2, 5), (2, 6), (3, 7), (4, 7), (5, 7), (6, 7), (7, 8), (7, 9), (7, 10), (7, 11), (7, 12)]
    for edge_x in edge_list:
        Temp_Dag.add_edge(edge_x[0], edge_x[1], weight=1)
    G = DAG.DAG()
    G.G = Temp_Dag
    G.DAG_ID = "M2_C1_S1"
    G.critical_path_config()
    return G


# (2) 场景2——3核2流:
def mode2_case1_scene2_3c2f():
    Temp_Dag = nx.DiGraph()
    node_list = [[1, 'Job-0(2)',        6732,   1],
                 [2, 'Job-1_1(2)',      264088, 2],
                 [3, 'Job-1_2(2)',      264088, 8],
                 [4, 'Job-3-1_1(2)',    118764, 3],
                 [5, 'Job-3-1_2(2)',    118764, 4],
                 [6, 'Job-3-1_3(2)',    118764, 5],
                 [7, 'Job-3-1_4(2)',    118764, 6],
                 [8, 'Job-3-1_5(2)',    118764, 9],
                 [9, 'Job-3-1_6(2)',    118764, 10],
                 [10, 'Job-3-1_7(2)',   118764, 11],
                 [11, 'Job-3-1_8(2)',   118764, 12],
                 [12, 'Job-3-2_1(2)',   97020,  7],
                 [13, 'Job-3-2_2(2)',   97020,  13],
                 [14, 'Job-7_1(2)',     75460,  14],
                 [15, 'Job-7_2(2)',     75460,  15],
                 [16, 'Job-7_3(2)',     75460,  15],
                 [17, 'Job-7_4(2)',     75460,  17],
                 [18, 'Job-7_5(2)',     75460,  18],
                 [19, 'Job-7_6(2)',     75460,  19],
                 [20, 'Job-7_7(2)',     75460,  20],
                 [21, 'Job-7_8(2)',     75460,  21],
                 [22, 'Job-3-3_1(2)',   55264,  22],
                 [23, 'Job-3-3_2(2)',   55264,  23]]
    for node_x in node_list:
        Temp_Dag.add_node(node_x[0], Node_ID=node_x[1], rank=0, critic=False, WCET=node_x[2], priority=node_x[3], state='blocked')
    edge_list = [(1, 2), (1, 3), (2, 4), (2, 5), (2, 6), (2, 7),
             (3, 8), (3, 9), (3, 10), (3, 11),
             (4, 12), (5, 12), (6, 12), (7, 12),
             (8, 13), (9, 13), (10, 13), (11, 13),
             (12, 14), (12, 15), (12, 16), (12, 17), (12, 22),
             (13, 18), (13, 19), (13, 20), (13, 21), (13, 23)
             ]
    for edge_x in edge_list:
        Temp_Dag.add_edge(edge_x[0], edge_x[1], weight=1)
    G = DAG.DAG()
    G.G = Temp_Dag
    G.DAG_ID = "M2_C1_S2"
    G.critical_path_config()
    return G


# (3) 场景3——5核6流:
def mode2_case1_scene3_5c6f():
    Temp_Dag = nx.DiGraph()
    node_list = [[1, 'Job-0(3)', 10000, 1],
                 [2, 'Job-1_1(3)', 290488, 2],
                 [3, 'Job-3-1_1(3)', 100000, 3],
                 [4, 'Job-3-1_2(3)', 100000, 4],
                 [5, 'Job-3-1_3(3)', 100000, 5],
                 [6, 'Job-3-1_4(3)', 100000, 6],
                 [7, 'Job-3-2_1(3)', 96008, 7],
                 [8, 'Job-1_2(3)', 290488, 8],
                 [9, 'Job-1_3(3)', 290488, 9],
                 [10, 'Job-1_4(3)', 290488, 10],
                 [11, 'Job-1_5(3)', 290488, 11],
                 [12, 'Job-1_6(3)', 290488, 12],
                 [13, 'Job-3-1_5(3)', 100000, 13],
                 [14, 'Job-3-1_6(3)', 100000, 14],
                 [15, 'Job-3-1_7(3)', 100000, 15],
                 [16, 'Job-3-1_8(3)', 100000, 16],
                 [17, 'Job-3-1_9(3)', 100000, 17],
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
                 [33, 'Job-3-2_2(3)', 96008, 33],
                 [34, 'Job-3-2_3(3)', 96008, 34],
                 [35, 'Job-3-2_4(3)', 96008, 35],
                 [36, 'Job-3_2_5(3)', 96008, 36],
                 [37, 'Job-3_2_6(3)', 96008, 37],
                 [38, 'Job 7_1(3)', 87560, 38],
                 [39, 'Job 7_2(3)', 87560, 39],
                 [40, 'Job 7_3(3)',     87560,  40],
                 [41, 'Job 7_4(3)',     87560,  41],
                 [42, 'Job 7_5(3)',     87560,  42],
                 [43, 'Job 7_6(3)',     87560,  43],
                 [44, 'Job 7_7(3)',     87560,  44],
                 [45, 'Job 7_8(3)',     87560,  45],
                 [46, 'Job 7_9(3)',     87560,  46],
                 [47, 'Job 7_10(3)',    87560,  47],
                 [48, 'Job 7_11(3)',    87560,  48],
                 [49, 'Job 7_12(3)',    87560,  49],
                 [50, 'Job 7_13(3)',    87560,  50],
                 [51, 'Job 7_14(3)', 87560, 51],
                 [52, 'Job 7_15(3)', 87560, 52],
                 [53, 'Job 7_16(3)', 87560, 53],
                 [54, 'Job 7_17(3)', 87560, 54],
                 [55, 'Job 7_18(3)', 87560, 55],
                 [56, 'Job 7_19(3)', 87560, 56],
                 [57, 'Job 7_20(3)', 87560, 57],
                 [58, 'Job 7_21(3)', 87560, 58],
                 [59, 'Job 7_22(3)', 87560, 59],
                 [60, 'Job 7_23(3)', 87560, 60],
                 [61, 'Job 7_24(3)', 87560, 61],
                 [62, 'Job 3-3_1(3)', 57332, 62],
                 [63, 'Job 3-3_2(3)', 57332, 63],
                 [64, 'Job 3-3_3(3)', 57332, 64],
                 [65, 'Job 3-3_4(3)', 57332, 65],
                 [66, 'Job 3-3_5(3)', 57332, 66],
                 [67, 'Job 3-3_6(3)', 57332, 67]
                 ]
    for node_x in node_list:
        Temp_Dag.add_node(node_x[0], Node_ID=node_x[1], rank=0, critic=False, WCET=node_x[2], priority=node_x[3], state='blocked')

    edge_list = [(1, 2), (1, 8), (1, 9), (1, 10), (1, 11), (1, 12),
                 (2, 3), (2, 4), (2, 5), (2, 6),
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

                 (7, 38), (7, 39), (7, 40), (7, 41), (7, 62),
                 (33, 42), (33, 43), (33, 44), (33, 45), (33, 63),
                 (34, 46), (34, 47), (34, 48), (34, 49), (34, 64),
                 (35, 50), (35, 51), (35, 52), (35, 53), (35, 65),
                 (36, 54), (36, 55), (36, 56), (36, 57), (36, 66),
                 (37, 58), (37, 59), (37, 60), (37, 61), (37, 67)
                 ]
    for edge_x in edge_list:
        Temp_Dag.add_edge(edge_x[0], edge_x[1], weight=1)
    G = DAG.DAG()
    G.G = Temp_Dag
    G.DAG_ID = "M2_C1_S3"
    G.critical_path_config()
    return G


# 2.2.2 情况2
# (1) 场景1——2核1流:
def mode2_case2_scene1_2c1f():
    Temp_Dag = nx.DiGraph()
    node_list = [[1, 'Job-0(1)',    3032, 1],
                 [2, 'Job-3-1(1)', 89840, 2] ]
    for node_x in node_list:
        Temp_Dag.add_node(node_x[0], Node_ID=node_x[1], rank=0, critic=False, WCET=node_x[2], priority=node_x[3], state='blocked')
    edge_list = [(1, 2)]
    for edge_x in edge_list:
        Temp_Dag.add_edge(edge_x[0], edge_x[1], weight=1)
    G = DAG.DAG()
    G.G = Temp_Dag
    G.DAG_ID = "M2_C2_S1"
    G.critical_path_config()
    return G


# (2) 场景2——3核2流:
def mode2_case2_scene2_3c2f():
    Temp_Dag = nx.DiGraph()
    node_list = [[1, 'Job-0(2)',    6732,  1],
                 [2, 'Job-1_1(2)', 108328, 2],
                 [3, 'Job-1_2(2)', 108328, 3]]
    for node_x in node_list:
        Temp_Dag.add_node(node_x[0], Node_ID=node_x[1], rank=0, critic=False, WCET=node_x[2], priority=node_x[3], state='blocked')
    edge_list = [(1, 2), (1, 3)]
    for edge_x in edge_list:
        Temp_Dag.add_edge(edge_x[0], edge_x[1], weight=1)
    G = DAG.DAG()
    G.G = Temp_Dag
    G.DAG_ID = "M2_C2_S2"
    G.critical_path_config()
    return G


# (3) 场景3——5核6流:
def mode2_case2_scene3_5c6f():
    Temp_Dag = nx.DiGraph()
    node_list = [[1, 'Job-0(3)', 10000, 1],
                 [2, 'Job-1_1(3)', 120000, 2],
                 [3, 'Job-1_2(3)', 120000, 3],
                 [4, 'Job-1_3(3)', 120000, 4],
                 [5, 'Job-1_4(3)', 120000, 5],
                 [6, 'Job-1_5(3)', 120000, 6],
                 [7, 'Job-1_6(3)', 120000, 7]]
    for node_x in node_list:
        Temp_Dag.add_node(node_x[0], Node_ID=node_x[1], rank=0, critic=False, WCET=node_x[2], priority=node_x[3], state='blocked')
    edges = [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7)]
    for edge in edges:
        Temp_Dag.add_edge(edge[0], edge[1], weight=1)
    G = DAG.DAG()
    G.G = Temp_Dag
    G.DAG_ID = "M2_C2_S3"
    G.critical_path_config()
    return G


# 三.自制的
def self_make_DAG1():
    Temp_Dag_mine = nx.DiGraph()
    node_list = [[1, 'Job-1', 9,  1],
                 [2, 'Job-2', 10, 2],
                 [3, 'Job-3', 4,  5],
                 [4, 'Job-4', 8,  4],
                 [5, 'Job-5', 11, 3],
                 [6, 'Job-6', 6,  6],
                 [7, 'Job-7', 5,  7]]
    for node_x in node_list:
        Temp_Dag_mine.add_node(node_x[0], Node_ID=node_x[1], rank=0, critic=False, WCET=node_x[2], priority=node_x[3], state='blocked')
    edge_list = [(1, 2), (1, 3), (1, 4), (2, 5), (3, 5), (5, 6), (6, 7), (4, 7)]
    for edge_x in edge_list:
        Temp_Dag_mine.add_edge(edge_x[0], edge_x[1], weight=1)
    G = DAG.DAG()
    G.G = Temp_Dag_mine
    G.DAG_ID = "Self_DAG_1"
    G.critical_path_config()
    return G


def self_make_DAG2():
    Temp_Dag_mine = nx.DiGraph()
    node_list = [[1, 'Job-1', 9,  1],
                 [2, 'Job-2', 10, 2],
                 [3, 'Job-3', 4,  3],
                 [4, 'Job-4', 8,  6],
                 [5, 'Job-5', 11, 4],
                 [6, 'Job-6', 6,  5],
                 [7, 'Job-7', 5,  7]]
    for node_x in node_list:
        Temp_Dag_mine.add_node(node_x[0], Node_ID=node_x[1], rank=0, critic=False, WCET=node_x[2], priority=node_x[3], state='blocked')
    edge_list = [(1, 2), (1, 3), (1, 4), (2, 5), (3, 5), (5, 6), (6, 7), (4, 7)]
    for edge_x in edge_list:
        Temp_Dag_mine.add_edge(edge_x[0], edge_x[1], weight=1)
    G = DAG.DAG()
    G.G = Temp_Dag_mine
    G.DAG_ID = "Self_DAG_2"
    G.critical_path_config()
    return G


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
            # step1. DAG结构生成
            Temp_DAG.gen("mine")
            # step2. DAG WCET配置；
            Temp_DAG.WCET_Config("random")
            # step3. DAG 优先级配置；
            Temp_DAG.Priority_Config("random")
            # step4. DAG 关键路径配置；
            Temp_DAG.critical_path_config()
            # stpe5. 加入DAG 集合
            self.Add_DAG(Temp_DAG)

    def Add_DAG(self, Dag):
        self.Dag_Set.append(Dag)

    #####################################
    #   更新DAG集合中所有DAG节点的状态，
    #   即将所有前驱节点为0，状态为阻塞态的节点
    #   转换为的就绪态状态
    #####################################
    def Status_Data_Up(self):
        for x in self.Dag_Set:
            for y in x.G.nodes(data=True):
                if (len(list(x.G.predecessors(y[0]))) == 0) and (y[1].get('state') == 'blocked'):
                    y[1]['state'] = 'ready'

    def Status_Data_Up_Store(self, store):
        for x in self.Dag_Set:
            for y in x.G.nodes(data=True):
                if (len(list(x.G.predecessors(y[0]))) == 0) and (y[1].get('state') == 'blocked'):
                    store.put(simpy.PriorityItem(y[1].get('priority'), (x.DAG_ID,y)))
                    y[1]['state'] = 'ready'

    #####################################
    #   DAG的优先级配置
    #####################################
    def Single_DAG_Priority_Config(self, insert_DAG):
        temp_node_wcet_1 = nx.get_node_attributes(insert_DAG, 'WCET')
        temp_node_wcet_2 = dict(sorted(temp_node_wcet_1.items(), key=lambda x: x[1], reverse=True))
        Temp_1 = 1
        for k, v in temp_node_wcet_2.items():
            insert_DAG.node[k]['priority'] = Temp_1
            Temp_1 += 1
        return False

    def Mulit_DAG_Priority_Config(self):
        if len(self.Dag_Set) > 1:
            node_num_list = []
            for x in self.Dag_Set:
                node_num_list.append(x.get_node_num())
            max_node_num = max(node_num_list)
            for x in self.Dag_Set:
                temp_pri = x.Priority
                for y in x.G.nodes(data=True):
                    y[1]['priority'] = y[1]['priority'] + temp_pri * max_node_num

    #####################################
    #   获取DAG集合的数量#
    #####################################
    def get_dag_num(self):
        return len(self.Dag_Set)

    #####################################
    #   根据DAG_ID 获取DAG
    #####################################
    def get_dag(self, DAG_ID):
        for x in self.Dag_Set:
            if x.DAG_ID == DAG_ID:
                return x
        return False

    # #####################################
    # #   根据DAG_ID, Node_ID 获取对应的node
    # #####################################
    # def get_node(self, DAG_ID, Node_ID):
    #     for x in self.Dag_Set:
    #         if x.DAG_ID == DAG_ID:
    #             return x.G.node[Node_ID]
    #     return False

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
        temp_list = []
        for x in self.Dag_Set:
            temp_ready_list = x.get_ready_node_list()
            for y in temp_ready_list:
                temp_list.append((x.DAG_ID, y))
        return temp_list

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
        ret_list = []
        for x in self.Dag_Set:
            temp_dict[x] = x.Priority
        temp_dict = sorted(temp_dict.items(), key=lambda x: x[1])
        for k, v in temp_dict:
            DAG_ID = k.DAG_ID
            temp_ready_list = k.get_ready_node_list()
            if len(temp_ready_list) == 0:
                continue
            ret_list.append( (DAG_ID, temp_ready_list) )
        return ret_list
        # return False, False

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
        # for x in self.Dag_Set:
        #     x.show_dag()

    #####################################
    #   自定义 DAG 算法#
    #####################################
    def user_defined_dag(self):
        # he_2019_DAG1()
        # he_2019_DAG2
        # self_make_DAG1
        # self_make_DAG2
        G1_1_1_M = mode1_case1_scene1_2c1f()
        G1_1_2_M = mode1_case1_scene2_3c2f()
        G1_2_1_M = mode1_case2_scene1_2c1f()
        G1_2_2_M = mode1_case2_scene2_3c2f()
        G2_1_1_M = mode2_case1_scene1_2c1f()
        G2_1_2_M = mode2_case1_scene2_3c2f()
        G2_1_3_M = mode2_case1_scene3_5c6f()
        G2_2_1_M = mode2_case2_scene1_2c1f()
        G2_2_2_M = mode2_case2_scene2_3c2f()
        G2_2_3_M = mode2_case2_scene3_5c6f()

        G1_1_1_M.Priority = 2
        G1_1_2_M.Priority = 1

        G1_2_1_M.Priority = 2
        G1_2_2_M.Priority = 1

        G2_1_1_M.Priority = 3
        G2_1_2_M.Priority = 2
        G2_1_3_M.Priority = 1

        G2_2_1_M.Priority = 3
        G2_2_2_M.Priority = 2
        G2_2_3_M.Priority = 1

        self.Single_DAG_Priority_Config(G1_1_1_M.G)
        self.Single_DAG_Priority_Config(G1_1_2_M.G)
        self.Single_DAG_Priority_Config(G1_2_1_M.G)
        self.Single_DAG_Priority_Config(G1_2_2_M.G)

        self.Single_DAG_Priority_Config(G2_1_1_M.G)
        self.Single_DAG_Priority_Config(G2_1_2_M.G)
        self.Single_DAG_Priority_Config(G2_1_3_M.G)
        self.Single_DAG_Priority_Config(G2_2_1_M.G)
        self.Single_DAG_Priority_Config(G2_2_2_M.G)
        self.Single_DAG_Priority_Config(G2_2_3_M.G)

        # self.Add_DAG(G1_1_1_M)
        # self.Add_DAG(G1_1_2_M)

        # self.Add_DAG(G1_2_1_M)
        # self.Add_DAG(G1_2_2_M)

        # self.Add_DAG(G2_1_1_M)
        # self.Add_DAG(G2_1_2_M)
        # self.Add_DAG(G2_1_3_M)

        self.Add_DAG(G2_2_1_M)
        self.Add_DAG(G2_2_2_M)
        # self.Add_DAG(G2_2_3_M)
        self.Mulit_DAG_Priority_Config()


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


