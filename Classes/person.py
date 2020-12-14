from random import uniform
from abc import ABC, abstractmethod
import numpy as np
from mesa import Agent, Model

class Person(Agent):
    """
        Main class that houses most of a persons logic, like political views 
    """
    def __init__(self, unique_id, model, limit, position=None):
        super().__init__(unique_id, model)
        self.isCandidate = False
        self.color = None

        if type(position).__module__ == np.__name__:
            # values between 0 & 2, 1 is exactly in the middle of the spectrum.
            self.position = position 
        else:
            self.position = self.generatePosition(limit)

    
    def generatePosition(self, limit) -> [float, float]:
        widthL, widthR, heightT, heightB = 0, limit[0], 0, limit[1]
        return np.array([uniform(widthL, widthR), uniform(heightB, heightT)])


    def step(self):
        pass


class Candidate(Person):

    def __init__(self, unique_id, model, limit, position=None):
        super().__init__(unique_id, model, limit, position)
        self.amountVotes = 0
        self.isCandidate = True
        self.color = f"rgba({abs(127.5*self.position[0])},{127.5*self.position[1]},{(127.5*((self.position[0]) + self.position[1])/2)},1)"


    def addVotes(self, n:int) -> int:
        self.amountVotes += n
        return self.amountVotes
    

    def cleanVotes(self):
        self.amountVotes = 0

    def getVotes(self):
        return self.amountVotes
    

class Voter(Person):

    def __init__(self, unique_id, model, limit, position=None):
        super().__init__(unique_id, model, limit, position)
    
    def distanceCandidates(self): # calculating the distance between the voter and the candidate
        pass

    def choseCandidate(self) -> Candidate:
        pass


class HonestVoter(Voter):
    # a honest voter is a person who does not apply any startegy when voting
    def __init__(self, unique_id, model, limit, position=None):
        super().__init__(unique_id, model, limit, position)
    # Methods that define the behavior of a honest voter in a Plurality voting system.
    @abstractmethod
    def distanceCandidates(self, candidates:list):
        'Calculating the distance between voters and candidate'
        distance =  {}

        for _, cand in enumerate(candidates,0):
            distance[cand] = np.linalg.norm(self.position - cand.position)
        return distance
    
    @abstractmethod
    def choseCandidate(self,distCand:dict) -> Candidate:
        finalCandidate = None
        smallestDistance = 100

        for cand, distance in distCand.items():
            if distance < smallestDistance:
                finalCandidate = cand
                smallestDistance = distance

        self.color = finalCandidate.color
        return finalCandidate
    
    @abstractmethod
    def step(self):
        dist = self.distanceCandidates(self.model.candidates)
        self.choseCandidate(dist).addVotes(1)




class StrategicVoter(Voter):
    # This class represent a strategic voter in a Plurality aand a approval voting systems. Based on the voting systems, a strategic voter will implement certain methods(strategy)in order to cast its vote. 
    def __init__(self, unique_id, model, limit, position=None):
        super().__init__(unique_id, model, limit, position)
    
    #The behavior of a stratgic voter in a Plurality voting system.
    @abstractmethod
    def distanceCandidates(self, candidates:list):
        'Calculating the distance between voters and candidate'
        distance =  {}

        for _, cand in enumerate(candidates,0):
            distance[cand] = np.linalg.norm(self.position - cand.position)
        return distance

    @abstractmethod
    def choseCandidate(self, distCand:dict, resultPoll:dict): #TODO define function in Model.py to get the result of a poll
        distCand = sorted(distCand.items(), key=lambda x: x[1])
        finalCandidate = distCand[0]
        runnerUp = distCand[1]

        #now that we have the Candidate with highest chance of winning, we want to also consider the distance between voter and candidates.
        if resultPoll.get(finalCandidate[0]) < resultPoll.get(runnerUp[0]):
            diff = resultPoll.get(runnerUp[0]) - resultPoll.get(finalCandidate[0])
            # print('diff',diff)
            if diff / resultPoll.get(runnerUp[0]) > self.model.loyalty: 
                #We vote for that candidate
                finalCandidate = runnerUp

        self.color = finalCandidate[0].color
        return finalCandidate[0]



    @abstractmethod
    def step(self):
        dist = self.distanceCandidates(self.model.candidates)
        self.choseCandidate(dist, self.model.currentPoll).addVotes(1)
