#!/usr/bin/python3
# -*- coding: utf-8 -*-

################################################################################
# Dispatcher
# Fang YJ
# Real-Time Systems Group
# Hunan University HNU
################################################################################

import networkx as nx
import DAG_Set
import Processor
import copy
import matplotlib.pyplot as plt


class Dispatcher:
    def __init__(self, dag_set, processor):
        self.DAG_Set = dag_set  # DAG:-networkX结构
        self.Processor = processor
        self.DAG_Set_Num = dag_set.get_dag_num()

    # def Calculation_Priority(self):

    def Show(self):
        self.DAG_Set.Show_DAG_Set()
        self.Processor.Show_Processor()

    def Scheduling(self):
        # 1.为每个DAG分配优先级（单DAG可忽略）
        # 2.为每个DAG中所有节点分配优先级
        trm_i = 1 + 1
        self.DAG_Set.Show_DAG_Set()
        return trm_i
        # 返回DAG，其中每个节点都有优先级

    def Mapping(self, Processor_list, DAG_Set):
        # 为每个DAG节点分配core
        # 为每一类核分配一个列表，在每个列表中为每个核确定一个列表，一个列表，具体为每个节点的起始时间，执行时间，和运行在什么核上
        processor = Processor.Processor(Processor_list, 'GD_32')
        processor.Update_Processor_State(0)  # 初始化系统时间为 0

    def Simulation(self):
        # 多DAG在多处理器上的运行仿真
        Temp_Current_Time = 0
        Temp_DAG_Set = copy.deepcopy(self.DAG_Set)
        # 获取所有当前所有DAG中前驱为0的状态state为节点，将其状态设为Ready
        while Temp_DAG_Set.get_node_num() > 0:
            # step-1.将Temp_DAG_Set中前驱节点为0且未就绪的节点的节点进入就绪队列
            for x in Temp_DAG_Set.Dag_Set:
                for y in x.G.nodes(data=True):
                    # for y in Temp_DAG_Set[x].nodes(data=True):
                    if (len(list(x.G.predecessors(y[0]))) == 0) and (y[1].get('state') == 'blocked'):
                        y[1]['state'] = 'ready'
            # step-2.将结合当前core_running_list中，运行时间小于当前时间的核，为其分配就绪队列中优先级最大的任务，
            # 将就绪态任务一次交予空闲core执行
            Idle_processor_list = self.Processor.Get_Idle_Core_ID() # 找到当前空闲的core
            for x in Idle_processor_list:
                DAG_ID, Temp_node = Temp_DAG_Set.get_priorituy_ready_node_list()
                if not DAG_ID:
                    break
                self.Processor.Add_Task_To_Core(x.Core_ID,
                                                DAG_ID=DAG_ID,
                                                Task_ID=Temp_node[0],
                                                Star_Time=Temp_Current_Time,
                                                WCET=Temp_node[1].get('WCET'),
                                                Task_name=Temp_node[1].get('Node_ID'))
                Temp_node[1]['state'] = 'running'
                x.Insert_Core_Busy()
                # 关键：具体为选择什么任务上处理器 ，不同的调度算法可能有所不同
                # 这里选择就绪节点中，优先级最高的节点上处理器
            # step-3 集中所有忙碌的核，在这些核心中找到最早结束的
            Temp_busy_list = self.Processor.Get_Busy_Core_ID()
            dicc = {}
            for x in Temp_busy_list:
                dicc[x] = x.Last_comleted_Time
            dicc_list = sorted(dicc.items(), key=lambda x: x[1])
            temp_close_time = dicc_list[0][1]
            finish_core_list = []
            for x in dicc_list:
                if x[1] == temp_close_time:
                    finish_core_list.append(x[0])
            Temp_Current_Time = temp_close_time
            # Temp_Current_Time = dicc_list[0][0].Last_comleted_Time  # 更新系统时间
            for x in finish_core_list:
                x.Core_State_Is_IDLE = True
                tem_DAG_ID, tem_Task_ID, tem_Start_Time, tem_Finish_Time, tem_WCET, tem_Task_name = \
                    x.Core_Running_Task[-1]
                Temp_DAG_Set.delet_DAG_Node(tem_DAG_ID, tem_Task_ID)
        return True

    def show_dag_and_makespan(self):
        for x in range(0, len(self.DAG_Set.Dag_Set)):
            posi = 200 + 10 * len(self.DAG_Set.Dag_Set) + (x+1)
            plt.subplot(posi)
            # for x in self.Processor.Core_list:
            self.DAG_Set.Dag_Set[x].graph_node_position_determine()
        plt.subplot(212)
        # plt.subplot()
        for x in range(0, len(self.Processor.Core_list)):
            for y in self.Processor.Core_list[x].Core_Running_Task:
                # (DAG_ID, Task_ID, Start_Time, Finish_Time, WCET)
                plt.barh(y=x*3, width=y[3], height=2, left=y[2], color='grey', edgecolor='black')
                plt.text(x=y[4],        y=x*3+1, s=y[4], fontsize=5)
                plt.text(x=y[2]+y[3]/2, y=x*3,   s='{0}\n{1}'.format(y[0], y[5]), fontsize=5)
                plt.text(x=y[2],        y=x*3-1, s=y[2], fontsize=5)
        plt.show()


if __name__ == "__main__":
    # 1.Processor initial
    proc = Processor.Processor([4], 'GD_32')
    # 2.Dag_Set initial
    ds = DAG_Set.DAG_Set()
    ds.user_defined_dag()
    disp = Dispatcher(ds, proc)
    disp.Show()
    disp.Simulation()
    proc.Show_Processor()
    # proc.Show_Processor_makespan()
    disp.show_dag_and_makespan()
