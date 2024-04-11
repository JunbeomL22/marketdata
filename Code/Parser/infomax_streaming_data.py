import json
import pandas as pd

# File path
file_path = "D:/Projects/marketdata/RealTimeData/realtime.json"

# Read the JSON data from the file
with open(file_path, "r") as file:
    json_data = file.read()

# Extract JSON strings from the document content
json_strings = json_data.replace('\n\n', '\n').strip().split('\n')

# Parse JSON strings and extract relevant data
data = []
for json_string in json_strings:
    json_string = json_string.replace('\\\\', '\\')  # Replace double backslashes with single backslashes
    json_string = json_string.replace('\\"', '"')  # Replace escaped quotes with regular quotes
    json_string = json_string.strip('"')  # Remove the outer quotes
    print("1", json_string)
    json_obj = json.loads(json_string)
    print("2", json_obj)
    payload = json.loads(json_obj['payload'].replace('\\"', '"'))
    print("3", payload)
    out_block = payload['OutBlock']
    print("4", out_block)
    data.append(out_block)

# Create a DataFrame from the extracted data
df = pd.DataFrame(data)

# Print the resulting DataFrame
print(df)