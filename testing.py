import json
import time
from requests import get


i = 0
while True :
    
    get("http://localhost:5000/testing", data=json.dumps({"key":"key", "value": i}))
    time.sleep(1)
    i += 1