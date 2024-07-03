# from cmp.tools.parsing import LR1Parser
from hulk.parser.lr1 import LR1Parser
from hulk.hulk_grammar import G
from hulk.hulk_ast import *
from hulk.hulk_lexer import Lexer
from hulk.lexer.regex_table import table
from hulk.lexer.token_type import TokenType
from hulk.lexer.regex import Regex

parser = LR1Parser(G=G, verbose=False, load=True)
lexer = Lexer(table=table, eof=TokenType.EOF)

code_example = """
let x = 5;
let y = 3;
let z = x + y; """

tokens = lexer(code_example)

for token in tokens:
    print(f'row: {token.row}, column: {token.column}, token type: {token.token_type}, lex: {token.lex}')





# print("========== STATES ==========")
# for item in dfa.map.items():
#     print(item)
# print("========== FINALS ==========")
# for item in dfa.finals:
#     print(item)
# print("========== START ===========")
# print(dfa.start)
# print("============================")