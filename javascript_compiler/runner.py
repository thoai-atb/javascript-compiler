from javascript_compiler.lexer import *
from javascript_compiler.parser import *
from javascript_compiler.interpreter import *
from javascript_compiler.symbol_table import *
from javascript_compiler.context import *
import math

############################################################### RUN

global_symbol_table = SymbolTable()
global_symbol_table.set('NULL', Number(0))
global_symbol_table.set('TRUE', Number(1))
global_symbol_table.set('FALSE', Number(0))
global_symbol_table.set('PI', Number(math.pi))

def run(file_name, text):
    # LEXICAL ANALYSIS
    lexer = Lexer(file_name, text)
    tokens, error = lexer.make_tokens()
    if error:
        return None, error
    print('result of lexer: ')
    print(tokens)

    # PARSING
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error:
        return None, ast.error
    print('result of parser: ')
    print(ast.node)

    # INTERPRETATION
    interpreter = Interpreter()
    context = Context('<program>')
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)
    return result.value, result.error