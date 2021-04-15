class SymbolTable:
    def __init__ (self):
        self.parent = None
        self.symbols = {}

    def get(self, name):
        value = None
        if name in self.symbols:
            value = self.symbols[name]
        elif self.symbols and self.parent:
            value = self.parent.get(name)
        return value
    
    def set(self, name, value):
        self.symbols[name] = value
    
    def remove(self, name):
        del self.symbols[name]