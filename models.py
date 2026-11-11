from dataclasses import dataclass, field
from enum import StrEnum
from typing import NamedTuple

from config import UNLIMITED, GOODS_INDEX, CycleState


class Kind(StrEnum):
    CENTER = "center"
    HOUSE = "house"
    LUMBER = "lumber"
    FISHER = "fisher"
    FARM = "farm"
    WEAVER = "weaver"
    
@dataclass(frozen=True)
class BuildingType:
    kind: Kind
    production_time: int
    build_cost: dict[str, int]
    input: dict[str, int] = field(default_factory=dict)
    output: dict[str, int] = field(default_factory=dict)
    required_humans: int = 0
    alternating_rounding: bool = False
    capacity: int = UNLIMITED
    
    @property
    def has_input(self) -> bool:
        return bool(self.input)

    @property
    def input_total(self) -> int:
        return sum(self.input.values())

    @property
    def has_capacity(self) -> bool:
        return self.capacity != UNLIMITED
    
    @property 
    def produces(self) -> bool:
        return bool(self.output)
    
    @property 
    def fill_limit(self) -> int:
        return self.input_total if self.has_input else self.capacity
        
    
class House(NamedTuple):
    kind: Kind
    remaining_time: int
    residents: int
    deletable: bool
    
class Producer(NamedTuple):
    kind: Kind
    remaining_time: int
    loaded_input: int       # 0 bei Gebäude ohne Input
    cycle: CycleState
    deletable: bool
    
Building = House | Producer

class ActionKind(StrEnum):
    WAIT = "wait"
    BUILD = "build"
    DELETE = "DELETE"
    
class Action(NamedTuple):
    kind: ActionKind
    target: BuildingType | Building | None
    duration: int
    
@dataclass (frozen=True, slots=True)
class State:
    stock: tuple[int, ...]
    buildings: tuple[Building, ...]
    
    def __post_init__(self):
        object.__setattr__(self, "buildings", tuple(sorted(self.buildings)))
        
    @property
    def humans(self) -> int:
        return self.stock[GOODS_INDEX["human"]]
        
