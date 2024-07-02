from hulk.parser.lr1 import LR1Parser
from hulk.hulk_grammar import G
from hulk.hulk_ast import *
from hulk.hulk_lexer import Lexer
from hulk.lexer.regex_table import table
from hulk.lexer.token_type import TokenType


parser = LR1Parser(G=G, verbose=False, load=True, save=False)

lexer = Lexer(table=table, eof=TokenType.EOF)

code_example = """
let x = 5;
let y = 3;
let z = x + y; """


tokens = lexer(code_example + TokenType.EOF.value)
for token in tokens:
    print(token)
