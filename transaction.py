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
            'origin': self._origin,
            'key': self._key,
            'value': self._value,
            'timestamp': self._timestamp
        }
        return d
    
    def __str__(self) -> str:
        
        return str(self.rep())
    
    def __eq__(self, __o: object) -> bool:
        
        if self._origin == __o._origin and self._key == __o._key and self._value ==__o._value and self._timestamp == __o._timestamp:
           return True
        else:
            return False
            