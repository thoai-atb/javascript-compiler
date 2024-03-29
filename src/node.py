class ValueNode:
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
    def __init__ (self, var_name_token, equal_tok, expr_node):
        self.var_name_token = var_name_token
        self.equal_tok = equal_tok
        self.expr_node = expr_node
        self.pos_start = var_name_token.pos_start
        self.pos_end = expr_node.pos_end
    
    def __repr__ (self):
        return f'{self.var_name_token} = ({self.expr_node})'

class VarDeclarationNode:
    def __init__ (self, keyword_var, var_name_token, equal_tok, expr_node=None):
        self.keyword_var = keyword_var
        self.var_name_token = var_name_token
        self.equal_tok = equal_tok
        self.expr_node = expr_node
        self.pos_start = keyword_var.pos_start
        self.pos_end = expr_node.pos_end if expr_node else var_name_token.pos_end

    def __repr__ (self):
        if self.expr_node:
            return f'{self.var_name_token} = ({self.expr_node})'
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
    def __init__ (self, open_bracket, node_list, close_bracket):
        self.open_bracket = open_bracket
        self.list = node_list
        self.close_bracket = close_bracket
        if self.open_bracket and self.close_bracket:
            self.pos_start = self.open_bracket.pos_start
            self.pos_end = self.close_bracket.pos_end
        elif len(node_list) != 0:
            self.pos_start = self.list[0].pos_start
            self.pos_end = self.list[-1].pos_end
    
    def __repr__ (self):
        return self.list.__repr__()

class IfNode:
    def __init__(self, keyword_if, left_paren, expr_node, right_paren, stmt):
        self.keyword_if = keyword_if
        self.left_paren = left_paren
        self.expr_node = expr_node
        self.right_paren = right_paren
        self.stmt = stmt
        self.pos_start = keyword_if.pos_start
        self.pos_end = stmt.pos_end
        

    def __repr__(self):
        return f'IF({self.expr_node}, {self.stmt})'  

class IfElseNode:
    def __init__(self, keyword_if, left_paren, expr_node, right_paren, stmt1, keyword_else, stmt2):
        self.keyword_if = keyword_if
        self.left_paren = left_paren
        self.expr_node = expr_node
        self.right_paren = right_paren
        self.stmt1 = stmt1
        self.keyword_else = keyword_else
        self.stmt2 = stmt2
        self.pos_start = keyword_if.pos_start
        self.pos_end = stmt2.pos_end
        

    def __repr__(self):
        return f'IF_ELSE({self.expr_node}, {self.stmt1}, {self.stmt2})'  

class FuncDefNode:
    def __init__(self, func_tok, var_name_tok, left_paren, arg_name_toks, right_paren, body_node):
        self.func_tok = func_tok
        self.var_name_tok = var_name_tok
        self.left_paren = left_paren
        self.arg_name_toks = arg_name_toks
        self.right_paren = right_paren
        self.body_node = body_node

        if self.var_name_tok:
            self.pos_start = self.var_name_tok.pos_start
        elif len(self.arg_name_toks) > 0:
            self.pos_start = self.arg_name_toks[0].pos_start
        else:
            self.pos_start = self.body_node.pos_start

        self.pos_end = self.body_node.pos_end
    
    def __repr__(self):
        return f'FUNCTION <{self.var_name_tok}> ({self.arg_name_toks}) -> {self.body_node}'

class ReturnNode:
    def __init__(self, keyword_return, node_to_return):
        self.keyword_return = keyword_return
        self.node_to_return = node_to_return
        self.pos_start = keyword_return.pos_start
        self.pos_end = node_to_return.pos_end

    def __repr__(self):
        return f'RETURN({self.node_to_return})'

class FuncCallNode:
    def __init__(self, node_to_call, open_paren, arg_nodes, close_paren):
        self.node_to_call = node_to_call
        self.open_paren = open_paren
        self.arg_nodes = arg_nodes
        self.close_paren = close_paren

        self.pos_start = self.node_to_call.pos_start
        self.pos_end = self.close_paren.pos_end
        
    def __repr__(self):
        return f'CALL: {self.node_to_call} ({self.arg_nodes})'