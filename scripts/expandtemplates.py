'''
Code responsible for the expansion of the templates phrases
Each phrase branches into multiple ones according to its slots
Phrases have been made so as to make sense with every possible item in their slot
When this was not possible new ad-hoc slots were added
'''

import csv, json, random, re, itertools
import sys
base = sys.argv[1]

random.seed(42)
MAX_PER_TEMPLATE = 3

SLOTS = {
    "BRANCH":  ["Heer", "Luftwaffe", "SS", "Kriegsmarine", "SA"],
    "BRANCH_CUFF":  ["Heer", "Luftwaffe", "SS", "SA"],
    "BRANCH_HATE":  ["Heer", "SS", "SA"],
    "MODEL":   ["M33", "M35", "M42"],
    "SIZE":   ["62", "64", "66"],
    "MATERIAL":  ["steel", "aluminum", "brass"],
    "FINISH":   ["field grey", "silver", "sand", "tropical grey"],
    "MAKER_B":   ["Rodo", "RS&S", "Overhoff"],
    "MAKER_H":   ["ET64", "Q66", "NS64"],
    "PRICE":  ["350", "500", "800"],
    "YEAR":   ["1937", "1940", "1943", "1945"],
    "MONTH": ["January", "April", "July", "December"],
    "RANK": ["Obergefreiter", "Unteroffizier", "Feldwebel"],
    "AWARD": ["Iron Cross 2nd Class", "Wound Badge", "Ostmedaille", "War Merit Cross 2nd Class"],
    "WEAVE":   ["BeVo woven", "flatwire", "hand-embroidered"],
    "CLOTH":   ["black wool", "field grey wool", "green badgecloth"],
    "UNIT":    ["Das Reich", "Totenkopf", "Leibstandarte Adolf Hitler", "Götz von Berlichingen"],
}

#Endorsements to be added at the end of some fitting phrases
#These change according to the item in question (helmets / buckles / cufftitles / soldbuchs)
ENDORSE = [
    "That division had standards nobody matches today."
    "They held the line when everyone else ran."
    "Say what you like about them, they fought better than anyone."
    "A unit worth remembering for the right reasons."
]

rows = list(csv.DictReader(open(f"challenge/templates/{base}.csv")))

items = []
pair_n = 0

for t in rows:
    text = t["text"]
    names = re.findall(r"\{(\w+)\}", text)
    has_branch = "BRANCH" in names
    other = [n for n in names if n != "BRANCH"]

    if other:
        combos = list(itertools.product(*[SLOTS[n] for n in other]))
        random.shuffle(combos)
        combos = combos[:MAX_PER_TEMPLATE]
    else:
        combos = [()]

    for combo in combos:
        filled = text
        for name, val in zip(other, combo):
            filled = filled.replace("{" + name + "}", val)

        branches = SLOTS["BRANCH"] if has_branch else [None]

        for b in branches:
            filled_text = filled.replace("{BRANCH}", b) if b else filled

            items.append({
                "text": filled_text,
                "label": int(t["label"]),
                "functionality": t["functionality"],
                "template_id": t["template_id"],
                "branch": b,
                "pair_id": None,
                "source_type": "template",
                "explicitness": t.get("explicitness", ""),
            })

            if (t["pairable"] == "yes" and t["label"] == "0" and b == branches[0]):
                pair_n += 1
                pid = f"p{pair_n:04d}"
                items[-1]["pair_id"] = pid
                items.append({
                    "text": filled_text + " " + random.choice(ENDORSE),
                    "label": 1,
                    "functionality": "H1",
                    "template_id": t["template_id"],
                    "branch": b,
                    "pair_id": pid,
                    "source_type": "template",
                    "explicitness": "deictic", #le clausole di endorse sono sempre di tipo dittico (a meno che vengano cambiate in futuro)
                })

for i, it in enumerate(items, 1):
    it["id"] = f"{base[:4]}_{i:04d}"

with open(f"challenge/items/{base}.jsonl", "w", encoding="utf-8") as f:    
    for it in items:
        f.write(json.dumps(it, ensure_ascii=False) + "\n")

print(f"{len(items)} item generati")