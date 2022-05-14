import random
import simpy
import networkx as nx
import DAG_Set
import matplotlib.pyplot as plt
import copy
import random
import simpy
import networkx as nx
import DAG_Set
import matplotlib.pyplot as plt
import copy


class Dispatcher_Workspace(object):
    """ 一个处理器（Processor），拥有特定数量的资源（core，内存，缓存等）。
    一个客户首先申请服务。在对应服务时间完成后结束并离开工作站 """

    def __init__(self, env, Dag_Set, Core_Num):
        self.env = env  # simpy实体
        self.Core_Num = Core_Num
        self.Makespan_List = []         # Makespan信息，结束后分析使用
        self.Makespan_Dict = {}
        self.Sys_Event = env.event()    # 系统用事件，每个node运行结束后就会向调度程序发一个事件以重新运行新的node
        self.Core_Set = simpy.PriorityResource(env, capacity=Core_Num)  # 类给env配资源
        self.Dag_Set = Dag_Set
        self.Dag_Set.Status_Dataup()  # 更新节点状态，所有前驱为0的节点进入就绪态
        self.Temp_DAG_Set = copy.deepcopy(self.Dag_Set)
        self.Temp_all_node = self.Temp_DAG_Set.get_node_num()

    def Run(self):
        while self.Temp_DAG_Set.get_node_num() > 0:
            DAG_ID, ready_high_node = self.Temp_DAG_Set.get_priorituy_ready_node()  # 获取一个优先级最高的
            if not ready_high_node:
                yield env.timeout(1)
                continue
            ready_high_node[1]['state'] = 'running'
            self.env.process(self.Node_Run(DAG_ID, ready_high_node))
        self.Makespan_Dict = dict(sorted(self.Makespan_Dict.items(), key=lambda x: x[1][1]))
        print(self.Makespan_Dict)
        self.Makespan_Assign()
        self.show_dag_and_makespan()

    def Makespan_Assign(self):
        temp_max_time = [[(0, 0, 0, 0)] for x in range(self.Core_Num)]
        ii = 0
        for k, v in self.Makespan_Dict.items():
            for x in temp_max_time:
                if x[-1][-1] <= v[1]:
                    x.append((k, v[0], v[1], v[2]))
                    ii += 1
                    break
        self.Makespan_List = temp_max_time
        assert ii == len(self.Makespan_Dict)
        for x in range(self.Core_Num):
            temp_max_time[x].pop(0)
        temp_dit = {}
        for x in range(len(self.Makespan_List)):
            temp_dit[x] = []
            for y in self.Makespan_List[x]:
                temp_dit[x].append((y[0], y[1], y[2], y[3]))
        self.Makespan_Dict = temp_dit
        print(self.Makespan_Dict)

    def Node_Run(self, DAG_ID, ready_high_node):
        Arrive_Time = self.env.now
        with self.Core_Set.request(
                priority=ready_high_node[1].get('priority') +
                self.Temp_all_node * self.Dag_Set.get_dag(DAG_ID).Priority
        ) as request:
            yield request
            Start_Time = self.env.now
            yield env.timeout(ready_high_node[1].get('WCET'))
            End_Time = self.env.now
            self.Makespan_List.append(
                (DAG_ID, ready_high_node[1].get('Node_ID'), Arrive_Time, Start_Time, End_Time) )
            self.Makespan_Dict["{0}-{1}".format(DAG_ID, ready_high_node[1].get('Node_ID'))] \
                = [Arrive_Time, Start_Time, End_Time]
        # 删除节点，更新DAG状态
        self.Temp_DAG_Set.delet_DAG_Node(DAG_ID, ready_high_node[0])
        self.Temp_DAG_Set.Status_Dataup()

    def makespan_compute(self):
        temp_endtime_list = []
        for k, v in self.Makespan_Dict.items():
            for x in v:
                temp_endtime_list.append(x[3])
        temp_endtime_list.sort()
        return temp_endtime_list[-1]

    def show_dag_and_makespan(self):
        for x in range(0, len(self.Dag_Set.Dag_Set)):
            posi =200 + 10 * len(self.Dag_Set.Dag_Set) + (x + 1)
            plt.subplot(posi)
            self.Dag_Set.Dag_Set[x].graph_node_position_determine()
            plt.title("{0}\nrta_non_preempt:{1}\nrta_preempt:{2}".format(
                        self.Dag_Set.Dag_Set[x].DAG_ID,
                        self.Dag_Set.Dag_Set[x].Response_Time_analysis("non-preemptive", self.Core_Num),
                        self.Dag_Set.Dag_Set[x].Response_Time_analysis("preemptive", self.Core_Num)),
                      fontsize=5, color="black", weight="light", ha='left', x=0)
        plt.subplot(212)
        core_channel = 0
        for k, v in self.Makespan_Dict.items():
            for x in v:
                plt.barh(y=core_channel * 3, width=x[3] - x[2], height=2, left=x[2], color='grey', edgecolor='black')
                plt.text(x=x[2], y=core_channel * 3 + 1, s=x[2], fontsize=5)
                plt.text(x=x[2] + (x[3] - x[2]) / 2, y=core_channel * 3, s='{0}\n{1}'.format(x[0], x[3]-x[2]), fontsize=5)
                plt.text(x=x[3], y=core_channel * 3 - 1, s=x[3], fontsize=5)
            core_channel += 1
        plt.title("makespan:{0}".format(self.makespan_compute()),
            fontsize=5, color="black", weight="light", ha='left', x=0)
        plt.show()


if __name__ == "__main__":
    env = simpy.Environment()  # 创建一个环境并开始仿真
    # DAG = user_dag()
    DAG_Set = DAG_Set.DAG_Set()
    # ####### 1.手动DAG set ######## #
    DAG_Set.user_defined_dag()
    # ####### 2.随机生成DAG set ##### #
    # DAG_Set.Random_DAG_Set(DAG_count=3, parallelism_list=[3, 4, 5], critical_path_list=[3, 4, 5])
    Dispatcher = Dispatcher_Workspace(env, DAG_Set, Core_Num=5)  # 分配器建立资源，只要有资源就开始运行
    env.process(Dispatcher.Run())
    # env.run(until=10000000)
    env.run()
