from mesa import Agent, Model
from mesa.visualization.ModularVisualization import ModularServer

from mesa.visualization.modules import CanvasGrid
from mesa.visualization.modules import ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from Classes.Person import Person, Voter, HonestVoter, StrategicVoter, Candidate
from Classes.Model import VoterModel

def agent_portrayal(agent):
    portrayal = {"Shape": "circle", "Filled": "true", "r": 0.5}

    portrayal["Color"] = "red"
    portrayal["Layer"] = 1
    portrayal["r"] = 0.5
    return portrayal

if __name__ == "__main__":
    model_params = {
        "n_voters": UserSettableParameter( "slider", "Number of Voters", 100, 2, 1000, 5, description="Choose how many agents to include in the model"),
        "n_candidates": UserSettableParameter( "slider", "Number of Candidates", 3, 2, 12, 1, description="Choose how many agents to include in the model"),
        "width": 20,
        "height": 20,
    }

    grid = CanvasGrid(agent_portrayal, 20, 20, 500, 500)

    server = ModularServer(VoterModel, [grid], "Money Model", model_params)
    server.port = 8521
    server.launch()

    

    # total = 0
    # for i, can in enumerate(candidates): # See the final score and actual candidate position
    #     print(i,can.amountVotes,can.position)
    #     total += can.amountVotes

    # print(total)