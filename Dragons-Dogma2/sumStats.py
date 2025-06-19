import os
import pandas as pd
from io import StringIO

# === Get script directory and build file path ===
script_dir = os.path.dirname(os.path.abspath(__file__))
stat_file_path = os.path.join(script_dir, "statData.md")

# === Vocation multipliers ===
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

# === Shorthand maps ===
stat_shorts = {
    "Health": "Hp",
    "Stamina": "Sta",
    "Strength": "Str",
    "Defense": "Def",
    "Magick": "Mag",
    "Magick Def": "MgD"
}

vocation_shorts = {
    "Archer": "Arc",
    "Fighter": "Fight",
    "Mage": "Mage",
    "Thief": "Thief",
    "Mystic Spearhand": "MSpear",
    "Magick Archer": "MArc",
    "Sorcerer": "Sorc",
    "Trickster": "Trick",
    "Warrior": "War",
    "Warfarer": "Wfar"
}

# === Read stat data ===
with open(stat_file_path) as f:
    lines = f.readlines()

data_lines = lines[2:]  # skip header + divider
data_str = "".join(data_lines)

df = pd.read_csv(StringIO(data_str), sep="|", skipinitialspace=True, header=None)
df = df.dropna(axis=1, how='all')

stat_cols = ["Health", "Stamina", "Strength", "Defense", "Magick", "Magick Def"]
df.columns = ["Level"] + stat_cols
df = df.astype(str).apply(lambda col: col.str.strip())
df[["Level"] + stat_cols] = df[["Level"] + stat_cols].apply(pd.to_numeric)

# === Compute max-per-column to get peak %
max_stats = df[stat_cols].max()
percent_df = df[stat_cols].divide(max_stats)

# === Process dominant stats ===
rows = []
for i, row in df.iterrows():
    level = row["Level"]
    row_percents = percent_df.loc[i]
    top4 = row_percents.sort_values(ascending=False).head(4)
    voc_counts = {}
    data_row = [str(level)]

    for stat in top4.index:
        short = stat_shorts.get(stat, stat[:3])
        perc = f"{row_percents[stat]*100:.1f}%"
        idx = stat_cols.index(stat)
        best_voc = max(vocations.items(), key=lambda v: v[1][idx])[0]
        voc_short = vocation_shorts.get(best_voc, best_voc[:3])
        data_row += [short, perc, voc_short]
        voc_counts[voc_short] = voc_counts.get(voc_short, 0) + 1

    # Decide "average" voc: highest freq
    top_voc = max(voc_counts.items(), key=lambda x: x[1])[0]
    data_row.append(top_voc)
    rows.append(data_row)

# === Markdown Table Output ===
headers = ["Lvl", "Stat.1", "%.1", "V.1", "Stat.2", "%.2", "V.2", "Stat.3", "%.3", "V.3", "Stat.4", "%.4", "V.4", "Avg"]
align = [":-:" for _ in headers]

header_row = "| " + " | ".join(headers) + " |"
divider_row = "| " + " | ".join(align) + " |"
data_rows = ["| " + " | ".join(row) + " |" for row in rows]

output = "\n".join([header_row, divider_row] + data_rows)
print(output)
