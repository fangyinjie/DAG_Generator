#!/usr/bin/python3
# -*- coding: utf-8 -*-

################################################################################
# Core config
# Fang YJ
# Real-Time Systems Group
# Hunan University HNU
################################################################################

class Core:
    def __init__(self):
        self.Core_ID            = ''
        self.Core_Type          = ''        # e.g. 'Cortex-M3'；
        self.Core_Running_Task  = []        # the running log about this core

    def Insert_Task_Info(self, dag_ID, node_ID, arrive_time, star_time, finish_time):
        temp_dict = {
            'dag_ID':           dag_ID,
            'node_ID':          node_ID,
            'arrive_time':      arrive_time,
            'star_time':        star_time,
            'finish_time':      finish_time,
            'execution_time':   finish_time - star_time}
        self.Core_Running_Task.append(temp_dict)
        return True

    def Show_Core(self):
        print(" Core_ID:", self.Core_ID)
        print(" Running List:", len(self.Core_Running_Task))
        for x in range(0, len(self.Core_Running_Task)):
            print("     ", self.Core_Running_Task[x])

    def Get_core_finish_time(self):
        sorted(self.Core_Running_Task, key=lambda k: k['finish_time'])
        return self.Core_Running_Task[-1]['finish_time']
    """ old code """
    # def Get_Core_Running_List(self):
    #     # 返回Core_Running_Task列表；
    #     return self.Core_Running_Task
    #
    # def Insert_Task(self, DAG_ID, Task_ID, Star_Time, WCET, Task_name):
    #     # 向Core_Running中加入元素
    #     self.Core_Running_Task.append(
    #         (DAG_ID,     Task_ID,   Star_Time,  WCET,   Star_Time + WCET, Task_name)
    #     )
    #     self.Last_comleted_Time = Star_Time + WCET  # 更新core的完成时间
    #     self.Insert_Core_Busy()                     # 更新core状态为BUSY
    #     return True
    #
    # def Insert_Core_Busy(self):
    #     self.Core_State_Is_IDLE = False
    #
    # def Insert_Core_False(self):
    #     self.Core_State_Is_IDLE = True
    #


if __name__ == "__main__":
    core = Core()
    core.Core_ID = "1_1"
    core.Insert_Task_Info(dag_ID='1', node_ID='1', arrive_time=10, star_time=100, finish_time=200)
    core.Insert_Task_Info(dag_ID='2', node_ID='2', arrive_time=10, star_time=100, finish_time=200)
    core.Insert_Task_Info(dag_ID='3', node_ID='3', arrive_time=10, star_time=100, finish_time=200)
    core.Insert_Task_Info(dag_ID='4', node_ID='4', arrive_time=10, star_time=100, finish_time=200)
    core.Show_Core()

