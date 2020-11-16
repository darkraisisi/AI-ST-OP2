from random import seed, randint
from Classes.Group import Group
import simpy


class Lift:
    def __init__(self,env):
        pass


if __name__ == "__main__":
    # seed(21)
    # env = simpy.Environment()
    # sim = Lift(env)
    # env.run()
    groupManager = Group(10,0,6)
    for person in groupManager.people:
        person.print()