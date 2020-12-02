from random import uniform
from abc import ABC, abstractmethod
import numpy as np

class Person:
    """
        Main class that houses most of a persons logic, like political views 
    """
    def __init__(self, position=None):
        if position:
            # values between -1 & 1, 0 is exactly in the middle of the spectrum.
            self.position = position 
        else:
            self.position = self.generatePosition()

    
    def generatePosition(self) -> [float, float]:
        return np.array([uniform(-1, 1), uniform(-1, 1)])


class Candidate(Person):

    def __init__(self):
        super().__init__()
        self.amountVotes = 0


    def addVotes(self, n:int) -> int:
        self.amountVotes += n
        return self.amountVotes

    

class Voter(Person):

    def __init__(self):
        super().__init__()
    

    def castVote(self):
        pass


class HonestVoter(Voter):
    def __init__(self):
        super().__init__()
    
    @abstractmethod
    def castVote(self,candidates:list):
        finalCandidate = None
        runnerUp = 100

        for i, cand in enumerate(candidates,0):
            distance = np.linalg.norm(self.position - cand.position)

            if distance < runnerUp:
                finalCandidate = cand
                runnerUp = distance

        finalCandidate.addVotes(1)




class StrategicVoter(Voter):
    def __init__(self):
        super().__init__()
    
    @abstractmethod
    def castVote(self):
        pass