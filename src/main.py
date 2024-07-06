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
print("Hello World342")

code_example ="""{
    let a = 42, mod = a % 3 in
        print(
            if (mod == 0) "Magic"
            elif (mod % 3 == 1) "Woke"
            else "Dumb"
        );
    let a = 10 in while (a >= 0) {
        print(a);
        a := a - 1;
    };
    
    for (x in range(0, 10)) print(x);
    let iterable = range(0, 10) in
        while (iterable.next())
            let x = iterable.current() in
                print(x);

    let pt = new Point() in
        print("x: " @ pt.getX() @ "; y: " @ pt.getY());
    let pt = new Point(3,4) in
        print("x: " @ pt.getX() @ "; y: " @ pt.getY());
    let pt = new PolarPoint(3,4) in
        print("rho: " @ pt.rho());

    let p = new Knight("Phil", "Collins") in
        print(p.name());
    let x: Number = 42 in print(x);

    let x = new Superman() in
        print(
            if (x is Bird) "Its bird!"
            elif (x is Plane) "Its a plane!"
            else "No, its Superman!"
        );
    let x = 42 in print(x);
    let total = ({ print("Total"); 5; }) + 6 in print(total);
    let x : A = if (rand() < 0.5) new B() else new C() in
        if (x is B)
            let y : B = x as B in {
                y.hello();
            }
        else {
            print("x cannot be downcasted to B");
        };

    let numbers = [1,2,3,4,5,6,7,8,9] in
        for (x in numbers)
            print(x);
    let numbers = [1,2,3,4,5,6,7,8,9] in print(numbers[7]);

    let squares = [x^2 || x in range(1,10)] in print(x);

    let squares = [x^2 || x in range(1,10)] in for (x in squares) print(x);
    let x : Hashable = new Point(0,0) in print(x.hash());
}
"""
print(code_example)
tokens = lexer(code_example)



for token in tokens:
    print(
        f"row: {token.row}, column: {token.column}, token type: {token.token_type}, lex: {token.lex}"
    )
parse, operations = parser(tokens)
# print(parse)
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
