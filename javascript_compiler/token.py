TT_IDENTIFIER = 'IDENTIFIER'
TT_KEYWORD = 'KEYWORD'

TT_INT = 'INT'
TT_FLOAT = 'FLOAT'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_POWER = 'POWER'
TT_EQUAL = 'EQUAL'

TT_EE = 'EE'
TT_NE = 'NE'
TT_LT = 'LT'
TT_GT = 'GT'
TT_LTE = 'LTE'
TT_GTE = 'GTE'

TT_AND = 'AND'
TT_OR = 'OR'
TT_NOT = 'NOT'

TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'

TT_EOF = 'EOF'

KEYWORDS = [
    'var'
]


class Token:
    def __init__ (self, _type, value=None, pos_start=None, pos_end=None):
        self.type = _type
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()
        
        if pos_end:
            self.pos_end = pos_end.copy()
    
    def __repr__ (self):
        if self.value:
            return f'{self.type}: {self.value}'
        return f'{self.type}'

    def matches (self, _type, value):
        return self.type == _type and self.value == value