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
        print(" LOADING PARSING ...")
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
        print(
            "Unexpected symbol",
            current_token.token_type,
            "At row ",
            current_token.row,
            " column ",
            current_token.column,
            ", value ",
            current_token.lex,
            ". Expected",
            expected_symbol,
        )

    def find_unexpected_symbol_and_notify(self, state, token):
        print(
            "Unexpected symbol",
            token.lex,
            " at row ",
            token.row,
            " and column",
            token.column,
        )
        posibilities = list(filter(lambda x: x[0] == state, self.action.keys()))
        print("Posibilities result ", [x[1] for x in posibilities])

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

    def __call__(self, tokens):
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
                return

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
                    return
                output.append(production)
                operations.append(ShiftReduceParser.REDUCE)

            # Your code here!!! (OK case)
            elif action == ShiftReduceParser.OK:
                # operations.append(ShiftReduceParser.OK) # Not necessary to append OK
                return output, operations

            # Your code here!!! (Invalid case)
            else:
                raise ValueError("Unknown action", action)
