import time
from simpy.rt import RealtimeEnvironment
import simpy

# core_list = ["core_1", "core_2", "core_3", "core_4", "core_5"]
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

def test(env, store, time_run, Task_ID, pri):
    while True:
        x = yield store.get()
        start_time = env.now
        yield env.timeout(time_run)
        store.put(x)
        end_time = env.now
        print("{0} get Core_ID Is {1} Start at {2}  End at {3}".format(
            Task_ID, x, start_time, end_time))


env = simpy.Environment()  # 创建一个环境并开始仿真
log = []
store = simpy.PriorityStore(env)
for x in core_list:
    store.put(x)
env.process(test(env, store, 10, 'task1'))
env.process(test(env, store, 20, 'task2'))
env.process(test(env, store, 30, 'task3'))
env.process(test(env, store, 40, 'task4'))
env.run(200)
print(log)


# The filter function is repeatedly called for every item in the store
# until a match is found.
# assert log == [
#         'put 0', 'check 0',
#         'put 1', 'check 0', 'check 1',
#         'put 2', 'check 0', 'check 1', 'check 2',
#         'put 3', 'check 0', 'check 1', 'check 2', 'check 3', 'get 3',
# ]
#
