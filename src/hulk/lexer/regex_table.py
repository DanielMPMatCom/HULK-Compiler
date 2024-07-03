from hulk.lexer.token_type import *
from hulk.hulk_grammar import G

operators = [
    (";", G[";"]),
    (":", G[":"]),
    (",", G[","]),
    (".", G["."]),
    ("(", G["("]),
    (")", G[")"]),
    ("{", G["{"]),
    ("}", G["}"]),
    ("[", G["["]),
    ("]", G["]"]),
    ("+", G["+"]),
    ("-", G["-"]),
    ("*", G["*"]),
    ("/", G["/"]),
    ("^", G["^"]),
    ("**", G["**"]),
    ("@", G["@"]),
    ("@@", G["@@"]),
    ("=>", G["=>"]),
    ("%", G["%"]),
    ("=", G["="]),
    ("!=", G["!="]),
    ("<", G["<"]),
    ("<=", G["<="]),
    (">", G[">"]),
    (">=", G[">="]),
    ("==", G["=="]),
    (":=", G[":="]),
    ("&", G["&"]),
    ("|", G["|"]),
    ("!", G["!"]),
    ("||", G["||"]),
]

OPERATORS = extend_tuple(operators, False)

keywords = [
    ("let", G["let"]),
    ("in", G["in"]),
    ("is", G["is"]),
    ("as", G["as"]),
    ("if", G["if"]),
    ("elif", G["elif"]),
    ("else", G["else"]),
    ("while", G["while"]),
    ("for", G["for"]),
    ("new", G["new"]),
    ("type_id", G["type_id"]),
    ("func", G["func"]),
    ("type", G["type"]),
    ("inherits", G["inherits"]),
    ("protocol", G["protocol"]),
    ("extends", G["extends"]),
    ("base", G["base"]),
]

KEYWORDS = extend_tuple(keywords, False)

positive = "(" + "|".join(str(n) for n in range(1, 10)) + ")"
non_negative = "(" + "|".join(str(n) for n in range(10)) + ")"
lower_letters = "(" + "|".join(chr(n) for n in range(ord("a"), ord("z") + 1)) + ")"
upper_letters = "(" + "|".join(chr(n) for n in range(ord("A"), ord("Z") + 1)) + ")"


regexs = [
    (
        f"({lower_letters}|{upper_letters}|_)({non_negative}|{lower_letters}|{upper_letters}|_)*",
        G["id"],
    ),
    (f"(True)|(False)", G["bool"]),
    (
        f"{positive}{non_negative}*|({positive}{non_negative}.{non_negative}*)|({non_negative}.{non_negative}*)",
        G["num"],
    ),
    (
        f'"({lower_letters}|{upper_letters}|_)({lower_letters}|{upper_letters}|{non_negative}|_)*"',
        G["str"],
    ),
]

REGEXS = extend_tuple(regexs, True)


# table = OPERATORS + KEYWORDS + REGEXS
table = OPERATORS + KEYWORDS + REGEXS

# -----Testing----- #
# table = [REGEXS[0]]
