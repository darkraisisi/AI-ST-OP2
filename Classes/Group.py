from Classes.Person import Person

# Class Group definieer een groep mensen (Person objects) die aan het wachten zijn voor de lift
# of die hebben uit de lift gestapt.
class Group:

    def __init__(self,groupSize,startFloor,amntFlrs):
        self.waiting = [] # mensen die wachten in de lift. 
        self.arrived = [] # mensen die uit de lift zijn gestapt.

        #Creer Person objects en voeg ze toe in "waiting".
        for i in range(groupSize):
            person = Person(startFloor,amntFlrs)
            self.waiting.append(person)

    # Geeft terug een lijst van aantal mensen uit "waiting".
    def getWaiting(self,amount:int) -> Person:
        ret = []
        # Bekijk of alle personen in de lift kunnen.
        if amount > len(self.waiting):
            amount = len(self.waiting)

        #Haal uit de een "amount" mensen in waiting en voeg ze toe in de lijst "ret".
        for i in range(amount):
            ret.append(self.waiting.pop(0))
        return ret

    #Voeg een persoon (Person object) toe in een "arrived"
    def putArrivals(self,person:Person) -> None:
        self.arrived.append(person)