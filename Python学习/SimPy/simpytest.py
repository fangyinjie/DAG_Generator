import simpy
from random import randint
# # 定义一个汽车进程
# def car(env):
#     while True:
#         print('Start parking at %d' % env.now)
#         parking_duration = 5
#         yield env.timeout(parking_duration) # 进程延时 5s
#         print('Start driving at %d' % env.now)
#         trip_duration = 2
#         yield env.timeout(trip_duration)   # 延时 2s

# def clock(env, name, tick):
#     while True:
#         print(name, env.now)
#         yield env.timeout(tick)
#

### Timeout events let time pass ###
def speaker(env, start):
    until_start = start - env.now
    yield env.timeout(until_start)
    yield env.timeout(30)

###  Processes are events, too  ###
def speaker(env):
     yield env.timeout(3)
     return 'handout'

def moderator(env):
    for i in range(3):
        val = yield env.process(speaker(env))
        print(val)

### Asynchronous interrupts ###
def speaker2(env):
    try:
        yield env.timeout(randint(25, 35))
    except simpy.Interrupt as interrupt:
        print(interrupt.cause)

def moderator2(env):
    for i in range(3):
        speaker_proc = env.process(speaker(env))
        yield env.timeout(3)
        speaker_proc.interrupt('No time left')

### Condition events ###
def speaker3(env):
    try:
        yield env.timeout(randint(3, 5))
    except simpy.Interrupt as interrupt:
        print(interrupt.cause)

def moderator3(env):
    for i in range(3):
        speaker_proc = env.process(speaker(env))
        results = yield speaker_proc | env.timeout(10)
        if speaker_proc not in results:
            speaker_proc.interrupt('No time left')
# def generator(x):
#     y = yield x + 1
#     return y + 1
# g = generator(1)
# next(g)
# g.send(3)

# # 仿真启动
env = simpy.Environment()   # 实例化环境
# env.process(car(env))   # 添加汽车进程

# env.process(clock(env, 'fast', 0.5))
# env.process(clock(env, 'slow', 1))
env.process(moderator3(env))

# moderator2(env)

# env.run(until=2)
env.run(until=115)   # 设定仿真结束条件, 这里是 15s 后停止

