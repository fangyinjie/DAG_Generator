import simpy


class Dispatcher:
    def __init__(self, environment, DAG_Set, Core_num):
        self.Core_num = simpy.Resource(env, capacity=Core_num)
        self.Dag_Set = DAG_Set
        self.dispatcher = env.process(self.Core_monitor(environment))
        # self.fuel_dispensers = simpy.Resource(env, capacity=2)
        # self.gas_tank        = simpy.Container(env, init=100, capacity=1000)

    def Core_monitor(self, environment):
        c = 0
        for x in self.DAG_Set:
            c += x.number_of_nodes()
        while c > 0:
            with self.Core_num.request() as req:
                yield req

            if self.gas_tank.level < 200:

                print('Calling tanker at %s' % environment.now)
                env.process(tanker(environment, self))
            yield env.timeout(1)


def tanker(env, gas_station):
    yield env.timeout(10)  # Need 10 Minutes to arrive
    print('Tanker arriving at %s' % env.now)
    amount = gas_station.gas_tank.capacity - gas_station.gas_tank.level
    # yield env.timeout(amount)
    yield gas_station.gas_tank.put(amount)


def car(name, env, gas_station):
    print('Car %s arriving at %s' % (name, env.now))
    with gas_station.fuel_dispensers.request() as req:
        yield req
        print('Car %s starts refueling at %s' % (name, env.now))
        yield gas_station.gas_tank.get(40)
        yield env.timeout(5)
        print('Car %s done refueling at %s' % (name, env.now))


def car_generator(env, gas_station):
    for i in range(10):
        env.process(car(i, env, gas_station))
        yield env.timeout(5)


def print_status(res):
    print('res.count=', res.count)
    print('res.capacity=', res.capacity)
    print('res.users=', res.users)
    print('res.queue=', res.queue)


env = simpy.Environment()
gas_station = Dispatcher(env)
car_gen = env.process(car_generator(env, gas_station))
env.run(400)
