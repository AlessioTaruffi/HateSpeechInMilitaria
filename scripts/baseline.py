'''
Baseline with match based binary classification on HurtLex

The code loads HurtLex and only keeps lemmas tagged as 'conservative', which have low ambiguity
A post is labeled as hate onlu if it contains at least one of such lemmas.

On benchmarks (HateXplaion and Olid) the code reports macro-F1 and precision/recall/F1 on the positive class
On the challenge set it reports teh false positive rate on the descriptive items and recall on hateful ones.
'''

import glob, re
import pandas as pd
from sklearn.metrics import f1_score, precision_recall_fscore_support
from collections import Counter

# HurtLex: colonne category, pos, lemma, level
hl = pd.read_csv("data/raw/hurtlex_EN.tsv", sep="\t")
lexicon = set(hl[hl.level == "conservative"].lemma.str.lower())
print(len(lexicon), "termini nel lessico")

def predict(text):
    tokens = set(re.findall(r"\b\w+\b", text.lower()))
    return int(bool(tokens & lexicon))

def evaluate(df, name):
    df = df.copy()
    df["pred"] = df.text.map(predict)
    print(f"\n=== {name} ===")
    if "split" in df.columns:
        print(f"macro-F1: {f1_score(df.label, df.pred, average='macro'):.3f}")
        p, r, f, _ = precision_recall_fscore_support(df.label, df.pred, average=None)
        print(f"classe 1: P={p[1]:.3f} R={r[1]:.3f} F1={f[1]:.3f}")
    else:
        neg, pos = df[df.label == 0], df[df.label == 1]
        print(f"FPR: {(neg.pred == 1).mean():.3f}   TPR: {(pos.pred == 1).mean():.3f}")
        print(pos.groupby("explicitness")["pred"].mean())
        print(neg.groupby("source_type")["pred"].mean())
    return df

hx = pd.read_json("data/hatexplain.jsonl", lines=True)
evaluate(hx[hx.split == "test"], "HateXplain test")

olid = pd.read_json("data/olid.jsonl", lines=True)
evaluate(olid[olid.split == "test"], "OLID test")

files = sorted(glob.glob("challenge/items/*.jsonl"))
chal = pd.concat([pd.read_json(f, lines=True) for f in files], ignore_index=True)
out = evaluate(chal, "Challenge set")
out.to_json("predictions/lexicon_challenge.jsonl",
            orient="records", lines=True, force_ascii=False)
for t in out[(out.explicitness == "coded") & (out.pred == 1)].text.head(5):
    print(set(re.findall(r"\b\w+\b", t.lower())) & lexicon, "|", t[:70])


c = Counter()
for t in out[out.pred == 1].text:
    c.update(set(re.findall(r"\b\w+\b", t.lower())) & lexicon)
print(c.most_common(20))

print(out.groupby("pred").text.apply(lambda s: s.str.split().str.len().mean()))