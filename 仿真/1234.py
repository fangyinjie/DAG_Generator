import random
import simpy
import networkx as nx

# 可接受输入参数
RANDOM_SEED = 0     # 不设置
NUM_MACHINES = 2    # 可以同时处理的机器数（类似工作工位数）
TIME_CONSUMING = 5  # 单任务耗时 (可以设计成随机数)
TIME_INTERVAL = 5   # 来车的间隔时间约5分钟   (可以设计成随机数)
CLIENT_NUMBER = 2   # 初始时已经占用机器数


class Dispatcher(object):
    """ 一个处理器（Processor），拥有特定数量的资源（core，内存，缓存等）。
    一个客户首先申请服务。在对应服务时间完成后结束并离开工作站"""
    def __init__(self, env, Dag_Set, core_num):
        self.env = env                                          # simpy实体
        self.DAG_Set = Dag_Set
        self.core_Set = simpy.Resource(env, core_num)           # 类给env配资源

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

def setup(env, Dag_Set, core_num, t_inter, clientNumber):
    """
    创建一个调度器，多个DAG，多个core，然后持续有DAG到达.
    有的有固定的周期
    有的是随机到达（可以自定义）."""
    # workstation = WorkStation(env, num_machines, washtime)  # 创建工作站
    Dispatcher = Dispatcher(env, Dag_Set, core_num)  # 创建工作站
    for i in range(clientNumber):
        env.process(Client(env, 'Client_%d' % i, workstation))  # 创建clientNumber个初始客户
    while True:
        yield env.timeout(random.randint(t_inter - 2, t_inter + 3))  # 在仿真过程中持续创建客户 3-8分钟
        i += 1
        env.process(Client(env, 'Client_%d' % i, workstation))

if __name__ == "__main__":
    print('开始仿真')             # 初始化并开始仿真任务
    random.seed()               # 初始化seed，指定数值的时候方正结果可以复现
    Dag_Set = []
    core_num = []
    env = simpy.Environment()   # 创建一个环境并开始仿真
    # Dispatcher = Dispatcher(env, Dag_Set, core_num)  # 创建工作站
    env.process(setup(env, NUM_MACHINES, TIME_CONSUMING, TIME_INTERVAL, CLIENT_NUMBER))     # 开始执行!
    env.run(until=SIM_TIME)