from cmp.utils import Token
from cmp.pycompiler import Grammar

from hulk.regex.regex_ast import evaluate_reverse_parse
from hulk.regex.regex_ast import *
from hulk.parser.lr1 import LR1Parser

EPSILON = 'ε'

def build_grammar():
    G = Grammar()

    E = G.NonTerminal('E', True)
    T, F, A, X, Y, Z = G.NonTerminals('T F A X Y Z')
    pipe, star, opar, cpar, symbol, epsilon = G.Terminals('| * ( ) symbol ε')

    E %= T + X, lambda h,s: s[2], None, lambda h,s: s[1]
    X %= pipe + T + X, lambda h,s: s[3], None, None, lambda h,s: UnionNode(h[0], s[2])
    X %= G.Epsilon, lambda h,s: h[0]
    T %= F + Y, lambda h,s: s[2], None, lambda h,s: s[1]
    Y %= F + Y, lambda h,s: s[2], None, lambda h,s: ConcatNode(h[0], s[1])
    Y %= G.Epsilon, lambda h,s: h[0]
    F %= A + Z, lambda h,s: s[2], None, lambda h,s: s[1]
    Z %= star, lambda h,s: ClosureNode(h[0]), None
    Z %= G.Epsilon, lambda h,s: h[0]
    A %= opar + E + cpar, lambda h,s: s[2], None, None, None
    A %= symbol, lambda h,s: SymbolNode(s[1]), None 
    A %= epsilon, lambda h,s: EpsilonNode(EPSILON), None

    return G

def regex_tokenizer(text, G, skip_whitespaces=True):
    tokens = []

    fixed_tokens = {x: Token(x, G[x]) for x in ['|', '*', '(', ')', 'ε']}

    for char in text:
        if skip_whitespaces and char.isspace():
            continue
        if char in fixed_tokens.keys():
            tokens.append(fixed_tokens[char])
        else:
            tokens.append(Token(char, G['symbol']))

    tokens.append(Token('$', G.EOF))
    return tokens

G = build_grammar()
L = LR1Parser(G)

class Regex:
    def __init__(self, regex, skip_whitespaces=False):
        self.regex = regex
        self.automaton = self.build_automaton(regex)

    def __call__(self, text):
        self.automaton.recognize(text)

    @staticmethod
    def build_automaton(regex, skip_whitespaces=False):
        tokens = regex_tokenizer(regex, G, skip_whitespaces=False)
        lr1 = L(tokens)
        ast = evaluate_reverse_parse(lr1, tokens)
        nfa = ast.evaluate()
        dfa = nfa_to_dfa(nfa)
        dfa = automaton_minimization(dfa)
        return dfa   
        