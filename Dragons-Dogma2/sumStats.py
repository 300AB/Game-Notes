import pandas as pd
from io import StringIO
import os

# === RESOLVE LOCAL PATHS ===
script_dir = os.path.dirname(os.path.abspath(__file__))
stat_file = os.path.join(script_dir, "statData.md")
plan_file = os.path.join(script_dir, "vocation_plan.md")

# === CONFIG ===
use_file_plan = True  # Flip to True to use vocation_plan.md

# === VOCATION MULTIPLIERS ===
vocations = {
    "Archer":           [1, 1.2, 1.2, 1.2, 0.8, 0.8],
    "Fighter":          [1.4, 1, 1.3, 1.3, 0.6, 0.6],
    "Mage":             [0.8, 1, 0.8, 0.8, 1.4, 1.4],
    "Thief":            [0.9, 1.3, 1.2, 1, 0.8, 1],
    "Mystic Spearhand": [1.2, 1, 1.2, 0.9, 1.2, 0.9],
    "Magick Archer":    [1, 1, 0.9, 0.9, 1.4, 1.2],
    "Sorcerer":         [0.8, 1, 0.7, 0.7, 1.6, 1.5],
    "Trickster":        [1, 1.1, 1, 1.1, 1, 1.2],
    "Warrior":          [1.5, 1, 1.5, 1.2, 0.6, 0.5],
    "Warfarer":         [1, 1, 1, 1, 1, 1],
}

stat_cols = ["Health", "Stamina", "Strength", "Defense", "Magick", "Magick Def"]

# === LOAD STAT GAINS ===
with open(stat_file) as f:
    lines = f.readlines()

data_lines = lines[2:]
data_str = "".join(data_lines)
df = pd.read_csv(StringIO(data_str), sep="|", skipinitialspace=True, header=None)
df = df.dropna(axis=1, how='all')
df.columns = ["Level", *stat_cols]
df = df.astype(str).apply(lambda col: col.str.strip())
df[["Level"] + stat_cols] = df[["Level"] + stat_cols].apply(pd.to_numeric)

# === PLAN LOADING (start level + count logic) ===
def load_plan_from_file(path=plan_file):
    try:
        with open(path) as f:
            lines = f.readlines()
        data_lines = lines[2:]
        data_str = "".join(data_lines)
        voc_df = pd.read_csv(StringIO(data_str), sep="|", skipinitialspace=True, header=None)
        voc_df = voc_df.dropna(axis=1, how='all')
        voc_df.columns = ["Vocation", "Start", "End", "Count"]  # end is ignored now
        voc_df = voc_df.astype(str).apply(lambda col: col.str.strip())
        voc_df[["Start", "Count"]] = voc_df[["Start", "Count"]].apply(pd.to_numeric)
        return [(row["Vocation"], row["Start"], row["Count"]) for _, row in voc_df.iterrows()]
    except Exception as e:
        print(f"Error loading plan file: {e}")
        return []

# === FALLBACK PLAN ===
fallback_plan = [
    ("Warfarer", 2, 1),  # Only Level 2
]

plan = load_plan_from_file() if use_file_plan else fallback_plan

# === BUILD VOCATION MAP ===
level_to_voc = {}
for voc, start, count in plan:
    for lvl in range(start, start + count):
        level_to_voc[lvl] = voc

# === APPLY MULTIPLIERS ONLY TO PLANNED LEVELS ===
total_stats = {stat: 0 for stat in stat_cols}

for _, row in df.iterrows():
    lvl = row["Level"]
    if lvl not in level_to_voc:
        continue
    voc = level_to_voc[lvl]
    multipliers = vocations[voc]
    for i, stat in enumerate(stat_cols):
        total_stats[stat] += row[stat] * multipliers[i]

# === OUTPUT ===
print("== Total Stat Gains With Vocation Plan ==")
for stat, val in total_stats.items():
    print(f"{stat}: {val:.2f}")
