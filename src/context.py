from src.symbol_table import SymbolTable


class Context:
    def __init__(self, display_name, parent=None, parent_entry_pos=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table = None
        self.children = []

    def __repr__(self):
        return f'Context[name = {self.display_name}, depth = {self.get_depth()}]'
    
    def get_depth(self):
        count = 0
        current = self.parent
        while current:
            current = current.parent
            count += 1
        return count

    def log(self):
        log = f'Symbol Table for {self}:\n'
        log += str(self.symbol_table)
        for c in self.children:
            log += '\n' + c.log()
        return log
            
        

        
