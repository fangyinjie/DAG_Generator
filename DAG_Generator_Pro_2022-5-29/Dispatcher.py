import simpy
import DAG_Set
import matplotlib.pyplot as plt
import copy
import Core
# import random
# import networkx as nx

# Schedule Strategy
# (1) FCFS              First Come First Serve
# (1) SJF/SPF/SRTN      Shortest Job First/Shortest Process First/Shortest Remain Time Next
# (2) PSA               Priority-scheduling algorithm
# (3) HRRN              Highest response ratio next
# (2) RR                Round-Robin
# (3) RM                Rate Monotonic Scheduling
# (4) EDF               Earliest Deadline First Scheduling
# (5) LLF               Least laxity first scheduling
# (6) DM                Deadling Monotonic Scheduling
# (7) MFQ               Multilevel Feedback Queue


class Dispatcher_Workspace(object):
    """ 一个处理器（Processor），拥有特定数量的资源（core，内存，缓存等）。
    一个客户首先申请服务。在对应服务时间完成后结束并离开工作站 """
    def __init__(self, env, dag_set, core_num):
        self.env        = env       # simpy实体
        self.core_num   = core_num
        # （1）初始化DAG集合
        self.dag_set    = dag_set
        self.dag_set.Status_Dataup()    # 更新节点状态，所有前驱为0的节点进入就绪态
        self.Temp_DAG_Set = copy.deepcopy(self.dag_set)
        # （2）初始化CPU资源
        self.core_list = []
        for x in range(self.core_num):
            temp_core = Core.Core()
            temp_core.Core_ID = "{0}".format(x)
            self.core_list.append(temp_core)
        # （3）初始化任务完成后反馈给任务管理器的event
        self.job_event = self.env.event()       # event_1："job_finish"
        self.env.process(self.Setup())

    def Setup(self):
        # while True:
        while self.Temp_DAG_Set.get_node_num() > 0:
            # 1.获取Temp_DAG_Set中处于就绪态的节点列表
            x, temp_node_list = \
                self.Temp_DAG_Set.get_priority_ready_node_list()
            # 如果就绪的node，不管有没有CPU直接开进程
            if x:
                for temp_dagx in temp_node_list:
                    dag_ID = temp_dagx[0]
                    for t_nodex in temp_dagx[1]:
                        self.env.process(self.Core_Running(dag_ID, t_nodex))
            # 如果没有就绪的node，则等待node结束的event
            value = yield self.job_event
            if value == 'job_finish':
                self.Temp_DAG_Set.Status_Dataup()
            else:
                print('event job finish error!\n')
        self.Show_Core_Set()
        self.Show_Dag_And_Makespan()

    def Core_Running(self, dag_ID, node):
        arrive_time = self.env.now                          # 1.记录到达时间
        node[1]['state'] = 'running'                        # 2.标记节点进入运行态
        with self.core_set.request() as req:
            p, temp_core = yield req
        yield self.core_set.get(priority=1)
        p, temp_core = yield self.core_set.get(priority=1)            # 3.等待CPU资源getstore
        start_time = self.env.now                           # 4.记录运行时间
        yield self.env.timeout(node[1].get('WCET'))         # 5.延时运行
        finish_time = self.env.now                          # 6.记录完成时间
        self.Temp_DAG_Set.delet_DAG_Node(dag_ID, node[0])   # 7.删除节点
        self.Temp_DAG_Set.Status_Dataup()                   # 8.更新DAG集状态
        temp_core.Insert_Task_Info(
            dag_ID=dag_ID,
            node_ID=node[1].get('Node_ID'),
            arrive_time=arrive_time,
            star_time=start_time,
            finish_time=finish_time)
        self.core_set.put(simpy.PriorityItem(p, temp_core))
        self.job_event.succeed('job_finish')        # 8.向Setup发送完成事件
        self.job_event = self.env.event()


    def Dag_Generator(self):
        # Dag_Set中DAG的到达时间向 Temp中加入DAG。
        pass

    def Show_Core_Set(self):
        for temp_core in self.core_list:
            temp_core.Show_Core()

    def Show_Dag_And_Makespan(self):
        for x in range(0, len(self.dag_set.Dag_Set)):
            posi = 200 + 10 * len(self.dag_set.Dag_Set) + (x + 1)
            plt.subplot(posi)
            self.dag_set.Dag_Set[x].graph_node_position_determine()

            plt.title("{0}\nrta_non_preempt:{1}\nrta_preempt:{2}".format(
                        self.dag_set.Dag_Set[x].DAG_ID,
                        self.dag_set.Dag_Set[x].Response_Time_analysis("non-preemptive", self.core_num),
                        self.dag_set.Dag_Set[x].Response_Time_analysis("preemptive", self.core_num)),
                      fontsize=5, color="black", weight="light", ha='left', x=0)

        plt.subplot(212)
        core_channel = 0
        fort = {1: "core1", 2: "core2", 3: "core3"}

        plt.yticks([1,2,3,4],["core1","core2","core3","core4"])

        # for k, v in self.makespan_dict.items():
        #     for x in v:
        #         plt.barh(y=core_channel * 3, width=x[3] - x[2], height=2, left=x[2], color='grey', edgecolor='black')
        #         plt.text(x=x[3], y=core_channel * 3 + 1, s=x[3], fontsize=5)
        #         plt.text(x=x[2] + (x[3] - x[2]) / 2, y=core_channel * 3, s='{0}\n{1}'.format(x[0], x[1]), fontsize=5)
        #         plt.text(x=x[2], y=core_channel * 3 - 1, s=x[2], fontsize=5)
        #     core_channel += 1
        # plt.title("makespan:{0}".format(self.makespan_compute()),
        #     fontsize=5, color="black", weight="light", ha='left', x=0)
        plt.show()

if __name__ == "__main__":
    environment = simpy.Environment()
    DAG_Set = DAG_Set.DAG_Set()
    # ####### 1.手动DAG set ######## #
    DAG_Set.user_defined_dag()
    # ####### 2.随机生成DAG set ##### #
    # DAG_Set.Random_DAG_Set(DAG_count=4, parallelism_list=[3, 3, 3, 3], critical_path_list=[3, 3, 3, 3])
    Dispatcher = Dispatcher_Workspace(
        env=environment, dag_set=DAG_Set, core_num=3)
    # Dispatcher.Setup()

    environment.run(until=10000000)


