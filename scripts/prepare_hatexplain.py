'''
Code responsible for the normalization of HateXplain.

Resolves the three annotations by majority vote
Maps hatespeech to 1 and offensive/normal to 0 preserving the original label in label_orig
Recomposes the text from the tokens and aligns the placeholder and split name with the OLID convention.
'''

import json
from collections import Counter
import pandas as pd

data = json.load(open("data/raw/dataset.json"))
divisions = json.load(open("data/raw/post_id_divisions.json"))

split_of = {}
for split, ids in divisions.items():
    for pid in ids:
        split_of[pid] = split

rows, ties = [], 0

for pid, post in data.items():
    if pid not in split_of:
        continue

    labels = [a["label"] for a in post["annotators"]]
    counts = Counter(labels).most_common()

    if counts[0][1] == 1:
        ties += 1
        continue

    majority = counts[0][0]
    text = " ".join(post["post_tokens"])
    text = text.replace("<user>", "@USER").replace("<url>", "URL")

    rows.append({
        "id": "hx_" + pid,
        "text": text,
        "label": 1 if majority == "hatespeech" else 0,
        "label_orig": majority,
        "source": "hatexplain",
        "split": split_of[pid],
    })

df = pd.DataFrame(rows)
df["split"] = df["split"].replace("val", "dev")
df.to_json("data/hatexplain.jsonl", orient="records", lines=True, force_ascii=False)

print(f"scartati per assenza di maggioranza: {ties}")
print(df.groupby(["split", "label"]).size())
print(df.groupby(["split", "label_orig"]).size())