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
        # 所有符合最早完成的core
        for x in c_state_list:
            if x.Core_Finish_Time == min_finish_time:
                finish_node_list.append(x.Current_Running_Node)
        ret_dict['Finish_Node'] = finish_node_list
        return ret_dict

    # 将node_x中的job分配给Idle_Core_Set的core
    def update(self, Idle_Core_Set, node_x, current_time):
        # 在确定了将上处理机执行的node之后，更新各核心的执行状态数据
        for x in range(len(Idle_Core_Set)):
            temp_node = node_x[x]
            # step1.加入将要执行的任务信息
            x.Insert_Task_Info(
                dag_ID=1,
                node_ID=temp_node[1]['Node_ID'],
                arrive_time=current_time,
                star_time=current_time,
                finish_time=current_time + temp_node[1]['WCET'])
            # step2. 更新core的完成时间
            x.Core_Finish_Time = current_time + temp_node[1]['WCET']  # absolute time
            # step3. 更新正在实行的node
            x.Current_Running_Node = temp_node
        return Idle_Core_Set

    def Perfect_scheduling_1(self, input_core_list, input_dag_set, current_time):
        core_running_list = [core_x for core_x in input_core_list if (core_x.Core_Finish_Time - current_time > 0)]
        if len(core_running_list) > 0:
            step_time = min([core_running_x.Core_Finish_Time for core_running_x in core_running_list])  # 最小的完成时间
            current_time = step_time    # 更新完成时间到当前时间
            fn_list = [cr_x.Current_Running_Node for cr_x in core_running_list if cr_x.Core_Finish_Time == current_time]
            for finish_node_x in fn_list:
                input_dag_set.delet_DAG_Node(finish_node_x['DAG_ID'], finish_node_x['Node_ID'])   # 删除所有完成节点
        else:
            if input_dag_set.get_node_num() == 0:     # 说明DAG_Set中所有节点都运行结束了已经运行结束；
                return input_core_list
        input_dag_set.Status_Data_Up()                    # 更新删除节点后的DAG_set
        ready_node_list = input_dag_set.get_ready_node()  # 获取更新后的DAG_Set中的就绪节点：
        Idle_Core_Set_num = len([core_x for core_x in input_core_list if (core_x.Core_Finish_Time <= current_time)])
        res_list = []
        if len(ready_node_list) != 0 and Idle_Core_Set_num != 0:
            # pp = [x for x in itertools.combinations(ready_node_list, min(len(ready_node_list), Idle_Core_Set_num))]
            pp = []
            for x in pp:
            # for x in itertools.combinations(ready_node_list, min(len(ready_node_list), Idle_Core_Set_num)):
                temp_dag_list = copy.deepcopy(input_dag_set)          # 复制DAG_set
                temp_core_list = copy.deepcopy(input_core_list)       # 复制core_list
                temp_idle_Core_list = [core_x for core_x in temp_core_list if (core_x.Core_Finish_Time <= current_time)]
                for y in range(len(x)):                # 每种排列都作为一种情况，进行分配
                    temp_ready_node_x = x[y]                    # 第y个就绪节点
                    temp_idle_Core = temp_idle_Core_list[y]     # 选择运行y号就绪节点的空闲核
                    temp_dag_obj = temp_dag_list.get_dag(DAG_ID=temp_ready_node_x[0])
                    temp_dag_obj.G.node[temp_ready_node_x[1][0]]["state"] = 'running'
                    temp_idle_Core.Current_Running_Node['DAG_ID'] = temp_ready_node_x[0]
                    temp_idle_Core.Current_Running_Node['Node_ID'] = temp_ready_node_x[1][0]
                    temp_idle_Core.Core_Finish_Time = current_time + temp_ready_node_x[1][1]['WCET']
                    temp_idle_Core.Insert_Task_Info(temp_ready_node_x[0],
                                                    temp_ready_node_x[1][0],
                                                    current_time,
                                                    current_time,
                                                    current_time + temp_ready_node_x[1][1]['WCET'],
                                                    temp_ready_node_x[1][1]['Node_ID'])
                r_core_list = self.Perfect_scheduling_1(temp_core_list, temp_dag_list, current_time)
                res_list.append({'makespan': max([x.Core_Finish_Time for x in r_core_list]),
                                 'core_list': r_core_list})
            res_list.sort(key=lambda x: x['makespan'])
            return res_list[0]['core_list']
        else:
            r_core_list = self.Perfect_scheduling_1(input_core_list, input_dag_set, current_time)
            return r_core_list

    def show_dag_and_makespan(self, dag_set, core_obj_list ):
        for x in range(0, len(dag_set.Dag_Set)):
            posi = 200 + 10 * len(dag_set.Dag_Set) + (x + 1)
            plt.subplot(posi)
            dag_set.Dag_Set[x].graph_node_position_determine()
            # plt.title("{0}\nrta_non_preempt:{1}\nrta_preempt:{2}".format(
            #             self.dag_set.Dag_Set[x].DAG_ID,
            #             self.dag_set.Dag_Set[x].Response_Time_analysis(
            #                 "non-preemptive", self.core_num_list[0]),
            #             self.dag_set.Dag_Set[x].Response_Time_analysis(
            #                 "preemptive", self.core_num_list[0])),
            #           fontsize=5, color="black", weight="light", ha='left', x=0)
        plt.subplot(212)
        core_channel = 0
        yticke_1 = []
        yticke_2 = []
        for processor in core_obj_list:
            for core in processor:
                yticke_1.append(core_channel * 3)
                yticke_2.append(core.Core_ID)
                for job_info in core.Core_Running_Task:
                    plt.barh(
                        y=core_channel * 3,
                        width=job_info['execution_time'],
                        height=2,
                        left=job_info['star_time'], color='grey', edgecolor='black')
                    plt.text(
                        x=job_info['star_time'],
                        y=core_channel * 3 - 1, s=job_info['star_time'], fontsize=5)
                    plt.text(
                        x=job_info['star_time'] + job_info['execution_time'] / 2,
                        y=core_channel * 3, s='{1}\n{2}'.format(
                            job_info['dag_ID'], job_info['node_name'], job_info['execution_time']),
                        fontsize=5)
                    plt.text(
                        x=job_info['finish_time'],
                        y=core_channel * 3 + 1, s=job_info['finish_time'], fontsize=5)
                core_channel += 1
        temp_makespan_list = []
        for x in core_obj_list:
            for y in x:
                temp_makespan_list.append(y.Get_core_finish_time())
        temp_makespan = max(temp_makespan_list)
        plt.title("makespan:{0}\nCPU_utilization:{1:2f}\nDAG_VOL:{2}".format(
            temp_makespan,
            Metric.CPU_uilization(core_obj_list, temp_makespan),
            Metric.DAG_Set_volume(dag_set)),
            fontsize=5, color="black", weight="light", ha='left', x=0)
        plt.yticks(yticke_1, yticke_2, fontsize=8)
        plt.xticks(rotation=30)
        x = range(0, temp_makespan, 100000)
        plt.xticks(x, color='blue', rotation=0, fontsize=8)
        # 参数x空值X轴的间隔，第二个参数控制每个间隔显示的文本，后面两个参数控制标签的颜色和旋转角度
        plt.show()


if __name__ == "__main__":
    # ----------------------
    #       1.DAG 构建
    # ----------------------
    # step0. Dag initial
    DAG_S = DAG_Set()
    # ####### 1.手动 DAG set ######## #
    DAG_S.user_defined_dag()
    # ####### 2.随机生成DAG set ##### #
    # DAG_Set.Random_DAG_Set(DAG_count=3, parallelism_list=[3, 4, 5], critical_path_list=[3, 4, 5])
    """
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
    """
    # ----------------------
    #       2.core 配置
    # ----------------------
    core_num = 5
    core_list = []
    for core_num_x in range(core_num):
        temp_core = Core.Core()
        temp_core.Core_ID = "Core_{0}".format(core_num_x)
        core_list.append(temp_core)
    # ----------------------
    #       3.计算
    # ----------------------
    sch = Scheduler()
    T_DAG_S = copy.deepcopy(DAG_S)
    core_l = sch.Perfect_scheduling_1(core_list, T_DAG_S, 0)

    # ----------------------
    #       4.输出结果
    # ----------------------
    sch.show_dag_and_makespan(DAG_S, [core_l])
    # x = list(itertools.combinations(['a', 'b', 'c'], 2))


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
