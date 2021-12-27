import argparse
from blockchain import Block
from flask import Flask, render_template,request,jsonify
from peers import Peer
from logo import LOGO
from transaction import Transaction
import json
import time
from colorama import init
from termcolor import cprint
from pyfladesk import init_gui
import threading 
from threading import Timer,Thread,Event
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

    if request.method == 'POST':
        if request.form.get('s'):
            value = request.form.get('value')  # access the data inside 
            key = request.form.get('key')
            call =  request.form.get('callback')
            if call :
                p.put(key,value,time.asctime(),True) # add call back to user
            else:
                p.put(key,value,time.asctime(),False)

        if request.form.get('RETRIEVE'):
            key = request.form.get('key')
            retrieved_key = p.retrieve(key)
            return render_template('test2.html',retrieve_key = retrieved_key)
        
        if request.form.get('RETRIEVE ALL'):
            key = request.form.get('key')
            retrieved_keys = p.retrieve_all(key)
            return render_template('test2.html',retrieve_keys = retrieved_keys)
        
        if request.form.get('NETWORK'):
            return render_template('test2.html',p=p.peers)
        
    return render_template('test2.html')

@app.route('/peers')
def send_peers():
    return jsonify(p.peers)

@app.route('/addNewNode')
def addNewNode():
    new_peer= request.args.get('address')
    if new_peer not in p.peers:
        p.peers.append(new_peer)
        p.heartbeat_count[new_peer] = 0
    return jsonify(p.blockchain.last_block._hash)

@app.route('/keyChain')
def send_keyChain():
    return jsonify(str(p.blockchain))

@app.route('/memoryPool')
def sendMemoryPool():
    return jsonify(str(p.memoryPool))

@app.route('/addTransaction')
def newTransaction():
    print("new trans")
    t = request.args.get('transaction').replace("\'",'\"')
    p.add_transaction(Transaction(t))
    return jsonify({})

@app.route('/heartbeat')
def send_heartbeat():
    return jsonify({'address': p.address})
  
@app.route('/addNewBlock')
def addNewBlock():
    print("new block")
    b = request.args.get('block').replace("\'",'\"')
    p.add_block(Block(b))
    return jsonify(dict())

@app.route('/sku')
def update_peers():

    return jsonify({'e':'biatch'})

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
     
    cprint(LOGO,'red')
    thread = threading.Timer(0, p.mine)
    thread.daemon = True
    thread.start()
    
    app.run(port=port)
    #init_gui(app, port=port, width=1000, height=900,
           # window_title=f'localhost:{port}', icon="static/favicon-32x32.png")

    