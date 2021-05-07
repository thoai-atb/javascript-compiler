from .lexer import *
from .parser import *
from .interpreter import *
from .symbol_table import *
from .context import *
from .node_printer import *
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
    print('\nRESULT OF LEXER: ')
    print(tokens)

    # PARSING
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error:
        return None, ast.error
    print('\nRESULT OF PARSER: ')
    printer = NodePrinter(ast.node)
    printer.print()
    print()

    # INTERPRETATION
    interpreter = Interpreter()
    context = Context('<program>')
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)
    return result.value, result.error