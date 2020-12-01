from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation

class VoterModel(Model):
    def __init__(self, n_voters, n_candidates, width, height):
        self.num_agents = n_voters
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True