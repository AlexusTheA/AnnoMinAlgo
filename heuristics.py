import math

from buildings import BUILDING_TYPES
from config import BUILD_TIME, DELETE_TIME, GOAL_AMOUNT, GOODS_INDEX
from models import Kind, State
from simulation import type_of

WOOD = GOODS_INDEX["wood"]
TOOL = GOODS_INDEX["tool"]
LUMBER = BUILDING_TYPES[Kind.LUMBER]
UNREACHABLE = 10**6


def h_zero(state: State) -> int:
    return 0                       # Dijkstra


def h_wood(state: State) -> int:
    """Untere Schranke für die Zeit bis GOAL_AMOUNT Holz erreicht ist (zulässig).

    Optimistische Annahmen (alles hier kann nur zu schnell sein, nie zu langsam):
    - alle vorhandenen Gebäude werden sofort abgerissen und erstatten ihre Baukosten
    - aus dem gesamten Werkzeug entstehen so viele weitere Holzfäller wie möglich,
      alle gleichzeitig und ohne Bau-Reihenfolge
    """
    if state.stock[WOOD] >= GOAL_AMOUNT:
        return 0

    refund_wood = sum(type_of(b).build_cost.get("wood", 0) for b in state.buildings)
    tools_total = state.stock[TOOL] + sum(
        type_of(b).build_cost.get("tool", 0) for b in state.buildings)
    existing = [b.remaining_time for b in state.buildings if b.kind == Kind.LUMBER]
    max_new = max(0, tools_total // LUMBER.build_cost["tool"] - len(existing))

    missing = GOAL_AMOUNT - state.stock[WOOD] - refund_wood
    if missing <= 0:
        return DELETE_TIME         # ein Abriss genügt, mindestens so lange dauert er
    if not existing and not max_new:
        return UNREACHABLE

    cycles = math.ceil(missing / LUMBER.output["wood"])
    first_new = BUILD_TIME + LUMBER.production_time

    def completed(t: int) -> int:
        count = sum(0 if t < r else 1 + (t - r) // LUMBER.production_time for r in existing)
        if max_new and t >= first_new:
            count += max_new * (1 + (t - first_new) // LUMBER.production_time)
        return count

    lo = 0
    hi = max(existing + [first_new]) + LUMBER.production_time * cycles
    while lo < hi:                 # kleinstes t mit genug fertigen Zyklen
        mid = (lo + hi) // 2
        if completed(mid) >= cycles:
            hi = mid
        else:
            lo = mid + 1
    return lo


h = h_zero