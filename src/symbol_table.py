class SymbolTable:
    def __init__ (self, parent=None):
        self.parent = parent
        self.symbols = {}

    def has_local(self, name):
        return name in self.symbols

    def has(self, name):
        return self.get(name) != None

    def get(self, name):
        value = None
        if name in self.symbols:
            value = self.symbols[name]
        elif self.parent:
            value = self.parent.get(name)
        return value

    def set_declar(self, name, value):
        self.symbols[name] = value
    
    def set_assign(self, name, value):
        if self.has_local(name):
            self.symbols[name] = value
        elif self.parent:
            self.parent.set_assign(name, value)
        else:
            raise Exception(f'attempt assigning value {value} to undeclared variable {name}')
    
    def remove(self, name):
        del self.symbols[name]

    def __repr__(self):
        rep = ""
        for keys in self.symbols:
            rep += f'\t{keys} : {self.symbols[keys]}\n'
        return rep