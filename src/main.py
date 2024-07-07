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

load = True
save = not load

parser = LR1Parser(G=G, load=load, save=save)
lexer = Lexer(table=table, eof=G.EOF, load=load, save=save)


code_example = r"""
type Point {
    x: Number = x;
    y: Number = y;

    getX() => self.x;
    getY() => self.y;

    setX(x) => self.x := x;
    setY(y) => self.y := y;
}
type Person(firstname, lastname) {
    firstname = firstname;
    lastname = lastname;
    hash() : Number {
    print(43)
    }
    name() => self.firstname @@ self.lastname;
}
type Knight inherits Person {
    name() => "Sir" @@ base();
}
type Range(min:Number, max:Number) {
    min = min;
    max = max;
    current = min - 1;

    next(): Boolean => (self.current := self.current + 1) < max;
    current(): Number => self.current;
}

function gcd(a, b) => while (a > 0)
    let m = a % b in {
        b := a;
        a := m;
    };
function operate(x, y) {
    print(x + y);
    print(x - y);
    print(x * y);
    print(x / y);
}
function tan(x: Number): Number => sin(x) / cos(x);
function fib(n) => if (n == 0 | n == 1) 1 else fib(n-1) + fib(n-2);
function fact(x) => let f = 1 in for (i in range(1, x+1)) f := f * i;
protocol Hashable {
    hash(): Number;
}
protocol Equatable extends Hashable {
    equals(other: Object): Boolean;
}
function cot(x) => 1 / tan(x);

protocol Iterable {
    next() : Boolean;
    current() : Object;
}
type Range(min:Number, max:Number) {
    min = min;
    max = max;
    current = min - 1;

    next(): Boolean => (self.current := self.current + 1) < self.max;
    current(): Number => self.current;
}

type PolarPoint(phi, rho) inherits Point(rho * sin(phi), rho * cos(phi)) {
    rho() => sqrt(self.getX() ^ 2 + self.getY() ^ 2); 
}
type Superman {
}
type Bird {
}
type Plane {
}
type A {
    hello() => print("A");
}

type B inherits A {
    hello() => print("B");
}

type C inherits A {
    hello() => print("C");
}

type wacamole{
    y = 0;
    f() {
        self.y:=12;
        self := new A(); 
    }
    g(a,b,a) {
        self.y:=12;
        self := new A(); 
    }
    f() {
        print("esto da error malditasea");
    }
}


{
    42;
    print(42);
    print((((1 + 2) ^ 3) * 4) / 5);
    print("Hello World");
    print("The message is \"Hello World\"");
    print("The meaning of life is " @ 42);
    print(sin(2 * PI) ^ 2 + cos(3 * PI / log(4, 64)));
    {
        print(42);
        print(sin(PI/2));
        print("Hello World");
    };

    
    print(tan(PI) ** 2 + cot(PI) ** 2);

    let msg = "Hello World" in print(msg);
    let number = 42, text = "The meaning of life is" in
        print(text @ number);
    let number = 42 in
        let text = "The meaning of life is" in
            print(text @ number);
    let number = 42 in (
        let text = "The meaning of life is" in (
                print(text @ number)
            )
        );
    let a = 6, b = a * 7 in print(b);
    let a = 6 in
        let b = a * 7 in
            print(b);
    let a = 5, b = 10, c = 20 in {
        print(a+b);
        print(b*c);
        print(c/a);
    };
    let a = (let b = 6 in b * 7) in print(a);
    print(let b = 6 in b * 7);
    let a = 20 in {
        let a = 42 in print(a);
        print(a);
    };
    let a = 7, a = 7 * 6 in print(a);
    let a = 7 in
        let a = 7 * 6 in
            print(a);
    let a = 0 in {
        print(a);
        a := 1;
        print(a);
    };
    let a = 0 in
        let b = a := 1 in {
            print(a);
            print(b);
        };
    let a = 42 in
        if (a % 2 == 0) {
            print(a);
            print("Even");
        }
        else print("Odd");
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
        
    let p = new Person("Phil", "Collins") in
        print(p.name());
    let p: Person = new Knight("Phil", "Collins") in print(p.name());
    let x: Number = 42 in print(x);

    let p = new Person("Phil", "Collins") in
        let x: Number = fact(3)/print(p.name()) in print(x);
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
    let x : Hashable = new Person() in print(x.hash());
    let x : Hashable = new Point(0,0) in print(x.hash());

    let awacate: QueRico = new QueRico("siuuuu" @@ banda @ yaes + 4*5^2 @@ temporada_de_awacate == true) in aguacate.cascara("verde").lo_de_adentro(43*-1).semilla(true);
    let x : Hashable = new Person() in print(x.hash());
print(operate(2,3));
let msg = "Hello World" in print(msg);
let number = 42, text = "The meaning of life is" in
    print(text @ number);
let number = 42 in
    let text = "The meaning of life is" in
        print(text @ number);
let number = 42 in (
    let text = "The meaning of life is" in (
            print(text @ number)
        )
    );
let a = 6, b = a * 7 in print(b);
let a = 6 in
    let b = a * 7 in
        print(b);
let a = 5, b = 10, c = 20 in {
    print(a+b);
    print(b*c);
    print(c/a);
};
let a = (let b = 6 in b * 7) in print(a);
print(let b = 6 in b * 7);
let a = 20 in {
    let a = 42 in print(a);
    print(a);
};
let a = 7, a = 7 * 6 in print(a);
let a = 7 in
    let a = 7 * 6 in
        print(a);
let a = 0 in {
    print(a);
    a := 1;
    print(a);
};
let a = 0 in
    let b = a := 1 in {
        print(a);
        print(b);
    };
let a = 42 in if (a % 2 == 0) print("Even") else print("odd");
let a = 42 in
    if (a % 2 == 0) {
        print(a);
        print("Even");
    }
    else print("Odd");
let a = 42 in if (a % 2 == 0) print("Even") else print("odd");
let a = 42 in
    if (a % 2 == 0) {
        print(a);
        print("Even");
    }
    else print("Odd");
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
let x = 42 in print(x);
for (x in range(0,10)) {
    print(x)
};
let iterable = range(0, 10) in
    while (iterable.next())
        let x = iterable.current() in {
            print(x)
        };
let numbers = [1,2,3,4,5,6,7,8,9] in
    for (x in numbers)
        print(x);

let numbers = [1,2,3,4,5,6,7,8,9] in print(numbers[7]);

let squares = [x^2 || x in range(1,10)] in print(squares);

let a = 42 in if (a % 2 == 0) print("Even") else print("odd");
let a = 42 in print(if (a % 2 == 0) "even" else "odd");
let a = 42 in
    if (a % 2 == 0) {
        print(a);
        print("Even");
    }
    else print("Odd");
let a = 42, mod = a % 3 in
    print(
        if (mod == 0) "Magic"
        elif (mod % 3 == 1) "Woke"
        else "Dumb"
    );

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
