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
type Point(x, y) {
    x = x;
    y = y;
    getX() => self.x;
    getY() => self.y;

    setX(x) => self.x := x;
    setY(y) => self.y := y;
}

type PolarPoint inherits Point {
    rho() => sqrt(self.getX() ^ 2 + self.getY() ^ 2);
}

type Person(firstname, lastname) {
    firstname = firstname;
    lastname = lastname;

    name() => self.firstname @@ self.lastname;
}

type Knight inherits Person {
    name() => "Sir" @@ base();
}

type Bird {
    name() => "Bird";
}

type Plane {
    name() => "Plane";
}

type Superman {
    name() => "Superman";
}


type A {
    prop() => "A";
}

type B inherits A {
    prop() => "B";
}

type C inherits A {
    prop() => "C";
}

function gcd(a, b) {
    if (b == 0)  a
    else gcd(b, a % b);
}

function fib(n) {
    if (n <= 1) 1
    else {fib(n - 1) + fib(n - 2)};
}

type Recursive {
    r(n) => if (n == 0 | n == 1) 1 else self.r(n-1) + self.r(n-2); 
}

function fact(x) => let f = 1 in for (i in range(1, x+1)) f := f * i;



{
    
    let numbers = [1,2,3,4,5,6,7,8,9] in
        for (x in numbers)
            print(x);
    
    let numbers = [1,2,3,4,5,6,7,8,9] in print(numbers[7]);

    let squares = [x^2 || x in range(1,10)] in print(squares);

            
    let x = new Recursive() in
    print(x.r(5));
    print(fact(5));

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

ast, errors, context, scope = semantic_check_pipeline(ast, True)

if errors:
    exit(1)

print("\n=================== TREE INTERPRETER ======================")
interpreter = Interpreter(context=context)
result = interpreter.visit(ast)
print("\n=================== FINISH ================================")
print("Interpreter Evaluation: " + str(result))
