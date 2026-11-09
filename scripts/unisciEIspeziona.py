'''
merges the item files from the individual bases into a single challenge set and prints the profile.

The checks are used to verify that there are zero duplicate IDs, that no
feature is too sparsely populated and that each explicitness level has
enough hate items to report a recall. 
'''


import pandas as pd, glob

files = glob.glob("challenge/items/*.jsonl")
df = pd.concat([pd.read_json(f, lines=True) for f in files], ignore_index=True)
df.to_json("challenge/challenge_v1.jsonl", orient="records", lines=True, force_ascii=False)


print(len(df), "item")
print(df.id.duplicated().sum(), "ID duplicati")
print(df.text.duplicated().sum(), "testi duplicati")
print()
print(df.label.value_counts())
print()
print(df.groupby("functionality").size().sort_values())
print()
print(df[df.label == 1].explicitness.value_counts())
print()
print(df.pair_id.notna().sum(), "item appaiati")

#print(df[df.text.duplicated(keep=False)].sort_values("text")[["id","text"]].to_string())

