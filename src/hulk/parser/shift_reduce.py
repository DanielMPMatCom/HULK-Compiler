from serialized.Serialized import Serialized
from hulk.hulk_grammar import Grammar


class ShiftReduceParser:
    SHIFT = "SHIFT"
    REDUCE = "REDUCE"
    OK = "OK"

    def __init__(self, G: Grammar, verbose=False, load=False, save=False):
        self.G = G
        self.verbose = verbose
        self.action = {}
        self.goto = {}
        self.errors = []

        print("LOADING PARSING ...")
        serialized_instance = Serialized()
        if load:
            try:
                # rebuild Grammar
                stored_action = serialized_instance.load_object("action")
                productions = G.Productions

                for key, value in stored_action.items():
                    state, symbol = key
                    action, tag = value

                    if action == ShiftReduceParser.REDUCE:
                        tag = list(filter(lambda x: str(x) == str(tag), productions))[0]

                    self.action[state, G[str(symbol)]] = action, tag
                print(self.action)
                stored_goto = serialized_instance.load_object("goto")

                for key, value in stored_goto.items():
                    state, symbol = key
                    self.goto[state, G[str(symbol)]] = value

            except:
                load = False
                save = True
                print("Error loading the parsing table")
        else:
            self._build_parsing_table()

        if save:
            serialized_instance.save_object(self.action, "action")
            serialized_instance.save_object(self.goto, "goto")

        print("PARSER LOADED OK!")

    def _build_parsing_table(self):
        raise NotImplementedError()

    def notify_unexpected_symbols(self, current_token, expected_symbol):
        error = f"Unexpected symbol {current_token.token_type} with value {current_token.lex}, At row {current_token.row} and column {current_token.column}. Expected {expected_symbol}"
        self.errors.append(error)
        return

    def find_unexpected_symbol_and_notify(self, state, token):
        error = f"Unexpected symbol {token.lex} at row {token.row} and column {token.column}"
        possibilities = list(filter(lambda x: x[0] == state, self.action.keys()))
        error += " Possibilities result " + str([x[1] for x in possibilities])
        self.errors.append(error)

    def trackSymbols(self, state, lookahead):
        filtes = list(filter(lambda x: x[0] == state, self.action))
        for f in filtes:
            print(" - - - - - - - - - -")
            print("Filter: ", f[1], "Lookahead: ", lookahead)
            print("Filter Type: ", type(f[1]), "Lookahead Type: ", type(lookahead))
            print(
                "Are equals: ",
                f[1] == lookahead,
                "Are equals type: ",
                type(f[1]) == type(lookahead),
                "Are equals str: ",
                str(f[1]) == str(lookahead),
            )

    def refreshSymbol(self, state, lookahead):
        filters = list(
            filter(lambda x: x[0] == state and str(x[1]) == str(lookahead), self.action)
        )
        if len(filters) == 0:
            return (state, lookahead)
        return (state, filters[0][1])

    def force_ok_action(self):
        ok_action, lookahead = list(
            filter(lambda x: x[1] == self.G.EOF, self.action.keys())
        )[0]

        return (ok_action, lookahead)

    def reset_state(self, w, cursor, state):
        while cursor < len(w) and w[cursor] != self.G.EOF:
            cursor += 1
            if (state, w[cursor]) in self.action:
                return (state, cursor)
            elif (0, w[cursor]) in self.action:
                return (0, cursor)
        return (None, None)

    def __call__(self, tokens):
        self.errors = []
        stack = [0]
        cursor = 0
        output = []
        operations = []
        w = [t.token_type for t in tokens]

        while True:
            state = stack[-1]
            lookahead = w[cursor]

            if self.verbose:
                print(stack, "<---||--->", w[cursor:])

            # Your code here!!! (Detect error)
            if (state, lookahead) not in self.action:
                self.find_unexpected_symbol_and_notify(state, tokens[cursor])
                # state, cursor = self.reset_state(w, cursor, state)
                # if state is None or cursor is None:
                #     return [], []
                # lookahead = w[cursor]
                return [], []

            action, tag = self.action[state, lookahead]

            # Your code here!!! (Shift case)
            if action == ShiftReduceParser.SHIFT:
                if self.verbose:
                    print("SHIFT")
                stack.append(lookahead)
                stack.append(tag)
                cursor += 1
                operations.append(ShiftReduceParser.SHIFT)

            # Your code here!!! (Reduce case)
            elif action == ShiftReduceParser.REDUCE:
                production = tag
                if self.verbose:
                    print("REDUCE")
                    print("Production: ", production)
                    print("Production Left: ", production.Left)
                    print("Production Right: ", production.Right)

                for expected_symbol in reversed(production.Right):
                    stack.pop()  # Remove the state
                    symbol = stack.pop()
                    if self.verbose:
                        print("Symbol: ", symbol, "Expected Symbol: ", expected_symbol)
                    if symbol != expected_symbol:
                        self.notify_unexpected_symbols(tokens[cursor], expected_symbol)
                        # return [], []
                state = stack[-1]
                stack.append(production.Left)
                try:
                    stack.append(self.goto[state, production.Left])
                except KeyError:
                    print(
                        "Error: No transition for", production.Left, "at state", state
                    )
                    print(
                        "Possible symbols are",
                        list(filter(lambda x: x[0] == state, self.goto)),
                    )
                    return [], []
                output.append(production)
                operations.append(ShiftReduceParser.REDUCE)

            # Your code here!!! (OK case)
            elif action == ShiftReduceParser.OK:
                # operations.append(ShiftReduceParser.OK) # Not necessary to append OK
                return output, operations

            # Your code here!!! (Invalid case)
            else:
                raise ValueError("Unknown action", action)
