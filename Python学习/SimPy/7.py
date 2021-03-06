import simpy


class GasStation:
    def __init__(self, env):
        self.fuel_dispensers = simpy.Resource(env, capacity=3)
        self.gas_tank        = simpy.Container(env, init=100, capacity=1000)
        self.mon_proc        = env.process(self.monitor_tank(env))

    def monitor_tank(self, env):
        while True:
            if self.gas_tank.level < 20:
                print('Calling tanker at %s' % env.now)
                env.process(tanker(env, self))
            yield env.timeout(1)


def tanker(env, gas_station):
    yield env.timeout(10)  # Need 10 Minutes to arrive
    print('Tanker arriving at %s' % env.now)
    amount = gas_station.gas_tank.capacity - gas_station.gas_tank.level
    # yield env.timeout(amount)
    # yield gas_station.gas_tank.put(amount)
    yield gas_station.gas_tank.put(500)


def car(name, env, gas_station):
    print('Car %s arriving at %s' % (name, env.now))
    with gas_station.fuel_dispensers.request() as req:
        yield req
        print('Car %s starts refueling at %s' % (name, env.now))
        print(gas_station.fuel_dispensers.count)
        print(gas_station.fuel_dispensers.capacity)
        yield gas_station.gas_tank.get(40)
        yield env.timeout(5)
        print('Car %s done refueling at %s' % (name, env.now))


def car_generator(env, gas_station):
    for i in range(10):
        env.process(car(i, env, gas_station))
        yield env.timeout(5)


env = simpy.Environment()
gas_station = GasStation(env)
car_gen = env.process(car_generator(env, gas_station))
env.run(400)
