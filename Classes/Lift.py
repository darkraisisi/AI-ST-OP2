from Classes.Person import Person
from Classes.Group import Group

MAX_ELEVATOR_SIZE = 6
# Een lift Classe die aangemaakt kan worden, deze is zo opgezet dat hij zijn eigen wachtwij van vloeren heeft en alle mensen als input krijgt.
# Dit is belangrijk als je een gebouw wilt simuleren met meerdere liften die dezelde mensen probeert op te halen. 
class Lift:

    def __init__(self, name, groundLevel,totalFloors):
        # Zet sommige waardes vast.
        self.max = MAX_ELEVATOR_SIZE # Maximaal aantal mensen in de lift.
        self.riders = [] # De mensen die in de lift staan.
        self.groundLevel = groundLevel # Aangeven of 0/1 de beganegrond is.
        self.curr_floor = groundLevel # De lift start in het begin van de simulatie op de beganegrond.
        self.queue = [] # Een wachtrij van de vloeren waar de lift naartoe moet in volgorde.
        self.totalFloors = totalFloors # Het totale aantal verdiepingen.


    def addPerson(self,person):
        # Een of meerdere personen toevoegen aan de lift.
        self.riders.extend(person)


    def getRiders(self):
        # Het ophalen van de riders uit deze instantie van de class.
        return self.riders


    def makeQueue(self) -> None:
        # Het aanmaken van een wachtrij wordt hier na elke aankomst na dat alle mensen zijn uit/in-gestapt zijn gedaan.
        self.queue = [] # We willen een lege queue hebben voor we verder gaan omdat we hem overnieuw gaan opbouwen.
        lvls = sorted([person.destinationFloor for person in self.riders]) # Haal de verdieping nummers uit alle mensen die in de lift zitten.
        self.queue = lvls 
        before = []
        after = []

        # Split de queue zodat de verdiepingen die je al voorbij bent pas op het einde gedaan worden, dit zorgt voor meer ruimte in de lift.
        for x in self.queue:
            if x > self.curr_floor:
                before.append(x)
            else:
                after.append(x)

        before.extend(after)
        self.queue = before


    def fillLift(self,group:Group) -> int:
        # Vul de lift tot deze vol zit en initieer het maken van de nieuwe queue
        boardTime = 5
        x = self.max - len(self.riders) # Hoe veel mensen passen er nog in de lift.
        people = Group.getWaiting(group,x) # Haal x aantal mensen uit de groep mensen die staat te wachten.
        self.addPerson(people) # Voeg de mensen die in de lift kunnen toe aan de lift.
        self.makeQueue() # Nu alle nieuwe mensen er zijn maak de nieuwe queue.

        # Wat achtergrond informatie.
        print('Allowed to entering',x)
        print(f'people got in {len(people)} ')
        print('queue',self.queue)
        return len(people) * boardTime

    def move(self):
        # Deze functie simuleert het het verplaatsen naar de volgende verdieping in de wachtrij.
        moveTime = 30 # Tijd die het verplaatsen naar een andere verdieping kost.

        if len(self.queue) == 0: # Als de wachtrij leeg is volg een alternatieve wachtrij.
            if self.curr_floor == self.totalFloors-1: # als je helemaal bovenaan bent.
                # self.queue = range(self.groundLevel,self.totalFloors)
                # self.curr_floor = self.queue[0]
                return False, 0

            # Als de queue leeg is 
            self.queue = range(self.curr_floor+1,self.totalFloors)
            diff = abs(self.curr_floor - self.queue[0])*moveTime
            self.curr_floor = self.queue[0]
            return True, diff
        else:
            diff = abs(self.curr_floor - self.queue[0])*moveTime
            self.curr_floor = self.queue[0]
            return True, diff


    def empty(self):
        emptyTime = 4 # Time for one person to leave the lift
        print('current floor',self.curr_floor)
        # Haal de verdieping nummers uit alle mensen die in de lift zitten.
        destinations = [person.destinationFloor for person in self.riders]
        ret = []
        # Als het verdiepings nummer gelijk is aan de huidige verdieping haal de mensen uit de lift.
        for i in destinations:
            if i == self.curr_floor:
                index = destinations.index(i)
                ret.append(self.riders[index])
                self.riders[index] = None
                destinations[index] = None

        self.riders = [i for i in self.riders if i]
        destinations = [i for i in destinations if i]

        time = len(ret)*emptyTime
        return ret, time