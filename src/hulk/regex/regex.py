from cmp.utils import Token
from cmp.pycompiler import Grammar

from hulk.regex.regex_ast import evaluate_reverse_parse
from hulk.regex.regex_ast import *
from hulk.parser.lr1 import LR1Parser

EPSILON = 'ε'

def build_grammar():

    Automaton = G.NonTerminal('Automaton', startSymbol=True)
    Concat, Union, Clousure, Range, Atom= G.NonTerminals('Concat Union Clousure Range Atom')
    symbol, pipe, plus, minus, star, opar, cpar = G.Terminals('symbol | + - * ( )')

    Automaton %= Union, lambda h,s: s[1]

    Union %= Union + pipe + Concat, lambda h,s: UnionNode(s[1], s[3])
    Union %= Concat, lambda h,s: s[1]

    Concat %= Concat + plus + Clousure, lambda h,s: ConcatNode(s[1], s[3])
    Concat %= Clousure, lambda h,s: s[1]

    Clousure %= Clousure + star, lambda h,s: ClosureNode(s[1])
    Clousure %= Range, lambda h,s: s[1]

    Range %= symbol + minus + symbol, lambda h,s: RangeNode(s[1], s[3])
    Range %= Atom, lambda h,s: s[1]

    Atom %= symbol, lambda h,s: SymbolNode(s[1])
    Atom %= opar + Automaton + cpar, lambda h,s: s[2]

    return G

def regex_tokenizer(text, G, skip_whitespaces=True):
    tokens = []

    fixed_tokens = {x: Token(x, G[x]) for x in ['|', '*', '+', '-', '(', ')']}

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
        lr1, operations = L(tokens)
        ast = evaluate_reverse_parse(lr1, operations, tokens)
        nfa = ast.evaluate()
        dfa = nfa_to_dfa(nfa)
        dfa = automaton_minimization(dfa)
        return dfa   