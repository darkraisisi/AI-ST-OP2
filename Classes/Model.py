from mesa import Agent, Model
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation

from Classes.Person import Person, Voter, HonestVoter, StrategicVoter, Candidate

class VoterModel(Model):
    def __init__(self, n_voters, n_candidates, width, height):
        self.num_agents = n_voters
        self.grid = ContinuousSpace(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True

        # Test of plurality voting
        self.candidates = []
        for i in range(3): # Get some candidates
            self.candidates.append(Candidate(i,self))
        for i in range(10000): # Get some voters
            a = HonestVoter(i, self)
            self.schedule.add(a)
            self.grid.place_agent(a,(a.position[0],a.position[1]))
        
        
    def step(self):
        self.schedule.step()
        

        # for vot in voters: # Make all the voters vote
        #     # print(vot.position)
        #     vot.castVote(candidates)