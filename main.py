from random import seed, randint
from Classes.Group import Group
from Classes.Lift import Lift
import simpy

totalFloors = 6 + 1
groundLevel = 1


class EV:

    def __init__(self):
        self.totalTime = 0
        self.lift = Lift('Lift1',groundLevel,totalFloors)
        self.floors = self.populateFloors()
        self.leeg()


    def populateFloors(self):
        floors = {}
        for floorNr in range(groundLevel, totalFloors):
            floors.update({floorNr :Group(10, floorNr, totalFloors)})
        return floors


    def addTime(self,time):
        self.totalTime += time


    def open(self):
        n = len(self.lift.riders)
        if n == 0:
            self.leeg()
        elif n < self.lift.max:
            self.gevuld()
        elif n == self.lift.max:
            self.vol()


    def dicht(self):
        self.moving()


    def moving(self):
        hasMoves, time = self.lift.move()
        if not hasMoves:
            return

        self.addTime(time)
        self.stilstaan()


    def stilstaan(self):
        self.open()

    def vol(self):
        pplLeaving, time = self.lift.empty()
        if len(pplLeaving) == 0:
            self.dicht()
        else:
            self.addTime(time)
            self.floors[self.lift.curr_floor].putArrivals(pplLeaving)
            self.gevuld()
        


    def gevuld(self):
        pplLeaving, time = self.lift.empty()
        if len(pplLeaving) > 0:
            time = self.lift.fillLift(self.floors[self.lift.curr_floor])
            self.addTime(time)
            if self.lift.max == len(self.lift.riders):
                self.vol()
            else:
                self.dicht()
        else:
            time = self.lift.fillLift(self.floors[self.lift.curr_floor])
            self.addTime(time)
            if self.lift.max == len(self.lift.riders):
                self.vol()
            else:
                self.dicht()


    def leeg(self):
        time = self.lift.fillLift(self.floors[self.lift.curr_floor])
        self.addTime(time)
        if len(self.lift.riders) == 0:
            self.dicht()
        else:
            self.gevuld()


if __name__ == "__main__":
    ev = EV()

    # check if done
    for i in ev.floors:
        for person in ev.floors[i].waiting:
            person.print()
        print('')