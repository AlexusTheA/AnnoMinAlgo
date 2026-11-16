# Anno 1701 - Speedrun Build Order Minimization-Algorithm

> **Status:** Proof of Concept. The current algorithm works for small goals but will grow exponentially for even slightly bigger than small goals (see more below for further explanation)

This project is a proof of concept. The goal is to generate Build Orders for the game Anno 1701 (or in that sense all Anno Games) that fulfill a certain definded goal in minimal maketime.

## What is this about?

This project is an attempt in generating Speedrun Build Orders for Anno 1701 (and other Annos). Anno 1701 is the third iteration of the Anno Series. Its a city-builder strategy game with the main focus on island and ressource management. Speedrunning the game proved to be more of a challenge about strategizing and planing rather than execution. Thus automating the process of finding the best possible solution would seem to be the best way to minimize the maketime of any given scenario in Anno. In foresight this project would extend to every other Anno Series game, as well as any optimizaion problem, be it in a speedrunning context or even a competitiv PvE or PvP enviroment.

## How does it work?

For this proof of concept it was decided to choose a method that stays simple yet provides correctness and optimality. A* seemed to be a good candidate. Not only does it guarantee to find the optimal solution with enough time and hardware capacity, but it is also rather simple to grasp. But in order to apply this problem to any given Anno Scenario, an Anno Run had to be modelled as graph:

In a game of Anno the player will always start with an Inventory of Ressources and, depending on the game mode, with either non, one, or several buildings. Both can considered to be lists. The Resource List, with every resource being its own entry and a Building List, with every Building being its own entry. That's all you need for a fully simplified Anno Game. For this project we disregard objects such as Ships or Military Units, as those are not required for the first three Anno 1701 Scenario, which this project focuses on. 
Now with a list of resources and a list of buildings, we can define a State in an Anno Run. A state in Anno consists of a set of r ressources with r being constant and a set of b buildings. The starting state would be the state where the run begins, with a set amount of resources, a set amount of buildings. The end state would be the state, where the run ends. In scenarios that's usually the main objective which is tied to having a certain amount of ressources. 
A new state from a current state is reached with a certain amount of actions that can be performed at any current state. The amount of actions are dependend on the ressources and buildings of the current state. All actions have a positive cost which is the weight of any edge betwenn two states.
And thus any given Anno game can be modeled as Graph. And as such A* will in theory find an optimal solution.

## Result

The algorithm works. For a given starting state and goal it will find an optimal solution to reach the end state in the least maketime possible. With a very good heurisitic it will do so much faster than Dijsktra. However, the alogrithm is not capable of finding a solution for any given problem in a reasonable amount of time without a lot of manual rule writing by the user. Even the easiest goals will make the entire graph explode into millions of states. I wasn't even able to solve the first and by far the easiest scenario. It take an incredible amount of rules, fine tuning and heurisitic engeeniring to get the solution in a single run.

A run that works for example is just 30 wood and the heurisitc in the heuristic.py file. 

## Boundries

As mentioned, the graph will explode into millions of states if not regulated by the user. There are only two things that can be done to improve the performance considerably: making the heuristic as good as possible and regulating action as much as possible. The less actions the simulation can do at any given state, the less states will be generated. And the better the heurisitic the faster the alogrithm.

## Future

It may be necessary to switch to another algorithm which does not find the optimal solution, but rather the best solution possible in a reasonable amount of time.

## Usage

The project requires Python 3.12. It is run my executing the main.py file. The heurisitc function is passed in the main.py file, the goal is set in the config.py file, the starting state is defined in the scenarios.py file and rules are set in the relevance.py file.

'''bash
python main.py
'''
