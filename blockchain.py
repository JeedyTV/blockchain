"""
Blockchain (stub).
NB: Feel free to extend or modify.
"""
from hashlib import sha256
import json
import time

class Block:
    def __init__(self, id, transactions, previous_block, nonce):
        """Describe the properties of a block."""
        self.id = id
        self.transactions = transactions #list of transactions
        self.previous_block = previous_block #Hash pointer to the previous block
        self.nonce = nonce
    
    def hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        hash = sha256(block_string.encode()).hexdigest()
        self.proof = None
        return hash

    def proof(self):
        """Return the proof of the current block."""
        return self.nonce

    def transactions(self):
        """Returns the list of transactions associated with this block."""
        return self.transactions

    def contains(self, transaction):
        """Returns a boolean expressing wether or not the transaction is contained in the block."""
        return transaction in self.transactions


class Blockchain:
    def __init__(self, difficulty):
        """The bootstrap address serves as the initial entry point of
        the bootstrapping procedure. In principle it will contact the specified
        addres, download the peerlist, and start the bootstrapping procedure.
        """

        # Initialize the properties.
        self.blocks = []
        self.peers = []
        self.difficulty = difficulty

        # Initialize the chain with the Genesis block.
        self.add_genesis_block()

        #self.broadcast = Broadcast()
        self.broadcast = None
        self.new_transactions = []

    def last_block(self):
        return self.blocks[-1]
    
    def add_block(self, block):
        """Check if block is valid"""
        #Is previous hash the correct one ?
        if not block.previous_block == self.last_block.hash():
            return False
        #Is proof valid ?
        hash = block.hash()
        if not hash.startswith('0' * self.difficulty):
            return False
        self.blocks.append(block)
        return True

    def difficulty(self):
        """Returns the difficulty level."""
        return self.difficulty

    def is_valid(self):
        """Checks if the current state of the blockchain is valid.
        Meaning, are the sequence of hashes, and the proofs of the
        blocks correct?
        """
        raise NotImplementedError

    def psdinspi(self, block):
        #en gros gere le consensuc extend la chain avec le bon blok en fct du suivant et send les transactions au peers
    
        proof = self.pow(block)
        self.add_block(block, proof)
        self.new_transactions = []

        return True
    
    def pow(self, block):
        while True:
            hash = block.hash()
            if hash.startswith(self.difficulty * '0'):
                return hash
            block.nonce += 1

if __name__ == "__main__":
    #bc = Blockchain(0,0)
    b = Block(0,[],0)
    print(b.__dict__)
    print(b.hash())
    print(b.__dict__)
    print(b.hash())