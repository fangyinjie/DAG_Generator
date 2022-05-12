import random
import simpy
import networkx as nx


class Dispatcher_Workspace(object):
    """ 一个处理器（Processor），拥有特定数量的资源（core，内存，缓存等）。
    一个客户首先申请服务。在对应服务时间完成后结束并离开工作站"""
    def __init__(self, env, Dag_Set, core_num):
        self.env = env                                          # simpy实体
        self.DAG_Set = Dag_Set
        self.core_Set = simpy.Resource(env, core_num)           # 类给env配资源


def Core_act(environment, core_ID, Dispatcher):
    # print('%s 到达工作站 at %.2f.' % (name, env.now))
    while True:
        with Dispatcher.core_Set.request() as request:
            yield request
            print('%s 接受服务   at %.2f.' % (core_ID, environment.now))
            run_time = 10
            yield environment.process(node_run(run_time))
            print('%s 离开服务站 at %.2f.' % (core_ID, environment.now))


def setup(environment,  Dag, core_num):
    """ 创建一个工作站，几个初始客户，然后持续有客户到达. 每隔 t_inter - 2, t_inter + 3分钟（可以自定义）. """
    Dispatcher = Dispatcher_Workspace(environment, Dag, core_num)   # 分配器建立资源，只要有资源就开始运行
    for i in range(core_num):
        env.process(Core_act(env, "core_{0}".format(i), Dispatcher))  # 创建clientNumber个初始客户
    # while Dag_Set.get_node_num() > 0:
    while True:
        yield env.timeout(100)  # 在仿真过程中持续创建客户 3-8分钟
    #     i += 1
    #     env.process(Client(env, 'Client_%d' % i, workstation))


def node_run(run_time):
    yield env.timeout(run_time)


def user_dag():
    G = nx.DiGraph()
    nodes = [[0, 'source',  1, 1],
             [1, 'V1',      7, 5],
             [2, 'V2',      3, 6],
             [3, 'V3',      3, 7],
             [4, 'V4',      6, 2],
             [5, 'V5',      9, 3],
             [6, 'V6',      2, 4],
             [7, 'sink',    1, 8]]
    for x in nodes:
        G.add_node(x[0], Node_ID=x[1], rank=0, critic=False, WCET=x[2], priority=x[3])
    edges = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (4, 6), (5, 6), (1, 7), (2, 7), (3, 7), (6, 7)]
    for x in edges:
        G.add_edge(x[0], x[1], weight=1)
    return G


if __name__ == "__main__":
    env = simpy.Environment()       # 创建一个环境并开始仿真
    DAG = user_dag()
    env.process(setup(env, DAG, core_num=3))     # 开始执行!
    env.run(until=1000)
