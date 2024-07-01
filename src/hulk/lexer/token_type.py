from enum import Enum, auto

class TokenType(Enum):
    
    SEMICOLON = auto()
    COLON = auto()
    COMMA = auto()
    DOT = auto()
    OPAR = auto()
    CPAR = auto()
    OCURLY = auto()
    CCURLY = auto()
    OBRACK = auto()
    CBRACK = auto()

    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    DIV = auto()
    POWER = auto()
    POWER_STAR = auto()
    CONCAT = auto()
    DOBLECONCAT = auto()
    ARROW = auto()
    MOD = auto()

    EQ = auto()
    NEQ = auto()
    LE = auto()
    LEQ = auto()
    GR = auto()
    GREQ = auto()
    EQEQ = auto()
    DEST_EQ = auto()

    AND = auto()
    OR = auto()
    NOT = auto()

    NUM = auto()
    STR = auto()
    BOOL = auto()
    ID = auto()
    LET = auto()
    IN = auto()
    IS = auto()
    AS = auto()
    IF = auto()
    ELIF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    NEW = auto()
    TYPE_ID = auto()

    FUNC = auto()
    TYPE = auto()
    INHERITS = auto()
    PROTOCOL = auto()
    EXTENDS = auto()
    BASE = auto()

    BAR_BAR = auto()

def extend_tuple(elements, is_regex):
    return [(lex, token_type, is_regex) for (lex, token_type) in elements]


    
