from .value import *
from .token import *
from .context import *
from .symbol_table import *

class RTResult:
    def __init__ (self, log_file, context):
        self.log_file = log_file
        self.context = context
        self.reset()

    def reset(self):
        self.value = None
        self.error = None
        self.return_value = None

    def register(self, res):
        self.error = res.error
        self.return_value = res.return_value
        return res.value

    def success(self, value):
        self.reset()
        self.value = value
        tabs = self.context.get_depth() * '\t'
        self.log_file.write(f'\n{tabs}Passing Result: {value}')
        return self

    def success_return(self, value):
        self.reset()
        self.return_value = value
        tabs = self.context.get_depth() * '\t'
        self.log_file.write(f'\n{tabs}Returning Result: {value}')
        return self

    def failure(self, error):
        self.reset()
        self.error = error
        return self
    
    def should_return(self):
        return self.error or self.return_value

class Interpreter:
    def __init__(self, log_file):
        self.log_file = log_file

    def visit(self, node, context):
        tabs = context.get_depth() * '\t'
        self.log_file.write(f'\n{tabs}Visit {type(node).__name__}: {node}')
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)
    
    def no_visit_method(self, node, context):
        raise Exception(f'No visit_{type(node).__name__} method defined')
    
    ####################################

    def visit_ValueNode(self, node, context):
        if node.token.type == TT_INT:
            return RTResult(self.log_file, context).success(
                Number(node.token.value).set_context(context).set_pos(node.pos_start, node.pos_end)
            )
        if node.token.type == TT_STRING:
            return RTResult(self.log_file, context).success(
                String(node.token.value).set_context(context).set_pos(node.pos_start, node.pos_end)
            )

    def visit_VarAccessNode(self, node, context):
        res = RTResult(self.log_file, context)
        var_name = node.token.value
        value = context.symbol_table.get(var_name)
        if not value:
            return res.failure(RTError(
                node.pos_start, node.pos_end, f'Variable {var_name} is not defined', context
            ))
        value = value.copy().set_pos(node.pos_start, node.pos_end)
        return res.success(value)

    def visit_VarAssignNode(self, node, context):
        res = RTResult(self.log_file, context)
        var_name = node.var_name_token.value
        if not context.symbol_table.has(var_name):
            return res.failure(RTError(
                node.var_name_token.pos_start, node.var_name_token.pos_end, f'Variable {var_name} is not defined', context
            ))
        value = res.register(self.visit(node.expr_node, context))
        if res.should_return(): return res
        context.symbol_table.set_assign(var_name, value)
        return res.success(value)
 
    def visit_VarDeclarationNode(self, node, context):
        res = RTResult(self.log_file, context)
        var_name = node.var_name_token.value
        if context.symbol_table.has_local(var_name):
            return res.failure(RTError(
                node.var_name_token.pos_start, node.var_name_token.pos_end, f'Variable {var_name} is already declared', context
            ))
        value = res.register(self.visit(node.expr_node, context))
        if res.should_return(): return res
        context.symbol_table.set_declar(var_name, value)
        return res.success(value)

    def visit_IfElseNode(self, node, context):
        res = RTResult(self.log_file, context)
        expr_bool = res.register(self.visit(node.expr_node, context))
        if res.should_return(): return res
        if expr_bool.is_true():
            result = res.register(self.visit(node.stmt1, context))
            if res.should_return(): return res
            return res.success(result)
        result = res.register(self.visit(node.stmt2, context))
        if res.should_return(): return res
        return res.success(result.set_pos(node.pos_start, node.pos_end))
    
    def visit_IfNode(self, node, context):
        res = RTResult(self.log_file, context)
        expr_bool = res.register(self.visit(node.expr_node, context))
        if res.should_return(): return res
        if expr_bool.is_true():
            result = res.register(self.visit(node.stmt, context))
            if res.should_return(): return res
            return res.success(result)
        return res.success(None)

    def visit_FuncDefNode(self, node, context):
        res = RTResult(self.log_file, context)

        func_name = node.var_name_tok.value if node.var_name_tok else None
        body_node = node.body_node
        arg_names = [arg_name.value for arg_name in node.arg_name_toks]
        func_value = Function(func_name, body_node, arg_names).set_context(context).set_pos(node.pos_start, node.pos_end)

        if node.var_name_tok:
            context.symbol_table.set_declar(func_name, func_value)
        
        return res.success(func_value)

    def visit_FuncCallNode(self, node, context):
        res = RTResult(self.log_file, context)
        args = []

        value_to_call = res.register(self.visit(node.node_to_call, context))
        if res.should_return(): return res
        value_to_call = value_to_call.copy().set_pos(node.pos_start, node.pos_end).set_context(context)

        for arg_node in node.arg_nodes:
            args.append(res.register(self.visit(arg_node, context)))
            if res.should_return(): return res

        return_val = res.register(self.execute_function(value_to_call, args))
        if res.should_return(): return res
        return res.success(return_val)

    def execute_function(self, func, args):
        tabs = func.context.get_depth() * '\t'
        self.log_file.write(f'\n{tabs}Executing Function: {func}')

        res = RTResult(self.log_file, func.context)
        new_context = Context(func.name, func.context, func.pos_start)
        func.context.children.append(new_context)
        new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)

        if len(args) != len(func.arg_names):
            return res.failure(RTError(
                func.pos_start, func.pos_end,
                f'Numbers of args do not match (expected {len(func.arg_names)} but found {len(args)})',
                func.context
            ))

        for i in range(len(args)):
            arg_name = func.arg_names[i]
            arg_value = args[i]
            arg_value.set_context(new_context)
            new_context.symbol_table.set_declar(arg_name, arg_value)

        value = res.register(self.visit(func.body_node, new_context))
        if res.should_return() and res.return_value == None: return res
        return_value = res.return_value or value
        return res.success(return_value)

    def visit_ReturnNode(self, node, context):
        res = RTResult(self.log_file, context)
        value = None
        if node.node_to_return:
            value = res.register(self.visit(node.node_to_return, context))
            if res.should_return(): return res
        return res.success_return(value)

    def visit_StatementListNode(self, node, context):
        res = RTResult(self.log_file, context)
        value = None
        for n in node.list:
            value = res.register(self.visit(n, context))
            if res.should_return(): return res
        return res.success(value)
       
    def visit_BinOpNode(self, node, context):
        res = RTResult(self.log_file, context)
        left = res.register(self.visit(node.left_node, context))
        if res.should_return(): return res
        right = res.register(self.visit(node.right_node, context))
        if res.should_return(): return res

        result = None
        error = None
        
        tabs = context.get_depth() * '\t'
        self.log_file.write(f'\n{tabs}Executing Operation: {left} {node.token.type} {right}')

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
        
        if error: return res.failure(error.set_pos(node.token.pos_start, node.token.pos_end))
        return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self, node, context):
        res = RTResult(self.log_file, context)
        number = res.register(self.visit(node.node, context))
        if res.should_return(): return res

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