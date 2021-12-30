import json

class Transaction(dict):
    
    def __init__(self,*args):
        """A transaction, in our KV setting. A transaction typically involves
        some key, value and an origin (the one who put it onto the storage).
        Args:
        origin ([string]): [description]
        key ([string]): [description]
        value ([string]): [description]
        timestamp ([string], optional): [description]. Defaults to time.asctime().
        """
        if len(args)==4:
            self.origin = args[0] #adress of the peer
            self.key = args[1]
            self.value = args[2]
            self.timestamp = args[3]
            dict.__init__(self,origin=args[0],key=args[1],value=args[2],timestamp=args[3])
        elif len(args)==1:
            t = json.loads(args[0])
            self.origin = t['origin'] #adress of the peer
            self.key = t['key']
            self.value = t['value']
            self.timestamp = t['timestamp']
            dict.__init__(self,origin=t['origin'],key=t['key'],value=t['value'],timestamp=t['timestamp'])
    
    def __str__(self) -> str:
        return str(self.__dict__).replace('\'','\"')
    
    def __repr__(self) -> str:
        return str(self.__dict__).replace('\'','\"')
        
    def __eq__(self, __o: object) -> bool:
        
        if self.origin == __o.origin and self.key == __o.key \
            and self.value ==__o.value and self.timestamp == __o.timestamp:
           return True
        else:
            return False

if __name__ == '__main__':
    t = Transaction('l:500','ab','cd','mtn')
    print([t,t])
    s = '{"origin": "l:500", "key": "ab", "value": "cd", "timestamp": "mtn"}'
    t = Transaction(s)
    print([t,t])
    
