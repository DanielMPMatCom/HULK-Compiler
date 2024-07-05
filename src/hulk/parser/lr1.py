from hulk.parser.shift_reduce import ShiftReduceParser
from hulk.parser.automaton import build_LR1_automaton

class LR1Parser(ShiftReduceParser):

    def _build_parsing_table(self):
        G = self.G.AugmentedGrammar(True)

        automaton = build_LR1_automaton(G)
        for i, node in enumerate(automaton):
            if self.verbose:
                print(i, "\t", "\n\t ".join(str(x) for x in node.state), "\n")
            node.idx = i

        for node in automaton:
            idx = node.idx
            for item in node.state:
                if item.IsReduceItem:
                    if item.production.Left == G.startSymbol:
                        self._register(
                            self.action, (idx, G.EOF), (ShiftReduceParser.OK, 0)
                        )
                    else:
                        for lookahead in item.lookaheads:
                            self._register(
                                self.action,
                                (idx, lookahead),
                                (ShiftReduceParser.REDUCE, item.production),
                            )
                else:
                    next_symbol = item.NextSymbol
                    next_state = node.get(next_symbol.Name).idx
                    if next_symbol.IsTerminal:
                        self._register(
                            self.action,
                            (idx, next_symbol),
                            (ShiftReduceParser.SHIFT, next_state),
                        )
                    else:
                        self._register(
                            self.goto,
                            (idx, next_symbol),
                            next_state,
                        )

    @staticmethod
    def _register(table, key, value):
        assert (
            key not in table or table[key] == value
        ), "Shift-Reduce or Reduce-Reduce conflict!!!"
        table[key] = value
