import simpy
import pytest

# def child(env, event):
#     try:
#         x = yield event
#         print(x , env.now)
#         # pytest.fail('Should not get here.')
#     except ValueError as err:
#         print(err.args[0], env.now)
#
#
# def parent(env):
#     event = env.event()
#     event.callbacks.append(callback)    # 事件到达之前运行
#     env.process(child(env, event))
#     yield env.timeout(5)
#     event.succeed('ohai')
#     # event.fail(ValueError('fail hai'))
#
#
# def callback(event):
#     print("123", event.callbacks)
#     # assert event.callbacks is None
#
#
# if __name__ == "__main__":
#     env = simpy.Environment()
#     env.process(parent(env))
#     env.run()
#
#     # event = env.event()
#     # event.succeed()
#     # env.run(until=event)


def interruptee(env):
    try:
        yield env.timeout(10)
        print('Expected an interrupt')
        # pytest.fail('Expected an interrupt')
    except simpy.Interrupt as interrupt:
        print(interrupt.cause)
        # assert interrupt.cause == 'interrupt!'


def interruptor(env):
    child_process = env.process(interruptee(env))
    yield env.timeout(5)
    # child_process.interrupt('interrupt!')


# env = simpy.Environment()
# env.process(interruptor(env))
# env.run()

# def fox(env, coup, log):
#     # while True:
#     try:
#         yield coup
#         log.append('coup completed at %d' % env.now)
#         # env.exit()
#     except simpy.Interrupt:
#         log.append('coup interrupted at %d' % env.now)
#
#
# def master_plan(env, fox, coup):
#     yield env.timeout(1)
#     # Succeed and interrupt concurrently.
#     coup.succeed()
#     fox.interrupt()
#
#
#
# log = []
# env = simpy.Environment()
# coup = env.event()
# fantastic_mr_fox = env.process(fox(env, coup, log))
# env.process(master_plan(env, fantastic_mr_fox, coup))
#
# env.run(5)
# print(log)

def proc_a(env):
    timeouts = [env.timeout(3) for i in range(5)]
    while timeouts:
        try:
            yield timeouts.pop(0)
            print('Expected an interrupt')
            # assert False, 'Expected an interrupt'
        except simpy.Interrupt:
            print('interrupt!')
            # pass

def proc_b(env, proc_a):
    for i in range(2):
        yield env.timeout(1)
        proc_a.interrupt()
    # yield env.exit()

env = simpy.Environment()
proc_a = env.process(proc_a(env))
env.process(proc_b(env, proc_a))

env.run(until=10)