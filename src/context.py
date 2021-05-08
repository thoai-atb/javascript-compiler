class Context:
    def __init__ (self, display_name, parent=None, parent_entry_pos=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table = None
    
    def get_depth(self):
        count = 0
        current = self.parent
        while current:
            current = current.parent
            count += 1
        return count