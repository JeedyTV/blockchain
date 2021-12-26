from hashlib import sha256
import json
import time
from transaction import Transaction

class Block:
    
    def __init__(self, index, transactions,previous_hash,nonce=None,timestamp=time.asctime()):
        self._index = index
        self._transactions = transactions #list of transactions
        self._previous_hash = previous_hash #Hash pointer to the previous block
        self._timestamp = timestamp
        self._address = None
        self._nonce = nonce
    
    def hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        hash = sha256(block_string.encode()).hexdigest()
        return hash
    
    @property
    def _proof(self):
        """Return the proof of the current block."""
        return self.hash()

    def get_transactions(self):
        """Returns the list of transactions associated with this block."""
        return self._transactions

    def contains(self, transaction):
        """Returns a boolean expressing wether or not the transaction is contained in the block."""
        return transaction in self.transactions
    
    def rep(self):
        
        d = {
        'address': self._address,
        'index': self._index,
        'transactions': self.rep_transactions(),
        'proof':self._proof,
        'previous_hash': self._previous_hash,
        'timestamp': self._timestamp,
        'nonce': self._nonce
        }
        return d
    
    def rep_transactions(self):
        l = []
        for i in self._transactions:
            l.append(i.rep())
        return l


class Blockchain:

    def __init__(self,peer,difficulty=None,blocks=None):
        
        self._difficulty = difficulty
        self._blocks = None
        if blocks:
            #create from the dictionnary of bootstrap procedure
            self._copy(blocks)
        else:
            self._blocks = []
        
        self._pasdinspi = [] #contents blocks mined at the same times
        self._peer = peer
    @property
    def last_block(self):
        return self._blocks[-1]
    
    def difficulty(self):
        """Returns the difficulty level."""
        return self._difficulty

    def add_block(self, block):
        """Check if block is valid"""
        #Is previous hash the correct one ?
        #rajouter cas ou pluseir block mine en meme temps
        if not block.previous_block == self.last_block.hash():
            return False
        #Is proof valid ?
        hash = block.hash()
        if not hash.startswith('0' * self.difficulty):
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
    
    def _copy(self,rep):
        #cree l'objet block chain with a rep dic
        self._difficulty = int(rep['difficulty'])
        self._blocks = []
        for i in rep['keychain']:
            id = i['index']
            add = i['address']
            transactions = []
            for j in i['transactions']:
                o = j['origin']
                k = j['key']
                v = j['value']
                ts = j['timestamp']
                t = Transaction(o,k,v,ts)
                transactions.append(t)
            phash = i['previous_hash']
            n = i['nonce']
            tss = i['timestamp']
            b = Block(id,transactions,phash,n,tss)
            b._address = i['address']
            self._blocks.append(b)
    
    def rep(self):
        l = []
        for i in self._blocks:
            l.append(i.rep())
        d = {
            'difficulty': self._difficulty,
            'keychain': l
        }
        return d


if __name__ == "__main__":
    #bc = Blockchain(0,0)
    b = Block(0,[],"0")
    print(b.rep())
    
