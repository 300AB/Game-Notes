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
    ("Archer", 2, 9),
    ("Mage", 11, 2),
    ("Fighter", 13, 3),
    ("Warrior", 16, 3),
    ("Sorcerer", 19, 2),
]

# === EXPAND PLAN TO PER-LEVEL MAP ===
level_to_voc = {}
for voc, start, count in fallback_plan:
    for lvl in range(start, start + count):
        level_to_voc[lvl] = voc

# === CALCULATE TOTAL STATS WITH VOC MULTIPLIERS AND BASE ===
total_stats = {stat: base_level_1[stat] for stat in stat_cols}
included_levels = []

for _, row in df.iterrows():
    lvl = row["Level"]
    if lvl == 1:
        continue  # base level 1 already counted
    if lvl not in level_to_voc:
        continue
    voc = level_to_voc[lvl]
    included_levels.append((lvl, voc))
    multipliers = vocations.get(voc, [1]*6)
    for i, stat in enumerate(stat_cols):
        total_stats[stat] += row[stat] * multipliers[i]

# === MARKDOWN OUTPUT ===
def format_stat_table(stats_dict):
    header = "| Stat        | Total Gain |"
    divider = "|:-----------:|:----------:|"
    rows = [f"| {stat.ljust(11)} | {val:>10.2f} |" for stat, val in stats_dict.items()]
    return "\n".join([header, divider] + rows)

def format_levels_used(levels):
    lines = [
        "===== Levels Used =======",
        "|:---------:|:--------:|",
        "| Level     | Vocation |"
    ]
    for lvl, voc in levels:
        # Align spacing: pad lvl number to 2 digits, pad vocation left with spaces to 8 chars
        lvl_str = f"Level {lvl}:".ljust(9)
        voc_str = voc.ljust(8)
        lines.append(f"| {lvl_str} | {voc_str} |")
    return "\n".join(lines)


print("== Net Stat Gains With Plan ==")
print(format_stat_table(total_stats))

if included_levels:
    print()
    print(format_levels_used(sorted(included_levels)))
