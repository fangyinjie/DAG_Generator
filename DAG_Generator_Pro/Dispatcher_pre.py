import random
import simpy
import networkx as nx
import DAG_Set
import matplotlib.pyplot as plt
import copy


class Dispatcher_Workspace(object):
    """ 一个处理器（Processor），拥有特定数量的资源（core，内存，缓存等）。
    一个客户首先申请服务。在对应服务时间完成后结束并离开工作站 """

    def __init__(self, Dag_Set, core):
        self.env = simpy.Environment()      # 创建一个环境并开始仿真  # simpy实体
        self.Dag_Set = Dag_Set              # 初始化DAG集合
        self.Process_Dict = Process_Dict    # 环境中的处理器数量以及种类，例如{core_1:4,core_2:5}
        self.core_Set = []
        self.makespan_dict = {}             # CPU占用时间信息
        for x in Process_Dict:
            self.core_Set.append( simpy.PriorityResource(env, capacity=x) )

        self.Dag_Set.Status_Dataup()        # 更新节点状态，所有前驱为0的节点进入就绪态
        self.Temp_DAG_Set = copy.deepcopy(self.Dag_Set)     # DAG_Set缓存


    def run(self):
        while self.Temp_DAG_Set.get_node_num() > 0:
            with self.core_Set.request() as request:
                yield request
                # step1.有core资源的情况下，搜索当前的Dag_Set中处于就绪态的节点list。
                # 获取优先级最高的DAG以及此DAG中进入就绪状态的node list
                DAG_ID, ready_high_node = self.Temp_DAG_Set.get_priorituy_ready_node()
                if not ready_high_node:
                    yield env.timeout(1)
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
                    self.makespan_dict[core_ID].append(
                        (DAG_ID, ready_high_node[1].get('Node_ID'), start_time, end_time))
        self.show_dag_and_makespan()

        # 更显DAG的状态，将无前驱的节点进入就绪态
        # 挂起CPU资源，只要有资源就看看是否有就绪的节点，然让就绪的节点上处理器
        #

if __name__ == "__main__":
    env = simpy.Environment()  # 创建一个环境并开始仿真
    # DAG = user_dag()
    DAG_Set = DAG_Set.DAG_Set()
    # ####### 1.手动DAG set ######## #
    # DAG_Set.user_defined_dag()
    # ####### 2.随机生成DAG set ##### #
    DAG_Set.Random_DAG_Set(DAG_count=3, parallelism_list=[3, 4, 5], critical_path_list=[3, 4, 5])
    env.process(setup(env, DAG_Set, core_num=2))  # 开始执行!
    env.run(until=10000000)


    store = simpy.FilterStore(env)
    for x in core_list:
        store.put(x)
    env.process(test(env, store, 10, 'task1'))
    env.process(test(env, store, 20, 'task2'))
    env.process(test(env, store, 30, 'task3'))
    env.process(test(env, store, 40, 'task4'))
    env.run(200)
    print(log)


core_list = ["core_1", "core_2", ]
def putter(store):
    for i in range(4):
        log.append('put %s' % i)
        yield store.put(i)

def log_filter(item):
    log.append('check %s' % item)
    return item >= 3

def getter(store):
    log.append('get %s' % (yield store.get(log_filter)))

def test(env, store, time_run, Task_ID):
    while True:
        x = yield store.get()
        print("{0} Start at {1} Core_ID Is {2}".format(Task_ID, env.now, x))
        yield env.timeout(time_run)
        store.put(x)
        print("{0} End at {1}".format(Task_ID, env.now, x))


