from mesa import Agent, Model
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation


from Classes.person import Person, Voter, HonestVoter, StrategicVoter, Candidate

class VoterModel(Model):
    def __init__(self, n_voters, n_candidates, width, height):
        self.num_agents = n_voters
        self.grid = ContinuousSpace(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True
        self.voters = []

        # Test of plurality voting
        self.candidates = []
        for i in range(3): # Get some candidates
            self.candidates.append(Candidate(i,self))
        for i in range(10000): # Get some voters
            a = HonestVoter(i, self)
            self.voters.append(a)
            self.schedule.add(a)
            self.grid.place_agent(a,(a.position[0],a.position[1]))
    
        
    def poll(self, n):
        """
        gebruikt de resultaten van de huidige  poll in de volgende poll.
        :param n: huidie poll 3 TODO aanpasssen
        """
        resultPoll  = {}
        if n ==1:# eerste poll
            for i in self.voters:
                voter = HonestVoter(i, self, i.position) # create aantal Honestvoters
                distCand= voter.distanceCandidates(self.candidates)
                voter.castVote(distCand)
            for cand in self.candidates:
                resultPoll[cand] = cand.amountVotes 
            return resultPoll    
        else: # niet de eerste poll
            dist= self.voters.distanceCandidates(candidates)
            self.voters.castVote(dist, candidates.amountVotes)
            for cand in self.candidates:
                resultPoll[cand] = cand.amountVotes
            return resultPoll

        
    def step(self):
        self.schedule.step()

        

        # for vot in voters: # Make all the voters vote
        #     # print(vot.position)
        #     vot.castVote(candidates)