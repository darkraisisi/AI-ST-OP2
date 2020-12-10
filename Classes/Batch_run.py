from mesa.batchrunner import BatchRunner
from Classes.Model import  VoterModel, getCandidates
from Classes.Person import Person, Voter, HonestVoter, StrategicVoter, Candidate

def batch_run(nvoters, ncandidates,  iterations, max_nsteps):
    
    fixed_params = {
        "n_voters": nvoters, 
        "n_candidates": ncandidates,
        "voter_type": "Strategic",
        "maxpolls":  6,
        'loyalty':30, 
        "width": 2,
        "height":2,
    }
    

    batchrun = BatchRunner(
        VoterModel,
        None,
        fixed_params,
        iterations,
        max_nsteps,
        model_reporters  = {"Votes":getCandidates}
    )

    batchrun.run_all()
    dataCollection = batchrun.get_model_vars_dataframe()  # Get DataFrame with collected data
    return dataCollection