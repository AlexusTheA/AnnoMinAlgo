from heapq import heappop, heappush

from config import (
    GOAL_AMOUNT, GOAL_TYPE, GOODS_INDEX, MAX_ITERATIONS, MAX_SOLUTION_TIME,
    PROGRESS_PRINT_INTERVAL,
)
from heuristics import h
from models import Action, ActionKind, State
from simulation import successors


def is_target(state: State) -> bool:
    return state.stock[GOODS_INDEX[GOAL_TYPE]] >= GOAL_AMOUNT


def a_asterisk(start: State, heuristic=h, expand=successors):
    """Findet den schnellsten Weg zum Ziel. Gibt (Zeit, came_from, Zielzustand) zurück
    oder None, wenn keine Lösung innerhalb der Grenzen gefunden wurde."""
    counter = 0
    open_queue = [(heuristic(start), counter, 0, start)]   # (f, Zähler, g, Zustand)
    g_score: dict[State, int] = {start: 0}
    came_from: dict[State, tuple[State, ActionKind]] = {}
    iterations = 0

    while open_queue:
        _, _, g, current = heappop(open_queue)
        if g > g_score[current]:
            continue                      # veralteter Eintrag, besserer Weg wurde schon gefunden

        if is_target(current):
            return g, came_from, current, iterations  # erster Zielzustand ist optimal (zulässige Heuristik)

        iterations += 1
        if iterations % PROGRESS_PRINT_INTERVAL == 0:
            print(f"iteration: {iterations}, queue: {len(open_queue)}, zustände: {len(g_score)}, g: {g}")
        if iterations > MAX_ITERATIONS:
            print("abgebrochen: zu viele Iterationen")
            return None

        for action, following, price in expand(current):
            new_g = g + price
            if new_g >= g_score.get(following, float("inf")):
                continue
            new_f = new_g + heuristic(following)
            if new_f > MAX_SOLUTION_TIME:
                continue                  # obere Schranke schon beim Einfügen
            g_score[following] = new_g
            came_from[following] = (current, action)
            counter += 1
            heappush(open_queue, (new_f, counter, new_g, following))

    return None