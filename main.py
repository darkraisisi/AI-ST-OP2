from random import seed, randint
from Classes.Group import Group
from Classes.Lift import Lift
import simpy

totalFloors = 6 + 1
groundLevel = 1
class EV:

    # def __init__(self, env):
    #     self.env = env
    #     self.lift_proc = env.process(self.liftSim(env))


    def populateFloors(self):
        floors = {}
        for floorNr in range(groundLevel, totalFloors):
            floors.update({floorNr :Group(10, floorNr, totalFloors)})
        return floors


    def liftSim(self):
        totalTime = 0
        lift = Lift('Lift1',groundLevel,totalFloors)
        floors = self.populateFloors()
        hasMoves, time = lift.move()
        totalTime += time
        while hasMoves:
            floors[lift.curr_floor].putArrivals(lift.empty())

            time = lift.fillLift(floors[lift.curr_floor])
            totalTime += time

            hasMoves, time = lift.move()
            totalTime += time

        print(f'Total runtime in seconds: {totalTime}, minutes: {totalTime/60}')


if __name__ == "__main__":
    # env = simpy.Environment()
    # ev = EV(env)
    # env.run()

    
    # for i in floors:
    #     for person in floors[i].waiting:
    #         person.print()
    #     print('')

    # floors = EV.populateFloors(EV)

    # lift = Lift('Lift1',groundLevel,totalFloors)
    # lift.fillLift(floors[lift.curr_floor])
    # hasMoves, _ = lift.move()

    # while hasMoves:
    #     floors[lift.curr_floor].putArrivals(lift.empty())
    #     lift.fillLift(floors[lift.curr_floor])
    #     hasMoves,_ = lift.move()

    ev = EV()
    ev.liftSim()
