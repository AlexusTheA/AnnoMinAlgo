from config import GOAL_TYPE
from heuristics import h_wood
from relevance import make_expand
from scenarios import STARTING_STATE
from search import a_asterisk

if __name__ == "__main__":

    expand = make_expand(GOAL_TYPE)      # einmal erzeugen, nicht pro Zustand

    result = a_asterisk(STARTING_STATE, heuristic=h_wood, expand=expand)
    if result is None:
        print("keine Lösung gefunden")
    else:
        best_g, came_from, best_solution, iterations = result
        print("-----------------------------------------------")
        print(f"iterations: {iterations}")
        print(f"best time: {best_g}")
        print(f"Lager: {best_solution.stock}")
        print(f"Gebäude: ")
        print("-----------------------------------------------")
        print(*best_solution.buildings, sep="\n")
    
    
    
    # TEST_STATE = State(
    # (24, 4, 12, 3, 0, 0), (
    # create_building_tuple("center", None, None, -1, 1),
    # create_building_tuple("house", None, 8, -1, 1),
    # create_building_tuple("house", None, 8, -1, 1),
    # create_building_tuple("house", None, 8, -1, 1),
    # create_building_tuple("fisher", None, None, 0, 1),
    # create_building_tuple("lumber", None, None, -1, 1),
    # create_building_tuple("farm", None, None, -1, 1),
    # #create_building_tuple("weaver", None, None, -1, 1)
    #     )
    # )
    
    # state = TEST_STATE
    # for i in range(100):
    #     buildings, min_time = calc_wait(state)
    #     print(f"Schritt {i}: min_time={min_time}, buildings={buildings}")
    #     action = ("wait", buildings, min_time)
    #     state = calc_state(state, action)
    #     print(f"  -> stock={state.stock}")
    #     print(f"  -> buildings={state.buildings}")
    
    
    
    
    
    
    

"""
    
"""
