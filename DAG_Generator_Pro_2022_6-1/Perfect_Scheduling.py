import random
import simpy
import networkx as nx
from DAG_Set import DAG_Set
import matplotlib.pyplot as plt
import copy
import Core
import Metric
from random import randint
import DAG
import itertools


class Scheduler(object):
    def __init__(self):
        pass

    def min_node(self, c_state_list):
        ret_dict = {}
        node_finish_time_list = []
        finish_node_list = []
        # 将所有完成时间入栈
        for x in c_state_list:
            node_finish_time_list.append(x.Core_Finish_Time)
        # 找到最早的完成时间
        min_finish_time = min(node_finish_time_list)
        ret_dict['step_time'] = min_finish_time
        # sorted(node_finish_time_list, key=lambda k: k[0])
        # 所有符合最早完成的节点
        for x in c_state_list:
            if x.Core_Finish_Time == min_finish_time:
                finish_node_list.append(x.Current_Running_Node)
        ret_dict['Finish_Node'] = finish_node_list
        return ret_dict

    # 将node_x中的job分配给Idle_Core_Set的core
    def update(self, Idle_Core_Set, node_x, current_time):
        for x in range(len(Idle_Core_Set)):
            temp_node = node_x[x]
            x.Insert_Task_Info(
                dag_ID=1,
                node_ID=temp_node[1]['Node_ID'],
                arrive_time=current_time,
                star_time=current_time,
                finish_time=current_time + temp_node[1]['WCET'])
            x.Core_Finish_Time = current_time + temp_node[1]['WCET']  # absolute time
        return Idle_Core_Set

    def process(self, C_State, BET_BEQ_dict):
        pass

    def Perfect_scheduling(self, dag_set, current_time, C_State):
        temp_dag_set   = copy.deepcopy(dag_set)
        # (1) 所有当前未完成的core
        c_state_list = [c_state_x for c_state_x in C_State if (c_state_x.Core_Finish_Time-current_time > 0)]
        # (2) 在运行的核心中选择完成时间最早的core为下一次的步长
        current_time_1 = current_time
        if len(c_state_list) > 0:
            min_ret = self.min_node(c_state_list)
            Finish_Node_list = min_ret['Finish_Node']
            current_time_1 = current_time + min_ret['step_time']
            # (4) 删除 Finish_Node
            for x in Finish_Node_list:
                temp_dag_set.delet_DAG_Node(x['DAG_ID'], x['Node_ID'])
        # (5) 获取temp_dag_set的就绪节点集合
        temp_dag_set.Status_Data_Up()
        Ready_Node_Set = temp_dag_set.get_ready_node()  # temp_dag_set.获取就绪节点
        # (6) 获取当前的空闲core
        Idle_Core_Set = [state_x for state_x in C_State if (state_x.Core_Finish_Time-current_time_1 == 0)]
        # (7) 从就绪节点中选则上处理器执行的不同情况
        result_list = []
        for node_x in itertools.combinations(Ready_Node_Set, min(len(Ready_Node_Set), len(Idle_Core_Set))):
            # (8) 更新在选择此node_x上处理器执行的情况下的处理器状态。
            C_State_2 = self.update(Idle_Core_Set, node_x, current_time_1)
            BET, BEQ = self.Perfect_scheduling(temp_dag_set, current_time_1, C_State_2)
            result_list.append({"BET": BET, "BEQ": BEQ})
        result_list.sort(key=lambda user: user["BET"])
        # BET_x_1, BEQ_x_2 = min(result_list)
        # step1. DAG_Set 中的就绪节点
        return self.process(C_State, result_list[0])


if __name__ == "__main__":
    # ----------------------
    #       1.DAG 构建
    # ----------------------
    # step0. Dag initial
    DAG_S = DAG_Set()
    Temp_DAG = DAG.DAG()
    Temp_DAG.DAG_ID = "DAG_{}".format(0)
    Temp_DAG.Priority = 0
    Temp_DAG.parallelism = 3
    Temp_DAG.Critical_path = 5
    # step1. DAG结构生成
    Temp_DAG.gen("mine")
    # step2. DAG WCET配置；
    Temp_DAG.WCET_Config("random")
    # step3. DAG 优先级配置；
    Temp_DAG.Priority_Config("random")
    # step4. DAG 关键路径配置；
    Temp_DAG.critical_path_config()
    DAG_S.Add_DAG(Temp_DAG)
    # ----------------------
    #       2.core 配置
    # ----------------------
    core_num = 3
    core_list = []
    for x in range(core_num):
        temp_core = Core.Core()
        temp_core.Core_ID = "Core_{0}".format(x)
        core_list.append(temp_core)
    # ----------------------
    #       3.计算
    # ----------------------
    sch = Scheduler()
    BET, BEQ = sch.Perfect_scheduling(DAG_S, 0, core_list)

    # ----------------------
    #       4.输出结果
    # ----------------------
    x = list(itertools.combinations(['a', 'b', 'c'], 2))


"""
一、笛卡尔积：itertools.product(*iterables[, repeat])
    (1)直接对自身进行笛卡尔积：
    import itertools
    for i in itertools.product('ABCD', repeat = 2):
        print (''.join(i),end=' ')  # print (''.join(i))这个语句可以让结果直接排列到一起

    输出结果：
    AA AB AC AD BA BB BC BD CA CB CC CD DA DB DC DD

    (2)两个元组进行笛卡尔积：
    import itertools
    a = (1, 2, 3)
    b = ('A', 'B', 'C')
    c = itertools.product(a,b)
    for i in c:
        print(i,end=' ')

    输出结果：
    (1, 'A') (1, 'B') (1, 'C') (2, 'A') (2, 'B') (2, 'C') (3, 'A') (3, 'B') (3, 'C')

二、排列：itertools.permutations(iterable[, r])
    import itertools
    for i in itertools.permutations('ABCD', 2):
        print (''.join(i),end=' ')
    
    输出结果：
    AB AC AD BA BC BD CA CB CD DA DB DC

三、组合：itertools.combinations(iterable, r)

    import itertools
    for i in itertools.combinations('ABCD', 3):
        print (''.join(i))

输出结果：
    ABC ABD ACD BCD

四、组合(包含自身重复)：itertools.combinations_with_replacement(iterable, r)
    import itertools
    for i in itertools.combinations_with_replacement('ABCD', 3):
    print (''.join(i),end=' ')
    
    输出结果：
    AAA AAB AAC AAD ABB ABC ABD ACC ACD ADD BBB BBC BBD BCC BCD BDD CCC CCD CDD DDD
"""
