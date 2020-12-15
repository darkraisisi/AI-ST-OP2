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
        self.isCandidate = False # distinguish between a voter and a candidate
        self.color = None

        if type(position).__module__ == np.__name__:
            # values between 0 & 2, 1 is exactly in the middle of the spectrum.
            self.position = position 
        else:
            self.position = self.generatePosition(limit)

    
    def generatePosition(self, limit) -> [float, float]:
        """
        Generate random position(x,y) between 0 and 2 
        """
        widthL, widthR, heightT, heightB = 0, limit[0], 0, limit[1]
        return np.array([uniform(widthL, widthR), uniform(heightB, heightT)])


    def step(self):
        pass


class Candidate(Person):

    def __init__(self, unique_id, model, limit, position=None):
        super().__init__(unique_id, model, limit, position)
        self.amountVotes = 0
        self.isCandidate = True
        self.color = f"rgba({abs(127.5*self.position[0])},{127.5*self.position[1]},{(127.5*((self.position[0]) + self.position[1])/2)},1)" # generate based on position 


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
        """
        Vote  for the candidate with the shortest distance
         params:
         distCand: distCand: dictionary that contains the distance between the voters and ccandidates
        """
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
    def choseCandidate(self, distCand:dict, resultPoll:dict): 
        """
        params:
        distCand: dictionary that contains the distance between the voters and ccandidates
        resultPoll: the amount of Votes of each candidate of the previous poll
        """
        distCand = sorted(distCand.items(), key=lambda x: x[1]) # sort Candidates
        finalCandidate = distCand[0] # the canndidate who the voter is goin to vote for. Initial value will be the candidate wih the shortest distance
        runnerUp = distCand[1] 
        
        #Check whether finalCandidate has a better chance of winningg than runnerUp
        # TODO :  This startegy will only be applied too two candidates. What happens to the rest?
        if resultPoll.get(finalCandidate[0]) < resultPoll.get(runnerUp[0]):
            diff = resultPoll.get(runnerUp[0]) - resultPoll.get(finalCandidate[0])
            #Calculate how better of chance you have if you choose runner up
            if diff / resultPoll.get(runnerUp[0]) > self.model.loyalty: 
                #We vote for that candidate
                finalCandidate = runnerUp

        self.color = finalCandidate[0].color
        return finalCandidate[0]



    @abstractmethod
    def step(self):
        dist = self.distanceCandidates(self.model.candidates)
        self.choseCandidate(dist, self.model.currentPoll).addVotes(1)
