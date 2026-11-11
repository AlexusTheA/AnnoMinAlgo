from enum import IntEnum

# --- Güter ---
GOODS_INDEX = {"human": 0, "food": 1, "wood": 2, "tool": 3, "wool": 4, "cloth": 5}

# --- Ziel ---
GOAL_TYPE = "wood"
GOAL_AMOUNT = 60                  # vorher: GOAL

# --- Aktionskosten ---
BUILD_TIME = 5
DELETE_TIME = 5

# --- Haus ---
HOUSE_INITIAL_RESIDENTS = 1

# --- Suche ---
MAX_SOLUTION_TIME = 400          # vorher: best_g = 400
MAX_ITERATIONS = 10_000_000      # vorher: 500_000 * 20
PROGRESS_PRINT_INTERVAL = 10_000

# --- Sentinel-Werte ---
UNLIMITED = -1                   # max_capacity: keine Begrenzung
NO_PRODUCTION = -1               # pt: Gebäude produziert nichts

class CycleState(IntEnum):
    NONE = -1                    # Gebäude hat keinen Zyklus
    FLOOR = 0                    # Output wird abgerundet
    CEIL = 1                     # Output wird aufgerundet