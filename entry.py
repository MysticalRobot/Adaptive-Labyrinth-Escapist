class Key:
    def __init__(self, k1, k2):
        self.k1 = k1
        self.k2 = k2

    def __lt__(self, other):
        if (self.k1 < other.k1):
            return True
        elif (self.k1 == other.k1 and self.k2 <= other.k2):
            return True
        else:
            return False
        
    def __eq__(self, other):
        return self.k1 == other.k1 and self.k2 == other.k2
        
    def __str__(self):
        return f'({self.k1}, {self.k2})'
    
    def __repr__(self):
        return str(self)

class Entry:
    def __init__(self, s, key : Key):
        self.s = s
        self.key = key

    def __lt__(self, other):
        self.key < other.key

    def __eq__(self, other):
        return self.s == other.s
    
    def __str__(self):
        return f'[{self.s}, {self.key}]'
    
    def __repr__(self):
        return str(self)