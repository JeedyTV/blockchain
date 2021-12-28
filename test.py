class B:
    def __init__(self):
        self.l = [4,5,6]
    def __len__(self):
        return len(self.l)

    def __eq__(self, __o: object) -> bool:
        return self.l == __o.l
    #def __hash__(self):
        #return hash(self.__repr__())

a = B()
print(len(a))
"""
s = set()
s.add(a)
print(s)
print(a in s)

d = B()
print(d in s)
"""
z = list()
z.append(a)
print(a in z)