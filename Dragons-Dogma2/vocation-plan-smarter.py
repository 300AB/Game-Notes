import os
import pandas as pd
from io import StringIO

# === LEVELING PLAN ===
fallback_plan = [
    ("Archer", 2, 9),
    ("Mage", 11, 2),
    ("Fighter", 13, 3),
    ("Warrior", 16, 3),
#    ("Sorcerer", 19, 2),
    ("Sorcerer", 19, 3),
    ("Warrior", 28, 1),
    ("Sorcerer", 29, 3),
    ("Thief", 32, 2),
    ("Sorcerer", 34, 2),
    ("Thief", 36, 2),
]

# === CONFIG ===
stat_file = "statData.md"
show_level_log_first = False  # Show levels used & detailed log before summary
show_level_used = False       # Toggle on/off Levels Used table

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
short_cols = ["HP", "Stamina", "Str", "Def", "Magick", "Magick Def"]
base_level_1 = {
    "Health": 500,
    "Stamina": 600,
    "Strength": 40,
    "Defense": 40,
    "Magick": 30,
    "Magick Def": 30
}

# === LOAD STATS ===
script_dir = os.path.dirname(os.path.abspath(__file__))
stat_path = os.path.join(script_dir, stat_file)
with open(stat_path) as f:
    lines = f.readlines()
data_lines = lines[2:]
data_str = "".join(data_lines)
df = pd.read_csv(StringIO(data_str), sep="|", skipinitialspace=True, header=None)
df = df.dropna(axis=1, how='all')
df.columns = ["Level"] + stat_cols
df = df.astype(str).apply(lambda col: col.str.strip())
df[["Level"] + stat_cols] = df[["Level"] + stat_cols].apply(pd.to_numeric)

# === MAP PLAN TO LEVELS ===
level_to_voc = {}
for voc, start, count in fallback_plan:
    for lvl in range(start, start + count):
        level_to_voc[lvl] = voc

# === TRACK STATS & LOGS ===
total_stats = {stat: base_level_1[stat] for stat in stat_cols}
included_levels = []
per_level_log = []
running_totals = {stat: 0.0 for stat in stat_cols}

for _, row in df.iterrows():
    lvl = row["Level"]
    if lvl == 1 or lvl not in level_to_voc:
        continue
    voc = level_to_voc[lvl]
    included_levels.append((lvl, voc))
    mults = vocations.get(voc, [1]*6)
    gains = []
    for i, stat in enumerate(stat_cols):
        base_gain = row[stat]
        modded_gain = base_gain * mults[i]
        total_stats[stat] += modded_gain
        running_totals[stat] += modded_gain
        gains.append(modded_gain)
    per_level_log.append((lvl, voc, gains, running_totals.copy()))

# === FORMATTERS ===
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

def format_detailed_log(log):
    header = "===== Per-Level Stat Gains (With Vocation Mod) ======="
    table = ["| Lvl | Vocation | " + " | ".join(short_cols) + " | Growth |",
             "|:---:|:--------:|" + "|".join([":----:" if c != "Magick Def" else ":----------:" for c in short_cols]) + "|:-------:|"]
    for lvl, voc, gains, _ in log:
        growth = f"{sum(gains):7.1f}"
        row_gains = " | ".join(f"{g:5.1f}" for g in gains)
        table.append(f"| {lvl:<3} | {voc:<8} | {row_gains} | {growth} |")
    return "\n".join([header] + table)

# === OUTPUT ===
if show_level_log_first:
    if show_level_used:
        print(format_level_table(included_levels))
        print()
    print(format_detailed_log(per_level_log))
    print()
    print("== Net Stat Gains With Plan ==")
    print(format_stat_table(total_stats))
else:
    print("== Net Stat Gains With Plan ==")
    print(format_stat_table(total_stats))
    print()
    if show_level_used:
        print(format_level_table(included_levels))
        print()
    print(format_detailed_log(per_level_log))
