from .token import *
from .node import *
from .error import *

class ParseResult:
    def __init__ (self):
        self.error = None
        self.node = None

    def register(self, res):
        if res.error:
            self.error = res.error
        return res.node
    
    def success(self, node):
        self.node = node
        return self
    
    def failure(self, error):
        self.error = error
        return self

class Parser:
    def __init__ (self, tokens):
        self.tokens = tokens
        self.token_idx = -1
        self.current_token = None
        self.advance()
        self.idx_stack = []

    def update_current_token(self):
        self.current_token = self.tokens[self.token_idx] if self.token_idx < len(self.tokens) else None
        return self.current_token
    
    def advance (self):
        self.token_idx += 1
        return self.update_current_token()

    def retract (self):
        self.token_idx -= 1
        return self.update_current_token()
    
    def push(self):
        self.idx_stack.append(self.token_idx)
    
    def pop(self):
        self.token_idx = self.idx_stack.pop()
        self.update_current_token()

    def pop_discard(self):
        self.idx_stack.pop()

    def skip_eol(self):
        while self.current_token.type == TT_EOL:
            self.advance()

    ####################################

    def parse(self):
        res = self.stmt_list()
        if not res.error and self.current_token.type != TT_EOF:
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end, "Cannot reach EOF token"
            ))
        return res

    def bin_op(self, func, ops):
        res = ParseResult()
        left = res.register(func())
        if res.error:
            return res
        while self.current_token.type != TT_EOF:
            if not self.current_token.type in ops:
                if not self.current_token.value: 
                    break
                if type(ops) == str:
                    break
                if not (self.current_token.type, self.current_token.value) in ops:
                    break
            op_tok = self.current_token
            self.advance()
            right = res.register(func())
            if res.error: 
                return res
            left = BinOpNode(left, op_tok, right)
        return res.success(left)

    def atom(self):
        res = ParseResult()
        token = self.current_token
        # Unary:
        if token.type in (TT_PLUS, TT_MINUS):
            self.advance()
            factor = res.register(self.factor())
            if res.error:
                return res
            return res.success(UnaryOpNode(token, factor))
        # Number:
        elif token.type in (TT_INT, TT_FLOAT):
            self.advance()
            return res.success(NumberNode(token))
        # Identifier: variables and function call
        elif token.type in (TT_IDENTIFIER):
            self.advance()
            if (self.current_token.type != TT_LPAREN):
                return res.success(VarAccessNode(token))
            func_name_node = VarAccessNode(token)
            self.advance()
            arg_nodes = []
            if self.current_token.type == TT_RPAREN:
                self.advance()
            else:
                arg_nodes.append(res.register(self.expr()))
                if res.error: return res

                while self.current_token.type == TT_COMMA:
                    self.advance()
                    arg_nodes.append(res.register(self.expr()))
                    if res.error: return res

                if self.current_token.type != TT_RPAREN:
                    return res.failure(InvalidSyntaxError(
                        self.current_token.pos_start, self.current_token.pos_end,
                        f"Expected ',' or ')'"
                    ))
                
                self.advance()

            return res.success(FuncCallNode(func_name_node, arg_nodes))

        # ( Expresion )
        elif token.type == TT_LPAREN:
            self.advance()
            expr = res.register(self.expr())
            if res.error:
                return res
            if self.current_token.type == TT_RPAREN:
                self.advance()
                return res.success(expr)
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end, "Expected ')'"
            ))
        return res.failure(InvalidSyntaxError(
            token.pos_start, token.pos_end, f"Expected int, float, unary, (expresion), but found {token.type}"
        ))

    def factor(self):
        return self.bin_op(self.atom, (TT_POWER))

    def term(self):
        return self.bin_op(self.factor, (TT_MUL, TT_DIV))

    def arithm_expr(self):
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))
    
    def comp_expr(self):
        res = ParseResult()
        # NOT
        if self.current_token.type == TT_NOT:
            token = self.current_token
            self.advance()
            node = res.register(self.comp_expr())
            if res.error: return res
            return res.success(UnaryOpNode(token, node))
        # ARITHM OP ARITHM
        node = res.register(self.bin_op(self.arithm_expr, (TT_EE, TT_NE, TT_LT, TT_GT, TT_LTE, TT_GTE)))
        if res.error: return res
        return res.success(node)

    def expr(self):
        res = ParseResult()
        # DECLARATION
        if self.current_token.matches(TT_KEYWORD, 'var'):
            self.advance()
            if self.current_token.type != TT_IDENTIFIER:
                return res.failure(InvalidSyntaxError(
                    self.current_token.pos_start, self.current_token.pos_end, "Expected identifier"
                ))
            identifier_token = self.current_token
            self.advance()
            if self.current_token.type != TT_EQUAL:
                return res.failure(InvalidSyntaxError(
                    self.current_token.pos_start, self.current_token.pos_end, "Expected '='"
                ))
            self.advance()
            expr = res.register(self.expr())
            if res.error: return res
            return res.success(VarDeclarationNode(identifier_token, expr))
        
        # ASSIGNMENT
        if self.current_token.type == TT_IDENTIFIER:
            identifier_token = self.current_token
            self.advance()
            if self.current_token.type == TT_EQUAL:
                self.advance()
                expr = res.register(self.expr())
                if res.error: return res
                return res.success(VarAssignNode(identifier_token, expr))
            self.retract()
        
        node = res.register(self.bin_op(self.comp_expr, (TT_AND, TT_OR)))
        if res.error: return res
        return res.success(node)

    ############################

    def func_def(self):
        res = ParseResult()
        self.advance()

        if self.current_token.type == TT_IDENTIFIER:
            var_name_tok = self.current_token
            self.advance()
            if self.current_token.type != TT_LPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected '('"
                ))
        else:
            var_name_tok = None
            if self.current_token.type != TT_LPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected identifier or '('"
                ))
        
        self.advance()
        arg_name_toks = []

        if self.current_token.type == TT_IDENTIFIER:
            arg_name_toks.append(self.current_token)
            self.advance()
            
            while self.current_token.type == TT_COMMA:
                self.advance()

                if self.current_token.type != TT_IDENTIFIER:
                    return res.failure(InvalidSyntaxError(
                        self.current_token.pos_start, self.current_token.pos_end,
                        f"Expected identifier"
                    ))

                arg_name_toks.append(self.current_token)
                self.advance()
            
            if self.current_token.type != TT_RPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    f"Expected ',' or ')'"
                ))
        else:
            if self.current_token.type != TT_RPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    f"Expected identifier or ')'"
                ))

        self.advance()
        
        stmt = self.stmt()
        node_to_return = res.register(stmt)

        if res.error: return res
        return res.success(FuncDefNode(
            var_name_tok,
            arg_name_toks,
            node_to_return
        ))
        
    def stmt(self):
        res = ParseResult()
        pos_start = self.current_token.pos_start.copy()

        # If (expr) stmt else stmt
        if self.current_token.matches(TT_KEYWORD, 'if'):
            self.advance()
            if self.current_token.type == TT_LPAREN:
                self.advance()
                expr = res.register(self.expr())
                if res.error:
                    return res
                if self.current_token.type == TT_RPAREN:
                    self.advance()
                self.skip_eol()
                stmt1 = res.register(self.stmt())
                if res.error:
                    return res
                if self.current_token.type == TT_EOF:
                    return res.success(IfNode(expr, stmt1))
                self.push()
                self.skip_eol()
                if self.current_token.matches(TT_KEYWORD, 'else'):
                    self.pop_discard()
                    self.advance()
                    self.skip_eol()
                    stmt2 = res.register(self.stmt())
                    if res.error:
                        return res
                    while self.current_token.type != TT_EOL and self.current_token.type != TT_EOF:
                        self.retract()
                    return res.success(IfElseNode(expr, stmt1, stmt2))
                self.pop()
                return res.success(IfNode(expr, stmt1))
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end, "Expected '('"
            ))
        # function def
        elif self.current_token.matches(TT_KEYWORD, 'function'):
            func_def = res.register(self.func_def())
            if res.error: return res
            return res.success(func_def)
        # return
        elif self.current_token.matches(TT_KEYWORD, 'return'):
            self.advance()
            return_node = res.register(self.expr())
            if res.error: return res
            return res.success(ReturnNode(return_node, pos_start, self.current_token.pos_start.copy()))
        # { stmt_list }
        elif self.current_token.type == TT_LCURLY:
            self.advance()      
            stmt_list = res.register(self.stmt_list())
            if self.current_token.type == TT_RCURLY:
                self.advance()
                self.skip_eol()
                return res.success(stmt_list)
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end, "Expected '}'"
            ))           
        # expr  
        else:
            left = res.register(self.expr())
            if res.error:
                return res
            return res.success(left)

    def stmt_list(self):
        res = ParseResult()
        stmts = []
        while self.current_token.type != TT_EOF:
            if self.current_token.type == TT_EOL:
                self.advance()
                continue
            if self.current_token.type == TT_RCURLY:
                break
            stmts.append(res.register(self.stmt()))
            if res.error: 
                return res
            else:
                continue
            if self.current_token.type == TT_EOL:
                self.advance()
                continue
            if self.current_token.type == TT_EOF:
                continue
            return res.failure(InvalidSyntaxError(self.current_token.pos_start, self.current_token.pos_end, "Expected new line"))
        return res.success(StatementListNode(stmts))
    