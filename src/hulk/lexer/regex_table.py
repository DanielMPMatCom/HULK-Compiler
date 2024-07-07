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
    ("function", G["func"]),
    ("type", G["type"]),
    ("inherits", G["inherits"]),
    ("protocol", G["protocol"]),
    ("extends", G["extends"]),
    ("base", G["base"]),
    ("PI", G["PI"]),
    ("E", G["E"])
]

KEYWORDS = extend_tuple(keywords, False)

any_symbol = "(" + "|".join(chr(n) for n in range(0, 256) if (chr(n).isprintable() and chr(n) not in ['*', '|', '(', ')', 'ε', '\\', '\'', '"', ''])) + ")"
positive = "(" + "|".join(str(n) for n in range(1, 10)) + ")"
non_negative = "(" + "|".join(str(n) for n in range(10)) + ")"
lower_letters = "(" + "|".join(chr(n) for n in range(ord("a"), ord("z") + 1)) + ")"
upper_letters = "(" + "|".join(chr(n) for n in range(ord("A"), ord("Z") + 1)) + ")"
string_regex = "\"(\\\\\"|\\x00|\\x01|\\x02|\\x03|\\x04|\\x05|\\x06|\\x07|\\x08|\\t|\\n|\\x0b|\\x0c|\\r|\\x0e|\\x0f|\\x10|\\x11|\\x12|\\x13|\\x14|\\x15|\\x16|\\x17|\\x18|\\x19|\\x1a|\\x1b|\\x1c|\\x1d|\\x1e|\\x1f| |!|#|$|%|&|\'|\\(|\\)|\\*|+|,|-|.|/|0|1|2|3|4|5|6|7|8|9|:|;|<|=|>|?|@|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|[|\\\\|]|^|_|`|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|{|\\||}|~|\\x7f|\\x80|\\x81|\\x82|\\x83|\\x84|\\x85|\\x86|\\x87|\\x88|\\x89|\\x8a|\\x8b|\\x8c|\\x8d|\\x8e|\\x8f|\\x90|\\x91|\\x92|\\x93|\\x94|\\x95|\\x96|\\x97|\\x98|\\x99|\\x9a|\\x9b|\\x9c|\\x9d|\\x9e|\\x9f|\\xa0|¡|¢|£|¤|¥|¦|§|¨|©|ª|«|¬|\\xad|®|¯|°|±|²|³|´|µ|¶|·|¸|¹|º|»|¼|½|¾|¿|À|Á|Â|Ã|Ä|Å|Æ|Ç|È|É|Ê|Ë|Ì|Í|Î|Ï|Ð|Ñ|Ò|Ó|Ô|Õ|Ö|×|Ø|Ù|Ú|Û|Ü|Ý|Þ|ß|à|á|â|ã|ä|å|æ|ç|è|é|ê|ë|ì|í|î|ï|ð|ñ|ò|ó|ô|õ|ö|÷|ø|ù|ú|û|ü|ý|þ|ÿ)*\""


regexs = [
    (f"(true)|(false)", G["bool"]),
    (
        f"({lower_letters}|{upper_letters}|_)({non_negative}|{lower_letters}|{upper_letters}|_)*",
        G["id"],
    ),
    (
        f"0|{positive}{non_negative}*|({positive}{non_negative}*.{non_negative}*)|({non_negative}.{non_negative}*)",
        G["num"],
    ),
    (
        f'"({any_symbol}|(\\\\")|(\\\\\')|(\\|)|(\\\\)|(\\*))*"',
        G["str"],
    ),
]

REGEXS = extend_tuple(regexs, True)


# table = OPERATORS + KEYWORDS + REGEXS
table = OPERATORS + KEYWORDS + REGEXS

# -----Testing----- #
# table = [REGEXS[0]]
