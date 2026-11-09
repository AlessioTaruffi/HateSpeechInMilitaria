'''
Central configuration
SPLIT_SEED is used only once, by prepare_olid.py, to carve out the validation split
from then on, the splits live on disk. 
TRAIN_SEEDS collects the seeds used to run the fine-tuned models, used to estimate the
variance between runs. Colab notebooks cannot import this file and
replicate its values in the configuration cell.
In the end this file is mostly unused, but it's been kept for consistency's sake.
'''

import random
import numpy as np
import torch

DATA = "data"
CHALLENGE = "challenge"
PREDICTIONS = "predictions"
RESULTS = "results"

SPLIT_SEED = 42        
TRAIN_SEEDS = [67, 13, 1337]

def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)