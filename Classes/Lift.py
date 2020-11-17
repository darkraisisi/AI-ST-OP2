from Classes.Person import Person
from Classes.Group import Group

MAX_ELEVATOR_SIZE = 6

class Lift:

    def __init__(self, name, groundLevel,totalFloors):
        self.max = MAX_ELEVATOR_SIZE
        self.riders = []
        self.groundLevel = groundLevel
        self.curr_floor = groundLevel
        self.queue = []
        self.totalFloors = totalFloors


    def addPerson(self,person):
        self.riders.extend(person)


    def getRiders(self):
        return self.riders


    def makeQueue(self):
        self.queue = []
        # print(self.riders[0])
        lvls = sorted([person.destinationFloor for person in self.riders])
        self.queue = lvls
        before = []
        after = []

        for x in self.queue:
            if x > self.curr_floor:
                before.append(x)
            else:
                after.append(x)

        before.extend(after)
        self.queue = before


    def fillLift(self,group:Group):
        x = self.max - len(self.riders)
        people = Group.getWaiting(group,x)
        self.addPerson(people)
        self.makeQueue()

        print('Allowed to entering',x)
        print(f'people got in {len(people)} ')
        print('queue',self.queue)
        return len(people) * 5

    def move(self):
        moveTime = 30 # per floor
        if len(self.queue) == 0:
            if self.curr_floor == self.totalFloors-1:
                # self.queue = range(self.groundLevel,self.totalFloors)
                # self.curr_floor = self.queue[0]
                return False, 0

            self.queue = range(self.curr_floor+1,self.totalFloors)
            diff = abs(self.curr_floor - self.queue[0])*moveTime
            self.curr_floor = self.queue[0]
            return True, diff
        else:
            diff = abs(self.curr_floor - self.queue[0])*moveTime
            self.curr_floor = self.queue[0]
            return True, diff


    # def empty(self) -> list(Person):
    def empty(self):
        emptyTime = 4 # Time for one person to leave the lift
        print('current floor',self.curr_floor)
        destinations = [person.destinationFloor for person in self.riders]
        ret = []
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