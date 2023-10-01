import re

# Example list
strings_list = ['res="144p"']

# Regular expression pattern to extract text within double quotes
pattern = r'"([^"]+)"'

# Extracted string
extracted_string = re.search(pattern, strings_list[0]).group(1)

print("Extracted:", extracted_string)

