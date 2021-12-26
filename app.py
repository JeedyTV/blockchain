import argparse
from flask import Flask, render_template,request,jsonify
from peers import Peer
from logo import LOGO
from transaction import Transaction
import json
import time
from colorama import init
from termcolor import cprint
from pyfladesk import init_gui
from routes import *

init()

def parse_arguments():
    parser = argparse.ArgumentParser(
        "KeyChain - An overengineered key-value store "
        "with version control, powered by fancy linked-lists.")

    parser.add_argument("--miner", type=bool, default=False, nargs='?',
                        const=True, help="Starts the mining procedure.")
    parser.add_argument("--bootstrap", type=str,default=None,
                        help="Sets the address of the bootstrap node.")
    parser.add_argument("--difficulty", type=int, default=5,
                        help="Sets the difficulty of Proof of Work, only has "
                             "an effect with the `--miner` flag has been set.")
    parser.add_argument("--port", type=int,required=True,help="")

    arguments, _ = parser.parse_known_args()

    return arguments

app = Flask(__name__)

@app.route('/',methods=['post', 'get'])
def index():
    message = ''
    if request.method == 'POST':
        if request.form.get('s'):
            value = request.form.get('value')  # access the data inside 
            key = request.form.get('key')
            print(value,key)
            p.put(key,value,time.asctime(),False)
        if request.form.get('NETWORK'):
            print(p._peers)
        message = 'value add to the block'
        
    #return render_template('test.html', message=message)
    return render_template('test.html')

@app.route('/sku')
def update_peers():

    return jsonify({'e':'biatch'})

@app.route('/addTransaction')
def newTransaction():
    print("new trans")
    t = request.args.get('transaction').replace("\'",'\"')
    t = json.loads(t)
    t = Transaction(t['origin'],t['key'],t['value'],t['timestamp'])
    p.add_transaction(t)
    return jsonify({'state':'recu'})

@app.route('/peers')
def send_peers():
    return jsonify(p._peers)

@app.route('/heartbeat')
def send_heartbeat():
    return jsonify({'address': p._address})

@app.route('/keyChain')
def send_keyChain():
    return jsonify(p._blockchain.rep())

@app.route('/addNewNode')
def addNewNode():
    #print('b',p._peers)
    new_peer= request.args.get('address')
    if new_peer not in p._peers:
        p._peers.append(new_peer)
        p._heartbeat_count[new_peer] = 0
    #print(f" {new_peer} wants to access the network")
    #print('a',p._peers)
    #print(type(p._blockchain))
    #print(p._blockchain.rep())
    return jsonify(p._blockchain.last_block.hash())
    
@app.route('/memoryPool')
def sendMemoryPool():
    m = []
    for i in p._memoryPool:
        m.append(i.rep())
    return jsonify({'transaction':m})
    
@app.route('/addNewBlock')
def addNewBlock():
    print("Entré dans addNewBlock")
    new_block= request.form.get('block')
    print(new_block)
    print("Type new_block")
    print(type(new_block))
    #p._blockchain.add_block(new_block)
    return jsonify(dict())

if __name__ == "__main__":
    arguments = parse_arguments()
    
    port = arguments.port
    miner = arguments.miner
    difficulty = arguments.difficulty
    bootstrap = arguments.bootstrap
    
    if not bootstrap:
        #first peer
        p = Peer(f'localhost:{port}',miner,difficulty=difficulty)
    else:
        #bootstrap peer  
        p = Peer(f'localhost:{port}',miner,bootstrap=bootstrap)
     
    cprint(LOGO, 'red')

    init_gui(app, port=port, width=1000, height=900,
             window_title="Key-value Chain", icon="static/favicon-32x32.png")

    