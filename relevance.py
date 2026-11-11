"""Automatische Einschränkung der Aktionen auf das, was dem Ziel überhaupt helfen kann."""
from buildings import BUILDING_TYPES
from models import ActionKind
from simulation import calc_actions, calc_state


def relevant_goods(goal: str) -> set[str]:
    """Alle Güter, die direkt oder indirekt für das Zielgut gebraucht werden."""
    relevant, todo = set(), [goal]
    while todo:
        good = todo.pop()
        if good in relevant:
            continue
        relevant.add(good)
        for btype in BUILDING_TYPES.values():
            if good in btype.output:                  # Wer produziert das Gut ...
                todo += list(btype.build_cost)        # ... was kostet der Bau,
                todo += list(btype.input)             # ... was braucht er als Input,
                if btype.required_humans:             # ... und braucht er Menschen?
                    todo.append("human")
    return relevant


def make_expand(goal: str):
    """Nachfolgerfunktion, die nur zielrelevante Bau- und Abriss-Aktionen zulässt."""
    relevant = relevant_goods(goal)
    build_ok = {k for k, t in BUILDING_TYPES.items() if set(t.output) & relevant}
    delete_ok = {k for k, t in BUILDING_TYPES.items() if set(t.build_cost) & relevant}

    def expand(state):
        result = []
        for action in calc_actions(state):
            if action.kind == ActionKind.BUILD and action.target.kind not in build_ok:
                continue
            if action.kind == ActionKind.DELETE and action.target.kind not in delete_ok:
                continue
            result.append((action.kind, calc_state(state, action), action.duration))
        return result

    return expand