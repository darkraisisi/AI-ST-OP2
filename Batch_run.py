from mesa.batchrunner import BatchRunner
from Classes.Model import  VoterModel, getCandidates, getPoll
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
        model_reporters  = {"Votes":getCandidates, 
                            "Polls":getPoll}
    )

    batchrun.run_all()
    dataCollection = batchrun.get_model_vars_dataframe()  # Get DataFrame with collected data
    return dataCollection
    #TODO: get list of pollss for every run
if __name__ == "__main__":
    # Batch run 
    data_br = batch_run(1000, 3, 2, 10)
    for i in data_br['Polls']:
        for j in i:
            print(j.values())
    print("")
    
    # for run in data_br["Polls"]:
    #     for cand in run:
    #         print(run[cand]()) # execute function run[cand]
    #     print("")