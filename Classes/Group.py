from Classes.Person import Person

class Group:
    people = []
    def __init__(self,groupSize,startFloor,amntFlrs):
        for i in range(groupSize):
            person = Person(startFloor,amntFlrs)
            self.people.append(person)