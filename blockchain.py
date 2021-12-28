from hashlib import sha256
import json
from transaction import Transaction

class Block(dict):
    
    def __init__(self,*args):
        """[summary]
        Args:
            index ([int]): [description]
            address ([string]) : [description]
            transactions ([Transaction]): [description]
            previous_hash ([string]): [description]
            timestamp ([type]): [description]
        """
        if len(args)==5: 
            self.index = args[0]
            self.address = args[1]
            self.transactions = args[2] #list of transactions
            self.previous_hash = args[3] #Hash pointer to the previous block
            self.timestamp = args[4]
            self.nonce = 0
            dict.__init__(self,index=args[0],address=args[1],transactions=args[2],\
                previous_hash=args[3],timestamp=args[4],nonce=0)
        elif len(args)==1:
            b = json.loads(args[0])
            self.index = b['index']
            self.address = b['address']
            transactions = []
            for t in b['transactions']:
                transactions.append(Transaction(str(t).replace('\'','\"')))
            self.transactions = transactions #list of transactions
            self.previous_hash = b['previous_hash'] #Hash pointer to the previous block
            self.timestamp = b['timestamp']
            self.nonce = b['nonce']
            dict.__init__(self,index=b['index'],address=b['address'],transactions=transactions,\
                previous_hash=b['previous_hash'],timestamp=b['timestamp'],nonce=b['nonce'])

    @property
    def _hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        hash = sha256(block_string.encode()).hexdigest()
        return hash
    
    def get_transactions(self):
        """Returns the list of transactions associated with this block."""
        return self._transactions

    def contains(self, transaction):
        """Returns a boolean expressing wether or not the transaction is contained in the block."""
        return transaction in self.transactions
    
    def __str__(self) -> str:
        return str(self.__dict__).replace('\'','\"')
        
    def __repr__(self) -> str:
        return str(self.__dict__).replace('\'','\"')
    
    def __eq__(self, __o: object) -> bool:
        
        if self.index == __o.index and self.transactions == __o.transactions and \
            self.previous_hash ==__o.previous_hash and self.timestamp == __o.timestamp \
            and self.address == __o.address and self.nonce == __o.nonce:
           return True
        else:
            return False

class Blockchain:

    def __init__(self,*args):
        """[summary]
        Args:
            peer ([string]): [description]
            difficulty ([int]): [description]
            blocks ([Block], optional): [description]. Defaults to None.
        """
        if len(args)==3:
            self.peer = args[0]
            self.difficulty = args[1]
            self.blocks = [args[2]]
        elif len(args)==2:
            c = json.loads(args[1])
            self.peer = args[0]
            self.difficulty = c['difficulty']
            self.blocks = []
            for b in c['blocks']:
                self.blocks.append(Block(str(b).replace('\'','\"')))
        
        #self._pasdinspi = [] #contents blocks mined at the same times
    
    def __len__(self):
        return len(self.blocks)

    @property
    def last_block(self):
        return self.blocks[-1]

    def add_block(self, block):
        """Check if block is valid"""
        print("Entré dans blockchain.add_block")
        print("Length memory pool:")
        print(len(self.peer.memoryPool))
        #Is previous hash the correct one ?
        if not block.previous_hash == self.last_block._hash:
            return False
        #Is proof valid ?
        if not block._hash.startswith('0' * self.difficulty):
            return False
        self.blocks.append(block)
        return True

    def is_valid(self):
        """Checks if the current state of the blockchain is valid.

        Meaning, are the sequence of hashes, and the proofs of the
        blocks correct?
        """
        raise NotImplementedError
    
    def psdinspi(self):
        #en gros gere le consensuc extend la chain avec le bon blok en fct du suivant et readd les transtion au peers
        raise NotImplementedError
    
    def __repr__(self) -> str:
        return str(self.__dict__).replace('\'','\"')
        
    def __str__(self) -> str:
        return str(self.__dict__).replace('\'','\"')

if __name__ == "__main__":
    t = Transaction('l:500','ab','cd','mtn')
    b = Block(0,'l:5000',[t,t],"0","mtn")
    print([b,b])
    print(b._hash)
    s = '''{
        "index": 0,
        "address": "l:5000",
        "transactions":
            [
                {
                "origin": "l:500",
                "key": "ab",
                "value": "cd",
                "timestamp": "mtn"
                }, 
                {"origin": "l:500",
                "key": "ab",
                "value": "cd",
                "timestamp": "mtn"
                }
            ],
        "previous_hash": "0",
        "timestamp": "mtn",
        "nonce": 0
        }'''
    b = Block(s)
    print([b,b])
    print(b._hash)
    print("##############################")
    c = Blockchain('l:23',5,b)
    c.blocks.append(b)
    print(c)
    c = Blockchain("l:12",str(c))
    print(c)
    


    
