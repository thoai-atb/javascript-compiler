from .lexer import *
from .parser import *
from .interpreter import *
from .symbol_table import *
from .context import *
from .parse_printer import *
from .ast_printer import *
import codecs
import math

############################################################### RUN

global_symbol_table = SymbolTable()
global_symbol_table.set_declar('NULL', Number(0))
global_symbol_table.set_declar('TRUE', Number(1))
global_symbol_table.set_declar('FALSE', Number(0))
global_symbol_table.set_declar('PI', Number(math.pi))

def run(program_file_path, log_file_path):
    # OPEN LOG FILE
    log_file = codecs.open(log_file_path, 'w', 'utf-8')

    # LEXICAL ANALYSIS
    lexer = Lexer(program_file_path, open(program_file_path, 'r').read())
    tokens, error = lexer.make_tokens()
    if error:
        return None, error
    log_file.write('TOKEN LIST:\n\n')
    log_file.write(str(tokens))
    log_file.write('\n')
    log_file.write('\n')

    # PARSING
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error:
        return None, ast.error

    log_file.write('PARSE TREE:\n\n')
    printer = ParsePrinter(ast.node, log_file)
    printer.print()
    log_file.write('\n')

    log_file.write('ABSTRACT SYNTAX TREE:\n\n')
    printer = ASTPrinter(ast.node, log_file)
    printer.print()
    log_file.write('\n')

    # INTERPRETATION
    interpreter = Interpreter(log_file)
    context = Context('<program>')
    context.symbol_table = global_symbol_table
    log_file.write('EXECUTION PROCESS:\n')
    result = interpreter.visit(ast.node, context)
    return result.value, result.error