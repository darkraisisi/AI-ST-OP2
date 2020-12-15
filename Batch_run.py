from mesa.batchrunner import BatchRunnerMP, BatchRunner
from Classes.Model import  VoterModel, getPoll, getStratPerPollCounter
from Classes.Person import Person, Voter, HonestVoter, StrategicVoter, Candidate
import pickle

def batch_run(fixed_params, variable_params, iterations, max_nsteps):

    batchrun = BatchRunner(
        VoterModel,
        variable_params,
        fixed_params,
        iterations,
        max_nsteps,
        model_reporters  = {"Polls":getPoll,
                            "stratPerPollCounter":getStratPerPollCounter}
    )

    batchrun.run_all()
    dataCollection = batchrun.get_model_vars_dataframe()  # Get DataFrame with collected data
    return dataCollection

if __name__ == "__main__":
    voter_type = "Strategic"
    fixed_params = {
        "n_voters": 1000, 
        "n_candidates": 4,
        "voter_type": voter_type,
        "maxpolls": 14,
        "loyalty":30,
        "strat_chance":30,
        "width": 2,
        "height":2,
    }
    # Batch run
    data_br = batch_run(fixed_params, None, 1000, 10)
    pickle.dump(data_br,open(f'batch_run_{voter_type.lower()}_2_14poll','wb'))