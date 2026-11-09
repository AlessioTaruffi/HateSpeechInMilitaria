'''
Code reponsible for the normalization of OLID

Uses only the subtask_a (OFF/NOT) without filters.
The OLID test set keeps labels and text in separated files therefore it must be recomposed for the ID
The validation split which OLID doesn't give is cut out from training using SPLIT_SEED.
IDs are prefixed so as to not collide with HateXplain
'''

import sys
sys.path.append(".")

import pandas as pd
from sklearn.model_selection import train_test_split
from config import SPLIT_SEED

train = pd.read_csv("data/raw/olid-training-v1.0.tsv", sep="\t")
test_text = pd.read_csv("data/raw/testset-levela.tsv", sep="\t")
test_gold = pd.read_csv("data/raw/labels-levela.csv", names=["id", "subtask_a"])

test = test_text.merge(test_gold, on="id")

def to_schema(df, split):
    out = pd.DataFrame()
    out["id"] = "olid_" + df["id"].astype(str)
    out["text"] = df["tweet"]
    out["label"] = (df["subtask_a"] == "OFF").astype(int)
    out["source"] = "olid"
    out["split"] = split
    return out

tr, dev = train_test_split(
    train, test_size=0.1, random_state=SPLIT_SEED, stratify=train["subtask_a"]
)

parts = [to_schema(tr, "train"), to_schema(dev, "dev"), to_schema(test, "test")]
pd.concat(parts).to_json(
    "data/olid.jsonl", orient="records", lines=True, force_ascii=False
)

df = pd.read_json("data/olid.jsonl", lines=True)
print(df.groupby(["split", "label"]).size())