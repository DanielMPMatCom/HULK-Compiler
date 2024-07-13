import streamlit as st
from code_editor import code_editor
from streamlit_ace import st_ace
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
import sys

sys.setrecursionlimit(1000000)

load = True
save = not load

parser = LR1Parser(G=G, load=load, save=save)
lexer = Lexer(table=table, eof=G.EOF, load=load, save=save)


code_example = r"""
function tan(x: Number): Number => sin(x) / cos(x);
function cot(x) => 1 / tan(x);
function operate(x, y) {
    print(x + y);
    print(x - y);
    print(x * y);
    print(x / y);
}
function fib(n) => if (n == 0 | n == 1) 1 else fib(n-1) + fib(n-2);
function fact(x) => let f = 1 in for (i in range(1, x+1)) f := f * i;
function gcd(a, b) => while (a > 0)
        let m = a % b in {
            b := a;
            a := m;
        };
protocol Hashable {
    hash(): Number;
}
protocol Equatable extends Hashable {
    equals(other: Object): Boolean;
}
type Point(x,y) {
    x = x;
    y = y;

    getX() => self.x;
    getY() => self.y;

    setX(x) => self.x := x;
    setY(y) => self.y := y;
    hash() : Number {
        5;
    }
}
type PolarPoint(phi, rho) inherits Point(rho * sin(phi), rho * cos(phi)) {
    rho() => sqrt(self.getX() ^ 2 + self.getY() ^ 2);
}
type Knight inherits Person {
    name() => "Sir" @@ base();
}
type Person(firstname, lastname) {
    firstname = firstname;
    lastname = lastname;

    name() => self.firstname @@ self.lastname;
    hash() : Number {
        5;
    }
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
    }


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
    let a = 10 in while (a >= 0) {
        print(a);
        a := a - 1;
    };
    
    for (x in range(0, 10)) print(x);
    let iterable = range(0, 10) in
        while (iterable.next())
            let x = iterable.current() in
                print(x);

    let pt = new Point(0, 0) in
        print("x: " @ pt.getX() @ "; y: " @ pt.getY());
    let pt = new Point(3,4) in
        print("x: " @ pt.getX() @ "; y: " @ pt.getY());
    let pt = new PolarPoint(3,4) in
        print("rho: " @ pt.rho());

    let p = new Knight("Phil", "Collins") in
        print(p.name());
    let p: Person = new Knight("Phil", "Collins") in print(p.name());
    let x: Number = 42 in print(x);

    let x = new Superman() in
        print(
            if (x is Bird) "It's bird!"
            elif (x is Plane) "It's a plane!"
            else "No, it's Superman!"
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
    let squares = [x^2 || x in range(1,10)] in print(squares); 
    let squares = [x^2 || x in range(1,10)] in for (x in squares) print(x);
    let x : Hashable = new Person("juan", "pablo") in print(x.hash());
    let x : Hashable = new Point(0,0) in print(x.hash()); 
}"""

snippets = G.terminals

completions = []
for t in G.terminals:
    completions.append(
        {
            "caption": str(t),
            "value": str(t),
            "meta": "HULK",
            "name": "HULK",
            "score": 400,
        }
    )

builtin = [
    "print",
    "range",
    "sin",
    "cos",
]

completions += [
    {
        "caption": b,
        "value": b,
        "meta": "HULK",
        "name": "HULK",
        "score": 400,
    }
    for b in builtin
]


snippets = [str(s) for s in snippets]

snippets += builtin

css_string = """
background-color: #bee1e5;

.color-animation {
    animation-name: color-change;
    animation-duration: 2s;
    animation-iteration-count: infinite;
}

@keyframes color-change {
    0% {
        background-color: #fff;
    }
    50% {
        background-color: #000;
    }
    100% {
        background-color: #fff;
    }
}

body > #root .ace-streamlit-dark~& {
    background-color: #262830;
}

.ace-streamlit-dark~& span {
    color: #fff;
    opacity: 1;
}

span {
    color: #000;
    opacity: 1;
}

.code_editor-info.message {
    width: inherit;
    margin-right: 75px;
    order: 2;
    text-align: center;
    opacity: 0;
    transition: opacity 1s ease-out;
}
"""

buttons = [
    {
        "name": "Copy",
        "feather": "Copy",
        "hasText": True,
        "alwaysOn": True,
        "commands": [
            "copyAll",
            [
                "infoMessage",
                {
                    "text": "Copied to clipboard!",
                    "timeout": 2500,
                    "classToggle": "show",
                },
            ],
        ],
        "style": {"right": "3rem"},
    },
    {
        "name": "Run",
        "feather": "Play",
        "primary": True,
        "hasText": True,
        "showWithIcon": True,
        "alwaysOn": True,
        "commands": ["submit"],
        "style": {"bottom": "0.44rem", "right": "3rem"},
    },
]
# create info bar dictionary
info_bar = {
    "name": "language info",
    "css": css_string,
    "style": {
        "order": "1",
        "display": "flex",
        "flexDirection": "row",
        "alignItems": "center",
        "width": "100%",
        "height": "2.5rem",
        "padding": "0rem 0.75rem",
        "borderRadius": "8px 8px 0px 0px",
        "margin": "0px 0px -0.5rem 0px",
        "zIndex": "9993",
        "boxShadow": "0px 0px 10px 0px rgba(0,0,0,0.1)",
        "background": "rgb(0, 134, 20)",
        "color": "#fff",
        "fontFamily": "Arial, sans-serif",
        "fontSize": "1rem",
    },
    "info": [{"name": "HULK", "style": {"width": "100px"}}],
}


def process_text(text):
    tokens = lexer(text)
    if lexer.errors:
        ans = "Lexer Errors: \n"
        for le in lexer.errors:
            ans += "\t💥" + le + "\n"
        st.error(ans)
        return
    parse, operations = parser(tokens)
    if parser.errors:
        ans = "Parser Errors: \n"
        for error in parser.errors:
            ans += "\t💥" + error + "\n"
        st.error(ans)
        return

    ast = evaluate_reverse_parse_plus(parse, operations, tokens)
    ast, errors, context, scope = semantic_check_pipeline(ast, False)
    if errors:
        ans = "Semantic Errors: \n"
        for error in errors:
            ans += "\t💥" + str(error) + "\n"
        st.error(ans)
        return

    interpreter = Interpreter(context=context)
    result = interpreter.visit(ast)
    st.success("Interpreter Evaluation: " + str(result))
    


def main():

    st.markdown(
        """
    <style>
        [data-testid="baseButton-header"] {
            display: none
            }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # create sidebar
    st.sidebar.title("Avengers IDE")
    st.sidebar.write("## *Save the semester with code!*")
    st.sidebar.subheader("Choose your language")
    st.sidebar.radio(
        "Select Language",
        ["HULK", "StrangeCode", "StarkScript", "WebCrawlerMan", "Wakanda++", "GoThor"],
        disabled=True,
    )

    st.sidebar.subheader("Selected Language Reference:")
    st.sidebar.link_button(
        label="HULK Reference",
        url="https://matcom.in/hulk/",
        help="HULK is a strong programming language.",
    )

    # add info bar to code editor
    response_dict = code_editor(
        code=code_example,
        lang="tsx",
        info=info_bar,
        buttons=buttons,
        height="550px",
        focus=True,
        editor_props={
            "placeholder": "Write your code here...",
        },
        options={
            "fontSize": 16,
            "showLineNumbers": "true",
            "tabSize": "2",
            "useSoftTabs": "true",
        },
        component_props={
            "style": {
                "boxShadow": "0px 0px 10px 0px rgba(0,0,0,0.1)",
                "overflow": "scroll",
                "margin": "0.5rem 0.5rem 0.5rem 0.5rem",
                "width": "1150px",
            }
        },
        completions=completions,
        replace_completer=True,
        snippets=snippets,
    )

    if (
        "infoMessage" in response_dict
        and response_dict["infoMessage"] == "Copied to clipboard!"
    ):
        st.write("Copied to clipboard!")

    if "type" in response_dict and response_dict["type"] == "submit":
        process_text(response_dict["text"])


if __name__ == "__main__":
    st.set_page_config(
        page_title="VS Green",
        page_icon=":green_book:",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    main()
