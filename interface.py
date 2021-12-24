
from flask import Flask, render_template,request

from flask import jsonify
import time
import requests

app = Flask(__name__)



s = time.time()
node = 'localhost:5001'
"""while( s + 25 > time.time()):
    print(s-time.time())
    pass"""
    
#response = requests.get(f'http://{node}/sku')

"""if response.status_code == 200:
    print(response.json())"""

@app.route('/',methods=['post', 'get'])
def index():
    message = ''
    if request.method == 'POST':
        value = request.form.get('value')  # access the data inside 
        key = request.form.get('key')
        s = request.form.get('s')
        print(value,key,s)
        message = 'value add to the block'

    return render_template('test.html', message=message)

@app.route('/sku')
def update_peers():

    return jsonify({'e':'biatch'})


if __name__ == '__main__':
      app.run(host='0.0.0.0', port=8999)