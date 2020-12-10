from mesa import Agent, Model
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector


from Classes.Person import Person, Voter, HonestVoter, StrategicVoter, Candidate

def compute_gini(model):
    candvotes = [Candidate.amountVotes for agent in model.schedule.agents]
    X = sorted(candvotes)
    N = model.num_agents
    B = sum(xi * (N - i) for i, xi in enumerate(X)) / (N * sum(X))
    return 1 + (1 / N) - 2 * B

class VoterModel(Model):
    def __init__(self, n_voters, n_candidates, voter_type, maxpolls, loyalty, width, height):
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

        self.datacollector = DataCollector(model_reporters={"agent_count":
        lambda m: m.schedule.get_agent_count()},
        agent_reporters={"name": lambda a: a.name}) 

        # Test of plurality voting
        self.candidates = []
        for i in range(n_candidates): # Get some candidates
            c = Candidate(i,self,[width,height])
            self.candidates.append(c)
            self.space.place_agent(c,(c.position[0],c.position[1]))
            self.schedule.add(c)
        if voter_type == 'Strategic':
            print(voter_type)
            for i in range(n_voters): # Get some voters
                a = StrategicVoter(n_candidates + i, self,[width,height])
                self.voters.append(a)
                self.schedule.add(a)
                self.space.place_agent(a,(a.position[0],a.position[1]))
        else:
            for i in range(n_voters): # Get some voters
                a = HonestVoter(n_candidates + i, self,[width,height])
                self.voters.append(a)
                self.schedule.add(a)
                self.space.place_agent(a,(a.position[0],a.position[1]))
        
        md_rp = {}
        for i in range(len(self.candidates)):
            md_rp.update({f"cand{i}": self.candidates[i].getVotes})

        md_rp.update({"Total": self.getAllVotes})

        self.datacollector  = DataCollector(
            model_reporters = md_rp
        )

    def getAllVotes(self):
        return [i.amountVotes for i in self.candidates]
        
    def poll(self):
        """
        gebruikt de resultaten van de huidige  poll in de volgende poll.
        :param n: huidie poll  TODO aanpasssen
        """
        resultPoll  = {}
        if self.currentPollCounter == 0 or self.voter_type == 'Honest':# eerste poll
            print('Poll: 1st, or just honest')
            for cand in self.candidates:
                    resultPoll.update({cand: 0})

            for i in self.voters:
                voter = HonestVoter(i, self, [], i.position) # create aantal Honestvoters
                distCand = voter.distanceCandidates(self.candidates)
                chosenCandidate = voter.choseCandidate(distCand)

            return resultPoll    

        else: # niet de eerste poll
            # print('Poll: n\'d',self.currentPollCounter+1)
            # dist = [voter.distanceCandidates(self.candidates)  for  voter  in self.voters]
            # map(Voter.choseCandidate(dist), self.voters)
            # for cand in self.candidates:
            #     resultPoll[cand] = cand.amountVotes

            # return resultPoll
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
        if self.currentPollCounter == self.maxpolls:
            self.running = False
            
        for cand in self.candidates:
            cand.cleanVotes()
        
        self.currentPoll = self.poll()
        print(self.currentPoll)
        self.schedule.step()
        self.currentPollCounter += 1
        self.datacollector.collect(self)
