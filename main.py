from mesa import Agent, Model
from mesa.visualization.ModularVisualization import ModularServer

from mesa.visualization.modules import CanvasGrid
from mesa.visualization.modules import ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from Classes.ContinuousCanvas import SimpleCanvas

from Classes.Person import Person, Voter, HonestVoter, StrategicVoter, Candidate
from Classes.Model import VoterModel
from Classes.Batch_run import batch_run

def agent_portrayal(agent):
    portrayal = {"Shape": "circle", "Filled": "true", "r": 0.5,"Color":"red"}

    if agent.isCandidate:
        portrayal["Color"] = agent.color
        portrayal["Layer"] = 2
        portrayal["r"] = 3
    else:
        portrayal["Color"] = agent.color
        portrayal["Layer"] = 1
        portrayal["r"] = 1
    return portrayal

if __name__ == "__main__":
    size = 2
    model_params = {
        "n_voters": UserSettableParameter( "slider", "Number of Voters", 100, 2, 1000, 5, description="Choose how many agents to include in the model"),
        "n_candidates": UserSettableParameter( "slider", "Number of Candidates", 3, 2, 12, 1, description="Choose how many agents to include in the model"),
        "width": size,
        "height": size,
    }

    grid = SimpleCanvas(agent_portrayal, 500, 500) # 500, 500 canvas display size

    server = ModularServer(VoterModel, [grid], "Voter Model", model_params)
    server.port = 8521
    server.launch()

    # Batch run 
    data_br= batch_run(10, 3, 2, 10)
    print(data_br)
    
