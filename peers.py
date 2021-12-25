#rom keychain import Block
#from keychain import Transaction
#from keychain import Blockchain
import time
import requests
from collections import Counter
from blockchain import Block,Blockchain
from transaction import Transaction

class Peer:
    def __init__(self, address,miner,bootstrap=None,difficulty=None):
        
        self._address = address
        self._miner = miner
        self._memoryPool = None
        self._peers = []
        self._blockchain = None
        self._ready = False
        #if first peer create a blockchain for the whole network
        if not bootstrap:
            print("first peer instantiate the whole net")
            self._memoryPool = []
            self._blockchain = Blockchain(self,difficulty)
            # Initialize the chain with the Genesis block.
            self._add_genesis_block()
        else:
        # Bootstrap the chain with the specified bootstrap address.
            print("start the boostraping")
            self._bootstrap(bootstrap) #address ??

    def _add_genesis_block(self):
            """Adds the genesis block to your blockchain."""
            b = Block(0,[],"0",0)
            b._address = self._address
            self._blockchain._blocks.append(b)
            self._ready = True

    def _bootstrap(self, address):
            """Implements the bootstrapping procedure."""
            try:
                response = requests.get(f'http://{address}/peers')
                if response.status_code == 200:
                    self._peers.append(address)
                    self._peers += response.json()
                    if self._address in self._peers:
                        self._peers.remove(self._address)
                else:
                    print("bootstrapping procedure cannot get peers")
                    return
                hashes = {}
                print('mes peers',self._peers)
                for peer in self._peers:
                    print("wesh")
                    response = requests.get(f'http://{peer}/addNewNode?address={self._address}')
                    print('"""""""""""',response.json())
                    hashes[peer] = response.json()
                print('out',hashes)
                #retrieve most commun hash in the network
                mostCommunHash = Counter(hashes.values()).most_common(1)[0][0]
                #retrieve a node with the most commun
                p = list(hashes.keys())[list(hashes.values()).index(mostCommunHash)]
                response = requests.get(f'http://{p}/keyChain')
                print(response.json())
                self._blockchain =Blockchain(self,blocks=response.json())
                response = requests.get(f'http://{p}/memoryPool')
                self._memoryPool = response.json()
                print(self._memoryPool)
                print(self._blockchain.rep())
                
            except Exception:
                print(Exception.__traceback__)
                print("impossible de contazcter le noeud maybee crash ?")
                exit(1)
    
    def put(self, key, value, block=True):
            """Puts the specified key and value on the Blockchain.

            The block flag indicates whether the call should block until the value
            has been put onto the blockchain, or if an error occurred.
            """
            """
            put(key, value): Stores the value with the associated key.
If a value for key already exists in the store, then a new version of the pair is created with the value value.
Please make note of the fact that the put operation doesn't necessarily delivers after it has been completed. It may therefore be a good idea to 
add a callback procedure (or a different mechanism) that is called whenever the key has been added to the system, or if a failure occurred.
            """

            transaction = Transaction(self._address, key, value)
            #Add dans pool
            self.add_transaction(transaction)
            #self._blockchain.add_transaction(self, transaction)
            callback = Callback(transaction, self._blockchain)
            if block:
                callback.wait()
            
            #self.mine()
            return callback
    
    def add_transaction(self, transaction):
            """Adds a transaction to your current list of transactions,
            and broadcasts it to your Blockchain network.

            If the `mine` method is called, it will collect the current list
            of transactions, and attempt to mine a block with those.
            """
            #met dans la pool
            self._memoryPool.append(transaction)
            #Broadcast
            

    def mine(self):
            """Implements the mining procedure."""
            candidate_block = Block(len(self._blockchain) + 1, self._memoryPool, self._blockchain.last_block.hash())
            #Y a pas besoin d'un header dans le block, hein ?
            self._memoryPool = []
            
            raise NotImplementedError

    def retrieve(self, key):
            """Searches the most recent value of the specified key.

            -> Search the list of blocks in reverse order for the specified key,
            or implement some indexing schemes if you would like to do something
            more efficient.
            """
            raise NotImplementedError

    def retrieve_all(self, key):
        """Retrieves all values associated with the specified key on the
        complete blockchain.
        """
        raise NotImplementedError
    
    def alive():
        pass


class Callback:
    def __init__(self, transaction, blockchain):
        self._transaction = transaction
        self._blockchain = blockchain

    def wait(self):
        """Wait until the transaction appears in the blockchain."""
        while True:
            if self.completed():
                break

    def completed(self):
        """Polls the blockchain to check if the data is available."""
        for block in self.blockchain.blocks:
            if block.contains(self._transaction):
                return True
        return False

if __name__ == "__main__":
    p = Peer(f'localhost:{5000}',False,difficulty=5)
    
    print(p._blockchain.rep())