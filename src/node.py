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
    def __init__ (self, var_name_token, expr_node):
        self.var_name_token = var_name_token
        self.expr_node = expr_node
        self.pos_start = var_name_token.pos_start
        self.pos_end = expr_node.pos_end
    
    def __repr__ (self):
        return f'{self.var_token} = ({self.expr_node})'

class VarDeclarationNode:
    def __init__ (self, var_name_token, expr_node=None):
        self.var_name_token = var_name_token
        self.expr_node = expr_node
        self.pos_start = var_name_token.pos_start
        self.pos_end = expr_node.pos_end if expr_node else var_name_token.pos_end

    def __repr__ (self):
        if self.expr_node:
            return f'{self.var_token} = ({self.expr_node})'
        return f'{self.var_token}'

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

class StatementListNode:
    def __init__ (self, node_list):
        self.list = node_list
        self.pos_start = self.list[0].pos_start
        self.pos_end = self.list[-1].pos_end
    
    def __repr__ (self):
        return self.list

class IfNode:
    def __init__(self, expr_node, stmt):
        self.expr_node = expr_node
        self.stmt = stmt
        self.pos_start = expr_node.pos_start
        self.pos_end = stmt.pos_end
        

    def __repr__(self):
        return f'({self.expr_node}, {self.stmt})'  

class IfElseNode:
    def __init__(self, expr_node, stmt1, stmt2):
        self.expr_node = expr_node
        self.stmt1 = stmt1
        self.stmt2 = stmt2
        self.pos_start = expr_node.pos_start
        self.pos_end = stmt2.pos_end
        

    def __repr__(self):
        return f'({self.expr_node}, {self.stmt1}, {self.stmt2})'  