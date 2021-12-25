import argparse
from flask import Flask, render_template,request,jsonify
from peers import Peer
from logo import LOGO

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
        m = request.form.get('printNet')
        print(m)
        if request.form.get('printNet'):
            print(p._peers)
        message = 'value add to the block'
        pp = p._peers

    #return render_template('test.html', message=message)
    return render_template('test.html', pp=pp)

@app.route('/sku')
def update_peers():

    return jsonify({'e':'biatch'})

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
    return jsonify(p._memoryPool)

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
    print(LOGO)
    app.run(host='localhost', port=port)

    