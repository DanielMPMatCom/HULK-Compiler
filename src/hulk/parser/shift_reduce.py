from serialized.Serialized import Serialized


class ShiftReduceParser:
    SHIFT = "SHIFT"
    REDUCE = "REDUCE"
    OK = "OK"

    def __init__(self, G, verbose=False, load=False, save=False):
        self.G = G
        self.verbose = verbose
        self.action = {}
        self.goto = {}

        serialized_instance = Serialized()
        if load:
            try:
                self.action = serialized_instance.load_object("action")
                self.goto = serialized_instance.load_object("goto")
            except:
                load = False
                save = True
        else:
            self._build_parsing_table()

        if save:
            serialized_instance.save_object(self.action, "action")
            serialized_instance.save_object(self.goto, "goto")

    def _build_parsing_table(self):
        raise NotImplementedError()

    def notify_unexpected_symbols(self, current_token, expected_symbol):
        print(
            "Unexpected symbol",
            current_token,
            "Expected",
            expected_symbol,
        )

    def find_unexpected_symbol_and_notify(self, state, row, column):
        state_expected, token_expected = filter(
            self.action.keys(), lambda x: x[0] == state
        )[0]
        self.notify_unexpected_symbols(state_expected, token_expected)

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
                self.find_unexpected_symbol_and_notify(state)
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
                        self.notify_unexpected_symbols(w[cursor], expected_symbol)
                        return [], []
                state = stack[-1]
                stack.append(production.Left)
                stack.append(self.goto[state, production.Left])

                output.append(production)
                operations.append(ShiftReduceParser.REDUCE)

            # Your code here!!! (OK case)
            elif action == ShiftReduceParser.OK:
                # operations.append(ShiftReduceParser.OK) # Not necessary to append OK
                return output, operations

            # Your code here!!! (Invalid case)
            else:
                raise ValueError("Unknown action", action)
