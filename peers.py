import time
import requests
from collections import Counter
from requests.models import requote_uri
from blockchain import Block,Blockchain
from transaction import Transaction
from threading import Timer,Thread,Event
import json

class Peer:
    
    def __init__(self, address,miner,bootstrap=None,difficulty=None):
        
        self.address = address
        self.miner = miner
        self.mining = miner
        self.memoryPool = []
        self.peers = []
        self.blockchain = None
        self.ready = False
        self.peers_heartbeat = []
        self.heartbeat_count = {}
        self.transactions_historic = []

        #if first peer create a blockchain for the whole network
        if not bootstrap:
            print("first peer instantiate the whole net")
            # Initialize the chain with the Genesis block.
            b = Block(0,self.address,[],"0",time.asctime())
            self.blockchain = Blockchain(self,difficulty,b)
            self.ready = True
        else:
        # Bootstrap the chain with the specified bootstrap address.
            print("start the boostraping")
            self.bootstrapProc(bootstrap) #address ??
        
        t = perpetualTimer(3,self.heartbeat)
        t.start()

    def bootstrapProc(self, address):
            """Implements the bootstrapping procedure."""
            try:
                response = requests.get(f'http://{address}/peers')
                if response.status_code == 200:
                    self.peers.append(address)
                    self.peers += response.json()
                    if self.address in self.peers:
                        self.peers.remove(self.address)
                else:
                    print("bootstrapping procedure cannot get peers")
                    return
                
                chain_sizes = {}
                for peer in self.peers:
                    response = requests.get(f'http://{peer}/addNewNode?address={self.address}')
                    chain_sizes[peer] = response.json()

                #retrieve longest chain size in the network
                longestSize = max(chain_sizes.values())
                #retrieve a node with the longest chain size
                p = list(chain_sizes.keys())[list(chain_sizes.values()).index(longestSize)]
                #ask key chain to that node
                response = requests.get(f'http://{p}/keyChain')
                self.blockchain = Blockchain(self,response.json())
                #ask memoryPool to that node
                response = requests.get(f'http://{p}/memoryPool')
                for t in json.loads(response.json()):
                    self.memoryPool.append(Transaction(str(t).replace('\'','\"')))
                print(self.memoryPool)
                print(self.blockchain)
                self.ready = True
                
            except Exception as e:
                print("impossible de contazcter le noeud maybee crash ?")
                print(e)
                exit(1)

    def put(self, key, value, time,block=True):
            """Puts the specified key and value on the Blockchain.
            The block flag indicates whether the call should block until the value
            has been put onto the blockchain, or if an error occurred.
            """
            transaction = Transaction(self.address, key, value,time)
            #Add dans pool
            self.add_transaction(transaction)
            
            if block:
                callback = Callback(transaction, self.blockchain)
                callback.wait()
                mess = f'({key},{value} added to the store at index {callback.index} at {callback.time})'
                print(mess)
                return
            mess = f'({key},{value} will be eventually added to the store)'
            print(mess)
            return

    def add_transaction(self, transaction):
            """Adds a transaction to your current list of transactions,
            and broadcasts it to your Blockchain network.
            If the `mine` method is called, it will collect the current list
            of transactions, and attempt to mine a block with those.
            """
            #met dans la pool
            if transaction not in self.memoryPool and transaction not in self.transactions_historic:
                self.memoryPool.append(transaction)
                self.transactions_historic.append(transaction)
                self.broadcastTrans(transaction)
            else:
                print("++++++++++++++++++++++++ DISCARD TRANS")
            #Broadcast
    
    def handle_memoryPool(self, block):

        return_memoryPool = self.memoryPool.copy()
        for t in block.transactions:
            
            for t_mp in self.memoryPool: 
                if t.key == t_mp.key and t.value == t_mp.value \
                    and t.timestamp == t_mp.timestamp:
                    return_memoryPool.remove(t_mp)

        self.memoryPool = return_memoryPool.copy()



        
    
    def broadcastTrans(self,transaction):
        
        for peer in self.peers:
            try:
                requests.get(f'http://{peer}/addTransaction?transaction={str(transaction)}')
            
            except Exception:
                pass

    def broadcastBlock(self,block):
        
        for peer in self.peers:
            try:
                requests.get(f'http://{peer}/addNewBlock?block={str(block)}')

            except Exception:
                pass

    def add_block (self, block):
        #doit gerer ds autres node les transaction aussi 
        self.mining = False
        self.handle_memoryPool(block)
        print(f"Length memory pool:{len(self.memoryPool)}")
        
        if block not in self.blockchain.blocks:
                if(self.blockchain.add_block(block)):
                    self.broadcastBlock(block)
        else:
            print("++++++++++++++++++++++++ DISCARD BLOCK")
            #Broadcast
        
        print(" -- AFTER ADDING A BLOCK, THE BLOCKCHAIN IS : -- ")
        print(" ")
        print(self.blockchain)
        print(" ")
        self.mining = True

       
    def mine(self):
        """Implements the mining procedure."""

        if not self.miner:
            return False
        a, b, c = self.mining, self.memoryPool == [], self.ready
        #if not self.mining or self.memoryPool == [] or not self.ready:
        print("Valeur de la fonction f:" + str(c and (not a or b)))
        print("Valeur de a,b,c:")
        print(a,b,c)
        if c and (not a or b):
            time.sleep(2)
            print("wait trans in pool...")
            return self.mine()
        print(" ")
        print("------------------")
        print("-- Start mining...")
        print(f"Length self.memoryPool: {len(self.memoryPool)}")
        #print(f"On start mining vu les valeurs de a,b,c")

        candidate_block = Block(len(self.blockchain.blocks),self.address,self.memoryPool, self.blockchain.last_block._hash,time.asctime())
        #print("En train de Compute hash of candidate block and checks if below target")
        #Computes hash of candidate block and checks if it is below target.
        print("Difficulty=" + str(self.blockchain.difficulty))
        while True:
            if self.mining:
                #print("self.mining est True")
                hash = candidate_block._hash
                if hash.startswith('0' * self.blockchain.difficulty):
                    print("Trouvé below target !!!!!!!!!")

                    self.blockchain.add_block(candidate_block)
                    self.handle_memoryPool(candidate_block)
                    print("Length memory pool:")
                    print(len(self.memoryPool))
                    #print("On s'apprête à broadcast")
                    #Broadcast
                    for peer in self.peers:
                        try:
                            print("Broadcast à peer " + peer)
                            requests.get(f'http://{peer}/addNewBlock?block={str(candidate_block)}')
                
                        except Exception as e:
                            print(e)
                    print(self.blockchain)
                    print("-- End mining")
                    print("-------------")
                    print(" ")

                    return self.mine()
            
                candidate_block.nonce += 1
            else:
                print("self.mining est False du coup on return self.mine()")
                return self.mine()
            
    def retrieve(self, key):
            """Searches the most recent value of the specified key.

            -> Search the list of blocks in reverse order for the specified key,
            or implement some indexing schemes if you would like to do something
            more efficient.
            """
            latest_value = None
            for b in self.blockchain.blocks:
                for t in b.transactions:
                    if(t.key == key):
                        latest_value = (t.value,t.origin,t.timestamp)

            if latest_value != None:
                print("Latest value for the key : "+key)
                print(latest_value)

            return latest_value

    def retrieve_all(self, key):
        """Retrieves all values associated with the specified key on the
        complete blockchain.
        """
        values = []

        for b in self.blockchain.blocks:
            for t in b.transactions:
                    if(t.key == key):
                        values.append((t.value,t.origin,t.timestamp))

        if values != []:
            print("Values for the key : "+key)
            print(values)

        return values
 
    def heartbeat(self, removed):
        try:
            if not removed:
                #print("-- <3 HEARTBEAT MEASUREMENT <3 --")
                self.peers_heartbeat = self.peers.copy()
            
            #print(self.peers) 
            #print(self.peers_heartbeat)
            #print(self.heartbeat_count)
            #print(" ")
            for peer in self.peers_heartbeat:
                current_peer = peer
                requests.get(f'http://{peer}/heartbeat')
                self.heartbeat_count[peer] = 0

            
        except Exception:
            #print('A peer doesn\'t respond')

            self.peers_heartbeat.remove(current_peer)
            self.heartbeat_count[current_peer] += 1

            if self.heartbeat_count[current_peer] == 10:
                self.peers.remove(current_peer)
                del self.heartbeat_count[current_peer]

            self.heartbeat(1)

    def __str__(self) -> str:
        return f'\"{self.address}\"'
        
    def __repr__(self) -> str:
        return f'\"{self.address}\"'
     
#callback = Callback(transaction, self._blockchain)
class Callback:#retiens que cette transaction a été ajoutée
    #called whenever the key has been added to the system, or if a failure occurred.
    """
    quand tu prends une transaction et tu la put, elle est mise dans la pool
    callback attend jusque la transaction soit mise sur la chaîne
    """
    def __init__(self, transaction, blockchain):
        self.transaction = transaction
        self.blockchain = blockchain

    def wait(self):
        """Wait until the transaction appears in the blockchain."""
        #appelle infiniment quand est-ce que la transaction est
        while True:
            if self.completed():
                return True

    def completed(self):
        """Polls the blockchain to check if the data is available."""
        for block in self.blockchain.blocks:
            if block.contains(self.transaction):
                self.time = block.timestamp
                self.index = block.index
                return True
        return False

class perpetualTimer():

   def __init__(self,t,hFunction):
      self.t=t
      self.hFunction = hFunction
      self.thread = Timer(self.t,self.handle_function)
      self.thread.daemon = True

   def handle_function(self):
      self.hFunction(0)
      self.thread = Timer(self.t,self.handle_function)
      self.thread.start()

   def start(self):
      self.thread.start()

   def cancel(self):
      self.thread.cancel()



if __name__ == "__main__":
    p = Peer(f'localhost:{5000}',False,difficulty=5)
    
    print(p.blockchain)