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

        if position:
            # values between -1 & 1, 0 is exactly in the middle of the spectrum.
            self.position = position 
        else:
            self.position = self.generatePosition(limit)

    
    def generatePosition(self, limit) -> [float, float]:
        widthL, widthR, heightT, heightB = limit[0]/2*-1, limit[0]/2, limit[1]/2*-1, limit[1]/2
        return np.array([uniform(widthL, widthR), uniform(heightB, heightT)])


    def step(self):
        pass


class Candidate(Person):

    def __init__(self, unique_id, model, limit, position=None):
        super().__init__(unique_id, model, limit, position=None)
        self.amountVotes = 0
        self.isCandidate = True
        self.color = f"rgba({abs(self.position[0]*255)},{self.position[1]*255},{((self.position[0]) + self.position[1]) * 225 },1)"


    def addVotes(self, n:int) -> int:
        self.amountVotes += n
        return self.amountVotes
    

    def cleanVotes(self):
        self.amountVotes = 0

    

class Voter(Person):

    def __init__(self, unique_id, model, limit, position=None):
        super().__init__(unique_id, model, limit, position=None)
    
    def distanceCandidates(self): # calculating the distance between the voter and the candidate
        pass
    def castVote(self):
        pass


class HonestVoter(Voter):
    # a honest voter is a person who does not apply any startegy when voting
    def __init__(self, unique_id, model, limit, position=None):
        super().__init__(unique_id, model, limit, position=None)
    # Methods that define the behavior of a honest voter in a Plurality voting system.
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

        for cand, distance in distCand.items():
            if distance < runnerUp:
                finalCandidate = cand
                runnerUp = distance
                
        self.color = finalCandidate.color
        finalCandidate.addVotes(1)
    
    @abstractmethod
    def step(self):
        dist = self.distanceCandidates(self.model.candidates)
        self.castVote(dist)




class StrategicVoter(Voter):
    # This class represent a strategic voter in a Plurality aand a approval voting systems. Based on the voting systems, a strategic voter will implement certain methods(strategy)in order to cast its vote. 
    def __init__(self, unique_id, model, limit, position=None):
        super().__init__(unique_id, model, limit, position=None)
    
    #The behavior of a stratgic voter in a Plurality voting system.
    @abstractmethod
    def distanceCandidates(self, candidates:list):
        'Calculating the distance between voters and candidate'
        distance =  {}

        for _, cand in enumerate(candidates,0):
            distance[cand] = np.linalg.norm(self.position - cand.position)
        return distance

    @abstractmethod
    def castVote(self, distCand:dict, resultPoll:dict): #TODO define function in Model.py to get the result of a poll
        finalCandidate = None # Candidate that the voter is going to vote for.
        runnerUp =  0 # kans van de finalCandidate 
        #making a first choice based on the candidate wiith the highest chance of winning
        for i in resultPoll.keys:
            if resultPoll.get(i) > runnerUp:
                finalCandidate = i
                runnerUp = resultPoll.get(i)

        #now that we have the Candidate with highest chance of winning, we want to also consider the distance between voter and candidates.
        results =  sorted(resultPoll.values())
        for i in distCand.keys:
            if distCand.get(i) < distCand.get(finalCandidate):
                if results.index(resultPoll.get(i))!= -1: # if the candidates does not have the least chance of winnig the election.
                    #We vote for that candidate
                    finalCandidate = i
                    runnerUp = resultPoll.get(i)

        self.color = finalCandidate.color
        finalCandidate.addVotes(1) # cast vote 



    @abstractmethod
    def step(self):
        dist = self.distanceCandidates(self.model.candidates)
        poll = None
        self.castVote(dist, poll)