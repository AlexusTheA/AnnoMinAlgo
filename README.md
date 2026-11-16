# Anno 1701 - Speedrun Build Order Minimization-Algorithm

This project is a proof of concept. The goal is to generate Build Orders for the game Anno 1701 (or in that sense all Anno Games) that fulfill a certain definded goal in minimal maketime.

## The Algorithm

For this test the A* pathfinding algorithm has been utilized, due its simplicty, yet completness, optimality and optimal efficency, given the heuristic is chosen good enough.
Since it is possible to model an Anno run as a weighted graph, the algorithm would in theory be able to find the shortest path from a given source node to a goal node.

However, as proven by this test, optimizing Anno is an incredible hard problem. Infact it seems to be NP-Hard bein a Resource-Constraint Project Scheduling (RCPSP) problem. So proving optimality is a ought to fail from the the beginning as the search space explodes dramatically.
So while in theory the optimal solution eventually found with enough calculation time and memory, in practice, that will never happen with unsufficent hardware ressources and a Anno run being too big or long. By "too big" and "long" I mean the very first and easiest scenario. 
The algorithm works absolutly fine with small managable goals, a ton of manually written rules and a literally perfect heuristic. But once the goal is dependend on 3 other sub-goals and each step allows the simulation to chose 1 of 10 actions and there are at least 240 steps, our graph explodes extremly.
And that includes a perfect handcrafted heuristic that would probably need to be so good that you had solve the problem just to make it.

So in regards to that, we would need to find other algorithms that don't solve the problem, but aproximate it as much as possible. Possible candidates could be: 
- CP-SAT, however modelling the problem would be the biggest problem
- Beam-Search, aproximates the best solution, though the heuristic would decide how good the aproximation really is
- A*, we just continue and find ourself in a never ending heuristic writing session
