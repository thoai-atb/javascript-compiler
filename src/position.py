class Position:
    def __init__ (self, idx, ln, col, file_name, file_txt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.file_name = file_name
        self.file_txt = file_txt
    
    def advance (self, current_char=None):
        self.idx += 1
        self.col += 1
        if current_char == '\n':
            self.ln += 1
            self.col = 0
        return self
    
    def copy(self):
        return Position(self.idx, self.ln, self.col, self.file_name, self.file_txt)