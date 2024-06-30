from cmp.utils import Token
from cmp.pycompiler import Grammar

def regex_tokenizer(text:str, G:Grammar, is_regex:bool, symbol:str='symbol', skip_whitespaces:bool=True):
    tokens = []

    for char in text:
        if skip_whitespaces and char.isspace():
            continue
        
        token = Token(char, G[symbol] if G[char] is None or not is_regex else G[char])
        tokens.append(token)

    tokens.append(Token('$', G.EOF))
    return tokens