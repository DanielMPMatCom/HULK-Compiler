from cmp.utils import Token
from cmp.pycompiler import Grammar

def regex_tokenizer(text:str, G:Grammar, is_regex:bool, skip_whitespaces:bool=True):
    
    tokens = []

    fixed_tokens = {x: Token(x, G[x]) for x in ['|', '*', '(', ')', 'ε']}

    for char in text:
        if skip_whitespaces and char.isspace():
            continue
       
        if char in fixed_tokens.keys() and is_regex:
            tokens.append(fixed_tokens[char])
        else:
            tokens.append(Token(char, G['symbol']))

    tokens.append(Token('$', G.EOF))
    return tokens