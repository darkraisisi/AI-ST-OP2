from mesa import Agent, Model
from mesa.visualization.ModularVisualization import ModularServer

from mesa.visualization.modules import CanvasGrid
from mesa.visualization.modules import ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from Classes.Person import Person, Voter, HonestVoter, StrategicVoter, Candidate
from Classes.Model import VoterModel

if __name__ == "__main__":
    model_params = {
        "n_voters": UserSettableParameter( "slider", "Number of Voters", 100, 2, 1000, 5, description="Choose how many agents to include in the model"),
        "n_candidates": UserSettableParameter( "slider", "Number of Candidates", 3, 2, 12, 1, description="Choose how many agents to include in the model"),
        "width": 10,
        "height": 10,
    }

    server = ModularServer(VoterModel, [], "Money Model", model_params)
    server.port = 8521
    server.launch()

    # Test of plurality voting
    candidates = []
    voters = []
    for i in range(3): # Get some candidates
        candidates.append(Candidate())
    for i in range(10000): # Get some voters
        voters.append(HonestVoter())

    for vot in voters: # Make all the voters vote
        # print(vot.position)
        vot.castVote(candidates)

    total = 0
    for i, can in enumerate(candidates): # See the final score and actual candidate position
        print(i,can.amountVotes,can.position)
        total += can.amountVotes

    print(total)