from mesa.batchrunner import BatchRunner
from Classes.Model import  VoterModel, getCandidates, getPoll, getStratPerPollCounter
from Classes.Person import Person, Voter, HonestVoter, StrategicVoter, Candidate
import pickle

def batch_run(nvoters, ncandidates, voter_type, loyalty, strat_chance, iterations, max_nsteps):
    fixed_params = {
        "n_voters": nvoters, 
        "n_candidates": ncandidates,
        "voter_type": voter_type,
        "maxpolls":  6,
        'loyalty':30,
        'strat_chance':strat_chance,
        "width": 2,
        "height":2,
    }
    

    batchrun = BatchRunner(
        VoterModel,
        None,
        fixed_params,
        iterations,
        max_nsteps,
        model_reporters  = {"Votes":getCandidates, 
                            "Polls":getPoll,
                            "stratPerPollCounter":getStratPerPollCounter}
    )

    batchrun.run_all()
    dataCollection = batchrun.get_model_vars_dataframe()  # Get DataFrame with collected data
    return dataCollection
    #TODO: get list of pollss for every run
if __name__ == "__main__":
    voter_type = "Strategic"
    # Batch run
    data_br = batch_run(1000, 4, voter_type, 30, 30, 100, 10)
    pickle.dump(data_br,open(f'batch_run_{voter_type.lower()}_test','wb'))