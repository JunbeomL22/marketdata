import json

def parse_json(filepath):
    with open(filepath, 'r') as f:
        for line in f:
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue

realtime_data = list(parse_json('D:/Projects/marketdata/RealTimeData/realtime.json'))

