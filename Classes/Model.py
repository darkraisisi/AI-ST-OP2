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
    def __init__(self, n_voters, n_candidates, voter_type, maxpolls, width, height):
        self.voter_type = voter_type
        self.num_agents = n_voters
        self.space = ContinuousSpace(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True # model blijft runnen
        self.voters = []
        self.maxpolls = maxpolls
        self.currentPollCounter = 0
        self.currentPoll = None
        self.loyalty = 0.2

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
        
        # TODO datacollector aanpassen voor het tekenen van de grafiekk in de simulaatie 
        self.datacollector  = DataCollector(
            #model_reporters  = {"resultPoll": self.poll.values},
            agent_reporters   = {"Votes":  Voter.choseCandidate})
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
        if self.currentPollCounter == 0:# eerste poll
            print('Poll: 1st')
            for i in self.voters:
                voter = HonestVoter(i, self, [], i.position) # create aantal Honestvoters
                distCand = voter.distanceCandidates(self.candidates)
                chosenCandidate = voter.choseCandidate(distCand)
                
                if resultPoll.get(chosenCandidate):
                    # votes = resultPoll.get(chosenCandidate)
                    # votes += 1
                    # resultPoll.update({chosenCandidate: votes})
                    resultPoll.update({chosenCandidate: 0})
                else:
                    resultPoll.update({chosenCandidate: 0})

            return resultPoll    

        else: # niet de eerste poll
            # print('Poll: n\'d',self.currentPollCounter+1)
            # dist = [voter.distanceCandidates(self.candidates)  for  voter  in self.voters]
            # map(Voter.choseCandidate(dist), self.voters)
            # for cand in self.candidates:
            #     resultPoll[cand] = cand.amountVotes

            # return resultPoll
            for voter in self.voters:
                distCand = voter.distanceCandidates(self.candidates)
                chosenCandidate = voter.choseCandidate(distCand,self.currentPoll)
                
                if resultPoll.get(chosenCandidate):
                    votes = resultPoll.get(chosenCandidate)
                    votes += 1
                    resultPoll.update({chosenCandidate: votes})
                else:
                    resultPoll.update({chosenCandidate: 1})

            return resultPoll    
    
    
    def step(self):
        self.datacollector.collect(self)
        self.currentPoll = self.poll()
        print(self.currentPoll)
        self.schedule.step()
        self.currentPollCounter += 1