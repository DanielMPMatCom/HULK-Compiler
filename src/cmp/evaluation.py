from cmp.pycompiler import EOF
from hulk.parser.shift_reduce import ShiftReduceParser
from hulk.hulk_ast import *
from hulk.utils import Token


def evaluate_reverse_parse(right_parse, operations, tokens):
    if not right_parse or not operations or not tokens:
        return

    right_parse = iter(right_parse)
    tokens = iter(tokens)
    stack = []
    for operation in operations:
        if operation == ShiftReduceParser.SHIFT:
            token = next(tokens)
            stack.append(token.lex)
        elif operation == ShiftReduceParser.REDUCE:
            production = next(right_parse)
            head, body = production
            attributes = production.attributes
            assert all(
                rule is None for rule in attributes[1:]
            ), "There must be only synteticed attributes."
            rule = attributes[0]

            if len(body):
                synteticed = [None] + stack[-len(body) :]
                value = rule(None, synteticed)
                stack[-len(body) :] = [value]
            else:
                stack.append(rule(None, None))
        else:
            raise Exception("Invalid action!!!", operation)

    assert len(stack) == 1
    assert isinstance(next(tokens).token_type, EOF)
    return stack[0]


def stackParser(stack):
    st = []
    for i in stack:
        if isinstance(i, Token):
            st.append(i.lex)
        else:
            st.append(i)
    return st


def evaluate_reverse_parse_plus(right_parse, operations, tokens):
    if not right_parse or not operations or not tokens:
        return

    right_parse = iter(right_parse)
    stack = []
    cursor = 0

    for operation in operations:
        if operation == ShiftReduceParser.SHIFT:
            # print("Shift")
            token = tokens[cursor]
            cursor += 1
            stack.append(token)
        elif operation == ShiftReduceParser.REDUCE:
            # print("Reduce", stack)
            production = next(right_parse)
            head, body = production
            attributes = production.attributes
            assert all(
                rule is None for rule in attributes[1:]
            ), "There must be only synteticed attributes."
            rule = attributes[0]

            if len(body):
                synteticed = [None] + stackParser(stack[-len(body) :])
                value = rule(None, synteticed)

                tmp = stack[-len(body) :][0]
                # print(tmp)

                if isinstance(value, Node):
                    if isinstance(tmp, Node):
                        value.line = tmp.line
                        value.column = tmp.column
                    elif isinstance(tmp, Token):
                        value.line = tmp.row
                        value.column = tmp.column

                stack[-len(body) :] = [value]
            else:
                r = rule(None, None)
                if isinstance(r, Node):
                    r.line = tokens[cursor - 1].row
                    r.column = tokens[cursor - 1].column
                stack.append(r)
        else:
            raise Exception("Invalid action!!!", operation)
    st = stackParser(stack)
    assert len(stack) == 1
    assert isinstance(tokens[cursor].token_type, EOF)
    return stack[0]
