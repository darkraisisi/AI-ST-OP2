from mesa import Agent, Model
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa.batchrunner import BatchRunner

from Classes.Person import Person, Voter, HonestVoter, StrategicVoter, Candidate

def getCandidates(model):
    """
    Return a dictionary where:
    key: id of Candidate object
    value  : amoutVotes of Candidate object
    """
    md_rp = {}
    for agent in model.schedule.agents:
        if agent.isCandidate:
            md_rp.update({f"cand{agent.unique_id}": agent.getVotes})
    return md_rp

def getPoll(model):
    """
    Return list of all the results of the polls 
    """
    return model.poll_lst

def getPositionCandidate(model):
    """
    Get the position of the candidates in the model
    """
    return [i.position for i in model.candidates]

def getStratPerPollCounter(model):
    """
    Return the percentage of voters use a strategy per poll.
    """
    return (model.strat_counter / model.maxpolls) / model.num_agents * 100


class VoterModel(Model):
    def __init__(self, n_voters, n_candidates, voter_type, maxpolls, loyalty, strat_chance, width, height):
        self.voter_type = voter_type  
        self.num_agents = n_voters
        self.space = ContinuousSpace(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True # model will constantly keep running
        self.voters = []
        self.maxpolls = maxpolls # maximum polls 
        self.currentPollCounter = 0 # count the polls 
        self.currentPoll = None # keep track of the polls
        self.loyalty = loyalty / 100 # loyalty tells us (in percentage) how faithful a voter will be to a certain
        self.strat_chance = strat_chance # Chance that a voter will use a strategy.
        self.poll_lst = [] #  list that contains all the results of the currentPoll

        self.strat_counter = 0

        # Setup for the model
        self.candidates = [] # list to store Candidate object 
        # Generate the candidates: create n_candidates Candidates objects and store in candidates.
        for i in range(n_candidates): 
            c = Candidate(i,self,[width,height])
            self.candidates.append(c)
            self.space.place_agent(c,(c.position[0],c.position[1])) # place Candidates in the space at the given position 
            self.schedule.add(c)
        #Generate Strategic or Honest Voter objects, store voters in list voters and add Voter objects in the space at the given position
        if voter_type == 'Strategic':
            for i in range(n_voters): # Generate the strategic voters
                a = StrategicVoter(n_candidates + i, self,[width,height])
                self.voters.append(a)
                self.schedule.add(a)
                self.space.place_agent(a,(a.position[0],a.position[1]))
        else:
            for i in range(n_voters): # Generate the Honest voters
                a = HonestVoter(n_candidates + i, self,[width,height])
                self.voters.append(a)
                self.schedule.add(a)
                self.space.place_agent(a,(a.position[0],a.position[1]))


        # Collecting the Candidate objects from our model
        self.datacollector  = DataCollector(
            model_reporters = getCandidates(self)
        )
        
    def poll(self):
        """
        Return a dictionary where:
            key: Candidate objects
            value: amount of votes of a Candidate
        
        When determining the results for our first poll, we had decided that a voter  will always vote honestly in the first poll.

        """
        resultPoll  = {}
        if self.currentPollCounter == 0 or self.voter_type == 'Honest':# eerste poll
            for cand in self.candidates:
                    resultPoll.update({cand: 0})
            
            for i in self.voters:
                voter = HonestVoter(i, self, [], i.position) # create Honestvoters
                distCand = voter.distanceCandidates(self.candidates)
                chosenCandidate = voter.choseCandidate(distCand)
                votes = resultPoll.get(chosenCandidate)
                votes += 1
                resultPoll.update({chosenCandidate: votes})
                
            return resultPoll    

        else: # niet de eerste poll
            for cand in self.candidates:
                    resultPoll.update({cand: 0})

            for voter in self.voters:
                distCand = voter.distanceCandidates(self.candidates)
                chosenCandidate = voter.choseCandidate(distCand,self.currentPoll)
                votes = resultPoll.get(chosenCandidate)
                votes += 1
                resultPoll.update({chosenCandidate: votes})

            return resultPoll    

    
    def step(self):
        # for each tick in our model  we want to set amountVotes of each candidate to 0
        for cand in self.candidates:
            cand.cleanVotes()
        
        self.currentPoll = self.poll()
        self.poll_lst.append(self.currentPoll)
        self.schedule.step()
        self.currentPollCounter += 1
        self.datacollector.collect(self)

        if self.currentPollCounter == self.maxpolls or self.voter_type == 'Honest':
            # Finish the run when max polls is reached, or you're using honest voters(nothing will changes with more polls).
            self.running = False
