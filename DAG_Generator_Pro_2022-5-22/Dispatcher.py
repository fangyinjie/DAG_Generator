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
    def __init__(self, run_env, Dag_Set, core_num):
        self.env        = run_env       # simpy实体
        self.Dag_Set    = Dag_Set
        self.core_num   = core_num
        # 资源配置（CPU）
        # self.core_Set   = simpy.Resource(self.env, core_num)  # 类给env配资源
        self.core_Set   = simpy.PriorityStore(self.env, core_num)
        for x in range(3):
            temp_core = Core.Core(Core_ID="".format(x))
            self.core_Set.put(simpy.PriorityItem(1, temp_core))

        self.Dag_Set.Status_Dataup()  # 更新节点状态，所有前驱为0的节点进入就绪态
        self.makespan_dict = {}
        self.Temp_DAG_Set = copy.deepcopy(self.Dag_Set)

    # env = simpy.Environment()
    # pstore = simpy.PriorityStore(env, 3)
    # log = []
    # #
    # items = [x for x in range(3)]
    # items = [Core.Core(Core_ID="1_1")]
    # # Unorderable items are inserted with same priority.
    # env.process((pstore.put(simpy.PriorityItem(item, item)) for item in items))
    # env.process(getter(1))
    # env.process(getter(2))
    # env.process(getter(3))
    # env.process(getter(4))
    # env.process(getter(5))
    # env.run()
    # print(log)

    # 每个core的运作，系统中有几个core就有几个Core_act进程
    def Core_act(self, environment, core_ID):
        while self.Temp_DAG_Set.get_node_num() > 0:
            if Temp_DAG_Set.get
            # (1)若CPU资源和就绪队列有一个为空，则等待事件；
            # (2)否则将就绪队列中优先级最高的上处理器，包括抢占。
            with self.core_Set.request() as request:
                yield request
                # step1.有core资源的情况下，搜索当前的Dag_Set中处于就绪态的节点list。
                # 获取优先级最高的DAG以及此DAG中进入就绪状态的node list
                DAG_ID, ready_high_node = self.Temp_DAG_Set.get_priorituy_ready_node()
                if not ready_high_node:
                    yield environment.timeout(1)
                    continue
                # step2.将此list中优先级最高的节点上处理器，状态进入运行态；并记录开始时间
                start_time = environment.now
                ready_high_node[1]['state'] = 'running'
                # step3.运行节点，timeout = WCET
                WCET = ready_high_node[1].get('WCET')
                yield environment.process(self.Node_run(WCET))
                # step4.记录终止时间
                end_time = environment.now
                self.Temp_DAG_Set.delet_DAG_Node(DAG_ID, ready_high_node[0])
                self.Temp_DAG_Set.Status_Dataup()
                # step5.打印，core_ID;
                # print("Core_ID:{0}, DAG_ID:{1}, node_ID:{2}, start_time:{3}, end_time：{4}".format(
                #     core_ID, DAG_ID, ready_high_node[1].get('Node_ID'), start_time, end_time))
                if self.makespan_dict.get(core_ID) is None:
                    self.makespan_dict[core_ID] = [(DAG_ID, ready_high_node[1].get('Node_ID'), start_time, end_time)]
                else:
                    self.makespan_dict[core_ID].append((DAG_ID, ready_high_node[1].get('Node_ID'), start_time, end_time))
        self.show_dag_and_makespan()

    def makespan_compute(self):
        temp_endtime_list = []
        for k, v in self.makespan_dict.items():
            for x in v:
                temp_endtime_list.append(x[3])
        temp_endtime_list.sort()
        return temp_endtime_list[-1]

    def Node_run(self, run_time):
        yield env.timeout(run_time)

    def show_dag_and_makespan(self):
        for x in range(0, len(self.Dag_Set.Dag_Set)):
            posi = 200 + 10 * len(self.Dag_Set.Dag_Set) + (x + 1)
            plt.subplot(posi)
            self.Dag_Set.Dag_Set[x].graph_node_position_determine()

            plt.title("{0}\nrta_non_preempt:{1}\nrta_preempt:{2}".format(
                        self.Dag_Set.Dag_Set[x].DAG_ID,
                        self.Dag_Set.Dag_Set[x].Response_Time_analysis("non-preemptive", self.core_num),
                        self.Dag_Set.Dag_Set[x].Response_Time_analysis("preemptive", self.core_num)),
                      fontsize=5, color="black", weight="light", ha='left', x=0)
        plt.subplot(212)
        core_channel = 0
        for k, v in self.makespan_dict.items():
            for x in v:
                plt.barh(y=core_channel * 3, width=x[3] - x[2], height=2, left=x[2], color='grey', edgecolor='black')
                plt.text(x=x[3], y=core_channel * 3 + 1, s=x[3], fontsize=5)
                plt.text(x=x[2] + (x[3] - x[2]) / 2, y=core_channel * 3, s='{0}\n{1}'.format(x[0], x[1]), fontsize=5)
                plt.text(x=x[2], y=core_channel * 3 - 1, s=x[2], fontsize=5)
            core_channel += 1
        plt.title("makespan:{0}".format(self.makespan_compute()),
            fontsize=5, color="black", weight="light", ha='left', x=0)
        plt.show()


def setup(environment, dag_set, core_num):
    # 分配器建立资源，只要有资源就开始运行
    while Dispatcher.Temp_DAG_Set.get_node_num() > 0:
        for i in range(core_num):
            env.process(Dispatcher.Core_act(env, "core_{0}".format(i)))  # 创建clientNumber个初始客户
    # while Dag_Set.get_node_num() > 0:
    while True:
        yield env.timeout(100)  # 在仿真过程中持续创建客户 3-8分钟
        # env.process(Client(env, 'Client_%d' % i, workstation))


if __name__ == "__main__":

    environment = simpy.Environment()       # 创建一个环境并开始仿真
    DAG_Set = DAG_Set.DAG_Set()
    # ####### 1.手动DAG set ######## #
    # DAG_Set.user_defined_dag()
    # ####### 2.随机生成DAG set ##### #
    DAG_Set.Random_DAG_Set(DAG_count=4, parallelism_list=[3, 3, 3, 3], critical_path_list=[3, 3, 3, 3])
    Dispatcher = Dispatcher_Workspace(environment, DAG_Set, core_num=3)
    environment.process(setup(env, DAG_Set, core_num=2))  # 开始执行!
    environment.run(until=10000000)

