import json

s = '[{"origin": "l:500", "key": "ab", "value": "cd", "timestamp": "mtn"}]'

print(type(json.loads(s)[0]))