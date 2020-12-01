from mesa import Agent, Model
from mesa.visualization.ModularVisualization import ModularServer

from mesa.visualization.modules import CanvasGrid
from mesa.visualization.modules import ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from Classes.Person import Person, Voter, Candidate
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

