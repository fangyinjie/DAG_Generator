import simpy
def car(env):
    while True:
        print('start parking at %d'%env.now)
        parking_duration=5
        yield env.timeout(parking_duration)
        print('start driving at %d'%env.now)
        trip_duration=2
        yield env.timeout(trip_duration)

for x in range(3):
    env = simpy.Environment()
    env.process(car(env))
    env.run(until=15)