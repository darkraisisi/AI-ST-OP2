from mesa.batchrunner import BatchRunner
from  Classes.Model import  VoterModel
from Classes.Person import Person, Voter, HonestVoter, StrategicVoter, Candidate

def batch_run(nvoters, ncandidates,  iterations, max_nsteps):
    fixed_params = {
        "width": 2,
        "height":2,
        "n_voters": nvoters, 
        "n_candidates": ncandidates
    }
    # variable_params = {
    #     # Determine ranges for n_voters and n_candidates
    #     "n_voters": range(100,  1000, 10), 
    #     "n_candidates": range(2,12)
    # }
    
    batchrun = BatchRunner(
        VoterModel,
        #variable_params,
        fixed_params,
        iterations = iterations,
        max_steps = max_nsteps,
        model_reporters  = {"resultPoll": VoterModel.poll,
                            "Cand1":  VoterModel.getAllVotes[0],
                            "Cand2":VoterModel.getAllVotes[1],
                            "Cand3":VoterModel.getAllVotes[2]
                            },
        agent_reporters   = {"Votes": Voter.choseCandidate}
    )

    batchrun.run_all()
    dataCollection = batchrun.get_model_vars_dataframe()  # Get DataFrame with collected data
    return dataCollection