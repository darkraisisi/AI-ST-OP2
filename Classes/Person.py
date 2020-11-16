from random import seed, randint, choice

class Person:

    def __init__(self,startFlr,amntFlrs):
        self.startFloor = startFlr
        self.destinationFloor = choice([i for i in range(startFlr,amntFlrs) if i not in [startFlr]])

    def print(self):
        print(f'StartFloor: {self.startFloor}, Destination: {self.destinationFloor}')