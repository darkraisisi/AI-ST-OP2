from random import seed, randint
from Classes.Group import Group
from Classes.Lift import Lift
import simpy

# We definieren het totaal aantal verdiepingen in de simulatie
totalFloors = 6 + 1
# GroundLevel is de begane grond in onze simulatie, deze stellen we gelijk aan 1
groundLevel = 1

class EV:

    # def __init__(self, env):
    #     self.env = env
    #     self.lift_proc = env.process(self.liftSim(env))

    # Met populate floors zetten we een bepaald aantal mensen op een bepaalde verdieping.
    # deze mensen willen gebruik gaan maken van de lift.
    def populateFloors(self):
        floors = {}
        for floorNr in range(groundLevel, totalFloors):
            # We populeren elke verdieping van de simulatie met een groep van 10 personen.
            floors.update({floorNr :Group(10, floorNr, totalFloors)})
        return floors

    # Hieronder definieren we onze lift simulatie functie.
    def liftSim(self):
        # We willen de duratie van het vervoeren van een X aantal personen berekenen.
        # We stellen eerst de totale tijd gelijk aan 0.
        totalTime = 0
        # We creeëren een instantie van lift.
        lift = Lift('Lift1',groundLevel,totalFloors)
        # We roepen de functie populateFloors aan.
        floors = self.populateFloors()
        hasMoves, time = lift.move()
        # De lift gaat bewegen en we tellen de tijd dat dit kost op bij de totale tijd.
        totalTime += time
        # In de while loop stappen eerst de personen uit die op hun destination zijn.
        # Daarna wordt de lift weer gevuld met mensen die op de huidige verdieping staan en
        # een andere destination hebben
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
