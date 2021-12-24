import argparse
from flask import Flask, render_template,request,jsonify
from keychain.peers import Peer

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
        value = request.form.get('value')  # access the data inside 
        key = request.form.get('key')
        s = request.form.get('s')
        print(value,key,s)
        message = 'value add to the block'

    return render_template('test.html', message=message)

@app.route('/sku')
def update_peers():

    return jsonify({'e':'biatch'})

@app.route('/peers')
def send_peers():
    return jsonify(p._peers)

@app.route('/addNewNode')
def addNewNode():
    
    new_peer= request.args.get('address')
    p._peers.append(new_peer)
    print(f" {new_peer} wants to access the network")
    
    #return jsonify(p._blockchain.last_block.hash())
    return {'last_hash':"zzfezzef"}

@app.route('/memoryPool')
def sendMemoryPool():
    
    new_peer= request.args.get('address')
    p._peers.append(new_peer)
    print(f" {new_peer} wants to access the network")
    
    #return jsonify(p._blockchain.last_block.hash())
    return {'last_hash':"zzfezzef"}

if __name__ == "__main__":
    arguments = parse_arguments()
    port = arguments.port
    miner = arguments.miner
    difficulty = arguments.difficulty
    bootstrap = arguments.bootstrap
    if bootstrap:
        #first peer
        p = Peer(f'localhost:{port}',miner,difficulty=difficulty)
    else:
        #bootstrap peer  
        p = Peer(f'localhost:{port}',miner,bootstrap=bootstrap)
        p._peers = ['a','b','c']

    app.run(host='localhost', port=port)