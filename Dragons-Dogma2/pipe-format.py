import re

def format_to_pipe_table(text):
    lines = text.strip().split('\n')
    formatted = []
    for line in lines:
        # Finds ints or floats; ignores stray chars
        numbers = re.findall(r'\d+(?:\.\d+)?', line)
        if numbers:
            formatted.append("| " + " | ".join(numbers) + " |")
    return "\n".join(formatted)

# Paste your value block below
value_block = """
18 9 3 3 2 2
20 11 3 2 4 4
21.2 13 3 4 3 2
4+4 1.5
"""

# Format it
print(format_to_pipe_table(value_block))

