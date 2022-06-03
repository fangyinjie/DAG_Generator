import random
import simpy
import networkx as nx
import DAG_Set
import matplotlib.pyplot as plt
import copy
import Core


def CPU_uilization(Core_obj_set, makespan):
    core_num = 0
    all_execution_time = 0
    for x in Core_obj_set:
        core_num += len(x)
        for y in x:
            for z in y.Core_Running_Task:
                all_execution_time += z['execution_time']
    return all_execution_time/(core_num*makespan)


def DAG_Set_volume(dag_set):
    vol = 0
    for x in dag_set.Dag_Set:
        vol = x.get_dag_volume()
    return vol
