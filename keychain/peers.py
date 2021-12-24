from keychain import Block
from keychain import Transaction
from keychain import Blockchain
import time
import requests
from collections import Counter

class Peer:
    def __init__(self, address,miner,bootstrap=None,difficulty=None):
        
        self._address = address
        self._miner = miner
        self._memoryPool = None
        self._peers = None
        self._blockchain = None
        self._ready = False
        #if first peer create a blockchain for the whole network
        if not bootstrap:
            self._memoryPool = []
            self._peers = []
            self._blockchain = Blockchain(self,difficulty)
            # Initialize the chain with the Genesis block.
            self._add_genesis_block()
        else:
        # Bootstrap the chain with the specified bootstrap address.
            self._bootstrap(bootstrap)

    def _add_genesis_block(self):
            """Adds the genesis block to your blockchain."""
            b = Block(0,[],"0",timestamp=time.asctime())
            self._blockchain._blocks.append(b)
            self._ready = True

    def _bootstrap(self, address):
            """Implements the bootstrapping procedure."""
            try:
                response = requests.get(f'http://{address}/peers')
                if response.status_code == 200:
                    self._peers = response.json()
                else:
                    print("bootstrapping procedure cannot get peers")
                    return
                hashes = {}
                for peer in self._peers:
                    response = requests.get(f'http://{peer}/addNewNode?address={self._address}')
                    hashes['peer'] = response.json()['last_hash']
                
                #retrieve most commun hash in the network
                mostCommunHash = Counter(hashes.values()).most_common(1)[0][0]
                #retrieve a node with the most commun
                p = list(hashes.keys())[list(hashes.values()).index(mostCommunHash)]
                response = requests.get(f'http://{p}/keyChain')
                self._blockchain =Blockchain(self,blocks=response.json())
                response = requests.get(f'http://{p}/meoryPool')
                self._memoryPool = response.json()
                
            except Exception:
                print("impossible de contazcter le noeud maybee crash ?")
            raise NotImplementedError
    
    def put(self, key, value, block=True):
            """Puts the specified key and value on the Blockchain.

            The block flag indicates whether the call should block until the value
            has been put onto the blockchain, or if an error occurred.
            """

            transaction = Transaction(...)
            self._blockchain.add_transaction(self, transaction)
            callback = Callback(transaction, self._blockchain)
            if block:
                callback.wait()

            return callback
    
    def add_transaction(self, transaction):
            """Adds a transaction to your current list of transactions,
            and broadcasts it to your Blockchain network.

            If the `mine` method is called, it will collect the current list
            of transactions, and attempt to mine a block with those.
            """
            

    def mine(self):
            """Implements the mining procedure."""
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
    def __init__(self, transaction, chain):
        self._transaction = transaction
        self._chain = chain

    def wait(self):
        """Wait until the transaction appears in the blockchain."""
        raise NotImplementedError

    def completed(self):
        """Polls the blockchain to check if the data is available."""
        raise NotImplementedError