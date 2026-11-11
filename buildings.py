# buildings.py
from config import NO_PRODUCTION, HOUSE_INITIAL_RESIDENTS, CycleState
from models import BuildingType, Kind, House, Producer, Building

_ALL = (
    BuildingType(Kind.CENTER, NO_PRODUCTION, {"wood": 2, "tool": 8}),
    BuildingType(Kind.HOUSE, 15, {"wood": 2}, output={"human": 1}, capacity=8),
    BuildingType(Kind.LUMBER, 40, {"tool": 2}, output={"wood": 2}),
    BuildingType(Kind.FISHER, 90, {"wood": 3, "tool": 5}, output={"food": 1.5},
                 alternating_rounding=True),
    BuildingType(Kind.FARM, 30, {"wood": 4, "tool": 2}, output={"wool": 1},
                 required_humans=48),
    BuildingType(Kind.WEAVER, 30, {"wood": 3, "tool": 2}, input={"wool": 2},
                 output={"cloth": 1}, required_humans=48),
)

BUILDING_TYPES = {t.kind: t for t in _ALL}

def create_house(
    residents: int = HOUSE_INITIAL_RESIDENTS,
    remaining_time: int | None = None,
    deletable: bool = False,
) -> House:
    if remaining_time is None:
        remaining_time = BUILDING_TYPES[Kind.HOUSE].production_time
    return House(Kind.HOUSE, remaining_time, residents, deletable)

def create_producer(
    kind: Kind,
    remaining_time: int | None = None,
    loaded_input: int = 0,
    cycle: CycleState | None = None,
    deletable: bool = False,
) -> Producer:
    btype = BUILDING_TYPES[kind]
    if remaining_time is None:
        remaining_time = btype.production_time
    if cycle is None:
        cycle = CycleState.FLOOR if btype.alternating_rounding else CycleState.NONE
    return Producer(kind, remaining_time, loaded_input, cycle, deletable)

def create_building(kind: Kind) -> Building:
    if kind == Kind.HOUSE:
        return create_house()
    return create_producer(kind)

