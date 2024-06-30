from cmp.tools.parsing import LR1Parser
from cmp.evaluation import evaluate_reverse_parse
from hulk.lexer.automaton import nfa_to_dfa, automata_minimization

from lexer.regex_tokenizer import regex_tokenizer
from lexer.regex_grammar import G

class Regex:
    def __init__(self, regex:str, is_regex:bool=False):
        self.is_regex = is_regex
        self.regex = regex
        self.automaton = self._build_automaton()
    
    def _build_automaton(self):
        tokens = regex_tokenizer(self.regex, G, self.is_regex, skip_whitespaces=True)
        parser = LR1Parser(G)
        parse, operations = parser([t.token_type for t in tokens], get_shift_reduce=True) 
        ast = evaluate_reverse_parse(parse, operations, tokens)
        nfa = ast.evaluate()
        dfa = nfa_to_dfa(nfa)
        dfa = automata_minimization(dfa)

        # ---------- JUST FOR TESTING ---------- #
        self.ast = ast
        # -------------------------------------- #

        return dfa