from mesa import Agent, Model
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation

from Classes.Person import Person, Voter, HonestVoter, StrategicVoter, Candidate

class VoterModel(Model):
    def __init__(self, n_voters, n_candidates, width, height):
        self.num_agents = n_voters
        self.space = ContinuousSpace(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True

        # Test of plurality voting
        self.candidates = []
        for i in range(n_candidates): # Get some candidates
            c = Candidate(i,self,[width,height])
            self.candidates.append(c)
            self.space.place_agent(c,(c.position[0],c.position[1]))
            self.schedule.add(c)
        for i in range(n_voters): # Get some voters
            a = HonestVoter(n_candidates + i, self,[width,height])
            self.schedule.add(a)
            self.space.place_agent(a,(a.position[0],a.position[1]))
        
        
    def step(self):
        self.schedule.step()
        

        # for vot in voters: # Make all the voters vote
        #     # print(vot.position)
        #     vot.castVote(candidates)