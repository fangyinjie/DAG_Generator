import random
import simpy
import networkx as nx

# 可接受输入参数
RANDOM_SEED = 0     # 不设置
NUM_MACHINES = 2    # 可以同时处理的机器数（类似工作工位数）
TIME_CONSUMING = 5  # 单任务耗时 (可以设计成随机数)
TIME_INTERVAL = 5   # 来车的间隔时间约5分钟   (可以设计成随机数)

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


def Client(env, name, cw):
    """ 客户到达动作站接受服务，结束后离开 """
    print('%s 到达工作站 at %.2f.' % (name, env.now))
    with cw.machine.request() as request:
        yield request
        print('%s 接受服务   at %.2f.' % (name, env.now))
        yield env.process(cw.wash(name))
        print('%s 离开服务站 at %.2f.' % (name, env.now))


def setup(env, num_machines, washtime, t_inter, clientNumber):
    """创建一个调度器，多个初始客户，然后持续有客户到达. 每隔t_inter - 2, t_inter + 3分钟（可以自定义）."""
    workstation = WorkStation(env, num_machines, washtime)  # 创建工作站
    for i in range(clientNumber):
        env.process(Client(env, 'Client_%d' % i, workstation))  # 创建clientNumber个初始客户
    while True:
        yield env.timeout(random.randint(t_inter - 2, t_inter + 3))  # 在仿真过程中持续创建客户 3-8分钟
        i += 1
        env.process(Client(env, 'Client_%d' % i, workstation))


SIM_TIME = 1000     # 仿真总时间

# 模块2-场景1（2核1流）-情况2 DAG
Temp_Dag1 = nx.DiGraph()
node_list = [[1, 'Job-0(1)',    3032, 1],
             [2, 'Job-3-1(1)', 89840, 2] ]
for node_x in node_list:
    Temp_Dag1.add_node(node_x[0], Node_ID=node_x[1], rank=0,
                       critic=False, WCET=node_x[2], priority=node_x[3], state='blocked')
edges = [(1, 2)]
for edge in edges:
    Temp_Dag1.add_edge(edge[0], edge[1], weight=1)
# 模块2-场景2（3核2流）-情况2 DAG
Temp_Dag2 = nx.DiGraph()
node_list = [[1, 'Job-0(2)',    6732,  1],
             [2, 'Job-1_1(2)', 108328, 2],
             [3, 'Job-1_2(2)', 108328, 3]]
for node_x in node_list:
    Temp_Dag2.add_node(node_x[0], Node_ID=node_x[1], rank=0,
                       critic=False, WCET=node_x[2], priority=node_x[3], state='blocked')
edges = [(1, 2), (1, 3)]
for edge in edges:
    Temp_Dag2.add_edge(edge[0], edge[1], weight=1)
# 模块2-场景3（5核6流）-情况2 DAG
Temp_Dag3 = nx.DiGraph()
node_list = [[1, 'Job-0(3)',  10000,   1],
             [2, 'Job-1_1(3)', 120000, 2],
             [3, 'Job-1_2(3)', 120000, 3],
             [4, 'Job-1_3(3)', 120000, 4],
             [5, 'Job-1_4(3)', 120000, 5],
             [6, 'Job-1_5(3)', 120000, 6],
             [7, 'Job-1_6(3)', 120000, 7]]
for node_x in node_list:
    Temp_Dag3.add_node(node_x[0], Node_ID=node_x[1], rank=0,
                       critic=False, WCET=node_x[2], priority=node_x[3], state='blocked')
edges = [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7)]
for edge in edges:
    Temp_Dag3.add_edge(edge[0], edge[1], weight=1)

if __name__ == "__main__":
    print('开始仿真')             # 初始化并开始仿真任务
    env = simpy.Environment()   # 创建一个环境并开始仿真
    env.process(setup(env))     # 开始执行!
    env.run(until=SIM_TIME)
