from .position import * 
from .constant import *
from .token import *
from .error import *

class Lexer:
    def __init__ (self, file_name, text):
        self.file_name = file_name
        self.text = text
        self.pos = Position(-1, 0, -1, file_name, text)
        self.current_char = None
        self.advance()

    def advance (self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def make_tokens (self):
        tokens = []
        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in LETTERS:
                tokens.append(self.make_identifier())
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char == '"' or self.current_char == "'":
                if(self.current_char == "'"):
                    token, error = self.make_string("single")
                    if error: return [], error
                    tokens.append(token)
                if(self.current_char == '"'):
                    token, error = self.make_string("double")
                    if error: return [], error
                    tokens.append(token)
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL, pos_start=self.pos))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV, pos_start=self.pos))
                self.advance()
            elif self.current_char == '^':
                tokens.append(Token(TT_POWER, pos_start=self.pos))
                self.advance()
            elif self.current_char == '=':
                tokens.append(self.make_equals())
            elif self.current_char == '<':
                tokens.append(self.make_less_than())
            elif self.current_char == '>':
                tokens.append(self.make_greater_than())
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == '{':
                tokens.append(Token(TT_LCURLY, pos_start=self.pos))
                self.advance()
            elif self.current_char == '}':
                tokens.append(Token(TT_RCURLY, pos_start=self.pos))
                self.advance()
            elif self.current_char == '!':
                token, error = self.make_not()
                if error: return [], error
                tokens.append(token)
            elif self.current_char == '&':
                token, error = self.make_and()
                if error: return [], error
                tokens.append(token)
            elif self.current_char == '|':
                token, error = self.make_or()
                if error: return [], error
                tokens.append(token)
            elif self.current_char == ',':
                tokens.append(Token(TT_COMMA, pos_start=self.pos))
                self.advance()
            elif self.current_char == '\n':
                tokens.append(Token(TT_EOL, pos_start=self.pos))
                self.advance()
            else:
                char = self.current_char
                pos_start = self.pos.copy()
                self.advance()
                return [], IllegalCharError(pos_start, self.pos.copy(), "'" + char + "'")
        tokens.append(Token(TT_EOF, pos_start=self.pos))
        return tokens, None

    def make_number (self):
        num_str = ''
        dot_count = 0
        pos_start = self.pos.copy()
        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1:
                    break
                num_str += self.current_char
                dot_count += 1
            else:
                num_str += self.current_char
            self.advance()
        if dot_count == 1:
            return Token(TT_FLOAT, float(num_str), pos_start, self.pos)
        return Token(TT_INT, int(num_str), pos_start, self.pos)
    
    def make_string(self,quote_type):
        string = ""
        pos_start = self.pos.copy()
        
        self.advance()    

        escape_characters = {
            'n': '\n',
            't': '\t',
            '"' : "\"" if quote_type == "double" else '"',
            "'" : '\''if quote_type == "single" else "'"
        }

        escape_character = False
        escape_character_count = 0

        while self.current_char != None and (((self.current_char != "'" and quote_type == "single") or (self.current_char != '"' and quote_type == "double")) or escape_character):
            if(escape_character):
                if(self.current_char == "\\"):
                    string += "\\"
                else:
                    string += escape_characters.get(self.current_char)
                escape_character = False
            else:
                if self.current_char == '\\':
                    escape_character = True
                else:
                    string += self.current_char
            self.advance()
            pos_end = self.pos.copy()
        
        if(self.current_char == "'" and quote_type == "single") or (self.current_char == '"' and quote_type == "double"):
            self.advance()
            return(Token(TT_STRING,string,pos_start,self.pos.copy()),None)
        self.advance()
        return [], ExpectedCharError(pos_end, self.pos.copy(), "' expected at end the string" if quote_type == "single" else '" expected at end the string')
        

    def make_identifier (self):
        id_str = ''
        pos_start = self.pos.copy()
        while self.current_char != None and self.current_char in LETTERS_DIGITS + '_':
            id_str += self.current_char
            self.advance()
        if id_str in KEYWORDS:
            return Token(TT_KEYWORD, id_str, pos_start, self.pos.copy())
        return Token(TT_IDENTIFIER, id_str, pos_start, self.pos.copy())
    
    def make_not (self):
        pos_start = self.pos.copy()
        self.advance()
        if self.current_char == '=':
            self.advance()
            return Token(TT_NE, pos_start=pos_start, pos_end=self.pos.copy()), None
        return Token(TT_NOT, pos_start=pos_start, pos_end=self.pos.copy()), None
    
    def make_equals (self):
        pos_start = self.pos.copy()
        token_type = TT_EQUAL
        self.advance()
        if self.current_char == '=':
            self.advance()
            token_type = TT_EE
        return Token(token_type, pos_start=pos_start, pos_end=self.pos.copy())

    def make_less_than (self):
        pos_start = self.pos.copy()
        token_type = TT_LT
        self.advance()
        if self.current_char == '=':
            self.advance()
            token_type = TT_LTE
        return Token(token_type, pos_start=pos_start, pos_end=self.pos.copy())

    def make_greater_than (self):
        pos_start = self.pos.copy()
        token_type = TT_GT
        self.advance()
        if self.current_char == '=':
            self.advance()
            token_type = TT_GTE
        return Token(token_type, pos_start=pos_start, pos_end=self.pos.copy())
    
    def make_and (self):
        pos_start = self.pos.copy()
        self.advance()
        pos_mid = self.pos.copy()
        if self.current_char == '&':
            self.advance()
            return Token(TT_AND, pos_start=pos_start, pos_end=self.pos.copy()), None
        self.advance()
         
    
    def make_or (self):
        pos_start = self.pos.copy()
        self.advance()
        pos_mid = self.pos.copy()
        if self.current_char == '|':
            self.advance()
            return Token(TT_OR, pos_start=pos_start, pos_end=self.pos.copy()), None
        self.advance()
        return [], ExpectedCharError(pos_mid, self.pos.copy(), "'|' (after '|')")