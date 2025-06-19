import pandas as pd
from io import StringIO

# Read markdown file, skip header and divider lines
with open("your_stats.md") as f:
    lines = f.readlines()

data_lines = lines[2:]  # skip header + divider
data_str = "".join(data_lines)

# Load data from string buffer
df = pd.read_csv(StringIO(data_str), sep="|", skipinitialspace=True, header=None)

# Drop empty columns (edges from markdown pipes)
df = df.dropna(axis=1, how='all')

# Assign column names manually (match your markdown table)
df.columns = ["Level", "Health", "Stamina", "Strength", "Defense", "Magick", "Magick Def"]

# Clean whitespace
df = df.astype(str).apply(lambda col: col.str.strip())

# Convert all numeric columns
for col in ["Level", "Health", "Stamina", "Strength", "Defense", "Magick", "Magick Def"]:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Define stat columns for logic
stat_cols = ["Health", "Stamina", "Strength", "Defense", "Magick", "Magick Def"]

# Vocation multipliers
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

# Determine dominant stat and best vocation per row
def best_vocation_for_row(row):
    dominant_index = row[stat_cols].values.argmax()
    dominant_stat = stat_cols[dominant_index]
    best_vocation = max(vocations.items(), key=lambda v: v[1][dominant_index])[0]
    return pd.Series([dominant_stat, best_vocation], index=["Dominant Stat", "Best Vocation"])

df[["Dominant Stat", "Best Vocation"]] = df.apply(best_vocation_for_row, axis=1)

# Pretty markdown table formatter
def format_markdown_table(df):
    df_str = df.astype(str)
    widths = [max(len(col), *(df_str[col].str.len())) for col in df_str.columns]
    header = "| " + " | ".join(f"{col:<{w}}" for col, w in zip(df_str.columns, widths)) + " |"
    divider = "|-" + "-|-".join("-" * w for w in widths) + "-|"
    rows = []
    for _, row in df_str.iterrows():
        line = "| " + " | ".join(f"{val:<{w}}" for val, w in zip(row, widths)) + " |"
        rows.append(line)
    return "\n".join([header, divider] + rows)

# Print the final table
print(format_markdown_table(df))
