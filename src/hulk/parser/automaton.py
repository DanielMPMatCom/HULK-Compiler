from shift_reduce import ShiftReduceParser
from cmp.automata import State, multiline_formatter
from cmp.pycompiler import Item, Grammar
from cmp.utils import ContainerSet
def compute_local_first(firsts, alpha):
    """Computes First(alpha), given First(Vt) and First(Vn) alpha in (Vt U Vn)* """

    first_alpha = ContainerSet()
    
    try:
        alpha_is_epsilon = alpha.IsEpsilon
    except:
        alpha_is_epsilon = False
        
    if alpha_is_epsilon:
        first_alpha.set_epsilon(True)

    for symbol in alpha:
        first_symbol = firsts[symbol]
        first_alpha.update(first_symbol)
        if not first_symbol.contains_epsilon:
            break

    return first_alpha


def compute_firsts(G):
    """ Computes First(Vt) U First(Vn) U First(alpha) P: X -> alpha """
    firsts = {}
    change = True
    
    for terminal in G.terminals:
        firsts[terminal] = ContainerSet(terminal)
        
    for nonterminal in G.nonTerminals:
        firsts[nonterminal] = ContainerSet()
    
    while change:
        change = False
        
        for production in G.Productions:
            X = production.Left
            alpha = production.Right
            
            first_X = firsts[X]
                
            try:
                first_alpha = firsts[alpha]
            except KeyError:
                first_alpha = firsts[alpha] = ContainerSet()
            
            local_first = compute_local_first(firsts, alpha)
            
            change |= first_alpha.hard_update(local_first)
            change |= first_X.hard_update(local_first)
                    
    return firsts

def expand(item: Item, firsts: ContainerSet):
    """Given a LR(1) item, returns the set of items that can be expanded from it."""
    """ expand("$Y \to \alpha . X \delta, c$") = { "$X \to . \beta, b$" | $b \in First(\delta c)$ }"""
    next_symbol = item.NextSymbol
    if next_symbol is None or not next_symbol.IsNonTerminal:
        return []

    lookaheads = ContainerSet()
    for symbol in item.Preview():
        lookaheads.update(compute_local_first(firsts, symbol))
    assert not lookaheads.contains_epsilon

    return [Item(p, 0, lookaheads) for p in next_symbol.productions]


def compress(items):
    """ Given a set of items, it returns a set of items with the same core"""
    centers = {}

    for item in items:
        center = item.Center()
        try:
            lookaheads = centers[center]
        except KeyError:
            centers[center] = lookaheads = set()
        lookaheads.update(item.lookaheads)

    return {
        Item(x.production, x.pos, set(lookahead)) for x, lookahead in centers.items()
    }


def closure_lr1(items, firsts):
    """ Computes the closure of a LR(1) item set """
    closure = ContainerSet(*items)

    changed = True
    while changed:
        changed = False

        new_items = ContainerSet()
        for item in closure:
            suggestions = expand(item, firsts)
            new_items.update(ContainerSet(*suggestions))

        changed = closure.update(new_items)

    return compress(closure)


def goto_lr1(items, symbol, firsts=None, just_kernel=False):
    """ Given a LR(1) item set and a symbol X, computes the goto set """
    assert (
        just_kernel or firsts is not None
    ), "`firsts` must be provided if `just_kernel=False`"
    items = frozenset(item.NextItem() for item in items if item.NextSymbol == symbol)
    return items if just_kernel else closure_lr1(items, firsts)


def build_LR1_automaton(G):
    """ Builds the LR(1) automaton for a given grammar G """

    assert len(G.startSymbol.productions) == 1, "Grammar must be augmented"

    firsts = compute_firsts(G)

    firsts[G.EOF] = ContainerSet(G.EOF)

    start_production = G.startSymbol.productions[0]

    start_item = Item(start_production, 0, lookaheads=(G.EOF,))

    start = frozenset([start_item])

    closure = closure_lr1(start, firsts)

    automaton = State(frozenset(closure), True)

    pending = [start]

    visited = {start: automaton}

    while pending:

        current = pending.pop()

        current_state = visited[current]

        closure = closure_lr1(current, firsts)
        for symbol in G.terminals + G.nonTerminals:
            next_state_goto = goto_lr1(closure, symbol, just_kernel=True)
            if len(next_state_goto) <= 0:
                continue

            if next_state_goto not in visited.keys():
                current_state_clousure = closure_lr1(next_state_goto, firsts)
                next_state = State(frozenset(current_state_clousure), True)
                visited[next_state_goto] = next_state
                pending.append(next_state_goto)
            else:
                next_state = visited[next_state_goto]

            # SIN CONTAR LA CLOUSURE
            # next_state_goto = frozenset(goto_lr1(current_state.state, symbol, firsts))
            # if len(next_state_goto) <= 0:
            #     continue
            # if next_state_goto not in visited.keys():
            #     pending.append(next_state_goto)
            #     next_state = State(next_state_goto, True)
            #     visited[next_state_goto] = next_state
            # else:
            #     next_state = visited[next_state_goto]

            current_state.add_transition(symbol.Name, next_state)

    automaton.set_formatter(multiline_formatter)
    return automaton
