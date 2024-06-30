from hulk.lexer.automaton import NFA

def automata_union(a1, a2):
    transitions = {}

    start = 0
    d1 = 1
    d2 = a1.states + d1
    final = a2.states + d2

    for (origin, symbol), destination in a1.map.items():
        transitions[(origin + d1, symbol)] = [x + d1 for x in destination]

    for (origin, symbol), destination in a2.map.items():
        transitions[(origin + d2, symbol)] = [x + d2 for x in destination]

    transitions[(start, '')] = [d1, d2]

    for state in a1.finals:
        new_state = state + d1
        try:
            transitions[(new_state, '')].append(final)
        except:
            transitions[(new_state, '')] = [final]

    for state in a2.finals:
        new_state = state + d2
        try:
            transitions[(new_state, '')].append(final)
        except:
            transitions[(new_state, '')] = [final]

    states = final + 1
    finals = {final}

    return NFA(states, finals, transitions, start)

def automata_concatenation(a1, a2):
    transitions = {}

    start = 0
    d1 = 0
    d2 = a1.states + d1
    final = a2.states + d2

    for (origin, symbol), destinations in a1.map.items():
        transitions[(origin, symbol)] = [x for x in destinations]

    for (origin, symbol), destinations in a2.map.items():
        transitions[(origin + d2, symbol)] = [x + d2 for x in destinations]

    for state in a1.finals:
        try:
            transitions[(state, '')].append(d2)
        except:
            transitions[(state, '')] = [d2]

    for state in a2.finals:
        new_state = state + d2
        try:
            transitions[(new_state, '')].append(final)
        except:
            transitions[(new_state, '')] = [final]

    states = final + 1
    finals = {final}

    return NFA(states, finals, transitions, start)

def automata_closure(a1):
    transitions = {}

    start = 0
    d1 = 1
    final = a1.states + d1

    for (origin, symbol), destinations in a1.map.items():
        transitions[(origin + d1, symbol)] = [x + d1 for x in destinations]

    transitions[(start, '')] = [d1, final]

    for state in a1.finals:
        new_state = state + d1
        try:
            transitions[(new_state, '')].append(final)
        except:
            transitions[(new_state, '')] = [final]

    transitions[(final, '')] = [start]

    states = final + 1
    finals = {final}

    return NFA(states, finals, transitions, start)

