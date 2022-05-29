import simpy
#
#
# def getter(wait):
#     _, item = yield pstore.get()
#     yield env.timeout(wait)
#     log.append(item)
#     # env.process((pstore.put(simpy.PriorityItem(item, item))))
#     pstore.put(simpy.PriorityItem(item, item))
#
#
# env = simpy.Environment()
# pstore = simpy.PriorityStore(env, 3)
# log = []
# items = [x for x in range(3)]
# # Unorderable items are inserted with same priority.
# # 前者是优先级
# env.process((pstore.put(simpy.PriorityItem(3-item, item)) for item in items))
# pstore.put(simpy.PriorityItem(3, 0))
# pstore.put(simpy.PriorityItem(2, 1))
# pstore.put(simpy.PriorityItem(1, 2))
#
# env.process(getter(1))
# env.process(getter(2))
# env.process(getter(3))
# env.process(getter(4))
# env.process(getter(5))
# env.run()
# print(log)




"""
def child(env, event):
    yield env.timeout(10)
    while True:
        value = yield event
        print("{0}, {1}".format(value, env.now))
        yield env.timeout(10)
        # env.exit(value)


def parent(env):
    event = env.event()
    event.callbacks.append(callback)
    event.callbacks.append(callback_1)
    # event.succeed()

    env.process(child(env, event))
    yield env.timeout(5)
    event.succeed('ohai{0}'.format(1))


def callback(event):    # 事件解锁之前运行
    print(event.callbacks)
    print("hello")
    # assert event.callbacks is None


def callback_1(event):    # 事件解锁之前运行
    print(event.callbacks)
    print("hello_1")
    # assert event.callbacks is None
"""
# env = simpy.Environment()
# event = env.event()
# event.callbacks.append(callback)
# event.succeed()
# env.run(until=event)

# env = simpy.Environment()
# env.process(parent(env))
# env.run()


# def child(env, event):
#     try:
#         yield event
#         print('Should not get here.')
#     except ValueError as err:
#         print("{0}, {1}".format(err.args, env.now))
#
#
# def parent(env):
#     event = env.event()
#     env.process(child(env, event))
#     yield env.timeout(5)
#     event.fail(ValueError('ohai'))
#
# env = simpy.Environment()
# env.process(parent(env))
# env.run()


# def test_unavailable_value(env):
#     """If an event has not yet been triggered, its value is not availabe and
#     trying to access it will result in a AttributeError."""
#     event = env.event()
#
#     try:
#         event.value
#         assert False, 'Expected an exception'
#     except AttributeError as e:
#         assert e.args[0].endswith('is not yet available')

# def test_triggered(env):
#     def pem(env, event):
#         value = yield event
#         env.exit(value)
#
#     event = env.event()
#     event.succeed('i was already done')
#
#     result = env.run(env.process(pem(env, event)))
#
#     assert result == 'i was already done'


def process(id, env, res, delay, prio, preempt, log):
    yield env.timeout(delay)
    with res.request(priority=prio, preempt=preempt) as req:
        try:
            yield req
            yield env.timeout(5)
            log.append((env.now, id))
        except simpy.Interrupt as ir:
            log.append((env.now, id, 'interrupted'))
            # log.append((env.now, id, (ir.cause.by, ir.cause.usage_since)))


env = simpy.Environment()
log =[]
res1 = simpy.PreemptiveResource(env, 2)
res2 = simpy.PreemptiveResource(env, 2)
res = [res1, res2]
env.process(process(0, env, res, 0, 1, False, log))
env.process(process(1, env, res, 0, 1, False, log))
env.process(process(2, env, res, 1, 0, False, log))
env.process(process(3, env, res, 1, 0, False, log))
env.process(process(4, env, res, 2, 2, False, log))

env.run()
for x in log:
    print(x)
# assert log == [(1, 1, (p3, 0)), (5, 0), (6, 3), (10, 2), (11, 4)]

