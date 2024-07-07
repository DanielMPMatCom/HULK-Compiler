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
from hulk.tree_interpeter.interpeter import Interpreter

load = True
save = not load

parser = LR1Parser(G=G, load=load, save=save)
lexer = Lexer(table=table, eof=G.EOF, load=load, save=save)


code_example = r"""
type Point {
    x: Number = 0;
    y: Number = 0;

    getX() => self.x;
    getY() => self.y;

    setX(x) => self.x := x;
    setY(y) => self.y := y;
}

{
    let pt = new Point() in
    print("x: " @ pt.getX() @ "; y: " @ pt.getY());
}
"""
print(code_example)
tokens = lexer(code_example)


for token in tokens:
    print(
        f"row: {token.row}, column: {token.column}, token type: {token.token_type}, lex: {token.lex}"
    )
if lexer.errors:
    print("Lexer Errors:")
    for le in lexer.errors:
        print("\033[91m" + "\t💥" + le + "\033[0m")
    exit(1)

parse, operations = parser(tokens)
# print(parse)
if parser.errors:
    print("Parser Errors:")
    for error in parser.errors:

        print("\033[91m" + "\t💥" + error + "\033[0m")
    exit(1)
ast = evaluate_reverse_parse_plus(parse, operations, tokens)
print(ast)

print(" - - - -- - - - - VISITOR  - -- - - - - - - - - -- ")

a = FormatVisitor()
a.visit(ast)
print(a.ans)

ast, errors, context, scope = semantic_check_pipeline(ast)

if errors:
    exit(1)

print("\n=================== TREE INTERPRETER ======================")
interpreter = Interpreter(context=context)
result = interpreter.visit(ast)
print("\n=================== FINISH ================================")
print("Interpreter Evaluation: " + str(result))
