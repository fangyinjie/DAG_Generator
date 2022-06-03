import simpy

# def getter(wait):
#     yield env.timeout(wait)
#     item = yield pstore.get()
#     log.append(item)
# # Do not specify priority; the items themselves will be compared to
# # determine priority.
# env = simpy.Environment()
# pstore = simpy.PriorityStore(env, 3)
# log = []
# env.process((pstore.put(s) for s in 'bcadefg'))
# env.process(getter(1))
# env.process(getter(2))
# env.process(getter(3))
# env.run()
# assert log == ['a', 'b', 'c']
"""

def getter(wait):
    item1, item2 = yield pstore.get()
    yield env.timeout(wait)
    log.append([wait, item2, env.now])
    pstore.put(simpy.PriorityItem(item1, item2))

env = simpy.Environment()
# pstore = simpy.PriorityStore(env, 3)
pstore = simpy.FilterStore(env, 3)

log = []
# items = [object() for _ in range(3)]
items = [x for x in range(3)]
# Unorderable items are inserted with same priority.
# env.process((pstore.put(simpy.PriorityItem(item, item+1)) for item in items))

pstore.put(simpy.PriorityItem(1, 5))
pstore.put(simpy.PriorityItem(2, 4))
pstore.put(simpy.PriorityItem(3, 3))
pstore.put(simpy.PriorityItem(4, 2))
pstore.put(simpy.PriorityItem(5, 1))

for x in range(12):
    env.process(getter(6))
# env.process(getter(6))
# env.process(getter(6))
# env.process(getter(6))
# env.process(getter(6))
# env.process(getter(6))
env.run()

for x in log:
    print(x)
# Since the priorities were the same for all items, ensure that items are
# retrieved in insertion order.
# assert log == items
"""

# list_1 = [3, 45, 6, 7, 3, 14, 2]

def process_test_1(env):
    x = yield list_1.pop(1)
    print("now time = {0}, data = {1}".format(env.now, x))


def process_test_2(env):
    y = 10
    while True:
        yield env.timeout(100)
        list_1.append(y)
        y += 1


list_1 = []
env = simpy.Environment()
env.process(process_test_1(env))
env.process(process_test_2(env))
# env.run()
env.run(until=100)