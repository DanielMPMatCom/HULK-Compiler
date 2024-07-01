from cmp.utils import Token
from cmp.automata import State
from hulk.lexer.regex import Regex


class Lexer:
    def __init__(self, table, eof, parser):
        self.eof = eof
        self.cont = 0
        self.regexs = self._build_regexs(table)
        self.automaton = self._build_automaton()
        self.parser = parser

    def _build_regexs(self, table):
        regexs = []
        print(" ========== " + str(self.cont) + " ========== ")
        for n, (token_type, regex, is_regex) in enumerate(table):
            states = State.from_nfa(Regex(regex, is_regex, self.parser).automaton)
            for v in states:
                if v.final:
                    v.tag = (n, token_type)
            regexs.append(states)
        return regexs

    def _build_automaton(self):
        start = State("start")
        for regex in self.regexs:
            start.add_epsilon_transition(regex)
        return start.to_deterministic()

    def _walk(self, string):
        state = self.automaton
        final = state if state.final else None
        final_lex = lex = ""
        for symbol in string:
            new_state = state[symbol]
            if new_state is not None and new_state[0] is not None:
                new_state = new_state[0]
                lex += symbol

                if new_state.final:
                    # Check tag
                    final = new_state
                    final_lex = lex
                state = new_state
            else:
                break

        return final, final_lex

    def _tokenize(self, text):
        while text:
            final, final_lex = self._walk(text)
            if len(final_lex) == 0:
                # Error
                break
            n, token_type = min(final.tag)
            text = text[len(final_lex) :]
            yield final_lex, token_type
        yield "$", self.eof

    def __call__(self, text):
        return [Token(lex, token_type) for lex, token_type in self._tokenize(text)]
