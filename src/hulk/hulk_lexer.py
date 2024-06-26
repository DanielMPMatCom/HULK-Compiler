from cmp.utils import Token
from cmp.automata import State
from hulk.regex.regex import *

class Lexer:
    def __init__(self, table, eof):
        self.eof = eof
        self.regexs = self._build_regexs(table)
        self.automaton = self._build_automaton()

    def _build_regexs(self, table):
        regexs = []

        for n, (token_type, regex) in enumerate(table):
            _automaton = State.from_nfa(Regex(regex).automaton)
            for state in _automaton:
                if state.final:
                    state.tag(n, token_type)
                regexs.append(state)
        
        return regexs
        
    def _build_automaton(self):
        start = State('start')

        for v in self.regexs:
            start.add_epsilon_transition(v)
        return start.to_deterministic()
    
    def _walk(self, string):
        state = self.automaton
        final = state if state.final else None
        final_lex = lex = ''

        for symbol in string:
            _state = state[symbol]
            if _state is not None and _state[0] is not None:
                _state = _state[0]
                lex += symbol

                if _state.final:
                    final = _state
                    final_lex = lex

                state = _state
        
        return final, final_lex
    
    def _select_row_and_col(self, text, row, col):
        for letter in text:
            if letter == '\n':
                row += 1
                col = 1
            else:
                col += 1

        return row, col

    def _tokenize(self, text):
        row, col = 1, 1
        while text: 
            if text[0] == '\n':
                row, col = self._select_row_and_col(text[0], row, col)
                text = text[1:]
                continue
            final, final_lex = self._walk(text)
            if final == None:
                raise f'invalid token line {row}, column {col}'

            _, token_type = min(final.tag)
            text = text[len(final_lex):]
            yield final_lex, token_type
        yield '$', self.eof


    def __call__(self, text):
        return [Token(lex, ttype) for lex, ttype in self._tokenize(text)]