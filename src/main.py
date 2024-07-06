from hulk.parser.lr1 import LR1Parser
from hulk.lexer.regex_table import G
from hulk.hulk_ast import *
from hulk.hulk_lexer import Lexer
from hulk.lexer.regex_table import table
from hulk.lexer.token_type import TokenType
from hulk.lexer.regex import Regex
from cmp.evaluation import evaluate_reverse_parse_plus
from cmp.formatVisitor import FormatVisitor
from hulk.semantic_check.semantic_check_pipeline import semantic_check_pipeline

parser = LR1Parser(G=G, load=True)

lexer = Lexer(table=table, eof=G.EOF)

code_example ="""

print(z == 322.6 | z == 1);
"""
print(code_example)
tokens = lexer(code_example)


for token in tokens:
    print(
        f"row: {token.row}, column: {token.column}, token type: {token.token_type}, lex: {token.lex}"
    )

parse, operations = parser(tokens)
print(parse)
if parser.errors:
    print("Parser Errors:", parser.errors)
    exit(1)
ast = evaluate_reverse_parse_plus(parse, operations, tokens)
print(ast)

print(" - - - -- - - - - VISITOR  - -- - - - - - - - - -- ")

a = FormatVisitor()
a.visit(ast)
print(a.ans)

semantic_check_pipeline(ast, True)

# print("========== STATES ==========")
# for item in dfa.map.items():
#     print(item)
# print("========== FINALS ==========")
# for item in dfa.finals:
#     print(item)
# print("========== START ===========")
# print(dfa.start)
# print("============================")
