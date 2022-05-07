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

from collections import defaultdict
# Class: DAG (Directed Acyclic Graph Task)


def sched(dag, number_of_cores, algorithm="random", execution_model="WCET", T_MAX=1000000000):
    """
    Policies:
    - random (dynamic)
    - eligibility
    - TPDS2019
    - EMSOFT2019 (dynamic)

    Execution models:
    - WCET
    - half_random
    - full_random
    """

    t = 0

    # initialize cores
    cores = []
    for m in range(number_of_cores):
        core = Core()
        cores.append(core)

    # variables
    finished = False

    w_queue = dag.V.copy()  # waitting queue (not released due to constraints)
    r_queue = []  # ready nodes queue
    f_queue = []  # finished nodes queue

    # if algorithm == "eligibility":
    #     Prio = Eligiblity_Ordering_PA(dag.G, dag.C_dict)
    # elif algorithm == "TPDS2019":
    #     Prio = TPDS_Ordering_PA(dag.G, dag.C_dict)
    # pprint(Prio)

    # start scheduling
    trace(0, t, "Algorithm = {:s}, Exe_Model = {:s}, #Cores = {:d}".format(algorithm, execution_model, number_of_cores))

    # add the source node to the ready queue
    r_queue.append(1)
    w_queue.remove(1)

    while t < T_MAX and not finished:
        trace(0, t, "Scheduling point reached!")

        # update the ready queue (by iterative all left nodes)
        w_queue_c = w_queue.copy()
        f_queue_c = f_queue.copy()

        for i in w_queue_c:
            all_matched = True
            for elem in dag.pre[i]:
                if elem not in f_queue_c:
                    all_matched = False

            if all_matched:
                r_queue.append(i)
                w_queue.remove(i)

        # iterates all cores
        for m in range(number_of_cores):
            if cores[m].idle:
                # if anything is in the ready queue
                if r_queue:
                    # pick the next task
                    if algorithm == "random":
                        # dynamic priority
                        task_idx = random.choice(r_queue)
                    elif algorithm == "EMSOFT2019":
                        # dynamic priority
                        task_idx = EMOSFT_Ordering_PA(r_queue, dag.C_dict)
                    elif algorithm == "eligibility":
                        # static priority
                        # find the task with highest eligibities
                        E_MAX = 0
                        task_idx = r_queue[0]
                        for i in r_queue:
                            if Prio[i] > E_MAX:
                                task_idx = i
                                E_MAX = Prio[i]
                    elif algorithm == "TPDS2019":
                        # static priority
                        # find the task with highest eligibities
                        E_MIN = 1000000
                        task_idx = r_queue[0]
                        for i in r_queue:
                            if Prio[i] < E_MIN:
                                task_idx = i
                                E_MIN = Prio[i]
                    else:
                        task_idx = r_queue[0]

                    # get the task execution time
                    task_wcet = dag.C[task_idx - 1]

                    # assign task to core
                    tau = Job(idx_=task_idx, C_=task_wcet)
                    cores[m].assign(tau)
                    r_queue.remove(task_idx)
                    trace(0, t, "Job {:d} assgined to Core {:d}".format(task_idx, m))

        # check the next scheduling point (the shortest workload time)
        A_LARGE_NUMBER = float("inf")
        sp = A_LARGE_NUMBER
        for core in cores:
            if core.get_workload() != 0:
                if core.get_workload() < sp:
                    sp = core.get_workload()
        # (the default scheduling point is 1, i.e., check on each tick)
        if sp == A_LARGE_NUMBER:
            sp = 1

        # execute for time sp
        t = t + sp  # these two statement happens at the same time!
        for m in range(number_of_cores):
            (tau_idx, tau_finished) = cores[m].execute(sp)

            # check finished task and put into the finished queue
            if tau_finished:
                f_queue.append(tau_idx)
                trace(0, t, "Job {:d} finished on Core {:d}".format(tau_idx, m))

        # exit loop if all nodes are finished
        f_queue.sort()
        dag.V.sort()
        if f_queue == dag.V:
            finished = True

    makespan = t

    if t < T_MAX:
        trace(0, t, "Finished: Makespan is {:d}".format(makespan))
    else:
        trace(3, t, "Simulation Overrun!")

    return makespan