from .lexer import *
from .parser import *
from .interpreter import *
from .symbol_table import *
from .context import *
from .node_printer import *
import codecs
import math

############################################################### RUN

global_symbol_table = SymbolTable()
global_symbol_table.set('NULL', Number(0))
global_symbol_table.set('TRUE', Number(1))
global_symbol_table.set('FALSE', Number(0))
global_symbol_table.set('PI', Number(math.pi))

def run(program_file_path, log_file_path):
    # OPEN LOG FILE
    log_file = codecs.open(log_file_path, 'w', 'utf-8')

    # LEXICAL ANALYSIS
    lexer = Lexer(program_file_path, open(program_file_path, 'r').read())
    tokens, error = lexer.make_tokens()
    if error:
        return None, error
    log_file.write('RESULT OF LEXER: \n')
    log_file.write(str(tokens))
    log_file.write('\n')
    log_file.write('\n')

    # PARSING
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error:
        return None, ast.error
    log_file.write('RESULT OF PARSER: \n')
    printer = NodePrinter(ast.node, log_file)
    printer.print()
    log_file.write('\n')

    # INTERPRETATION
    interpreter = Interpreter()
    context = Context('<program>')
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)
    return result.value, result.error