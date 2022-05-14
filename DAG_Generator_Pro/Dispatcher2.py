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
        self.Makespan_dict = {}         # Makespan信息，结束后分析使用
        self.Sys_Event = env.event()    # 系统用事件，每个node运行结束后就会向调度程序发一个事件以重新运行新的node
        # self.Core_Set = simpy.Resource(env, Core_Num)  # 类给env配资源

        self.Dag_Set = Dag_Set
        self.Dag_Set.Status_Dataup()  # 更新节点状态，所有前驱为0的节点进入就绪态
        self.Temp_DAG_Set = copy.deepcopy(self.Dag_Set)

    def Run(self):
        for i in range(self.Core_Num):      # 每个core建立一个进程
            self.env.process( self.Core_Act("core_{0}".format(i)) ) # 创建clientNumber个初始客户
            self.Sys_Event.append()
        while self.Temp_DAG_Set.get_node_num() > 0:
            event_req = yield self.Sys_Event  # 两种事件（1）某节点（2）某处理器无节点可运行
            if event_req == 'Finish':
                pass
            elif event_req == 'Node_Req':
                pass
            else:
                print('event error!')

            # DAG_ID, ready_high_node = self.Temp_DAG_Set.get_priorituy_ready_node()
            # if not ready_high_node:  # 如果当前没有就绪任务
            #     yield env.timeout(1)
            #     continue
            # WCET = ready_high_node[1].get('WCET')
            # env.process(self.node_running(DAG_ID, ready_high_node, WCET))  # 开始执行!

    def Core_Act(self,Core_ID):
        while True: # core将永远持续运行
            # 查看DAG_Set里有没有就绪的node
            DAG_ID, ready_high_node = self.Temp_DAG_Set.get_priorituy_ready_node()
            if not ready_high_node:  # 如果当前没有就绪任务
                # 向调度器发一个event
                # 等待调度其派发event
            else:
                pass

    def Node_Run(self, DAG_ID, Node_ID, WCET ):
        # with self.core_Set.request() as request:
        #     yield request
        Start_Time = self.env.now
        yield env.timeout(WCET)
        End_Time = self.env.now
        print('DAG: %s; Task:%s : Start_Time at %d and End_Time at %d'
              % (DAG_ID, Node_ID, Start_Time, End_Time))
        self.Temp_DAG_Set.delet_DAG_Node(DAG_ID, ready_high_node[0])
        self.Temp_DAG_Set.Status_Dataup()
        # 删除节点

if __name__ == "__main__":
    env = simpy.Environment()  # 创建一个环境并开始仿真
    # DAG = user_dag()
    DAG_Set = DAG_Set.DAG_Set()
    # ####### 1.手动DAG set ######## #
    # DAG_Set.user_defined_dag()
    # ####### 2.随机生成DAG set ##### #
    DAG_Set.Random_DAG_Set(DAG_count=3, parallelism_list=[3, 4, 5], critical_path_list=[3, 4, 5])

    Dispatcher = Dispatcher_Workspace(env, DAG_Set, core_num=3)  # 分配器建立资源，只要有资源就开始运行

    Dispatcher.run()

    env.run(until=10000000)





