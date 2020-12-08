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
<<<<<<< HEAD
    def __init__(self, n_voters, n_candidates, width, height,maxpolls = 6):
=======
    def __init__(self, n_voters, n_candidates, voter_type, width, height):
        self.voter_type = voter_type
>>>>>>> 040f5c1fe5f63b59d095745cdfa6fc59d93bfac9
        self.num_agents = n_voters
        self.space = ContinuousSpace(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True # model blijft runnen
        self.voters = []
<<<<<<< HEAD
        self.maxpolls = maxpolls
        self.currentpoll = 0

=======
        self.datacollector = DataCollector(model_reporters={"agent_count":
        lambda m: m.schedule.get_agent_count()},
        agent_reporters={"name": lambda a: a.name}) 
>>>>>>> 040f5c1fe5f63b59d095745cdfa6fc59d93bfac9

        # Test of plurality voting
        self.candidates = []
        for i in range(n_candidates): # Get some candidates
            c = Candidate(i,self,[width,height])
            self.candidates.append(c)
            self.space.place_agent(c,(c.position[0],c.position[1]))
            self.schedule.add(c)
        if voter_type == 'Strategic':
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
        
        # TODO datacollector aanpassen voor het tekenen van de grafiekk in de simulaatie 
        self.datacollector  = DataCollector(
            #model_reporters  = {"resultPoll": self.poll.values},
            agent_reporters   = {"Votes":  Voter.castVote})
        # for i  in self.candidates:
        #     self.datacollector.model_reporters.update({"Cand {}".format(i.unique_id): i.amountVotes})
        #     print(self.datacollector.get_model_vars_dataframe)

    def getAllVotes(self):
        return [i.amountVotes for i in self.candidates]
        
    def poll(self):
        """
        gebruikt de resultaten van de huidige  poll in de volgende poll.
        :param n: huidie poll  TODO aanpasssen
        """
        resultPoll  = {}
        if self.currentpoll ==1:# eerste poll
            for i in self.voters:
                voter = HonestVoter(i, self, i.position) # create aantal Honestvoters
                distCand= voter.distanceCandidates(self.candidates)
                voter.castVote(distCand)
            for cand in self.candidates:
                resultPoll[cand] = cand.amountVotes 
            self.currentpoll +=1
            return resultPoll    
        else: # niet de eerste poll
            dist= [voter.distanceCandidates(self.candidates)  for  voter  in self.voters]
            map(Voter.castVote(self.candidates), self.voters)
            for cand in self.candidates:
                resultPoll[cand] = cand.amountVotes
            self.currentpoll+=1
            return resultPoll
        
    
    
    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

        

        # for vot in voters: # Make all the voters vote
        #     # print(vot.position)
        #     vot.castVote(candidates)