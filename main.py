from random import seed, randint
from Classes.Group import Group
from Classes.Lift import Lift
import simpy

totalFloors = 6 + 1
groundLevel = 1


class EV:

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
    # ev = EV()
    # ev.liftSim()