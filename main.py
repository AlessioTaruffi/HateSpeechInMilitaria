#Just little checks written when necessary

import pandas as pd
nat = pd.read_json("challenge\\items\\natural.jsonl", lines=True)
print(len(nat))
print(nat.groupby(["label", "functionality"]).size())