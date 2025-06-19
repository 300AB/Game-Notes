import pandas as pd
from io import StringIO
import os

# === Auto-locate script directory ===
script_dir = os.path.dirname(os.path.realpath(__file__))
stat_path = os.path.join(script_dir, "statData.md")

# === Read stat data from markdown file ===
with open(stat_path) as f:
    lines = f.readlines()

data_lines = lines[2:]  # Skip header and divider
data_str = "".join(data_lines)

df = pd.read_csv(StringIO(data_str), sep="|", skipinitialspace=True, header=None)
df = df.dropna(axis=1, how='all')
df.columns = ["Level", "Health", "Stamina", "Strength", "Defense", "Magick", "Magick Def"]
df = df.astype(str).apply(lambda col: col.str.strip())
for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

stat_cols = ["Health", "Stamina", "Strength", "Defense", "Magick", "Magick Def"]

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

# === Detect stat spike per row, vertically (across levels) ===
def find_vertical_dominance(df, stat_cols):
    dominant_rows = []
    for i, row in df.iterrows():
        level = row["Level"]
        # % of max value for each stat
        spike_values = {stat: row[stat] / df[stat].max() for stat in stat_cols}
        dom_stat = max(spike_values.items(), key=lambda x: x[1])[0]
        dom_score = spike_values[dom_stat]
        stat_index = stat_cols.index(dom_stat)
        best_vocation = max(vocations.items(), key=lambda v: v[1][stat_index])[0]
        dominant_rows.append((level, dom_stat, f"{dom_score*100:.1f}%", best_vocation))
    return pd.DataFrame(dominant_rows, columns=["Level", "Peak Stat", "Peak %", "Best Vocation"])

# === Run and show ===
result_df = find_vertical_dominance(df, stat_cols)
print(result_df.to_markdown(index=False))
