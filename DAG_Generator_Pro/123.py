import simpy

def test_succeed(env):
    """Test for the Environment.event() helper function."""
    def child(env, event):
        value = yield event
        print("value = {0}； time = {1}", value, env.now)

    def parent(env):
        event = env.event()
        env.process(child(env, event))
        yield env.timeout(5)
        event.succeed('ohai')

    env.process(parent(env))
    env.run()


if __name__ == "__main__":
    env = simpy.Environment()
    test_succeed(env)