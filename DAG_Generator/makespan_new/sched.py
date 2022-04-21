#!/usr/bin/python3
# -*- coding: utf-8 -*-

# DAG Scheduling Simulator
# Xiaotian Dai
# Real-Time Systems Group
# University of York, UK

import os
import logging
import pickle
import json
import random
import math
import operator
from pprint import pprint
import networkx as nx
from task import DAGTask, Job
from processor import Core


EXECUTION_MODEL = ["WCET", "HALF_RANDOM", "HALF_RANDOM_NORM", "FULL_RANDOM", "FULL_RANDOM_NORM", "BCET"]
PREEMPTION_COST = 0
MIGRATION_COST = 0

PATH_OF_SRC = os.path.dirname(os.path.abspath(__file__))
LOG_TO_FILE_LOCATION = PATH_OF_SRC + "/../results/log.txt"


def trace_init(log_to_file = False, debug = False):
    LOG_FORMAT = '[%(asctime)s-%(levelname)s: %(message)s]'
    LOG_DATEFMT = '%Y-%m-%d %H:%M:%S'

    if debug: log_mode = logging.DEBUG
    else: log_mode = logging.INFO

    if log_to_file == True:
        logging.basicConfig(filename='log.txt', filemode='a', level=log_mode,
                            format=LOG_FORMAT, datefmt=LOG_DATEFMT)
    else:
        logging.basicConfig(level=log_mode,
                            format=LOG_FORMAT, datefmt=LOG_DATEFMT)


def trace(msglevel, timestamp, message):
    if msglevel == 0: logging.debug("t = " + str(timestamp) + ": " + message)
    elif msglevel == 1: logging.info("t = " + str(timestamp) + ": " + message)
    elif msglevel == 2: logging.warning("t = " + str(timestamp) + ": " + message)
    elif msglevel == 3: logging.error("t = " + str(timestamp) + ": " + message)
    else: pass

"""
def EO_v1():
    EO_G = dag.G.copy()
    EO_V = dag.V.copy()
    wcet = dag.C.copy()

    EO_WCET = {}
    for i in EO_V:
        EO_WCET[i] = wcet[i - 1]

    # [Classify nodes]
    # I. find critical nodes
    _, EO_V_C = find_longest_path_dfs(EO_G, EO_V[0], EO_V[-1], wcet)
    
    # II. find associative nodes
    candidate = EO_V.copy()
    for i in EO_V_C:  candidate.remove(i)

    critical_nodes = EO_V_C.copy()
    critical_nodes.remove(EO_V_C[0])
    critical_nodes.remove(EO_V_C[-1]) # the source and the sink node is ignored

    EO_V_A = find_associative_nodes(EO_G, candidate, critical_nodes)

    # III. find non-critical nodes (V_NC = V \ V_C \ V_A)
    EO_V_NC = EO_V.copy()
    for i in EO_V_C:  EO_V_NC.remove(i)
    for i in EO_V_A:  EO_V_NC.remove(i)

    # [Assign eligibilities]
    EO_ELIG_BASE_C = 1000
    EO_ELIG_BASE_A = 100
    EO_ELIG_BASE_NC = 1
    
    Prio = {}

    # I. Critical
    offset = EO_ELIG_BASE_C
    sorted_x = sorted({k: EO_WCET[k] for k in EO_V_C}.items(), key=operator.itemgetter(1), reverse=False)
    
    for i in sorted_x:
        Prio[i[0]] = offset
        offset = offset + 1
    
    # II. Associate
    # order by WCET (longest first)
    offset = EO_ELIG_BASE_A
    sorted_x = sorted({k: EO_WCET[k] for k in EO_V_A}.items(), key=operator.itemgetter(1), reverse=False)
    for i in sorted_x:
        Prio[i[0]] = offset
        offset = offset + 1

    # III. Non-Critical
    offset = EO_ELIG_BASE_NC
    sorted_x = sorted({k: EO_WCET[k] for k in EO_V_NC}.items(), key=operator.itemgetter(1), reverse=False)
    for i in sorted_x:
        Prio[i[0]] = offset
        offset = offset + 1
    
    #pprint(Prio)
"""


def sched(dag, number_of_cores):
    t = 0
    wcet_test = [1, 7, 3, 3, 6, 1, 2, 1]
    # Prio      = [1, 5, 6, 7, 2, 8, 3, 4]
    Prio    = [1, 5, 6, 7, 2, 3, 4, 8]
    # initialize cores
    cores = []
    Fyj_Cores = []
    A_LARGE_NUMBER = float("inf")
    for m in range(number_of_cores):
        core = Core()
        cores.append(core)
        Fyj_Cores.append([])
    # variables
    finished = False
    w_queue = []
    for m in dag.nodes():
        w_queue.append(m)   # waitting queue (not released due to constraints)
    r_queue = []            # ready nodes queue
    f_queue = []            # finished nodes queue
    # add the source node to the ready queue
    r_queue.append(1)
    w_queue.remove(1)   # 删除元素1
    while not finished:
        # update the ready queue (by iterative all left nodes)
        w_queue_c = w_queue.copy()
        f_queue_c = f_queue.copy()
        for i in w_queue_c:
            all_matched = True
            for elem in G.predecessors(i):  # dag.pre[i]:
                if elem not in f_queue_c:
                    all_matched = False
            if all_matched:
                r_queue.append(i)
                w_queue.remove(i)
        # iterates all cores
        for m in range(number_of_cores):
            if cores[m].idle:
                if r_queue:     # if anything is in the ready queue. pick the next task
                    E_MAX = A_LARGE_NUMBER #  Prio[0]
                    task_idx = r_queue[0]
                    for i in r_queue:
                        if Prio[i - 1] < E_MAX:
                            task_idx = i
                            E_MAX = Prio[i - 1]

                    task_wcet = wcet_test[task_idx - 1]     # get the task execution time
                    tau = Job(idx_=task_idx, C_=task_wcet)  # assign task to core
                    cores[m].assign(tau)
                    Fyj_Cores[m].append((task_idx,task_wcet))
                    r_queue.remove(task_idx)
        # check the next scheduling point (the shortest workload time)
        # A_LARGE_NUMBER = float("inf")
        sp = A_LARGE_NUMBER
        for core in cores:
            if core.get_workload() != 0:
                if core.get_workload() < sp:
                    sp = core.get_workload()
        # (the default scheduling point is 1, i.e., check on each tick)
        if sp == A_LARGE_NUMBER:
            sp = 1
        # execute for time sp
        t += sp  # these two statement happens at the same time!
        for m in range(number_of_cores):
            if cores[m].idle:
                Fyj_Cores[m].append((0, sp))
            (tau_idx, tau_finished) = cores[m].execute(sp)
            # check finished task and put into the finished queue
            if tau_finished:
                f_queue.append(tau_idx)

        if len(f_queue) == dag.number_of_nodes():
            finished = True
    makespan = t
    return makespan


if __name__ == "__main__":
    # test code::
    # enable logger
    trace_init(log_to_file = False)
    
    for m in [2, 3, 4, 5, 6, 7, 8]:
        R_all = []
        for idx in range(1000):
            G = nx.DiGraph()
            HE_2019_nodes = [[1, 'V1', 1, 1],
                             [2, 'V2', 7, 5],
                             [3, 'V3', 3, 6],
                             [4, 'V4', 3, 7],
                             [5, 'V5', 6, 2],
                             [6, 'V6', 1, 3],
                             [7, 'V7', 2, 4],
                             [8, 'V8', 1, 8]]


            # for x in self_list:
            # self.G.add_node(0, Node_ID='souce_node', rank=0, critic=False, WCET=1)  # 起始节点（1）；rank=0
            for node_x in HE_2019_nodes:
                G.add_node(node_x[0], Node_ID=node_x[1], rank=0, critic=False, WCET=node_x[2], priority=node_x[3])

            edges = [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6),
                     (5, 7), (6, 7),
                     (2, 8), (3, 8), (4, 8), (7, 8)]
            for edge in edges:
                G.add_edge(edge[0], edge[1], weight=1)


            # G_dict, C_dict, C_array, lamda, VN_array, L, W = load_task(idx)
            # dag = DAGTask(G_dict, C_array)

            # find the high watermark of random
            R0 = 0
            for i in range(200):
                r = sched(G, number_of_cores=m)
                if r > R0:
                    R0 = r

            # R1 = sched(G, number_of_cores=m, algorithm="eligibility", execution_model="WCET")
            # R2 = sched(G, number_of_cores=m, algorithm="TPDS2019", execution_model="WCET")
            # R3 = sched(G, number_of_cores=m, algorithm="EMSOFT2019", execution_model="WCET")

    #         R_all.append([R0, R1, R2, R3])
    #
    #         print("{}, {}, {}, {}, {}".format(idx, R0, R1, R2, R3))
    #
    #     pickle.dump(R_all, open("m{}-simu.p".format(m), "wb"))
    #
    # print("Experiment finished!")

