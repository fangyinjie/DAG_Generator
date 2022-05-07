"""
服务站示例
场景介绍:
  一个有特定服务提供工作站，客户服务时长不一，工作机器数有限。
  Client接受服务步骤：Client到达工作站，若有空闲的机器就立刻接受服务，如果没有，就等待直到其他机器空闲下来。
  每个接受过服务的Client都有一个完成满意度（或者为进度）实时统计服务客户数和完成满意进度。
"""
import random
import simpy
import networkx as nx
import DAG_Set
import Proc

# 可接受输入参数
RANDOM_SEED = 0     # 不设置
NUM_MACHINES = 2    # 可以同时处理的机器数（类似工作工位数）
TIME_CONSUMING = 5  # 单任务耗时 (可以设计成随机数)
TIME_INTERVAL = 5   # 来车的间隔时间约5分钟   (可以设计成随机数)
SIM_TIME = 1000     # 仿真总时间
CLIENT_NUMBER = 2   # 初始时已经占用机器数


class WorkStation(object):
    """ 一个处理器（Processor），拥有特定数量的资源（core，内存，缓存等）。
    一个客户首先申请服务。在对应服务时间完成后结束并离开工作站"""
    def __init__(self, env, num_machines, washtime):
        self.env = env                                          # simpy实体
        self.machine = simpy.Resource(env, num_machines)        # 类给env配资源
        self.washtime = washtime                                # 浪费的时间
        self.allClient = 0                                      #
        self.accomplishClient = 0                               #

    def wash(self, car):
        """ 服务流程 """
        yield self.env.timeout(random.randint(2, 10))  # 假设服务时间为随机数（2~10）
        self.allClient += 1
        per = random.randint(50, 99)
        print("%s's 任务完成度：%d%%." % (car, per))
        if per > 80:
            self.accomplishClient += 1
        print("工作站服务客户数：%d, 工作站服务达标率：%.2f。"
              % (self.allClient, float(self.accomplishClient) / float(self.allClient)))


class Dispatcher_Workspace(object):
    """ 一个处理器（Processor），拥有特定数量的资源（core，内存，缓存等）。
    一个客户首先申请服务。在对应服务时间完成后结束并离开工作站"""
    def __init__(self, env, Dag_Set, core_num):
        self.env = env                                          # simpy实体
        self.DAG_Set = Dag_Set
        self.core_Set = simpy.Resource(env, core_num)           # 类给env配资源


def Client(env, name, cw):
    """ 客户到达动作站接受服务，结束后离开 """
    print('%s 到达工作站 at %.2f.' % (name, env.now))
    with cw.machine.request() as request:
        yield request
        print('%s 接受服务   at %.2f.' % (name, env.now))
        yield env.process(cw.wash(name))
        print('%s 离开服务站 at %.2f.' % (name, env.now))


def setup(env,  Dag_Set, core_num):
    """创建一个工作站，几个初始客户，然后持续有客户到达. 每隔t_inter - 2, t_inter + 3分钟（可以自定义）."""
    Dispatcher = Dispatcher_Workspace(env, Dag_Set, core_num)
    for i in range(Dag_Set.get_dag_num()):
        env.process(Client(env, 'Client_%d' % i, workstation))  # 创建clientNumber个初始客户
    while Dag_Set.get_node_num() > 0:
        #

    while True:
        yield env.timeout(random.randint(t_inter - 2, t_inter + 3))  # 在仿真过程中持续创建客户 3-8分钟
        i += 1
        env.process(Client(env, 'Client_%d' % i, workstation))


if __name__ == "__main__":
    print('开始仿真')                 # 初始化并开始仿真任务
    random.seed()                   # 初始化seed，指定数值的时候方正结果可以复现
    DagSet = DAG_Set.DAG_Set()
    DagSet.user_defined_dag()
    proc = Processor.Processor([3], 'GD_32')

    env = simpy.Environment()       # 创建一个环境并开始仿真
    env.process(setup(env, DagSet, Processor))     # 开始执行!
    env.run(until=SIM_TIME)
