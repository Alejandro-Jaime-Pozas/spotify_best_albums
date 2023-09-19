import re

# Your input string
input_string = "Wire 154 [as] (2006 Remastered Version) [more] (more)"

# Regular expression to remove everything inside parentheses and square brackets
output_string = re.sub(r'\([^)]*\)', '', re.sub(r'\[[^\]]*\]', '', input_string))

print(output_string)
