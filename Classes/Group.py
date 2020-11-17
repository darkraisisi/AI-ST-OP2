from Classes.Person import Person

class Group:

    def __init__(self,groupSize,startFloor,amntFlrs):
        self.waiting = []
        self.arrived = []

        for i in range(groupSize):
            person = Person(startFloor,amntFlrs)
            self.waiting.append(person)


    def getWaiting(self,amount:int) -> Person:
        ret = []
        if amount > len(self.waiting):
            amount = len(self.waiting)

        for i in range(amount):
            ret.append(self.waiting.pop(0))
        return ret

    def putArrivals(self,person:Person) -> None:
        self.arrived.append(person)