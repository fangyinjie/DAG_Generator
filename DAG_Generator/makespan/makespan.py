import random
from DAG_Generator.makespan.task import DAGTask, Job
from DAG_Generator.makespan.processor import Core
# from graph import find_longest_path_dfs, find_associative_nodes
# from rta_alphabeta_new import Eligiblity_Ordering_PA, TPDS_Ordering_PA, EMOSFT_Ordering_PA
# from rta_alphabeta_new import load_task

def sched(dag, number_of_cores, algorithm="random", execution_model="WCET", T_MAX=1000000000):
    # Policies: - random (dynamic) - eligibility - TPDS2019 - EMSOFT2019 (dynamic)
    # Execution models: - WCET - half_random - full_random
    # initialize cores
    cores = []
    for m in range(number_of_cores):
        core = Core()
        cores.append(core)

    # variables
    finished = False
    w_queue = []  # waitting queue (not released due to constraints)
    r_queue = []  # ready nodes queue
    f_queue = []  # finished nodes queue
    for id, label in enumerate(dag.V):
        w_queue.append(label)
    # if algorithm == "eligibility":
    #    Prio = Eligiblity_Orderiyng_PA(dag.G, dag.C_dict)
    #  elif algorithm == "TPDS2019":
    #    Prio = TPDS_Ordering_PA(dag.G, dag.C_dict)
    # pprint(Prio)
    # Prio = {1,2,3,4};
    Prio = {0, 3, 2, 4, 1, 5, 6, 7, 8, 9, 10, 13, 11, 12, 14, 15, 16}
    # start scheduling
    # trace(0, t, "Algorithm = {:s}, Exe_Model = {:s}, #Cores = {:d}".format(algorithm, execution_model, number_of_cores))
    # add the source node to the ready queue
    r_queue.append(0)
    w_queue.remove(0)

    t = 0
    while t < T_MAX and not finished:
        # update the ready queue (by iterative all left nodes)
        w_queue_c = w_queue.copy()
        f_queue_c = f_queue.copy()

        for i in w_queue_c:
            all_matched = True
            for elem in dag.pre:
                if elem not in f_queue_c:
                    all_matched = False

            if all_matched:
                r_queue.append(0)
                w_queue.remove(0)

        # iterates all cores
        for m in range(number_of_cores):
            if cores[m].idle:
                # if anything is in the ready queue
                if r_queue:
                    # pick the next task
                    """
                    if algorithm == "random":
                        # dynamic priority
                        task_idx = random.choice(r_queue)
                    # elif algorithm == "EMSOFT2019":
                        # dynamic priority
                        # task_idx = EMOSFT_Ordering_PA(r_queue, dag.C_dict)
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
                    """
                    task_idx = r_queue[0]
                    # get the task execution time
                    task_wcet = dag.C[task_idx - 1]

                    # assign task to core
                    tau = Job(idx_=task_idx, C_=task_wcet)
                    cores[m].assign(tau)
                    r_queue.remove(task_idx)
                    # trace(0, t, "Job {:d} assgined to Core {:d}".format(task_idx, m))

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
                # trace(0, t, "Job {:d} finished on Core {:d}".format(tau_idx, m))

        # exit loop if all nodes are finished
        f_queue.sort()
        dag.V.sort()
        if f_queue == dag.V:
            finished = True

    makespan = t

    # if t < T_MAX:
        # trace(0, t, "Finished: Makespan is {:d}".format(makespan))
    # else:
        # trace(3, t, "Simulation Overrun!")

    return makespan

import networkx as nx
import numpy as np
if __name__ == "__main__":
    # G_dict, C_dict, C_array, lamda, VN_array, L, W = load_task(idx)
    Matrix = np.array(
        [
            [0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
    )
    graph = nx.from_numpy_matrix(Matrix)

    WCET_HE = [12825, 6561, 5293, 7280, 6398, 4372, 4707, 3411, 2165, 2753, 1643, 1010, 1363, 1081, 1063, 1004, 4571]

    priority = [0, 3, 2, 4, 1, 5, 6, 7, 8, 9, 10, 13, 11, 12, 14, 15, 16]

    dag = DAGTask(graph, WCET_HE, priority)

    R1 = sched(dag, number_of_cores=6, algorithm="eligibility", execution_model="WCET")
