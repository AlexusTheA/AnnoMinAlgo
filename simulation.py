import math

from buildings import BUILDING_TYPES, create_building
from config import (
    BUILD_TIME, DELETE_TIME, GOODS_INDEX, HOUSE_INITIAL_RESIDENTS, CycleState,
)

from models import (
    Action, ActionKind, Building, BuildingType, House, Kind, Producer, State
)
        
MAX_POPULATION_REQ = max(t.required_humans for t in BUILDING_TYPES.values())
NEVER_BUILD = frozenset({})
NEVER_DELETE = frozenset({})

def type_of(b: Building) -> BuildingType:
    return BUILDING_TYPES[b.kind]

# ---------------------------------------------- Lager

def can_build(stock: tuple, btype: BuildingType) -> bool:
    return all(stock[GOODS_INDEX[good]] >= needed
               for good, needed in btype.build_cost.items())


def update_stock(stock: tuple, changes, human_delta: int = 0) -> tuple:
    delta = [0] * len(stock)
    for good, amount in changes:
        delta[GOODS_INDEX[good]] += amount

    delta[GOODS_INDEX["human"]] += human_delta
    return tuple(old + d for old, d in zip(stock, delta))

# ---------------------------------------------- Gebäude-Status

def is_full(b: Building) -> bool:
    if not isinstance(b, House):
        return False  # Input-Gebäude haben kein "Gesamt-Cap", max_capacity ist hier der Input-Bedarf
    btype = type_of(b)
    return btype.has_capacity and b.residents >= btype.fill_limit


def is_waiting_for_input(b: Building) -> bool:
    if not isinstance(b, Producer):
        return False
    btype = type_of(b)
    return btype.has_input and b.loaded_input < btype.input_total


def round_amount(amount: float, cycle: CycleState) -> float:
    if cycle == CycleState.CEIL:
        return math.ceil(amount)
    if cycle == CycleState.FLOOR:
        return math.floor(amount)
    return amount


def get_output(b: Building) -> list[tuple[str, float]]:
    if is_full(b):
        return []
    cycle = b.cycle if isinstance(b, Producer) else CycleState.NONE
    return [(good, round_amount(amount, cycle))
            for good, amount in type_of(b).output.items()]


def next_cycle(cycle: CycleState) -> CycleState:
    if cycle == CycleState.NONE:
        return CycleState.NONE
    return CycleState.CEIL if cycle == CycleState.FLOOR else CycleState.FLOOR

# ---------------------------------------------- Zeitfortschritt

def update_production_progress(state: State, dt: int) -> tuple[tuple, tuple]:
    stock = state.stock
    buildings = []
    
    for b in state.buildings:
        stock, b = _load_input(stock, b)
        buildings.append(b)
                            
    
    buildings = [_advance_time(b, dt) for b in buildings]
    
    
    for i, b in enumerate(buildings):
        if b.remaining_time == 0:
            stock = update_stock(stock, get_output(b), 0)
            buildings[i] = _restart_cycle(b)
        
    return stock, tuple(buildings)


def _load_input(stock: tuple, b: Building) -> tuple[tuple, Building]:
    if not isinstance(b, Producer):
        return stock, b
    btype = type_of(b)
    if not btype.has_input or b.loaded_input >= btype.input_total:
        return stock, b
    for good, amount in btype.input.items():
        available = stock[GOODS_INDEX[good]]
        if available > 0:
            taken = min(amount - b.loaded_input, available)
            stock = update_stock(stock, [(good, -taken)])
            b = b._replace(loaded_input=b.loaded_input + taken)
    return stock, b


def _advance_time(b: Building, dt: int) -> Building:
    if b.remaining_time < 0 or is_waiting_for_input(b) or is_full(b):
        return b
    return b._replace(remaining_time=b.remaining_time - dt)


def _restart_cycle(b: Building) -> Building:
    btype = type_of(b)
    if isinstance(b, House):
        return House(b.kind, btype.production_time, 
                     min(b.residents + 1, btype.fill_limit), True)    
    
    return Producer(b.kind, btype.production_time, 0, next_cycle(b.cycle), True)


# ---------------------------------------------- Aktionen

def calc_wait(state: State) -> int | None:
    """Zeit bis das nächste Gebäude fertig wird; None, wenn nichts mehr fertig werden kann.
 
    Der Input wird vorher eingelegt (wie in update_production_progress), sonst würde
    ein Weaver, für den schon Wolle im Lager liegt, fälschlich als wartend gelten
    und die Wartezeit könnte seine Fertigstellung überspringen.
    """
    stock = state.stock
    times = []
    for b in state.buildings:
        stock, b = _load_input(stock, b)
        if b.remaining_time >= 0 and not is_full(b) and not is_waiting_for_input(b):
            times.append(b.remaining_time)
    return min(times, default=None)



def calc_actions(state: State) -> list[Action]:
    actions = []
    wait = calc_wait(state)
    if wait is not None:
        actions.append(Action(ActionKind.WAIT, None, wait))
    humans = state.humans

    for kind, btype in BUILDING_TYPES.items():
        if not can_build(state.stock, btype) or humans < btype.required_humans:
            continue
        if kind in NEVER_BUILD:
            continue  # nie bauen für dieses Teilziel
        if kind == Kind.HOUSE and humans >= MAX_POPULATION_REQ:
            continue  # keine weiteren Häuser nötig
        actions.append(Action(ActionKind.BUILD, btype, BUILD_TIME))
    
    for b in state.buildings:
        if b.deletable and b.kind not in NEVER_DELETE:
            actions.append(Action(ActionKind.DELETE, b, DELETE_TIME))
    
    return actions


def build(state: State, btype: Building, duration: int) -> tuple[tuple, tuple]:
    stock, buildings = update_production_progress(state, duration)
    human_delta = HOUSE_INITIAL_RESIDENTS if btype.kind == Kind.HOUSE else 0
    stock = update_stock(
        stock, [(good, -amount) for good, amount in btype.build_cost.items()], human_delta)
    return stock, buildings + (create_building(btype.kind),)
    
def delete(state: State, building: Building, duration: int) -> tuple[tuple, tuple]:
    remaining = list(state.buildings)
    remaining.remove(building)
    stock, buildings = update_production_progress(State(state.stock, tuple(remaining)), duration)
    #Rückerstattung der Baukosten
    human_delta = -building.residents if isinstance(building, House) else 0
    stock = update_stock(stock, type_of(building).build_cost.items(), human_delta)
    return stock, buildings


def calc_state(state: State, action: Action) -> State:
    if action.kind == ActionKind.BUILD:
        stock, buildings = build(state, action.target, action.duration)
    elif action.kind == ActionKind.DELETE:
        stock, buildings = delete(state, action.target, action.duration)
    else:
        stock, buildings = update_production_progress(state, action.duration)
    return State(stock, buildings)


def successors(state: State) -> list[tuple[str, State, int]]:
    return [(a.kind, calc_state(state, a), a.duration) for a in calc_actions(state)]
    
