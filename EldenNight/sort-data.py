import csv
import os
import json

# Script location + input/output file names
script_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(script_dir, "yourfile.csv")
output_file = os.path.join(script_dir, "effect_output.json")

output_dict = {}

# Read CSV
with open(input_file, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        attach_id = row["attachEffectId"].strip()
        name = row["Name"].strip()
        if attach_id and name:
            output_dict[attach_id] = {"name": name}

# Sort keys and write as JSON with trailing commas preserved manually
sorted_items = sorted(output_dict.items())

with open(output_file, "w", encoding="utf-8") as f:
    f.write("{\n")
    for i, (key, value) in enumerate(sorted_items):
        comma = "," if i < len(sorted_items) - 1 else ""
        f.write(f'  "{key}": {json.dumps(value)}{comma}\n')
    f.write("}\n")

print(f"✅ Done. Saved to: {output_file}")
