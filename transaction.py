import time
class Transaction:
    
    def __init__(self,origin,key,value,timestamp=time.asctime()):
        """A transaction, in our KV setting. A transaction typically involves
        some key, value and an origin (the one who put it onto the storage).
        """
        self._origin = origin #adress of the peer
        self._key = key
        self._value = value
        self._timestamp = timestamp

    def rep(self):
        d = {
            'origin': self.origin,
            'key': self._key,
            'value': self._value,
            'timestamp': self._timestamp
        }
        return d