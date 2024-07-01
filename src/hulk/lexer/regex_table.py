from hulk.lexer.token_type import *

operators = [
    (';', TokenType.SEMICOLON), (':', TokenType.COLON), (',', TokenType.COMMA), ('.', TokenType.DOT),
    ('(', TokenType.OPAR), (')', TokenType.CPAR), ('{', TokenType.OCURLY), ('}', TokenType.CCURLY), ('[', TokenType.OBRACK), (']', TokenType.CBRACK),
    ('+', TokenType.PLUS), ('-', TokenType.MINUS), ('*', TokenType.STAR), ('/', TokenType.DIV), ('^', TokenType.POWER), ('**', TokenType.POWER_STAR),
    ('@', TokenType.CONCAT), ('@@', TokenType.DOBLECONCAT), ('=>', TokenType.ARROW), ('%', TokenType.MOD),
    ('=', TokenType.EQ), ('!=', TokenType.NEQ), ('<', TokenType.LE), ('<=', TokenType.LEQ),
    ('>', TokenType.GR), ('>=', TokenType.GREQ), ('==', TokenType.EQEQ), (':=', TokenType.DEST_EQ),
    ('&', TokenType.AND), ('|', TokenType.OR), ('!', TokenType.NOT), ('||', TokenType.BAR_BAR)
]

OPERATORS = extend_tuple(operators, False)

keywords = [
    ('let', TokenType.LET), ('in', TokenType.IN), ('is', TokenType.IS), ('as', TokenType.AS),
    ('if', TokenType.IF), ('elif', TokenType.ELIF), ('else', TokenType.ELSE), ('while', TokenType.WHILE),
    ('for', TokenType.FOR), ('new', TokenType.NEW), ('type_id', TokenType.TYPE_ID),
    ('func', TokenType.FUNC), ('type', TokenType.TYPE), ('inherits', TokenType.INHERITS), ('protocol', TokenType.PROTOCOL),
    ('extends', TokenType.EXTENDS), ('base', TokenType.BASE)
]

KEYWORDS = extend_tuple(keywords, False)

positive = '(' + '|'.join(str(n) for n in range(1 , 10)) + ')'
non_negative = '(' + '|'.join(str(n) for n in range(10)) + ')'
lower_letters = '(' + '|'.join(chr(n) for n in range(ord('a'), ord('z') + 1)) + ')'
upper_letters = '(' + '|'.join(chr(n) for n in range(ord('A'), ord('Z') + 1)) + ')'


regexs = [
    (f'({lower_letters}|{upper_letters})({lower_letters}|{upper_letters}|{non_negative})*', TokenType.ID)
    (f'(True)|(False)', TokenType.BOOL)
    (f'{positive}{non_negative}*', TokenType.NUM)
    (f'"({lower_letters}|{upper_letters}|{non_negative})*"')
]

REGEXS = extend_tuple(regexs, True)