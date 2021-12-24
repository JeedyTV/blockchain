import time

class Block:
    
    def __init__(self, index, transactions,previous_hash,timestamp=time.asctime()):
        self._index = index
        self._transactions = transactions
        self._previous_hash = previous_hash
        self._timestamp = timestamp
        self._proof = None
        
    def get_proof(self):
        """Return the proof of the current block."""
        return self._proof

    def get_transactions(self):
        """Returns the list of transactions associated with this block."""
        return self._transactions

    def contains(self, transaction):
        """Returns a boolean expressing wether or not the transaction is contained in the block."""

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
        
    def difficulty(self):
        """Returns the difficulty level."""
        return self._difficulty

    def is_valid(self):
        """Checks if the current state of the blockchain is valid.

        Meaning, are the sequence of hashes, and the proofs of the
        blocks correct?
        """
        raise NotImplementedError
    
    def psdinspi(self):
        #en gros gere le consensuc extend la chain avec le bon blok en fct du suivant et readd les transtion au peers
        raise NotImplementedError
    
    def _copy(self):
        #cree l'objet block chain with a rep dic
        pass

    
