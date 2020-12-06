from random import uniform
from abc import ABC, abstractmethod
import numpy as np
from mesa import Agent, Model

class Person(Agent):
    """
        Main class that houses most of a persons logic, like political views 
    """
    def __init__(self, unique_id, model, position=None):
        super().__init__(unique_id, model)
        if position:
            # values between -1 & 1, 0 is exactly in the middle of the spectrum.
            self.position = position 
        else:
            self.position = self.generatePosition()

    
    def generatePosition(self) -> [float, float]:
        return np.array([uniform(-10, 10), uniform(-10, 10)])


class Candidate(Person):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.amountVotes = 0


    def addVotes(self, n:int) -> int:
        self.amountVotes += n
        return self.amountVotes

    

class Voter(Person):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
    
    def distanceCandidates(self): # calculating the distance between the voter and the candidate
        pass
    def castVote(self):
        pass
    
    def step(self):
        pass


class HonestVoter(Voter):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    @abstractmethod
    def distanceCandidates(self, candidates:list):
        'Calculating the distance between voters and candidate'
        distance =  {}

        for _, cand in enumerate(candidates,0):
            distance[cand] = np.linalg.norm(self.position - cand.position)
        return distance
    
    @abstractmethod
    def castVote(self,distCand:dict):
        finalCandidate = None
        runnerUp =100

        for cand, distance in distCand.items:
            if distance < runnerUp:
                finalCandidate = cand
                runnerUp = distance

        finalCandidate.addVotes(1)
    
    @abstractmethod
    def step(self,model):
        self.castVote(model.candidates)




class StrategicVoter(Voter):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
    
    
    @abstractmethod
    def distanceCandidates(self, candidates:list):
        'Calculating the distance between voters and candidate'
        distance =  {}

        for _, cand in enumerate(candidates,0):
            distance[cand] = np.linalg.norm(self.position - cand.position)
        return distance

    @abstractmethod
    def castVote(self, distCand:dict, resultPoll:dict): #TODO define function in Model.py to get the result of a poll
        finalCandidate = None
        runnerUp =  0

        for i in resultPoll.keys:
            if resultPoll.get(i) > runnerUp:
                finalCandidate = i
                runnerUp = resultPoll.get(i)

        #now that we have the Candidate with highest chance of winning, we want to also consider the distance between voter and candidates.
        results =  sorted(resultPoll.values())
        for i in distCand.keys:
            if distCand.get(i) < distCand.get(finalCandidate):
                if results.index(resultPoll.get(i))!= -1:
                    finalCandidate = i
                    runnerUp = resultPoll.get(i)
        
        finalCandidate.addVotes(1) # cast vote 



    @abstractmethod
    def step(self):
        self.castVote(model.candidates)