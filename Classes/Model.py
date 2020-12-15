from mesa import Agent, Model
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa.batchrunner import BatchRunner

from Classes.Person import Person, Voter, HonestVoter, StrategicVoter, Candidate

def getCandidates(model):
    md_rp = {}
    for agent in model.schedule.agents:
        if agent.isCandidate:
            md_rp.update({f"cand{agent.unique_id}": agent.getVotes})
    return md_rp

def getPoll(model):
    return model.poll_lst

def getPositionCandidate(model):
    """
    Get the position of the candidates in the model
    """

    return [i.position for i in model.candidates]

def getStratPerPollCounter(model):
    return (model.strat_counter / model.maxpolls) / model.num_agents * 100


class VoterModel(Model):
    def __init__(self, n_voters, n_candidates, voter_type, maxpolls, loyalty, strat_chance, width, height):
        self.voter_type = voter_type
        self.num_agents = n_voters
        self.space = ContinuousSpace(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True # model blijft runnen
        self.voters = []
        self.maxpolls = maxpolls
        self.currentPollCounter = 0
        self.currentPoll = None
        self.loyalty = loyalty / 100
        self.strat_chance = strat_chance
        self.poll_lst = []

        self.strat_counter = 0

        # Setup for the model
        self.candidates = []
        for i in range(n_candidates): # Generate the candidates
            c = Candidate(i,self,[width,height])
            self.candidates.append(c)
            self.space.place_agent(c,(c.position[0],c.position[1]))
            self.schedule.add(c)
        if voter_type == 'Strategic':
            for i in range(n_voters): # Generate the strategic voters
                a = StrategicVoter(n_candidates + i, self,[width,height])
                self.voters.append(a)
                self.schedule.add(a)
                self.space.place_agent(a,(a.position[0],a.position[1]))
        else:
            for i in range(n_voters): # Generate the honest voters
                a = HonestVoter(n_candidates + i, self,[width,height])
                self.voters.append(a)
                self.schedule.add(a)
                self.space.place_agent(a,(a.position[0],a.position[1]))

        self.datacollector  = DataCollector(
            model_reporters = getCandidates(self)
        )
        
    def poll(self):
        """
        gebruikt de resultaten van de huidige  poll in de volgende poll.
        :param n: huidie poll  TODO aanpasssen
        """
        resultPoll  = {}
        if self.currentPollCounter == 0 or self.voter_type == 'Honest':# eerste poll
            for cand in self.candidates:
                    resultPoll.update({cand: 0})

            for i in self.voters:
                voter = HonestVoter(i, self, [], i.position) # create aantal Honestvoters
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
