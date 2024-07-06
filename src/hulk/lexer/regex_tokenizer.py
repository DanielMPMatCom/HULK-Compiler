from hulk.utils import Token
from cmp.pycompiler import Grammar

def regex_tokenizer(text:str, G:Grammar, is_regex:bool, skip_whitespaces:bool=True):
    
    tokens = []

    fixed_tokens = {x: G[x] for x in ['\\' ,'|', '*', '(', ')', 'ε']}

    column = 1
    for char in text:

        if skip_whitespaces and char.isspace():
            continue
       
        if char in fixed_tokens.keys() and is_regex:
            tokens.append(Token(char, fixed_tokens[char], row=1, column=column))
        else:
            tokens.append(Token(char, G['symbol'], row=1, column=column))

        column += 1

    tokens.append(Token('$', G.EOF, row=1, column=column))
    return tokens