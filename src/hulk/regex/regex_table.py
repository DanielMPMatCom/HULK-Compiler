from hulk.regex.regex_tokens import TokenType

symbols = [
    (';', TokenType.SEMICOLON), (':', TokenType.COLON),
    (',', TokenType.COMMA), ('.', TokenType.DOT),
    ('(', TokenType.OPAR), (')', TokenType.CPAR),
    ('{', TokenType.OCURLY), ('}', TokenType.CCURLY),
    ('[', TokenType.OBRACK), (']', TokenType.OBRACK),
    ('+', TokenType.PLUS), ('-', TokenType.MINUS),
    ('*', TokenType.STAR), ('/', TokenType.DIV),
    ('^', TokenType.POWER), ('**', TokenType.POWER_STAR),
    ('@', TokenType.CONCAT), ('@@', TokenType.DOUBLE_CONCAT),
    ('%', TokenType.MOD), ('=>', TokenType.ARROW),
    
    ('=', TokenType.EQ), ('!=', TokenType.NEQ),
    ('<', TokenType.LE), ('<=', TokenType.LEQ),
    ('>', TokenType.GR), ('>=', TokenType.GEQ),
    ('==', TokenType.EQEQ), ('=:', TokenType.DEST_EQ),

    ('&', TokenType.AND), 
    ('|', TokenType.OR), 
    ('!', TokenType.NOT),
]

keywords = [
    
]