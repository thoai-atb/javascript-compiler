from .number import *
from .token import *

class RTResult:
    def __init__ (self):
        self.value = None
        self.error = None

    def register(self, res):
        if isinstance(res, RTResult):
            if res.error:
                self.error = res.error
        return res.value

    def success(self, value):
        self.value = value
        return self
    
    def failure(self, error):
        self.error = error
        return self


class Interpreter:
    def visit(self, node, context):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)
    
    def no_visit_method(self, node, context):
        raise Exception(f'No visit_{type(node).__name__} method defined')
    
    ####################################

    def visit_NumberNode(self, node, context):
        return RTResult().success(
            Number(node.token.value).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_VarAccessNode(self, node, context):
        res = RTResult()
        var_name = node.token.value
        value = context.symbol_table.get(var_name)
        if not value:
            return res.failure(RTError(
                node.pos_start, node.pos_end, f'Variable {var_name} is not defined', context
            ))
        value = value.copy().set_pos(node.pos_start, node.pos_end)
        return res.success(value)

    def visit_VarAssignNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_token.value
        if not context.symbol_table.has(var_name):
            return res.failure(RTError(
                node.var_name_token.pos_start, node.var_name_token.pos_end, f'Variable {var_name} is not defined', context
            ))
        value = res.register(self.visit(node.expr_node, context))
        if res.error: return res
        context.symbol_table.set(var_name, value)
        return res.success(value)
 
    def visit_VarDeclarationNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_token.value
        if context.symbol_table.has(var_name):
            return res.failure(RTError(
                node.var_name_token.pos_start, node.var_name_token.pos_end, f'Variable {var_name} is already declared', context
            ))
        value = res.register(self.visit(node.expr_node, context))
        if res.error: return res
        context.symbol_table.set(var_name, value)
        return res.success(value)

    def visit_StatementListNode(self, node, context):
        res = RTResult()
        value = None
        for n in node.list:
            value = res.register(self.visit(n, context))
            if res.error: return res
        return res.success(value)
           
       
       
    def visit_BinOpNode(self, node, context):
        res = RTResult()
        left = res.register(self.visit(node.left_node, context))
        if res.error: return res
        right = res.register(self.visit(node.right_node, context))
        if res.error: return res

        result = None
        error = None

        if node.token.type == TT_PLUS:
            result, error = left.add(right)
        elif node.token.type == TT_MINUS:
            result, error = left.sub(right)
        elif node.token.type == TT_MUL:
            result, error = left.mult(right)
        elif node.token.type == TT_DIV:
            result, error = left.div(right)
        elif node.token.type == TT_POWER:
            result, error = left.pow(right)
        elif node.token.type == TT_EE:
            result, error = left.compare_ee(right)
        elif node.token.type == TT_NE:
            result, error = left.compare_ne(right)
        elif node.token.type == TT_LT:
            result, error = left.compare_lt(right)
        elif node.token.type == TT_GT:
            result, error = left.compare_gt(right)
        elif node.token.type == TT_LTE:
            result, error = left.compare_lte(right)
        elif node.token.type == TT_GTE:
            result, error = left.compare_gte(right)
        elif node.token.type == TT_AND:
            result, error = left.bool_and(right)
        elif node.token.type == TT_OR:
            result, error = left.bool_or(right)
        
        if error: return res.failure(error)
        return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self, node, context):
        res = RTResult()
        number = res.register(self.visit(node.node, context))
        if res.error: return res

        result = None
        error = None
        if node.token.type == TT_MINUS:
            result, error = number.mult(Number(-1))
            result = result.set_pos(node.pos_start, node.pos_end)
        elif node.token.type == TT_PLUS:
            result = number.set_pos(node.pos_start, node.pos_end)
        elif node.token.type == TT_NOT:
            result, error = number.bool_not()
            
        if error: return res
        return res.success(result)