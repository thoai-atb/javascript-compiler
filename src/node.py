class NumberNode:
    def __init__ (self, token):
        self.token = token
        self.pos_start = token.pos_start
        self.pos_end = token.pos_end
    
    def __repr__ (self):
        return f'{self.token}'

class VarAccessNode:
    def __init__ (self, token):
        self.token = token
        self.pos_start = token.pos_start
        self.pos_end = token.pos_end

    def __repr__ (self):
        return f'{self.token}'

class VarAssignNode:
    def __init__ (self, var_token, expr_token):
        self.var_token = var_token
        self.expr_token = expr_token
        self.pos_start = var_token.pos_start
        self.pos_end = expr_token.pos_end
    
    def __repr__ (self):
        return f'{self.var_token} = ({self.expr_token})'

class BinOpNode:
    def __init__ (self, left_node, token, right_node):
        self.left_node = left_node
        self.token = token
        self.right_node = right_node
        self.pos_start = left_node.pos_start
        self.pos_end = right_node.pos_end
    
    def __repr__ (self):
        return f'({self.left_node}, {self.token}, {self.right_node})'

class UnaryOpNode:
    def __init__ (self, token, node):
        self.token = token
        self.node = node
        self.pos_start = token.pos_start
        self.pos_end = node.pos_end
    
    def __repr__ (self):
        return f'({self.token}, {self.node})'