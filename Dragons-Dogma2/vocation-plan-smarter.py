import os
import pandas as pd
from io import StringIO

# === CONFIG ===
stat_file = "statData.md"

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

# === BASE LEVEL 1 STATS ===
base_level_1 = {
    "Health": 500,
    "Stamina": 600,
    "Strength": 40,
    "Defense": 40,
    "Magick": 30,
    "Magick Def": 30
}

# === Get file path ===
script_dir = os.path.dirname(os.path.abspath(__file__))
stat_path = os.path.join(script_dir, stat_file)

# === LOAD STAT GAINS FROM MARKDOWN ===
with open(stat_path) as f:
    lines = f.readlines()
data_lines = lines[2:]
data_str = "".join(data_lines)
df = pd.read_csv(StringIO(data_str), sep="|", skipinitialspace=True, header=None)
df = df.dropna(axis=1, how='all')
df.columns = ["Level"] + stat_cols
df = df.astype(str).apply(lambda col: col.str.strip())
df[["Level"] + stat_cols] = df[["Level"] + stat_cols].apply(pd.to_numeric)

# === LEVELING PLAN ===
fallback_plan = [
    ("Archer", 2, 9),
    ("Mage", 11, 2),
    ("Fighter", 13, 3),
    ("Warrior", 16, 3),
    ("Sorcerer", 19, 2),
]


# === LEVELING PLAN (Peak Stats) ===
#fallback_plan = [
#    ("Thief", 2, 10),
#    ("Sorcerer", 12, 1),
#    ("Warrior", 13, 1),
#    ("Thief", 14, 3),
#    ("Sorcerer", 17, 2),
#    ("Warrior", 19, 1),
#    ("Sorcerer", 20, 1),
#    ("Fighter", 21, 1),
#    ("Warrior", 22, 1),
#    ("Sorcerer", 23, 1),
#    ("Warrior", 24, 2),
#    ("Sorcerer", 26, 2),
#    ("Warrior", 28, 1),
#    ("Sorcerer", 29, 1),
#    ("Warrior", 30, 1),
#    ("Sorcerer", 31, 2),
#    ("Warrior", 33, 1),
#    ("Sorcerer", 34, 2),
#    ("Warrior", 36, 1),
#    ("Sorcerer", 37, 1),
#    ("Warrior", 38, 3),
#]

# === EXPAND TO LEVEL MAP ===
level_to_voc = {}
for voc, start, count in fallback_plan:
    for lvl in range(start, start + count):
        level_to_voc[lvl] = voc

# === CALCULATE STATS ===
total_stats = {stat: base_level_1[stat] for stat in stat_cols}
included_levels = []

for _, row in df.iterrows():
    lvl = row["Level"]
    if lvl == 1:
        continue
    if lvl not in level_to_voc:
        continue
    voc = level_to_voc[lvl]
    included_levels.append((lvl, voc))
    mults = vocations.get(voc, [1]*6)
    for i, stat in enumerate(stat_cols):
        total_stats[stat] += row[stat] * mults[i]

# === FORMAT OUTPUT ===
def format_stat_table(stats_dict):
    header = "| Stat        | Total Gain  |"
    divider = "|:-----------:|:-----------:|"
    rows = [f"| {stat:<11} | {val:>11.2f} |" for stat, val in stats_dict.items()]
    return "\n".join([header, divider] + rows)

def format_level_table(levels):
    header = "===== Levels Used ======="
    table_header = "| Level     | Vocation |\n|:---------:|:--------:|"
    rows = [f"| Level {lvl:<2}  | {voc:<8} |" for lvl, voc in sorted(levels)]
    return "\n".join([header, table_header] + rows)

# === OUTPUT ===
print("== Net Stat Gains With Plan ==")
print(format_stat_table(total_stats))
print()
print(format_level_table(included_levels))
