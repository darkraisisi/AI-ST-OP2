from random import seed, randint
from Classes.Group import Group
from Classes.Lift import Lift
import simpy

# We definieren het totaal aantal verdiepingen in de simulatie
totalFloors = 6 + 1
# GroundLevel is de begane grond in onze simulatie, deze stellen we gelijk aan 1
groundLevel = 1

amountPeoplePerFloor = 10

class EV:

    def __init__(self):
        self.totalTime = 0
        self.lift = Lift('Lift1',groundLevel,totalFloors)
        self.floors = self.populateFloors()
        self.leeg()

        for i in self.floors:
            for person in self.floors[i].waiting:
                person.print()
            print('')

    # Met populate floors zetten we een bepaald aantal mensen op een bepaalde verdieping.
    # deze mensen willen gebruik gaan maken van de lift.
    def populateFloors(self):
        floors = {}
        for floorNr in range(groundLevel, totalFloors):
            # We populeren elke verdieping van de simulatie met een groep van 10 personen.
            floors.update({floorNr :Group(amountPeoplePerFloor, floorNr, totalFloors)})
        return floors


    def addTime(self,time):
        # Global function to create a counter.
        self.totalTime += time

    
    def showTime(self):
        # A printing fucntion for the simulatin time.
        print(f'This simulation took: {self.totalTime}s / {int(self.totalTime/60)} minutes')


    def open(self):
        # Open state waar je over kan gaan naar states: leeg/gevuld/vol aan de hand van de lift volheid.
        n = len(self.lift.riders)
        if n == 0:
            self.leeg()
        elif n < self.lift.max:
            self.gevuld()
        elif n == self.lift.max:
            self.vol()


    def dicht(self):
        # een dichte lift kan alleen maar verplaatsen in de context van de simulatie.
        self.moving()


    def moving(self):
        # Bepalen wanneer de lift nog een stap mag zetten of dat de lift klaar is met verplaatsen.
        hasMoves, time = self.lift.move()
        if not hasMoves:
            return

        self.addTime(time)
        self.stilstaan() #Na het verplaatsen staat de lift stil.


    def stilstaan(self):
        # Na het stilstaan kan de lift (in deze contect) alleen zijn deuren openen.
        self.open()

    def vol(self):
        # Een collelift
        pplLeaving, time = self.lift.empty()
        if len(pplLeaving) == 0:# als er geen mensen uitstappen gaan de deuren dicht.
            self.dicht()
        else:
            self.addTime(time)
            # De volle lift zet mensen op de huidige verdieping.
            self.floors[self.lift.curr_floor].putArrivals(pplLeaving)
            # Ga naar de gevuld state.
            self.gevuld()
        


    def gevuld(self):
        # Dit is een gevulde lift die NIET vol zit.
        pplLeaving, time = self.lift.empty()
        if len(pplLeaving) > 0:
            # als er mensen uit de lift zijn gegaan mag je de lift nog eens proberen te vullen,
            # op de verdieping waar je net bent aangekomen.
            time = self.lift.fillLift(self.floors[self.lift.curr_floor])
            self.addTime(time)
            if self.lift.max == len(self.lift.riders):
                self.vol()
                # Als na het vullen de lift vol zit ga naar staat vol.
            else:
                # Zo niet blijf in deze staat en ga dicht.
                self.dicht()
        else:
            time = self.lift.fillLift(self.floors[self.lift.curr_floor])
            self.addTime(time)
            # Als er niemand is vertrokken kan je proberen de lift te vullen en anders verder te gaan.
            if self.lift.max == len(self.lift.riders):
                self.vol()
            else:
                self.dicht()


    def leeg(self):
        # Dit is een lege lift.
        # Probeer de lift te vullen.
        time = self.lift.fillLift(self.floors[self.lift.curr_floor])
        self.addTime(time)
        # Als de lift nog leeg is doe de deuren dicht.
        if len(self.lift.riders) == 0:
            self.dicht()
        else:
            # Als er mensen bij zijn gekomen ga naar gevuld.
            self.gevuld()


if __name__ == "__main__":
    ev = EV()
    ev.showTime()
