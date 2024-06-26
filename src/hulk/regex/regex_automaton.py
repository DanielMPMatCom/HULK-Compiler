from cmp.utils import ContainerSet, DisjointSet

class NFA:

    def __init__(self, states, finals, transitions, start=0):
        self.states = states
        self.start = start
        self.finals = set(finals)
        self.map = transitions
        self.vocabulary = set()
        self.transitions = { state: {} for state in range(states) }
        
        for (origin, symbol), destinations in transitions.items():
            assert hasattr(destinations, '__iter__'), 'Invalid collection of states'
            self.transitions[origin][symbol] = destinations
            self.vocabulary.add(symbol)
            
        self.vocabulary.discard('')
        
    def epsilon_transitions(self, state):
        assert state in self.transitions, 'Invalid state'
        try:
            return self.transitions[state]['']
        except KeyError:
            return ()

    def _repr_svg_(self):
        try:
            return self.graph().create_svg().decode('utf8')
        except:
            pass

class DFA(NFA):

    def __init__(self, states, finals, transitions, start=0):
        assert all(isinstance(value, int) for value in transitions.values())
        assert all(len(symbol) > 0 for origin, symbol in transitions)
        
        transitions = { key: [value] for key, value in transitions.items() }
        NFA.__init__(self, states, finals, transitions, start)
        self.current = start
    
    def _move(self, symbol):
        if symbol not in self.transitions[self.current].keys():
            return False
        
        self.current = self.transitions[self.current][symbol][0]
        return True
    
    def _reset(self):
        self.current = self.start

    def recognize(self, string):
        self._reset()
        for symbol in string:
            if not self._move(symbol):
                return False
        return self.current in self.finals
    
def move(automaton, states, symbol):
    moves = set()
    for state in states:
        if symbol in automaton.transitions[state].keys():
            moves.add(automaton.transitions[state][symbol])
    
    return moves

def epsilon_closure(automaton, states):
    pending = [s for s in states]
    closure = {s for s in states}

    while pending:
        state = pending.pop()

        _states = move(automaton, [state], '') - closure
        pending += _states
        closure.update(_states)

    return ContainerSet(*closure)
        
def nfa_to_dfa(automaton):
    transitions = {}

    start = epsilon_closure(automaton, [automaton.start])
    start.id = 0
    start.is_final = any(s in automaton.finals for s in start)

    states = [start]
    pending = [start]

    while pending:
        state = pending.pop()

        for symbol in automaton.vocabulary:
            closure = epsilon_closure(automaton, move(automaton, state, symbol))
        
            if not closure:
                continue

            if closure not in states:
                closure.id = len(states)
                closure.is_final = any(x in automaton.finals for x in closure)
                states.append(closure)
                pending.append(closure)

            else:
                closure.id = states.index(closure)

            try:
                transitions[state.id, symbol]
                assert False, 'Invalid DFA!!!'
            except:
                transitions[state.id, symbol] = closure

    finals = [state.id for state in states if state.is_final]
    
    return DFA(len(states), finals, transitions)


def automaton_union(a1, a2):
    transitions = {}

    start = 0
    d1 = 1
    d2 = a1.states + d1
    final = a2.states + d2

    for (origin, symbol), destination in a1.map.items():
        transitions[(origin + d1), symbol] = [x + d1 for x in destination]

    for (origin, symbol), destination in a2.map.items():
        transitions[(origin + d2), symbol] = [x + d2 for x in destination]

    transitions[(start, '')] = [d1, d2]

    for state in a1.final:
        _state = state + d1
        try:
            transitions[(_state, '')].extend([final])
        except:
            transitions[(_state, '')] = [final]

    for state in a2.final:
        _state = state + d2
        try:
            transitions[(_state, '')].extend([final])
        except:
            transitions[(_state, '')] = [final]

    states = final + 1
    finals = {final}

    return NFA(states, finals, transitions, start)

def automaton_concatenation(a1, a2):
    transitions = {}

    start = 0
    d1 = 1
    d2 = a1.states + d1
    final = a2.states + d2

    for (origin, symbol), destination in a1.map.items():
        transitions[(origin + d1), symbol] = [x + d1 for x in destination]

    for (origin, symbol), destination in a2.map.items():
        transitions[(origin + d2), symbol] = [x + d2 for x in destination]

    for state in a1.finals:
        _state = state + d1
        try:
            transitions[(_state, '')].extend([d2])
        except:
            transitions[(_state, '')] = [d2]

    for state in a2.finals:
        _state = state + d2
        try:
            transitions[(_state, '')].extend([final])
        except:
            transitions[(_state, '')] = [final]

    states = final + 1
    finals = {final}

    return NFA(states, finals, transitions, start)

def automaton_closure(a1):
    transitions = {}

    start = 0
    d1 = 1
    final = a1.states + d1

    for (origin, symbol), destination in a1.map.items():
        transitions[(origin + d1), symbol] = [x + d1 for x in destination]

    transitions[(start, '')] = [d1, final]

    for state in a1.finals:
        _state = state + d1
        try:
            transitions[(start, '')].extend([final])
        except:
            transitions[(start, '')] = [final]

    transitions[(final, '')] = [start]

    states = final + 1
    finals = {final}

    return NFA(states, finals, transitions, start)

def distinguish_states(group, automaton, partition):
    split = {}
    vocabulary = tuple(automaton.vocabulary)

    for member in group:
        key = []
        _member = member.value

        for symbol in vocabulary:
            parent = -1

            if symbol in automaton.transitions[member]:
                parent = partition[automaton.transition[member][symbol][0]].representative
            
            key.append(parent)

        key = tuple(key)
        
        try: 
            split[key].append(member)
        except:
            split[key] = [member]

    return [group for group in split.values()]

def state_minimization(automaton):
    partition = DisjointSet(*range(automaton.states))
    partition.merge(automaton.finals)
    partition.merge(set(range(automaton.states)) - automaton.finals)

    while True:
        _partition = DisjointSet(*range(automaton.states))

        for group in partition.groups:
            for subgroup in distinguish_states(group, automaton, partition):
                _partition.merge(subgroup)

        if len(_partition) == len(partition):
            break

        partition = _partition

    return partition

def automaton_minimization(automaton):
    partition = state_minimization(automaton)
    states = [s for s in partition.representatives]
    transitions = {}

    for i, state in enumerate(states):
        origin = state.value
        for symbol, destination in automaton.transitions[origin].items():
            destination = partition[destination[0]].representative

            try:
                transitions[(i, symbol)]
                assert False
            except:
                transitions[(i, symbol)] = states.index(destination)

    finals = [state.index(partition[x].representative) for x in automaton.finals]
    start = states.index(partition[automaton.start].representative)

    return DFA(len(states), finals, transitions, start)

