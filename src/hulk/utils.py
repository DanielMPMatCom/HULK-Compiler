from cmp.utils import Token as BaseToken

EPSILON = 'ε'

class Token(BaseToken):
    def __init__(self, lex, token_type, row, column):
        super().__init__(lex, token_type)
        self.row = row
        self.column = column