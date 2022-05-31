import random
import simpy
import networkx as nx
import DAG_Set
import matplotlib.pyplot as plt
import copy
import Core
import Metric


class Dispatcher_Workspace(object):
    def __init__(self, env, dag_set, core_num_list):
        self.env            = env           # simpy entity
        self.core_num_list  = core_num_list
        # 1.initial the dag_set
        self.dag_set        = dag_set
        self.Temp_DAG_Set   = copy.deepcopy(self.dag_set)
        # 2.PriorityStore save the ready node in Dag_Set.
        # self.node_store = simpy.FilterStore(self.env)
        self.node_store = simpy.PriorityStore(self.env)
        # 3.initial the CPU resource
        self.core_obj_list      = []
        for x in range(len(self.core_num_list)):
            temp_core_list = []
            for y in range(self.core_num_list[x]):
                temp_core = Core.Core()
                temp_core.Core_ID = "P{0}_Core_{1}".format(x, y)
                temp_core_list.append(temp_core)
            self.core_obj_list.append(temp_core_list)

    def Run(self):
        for Proccessor_ID in range(len(self.core_num_list)):
            for x in range(self.core_num_list[Proccessor_ID]):
                self.env.process(self.Core_running(self.core_obj_list[Proccessor_ID][x]))
        self.Temp_DAG_Set.Status_Data_Up_Store(self.node_store)

    def Core_running(self, core_obj):
        while True:
            prio, job = yield self.node_store.get()      # x是优先级，y是节点对象
            job_dag_id = job[0]
            job_node = job[1]
            start_time = self.env.now                    # 1.记录开始时间
            job_node[1]['state'] = 'running'             # 2.标记节点进入运行态
            yield self.env.timeout(job_node[1]['WCET'])  # 3.执行job，y的WCET或者WCET与BCET中的随机数
            finish_time = self.env.now                   # 4.记录完成时间
            self.Temp_DAG_Set.delet_DAG_Node(job_dag_id, job_node[0])  # 5.删除节点
            core_obj.Insert_Task_Info(
                dag_ID=job_dag_id,
                node_ID=job_node[1].get('Node_ID'),
                arrive_time=0,
                star_time=start_time,
                finish_time=finish_time)
            self.Temp_DAG_Set.Status_Data_Up_Store(self.node_store)
            if self.Temp_DAG_Set.get_node_num() == 0:
                self.show_dag_and_makespan()
                self.env.exit()

    def show_dag_and_makespan(self):
        for x in range(0, len(self.dag_set.Dag_Set)):
            posi = 200 + 10 * len(self.dag_set.Dag_Set) + (x + 1)
            plt.subplot(posi)
            self.dag_set.Dag_Set[x].graph_node_position_determine()
            plt.title("{0}\nrta_non_preempt:{1}\nrta_preempt:{2}".format(
                        self.dag_set.Dag_Set[x].DAG_ID,
                        self.dag_set.Dag_Set[x].Response_Time_analysis(
                            "non-preemptive", self.core_num_list[0]),
                        self.dag_set.Dag_Set[x].Response_Time_analysis(
                            "preemptive", self.core_num_list[0])),
                      fontsize=5, color="black", weight="light", ha='left', x=0)
        plt.subplot(212)
        core_channel = 0
        yticke_1 = []
        yticke_2 = []
        for processor in self.core_obj_list:
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
                            job_info['dag_ID'], job_info['node_ID'], job_info['execution_time']),
                        fontsize=5)
                    plt.text(
                        x=job_info['finish_time'],
                        y=core_channel * 3 + 1, s=job_info['finish_time'], fontsize=5)
                core_channel += 1
        temp_makespan_list = []
        for x in self.core_obj_list:
            for y in x:
                temp_makespan_list.append(y.Get_core_finish_time())
        temp_makespan = max(temp_makespan_list)
        plt.title("makespan:{0}\nCPU_utilization:{1:2f}".format(
            temp_makespan, Metric.CPU_uilization(self.core_obj_list, temp_makespan)),
            fontsize=5, color="black", weight="light", ha='left', x=0)
        plt.yticks(yticke_1, yticke_2, fontsize=8)
        plt.xticks(rotation=30)
        x = range(0, temp_makespan, 100000)
        plt.xticks(x, color='blue', rotation=0, fontsize=8)
        # 参数x空值X轴的间隔，第二个参数控制每个间隔显示的文本，后面两个参数控制标签的颜色和旋转角度
        plt.show()


if __name__ == "__main__":
    environment = simpy.Environment()  # create a environment for simulation
    DAG_Set = DAG_Set.DAG_Set()
    # ####### 1.手动 DAG set ######## #
    # DAG_Set.user_defined_dag()
    # ####### 2.随机生成DAG set ##### #
    DAG_Set.Random_DAG_Set(DAG_count=3, parallelism_list=[3, 4, 5], critical_path_list=[3, 4, 5])
    Dispatcher = Dispatcher_Workspace(environment, DAG_Set, core_num_list=[5])
    Dispatcher.Run()
    environment.run()
