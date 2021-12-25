"""import requests
node = 'localhost:5001'
response = None
try:
    
    response = requests.get(f'http://{node}/addNewNode?address=localhost:5001')
except Exception:
    print("mohim")

if response.status_code == 200:
    print(response.json())
    f = response.json()

    print(type(f))"""

from logo import LOGO

print(LOGO)
