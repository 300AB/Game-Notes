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

# === Get file path ===
script_dir = os.path.dirname(os.path.abspath(__file__))
stat_path = os.path.join(script_dir, stat_file)

# === LOAD STAT GAINS FROM MARKDOWN ===
with open(stat_path) as f:
    lines = f.readlines()
data_lines = lines[2:]  # skip header + divider
data_str = "".join(data_lines)
df = pd.read_csv(StringIO(data_str), sep="|", skipinitialspace=True, header=None)
df = df.dropna(axis=1, how='all')
df.columns = ["Level"] + stat_cols
df = df.astype(str).apply(lambda col: col.str.strip())
df[["Level"] + stat_cols] = df[["Level"] + stat_cols].apply(pd.to_numeric)

# === IN-CODE LEVELING PLAN ===
# Format: ("Vocation", StartLevel, Count)
fallback_plan = [
    ("Archer", 2, 8),       # Levels 2–6 as Thief
    ("Mage", 11, 2,),    # Levels 7–9 as Sorcerer
    ("Fighter", 13, 3),
    ("Warrior", 16, 3),
    ("Sorcerer", 19, 1),
]

# === EXPAND PLAN TO PER-LEVEL MAP ===
level_to_voc = {}
for voc, start, count in fallback_plan:
    for lvl in range(start, start + count):
        level_to_voc[lvl] = voc

# === APPLY MULTIPLIERS ===
total_stats = {stat: 0 for stat in stat_cols}
included_levels = []

for _, row in df.iterrows():
    lvl = row["Level"]
    if lvl not in level_to_voc:
        continue
    voc = level_to_voc[lvl]
    included_levels.append((lvl, voc))
    multipliers = vocations.get(voc, [1]*6)
    for i, stat in enumerate(stat_cols):
        total_stats[stat] += row[stat] * multipliers[i]

# === MARKDOWN OUTPUT ===
def format_stat_table(stats_dict):
    header = "| Stat | Total Gain |"
    divider = "|:-----|-----------:|"
    rows = [f"| {stat} | {val:.2f} |" for stat, val in stats_dict.items()]
    return "\n".join([header, divider] + rows)

print("== Net Stat Gains With Plan ==")
print(format_stat_table(total_stats))

# === LEVEL LOG ===
if included_levels:
    print("\n== Levels Used ==")
    for lvl, voc in sorted(included_levels):
        print(f"Level {lvl}: {voc}")
