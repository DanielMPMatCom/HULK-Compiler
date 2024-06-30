from cmp.pycompiler import Grammar
from hulk.lexer.regex_ast import *

def build_regex_grammar():
    G = Grammar()

    Automaton = G.NonTerminal('E', True)
    Union, Concat, Closure, Atom = G.NonTerminals('Union Concat Closure Atom')
    pipe, star, opar, cpar, symbol, epsilon = G.Terminals('| * ( ) symbol ε')

    # -------------------- PRODUCTIONS -------------------- #

    Automaton %= Union, lambda h,s: s[1]
    
    Union %= Union + pipe + Concat, lambda h,s: UnionNode(s[1], s[3]) 
    Union %= Concat, lambda h,s: s[1]
    
    Concat %= Concat + Closure, lambda h,s: ConcatNode(s[1], s[2])
    Concat %= Closure, lambda h,s: s[1]

    Closure %= Atom + star, lambda h,s: ClosureNode(s[1])
    Closure %= Atom, lambda h,s: s[1]
    
    Atom %= opar + Automaton + cpar, lambda h,s: s[2]
    Atom %= symbol, lambda h,s: SymbolNode(s[1])
    Atom %= epsilon, lambda h,s: EpsilonNode(s[1])

    return G

G = build_regex_grammar()