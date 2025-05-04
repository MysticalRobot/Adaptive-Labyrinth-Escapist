import heapq
from entry import Entry, Key
from graph import Graph
from typing import Tuple, List
from search_algorithm import SearchAlgorithm
import random
    
class DStarLite(SearchAlgorithm):
    
    # G = Graph
    # S = G.GetVertices()
    # s = Current vertex
    # G.Cost(v1, v2) = Cost of path between vertices. ∞ cost represents no edge/wall.
    # G.GetAdjacent(s) = List of current vertex's predecessor and successor vertices
    # G.start = Start/AmongUs/SussyBaka
    # G.end = End/Vent/Imposter
    # g(s) = Estimated cost from start to current vertex

    # procedure Initialize()
    def __init__(self, G : Graph):
        self.G = G
        # U = fringe
        self.U = []
        # k_m accumulates heuristic
        self.k_m = 0
        self.rhs = {}
        self.g = {}
        self.recently_visited = []  # track recently visited nodes with frequency

        for s in self.G.GetVertices():
            self.rhs[s] = float('inf')
            self.g[s] = float('inf')
        
        self.rhs[self.G.goal] = 0
        self.InsertIntoU(self.G.goal, self.CalculateKey(self.G.goal))

        self.last = self.G.start
    
    # our Hueristic is based on whether diagonal movement is allowed
    def heuristic(self, u1 : Tuple[int, int], u2 : Tuple[int, int]) -> float:
        # Chebyshev Distance
        if self.G.allow_diagonal_movement:
            return max(abs(u1[0] - u2[0]), abs(u1[1] - u2[1]))
        # Manhattan Distance
        else:
            return abs(u1[0] - u2[0]) + abs(u1[1] - u2[1])
    
    # procedure CalculateKey(s)
    def CalculateKey(self, s : Tuple[int, int]) -> Key:
        return Key(min(self.g[s], self.rhs[s]) + self.heuristic(self.G.start, s) + self.k_m, min(self.g[s], self.rhs[s]))
    
    # checks if s is in U
    def UContains(self, s : Tuple[int, int]) -> bool: 
        # create entry with dummy key
        return Entry(s, Key(-1, -1)) in self.U
    
    # inserts Entry (vertex and calculated key) into U
    def InsertIntoU(self, u : Tuple[int, int], calculated_key : Key) -> None:
        heapq.heappush(self.U, Entry(u, calculated_key))
    
    # removes s from U
    def RemoveFromU(self, s : Tuple[int, int]) -> None:
        # create entry with dummy key
        self.U.remove(Entry(s, Key(-1, -1)))
        heapq.heapify(self.U)
    
    # pops the top entry from U (assumes that it is nonempty)
    def PopFromU(self) -> Tuple[int, int]:
        return heapq.heappop(self.U)

    # procedure UpdateVertex(u)
    def UpdateVertex(self, u : Tuple[int, int]) -> None:
        if (u != self.G.goal):
            self.rhs[u] = min([float('inf')] + [self.G.GetCost(u, u_adjacent) + self.g[u_adjacent] for u_adjacent in self.G.GetTraversableAdjacent(u)])
        if (self.UContains(u)):
            self.RemoveFromU(u)
        if (self.g[u] != self.rhs[u]):
            self.InsertIntoU(u, self.CalculateKey(u))

    # procedure ComputeShortestPath()
    def ComputePath(self) -> None:
        # process the priority queue until the shortest path is found
        while (self.U and self.U[0].key < self.CalculateKey(self.G.start) or self.rhs[self.G.start] != self.g[self.G.start]):
            top_entry = self.PopFromU()
            u = top_entry.s
            k_old = top_entry.key
            k_new = self.CalculateKey(u)
            if k_old < k_new:
                self.InsertIntoU(u, k_new)
            elif self.g[u] > self.rhs[u]:
                self.g[u] = self.rhs[u]
                for s in self.G.GetAdjacent(u):
                    self.UpdateVertex(s)
            else:
                self.g[u] = float('inf')
                self.UpdateVertex(u)
                for s in self.G.GetAdjacent(u) + [u]:
                    self.UpdateVertex(s)
        
        # ensure the start node is not prematurely marked as having reached the goal
        if self.G.start == self.G.goal and self.rhs[self.G.start] == self.g[self.G.start]:
            self.g[self.G.start] = self.rhs[self.G.start]

    # select the next best successor to move toward the goal
    def PickSuccessor(self) -> Tuple[int, int]:
        val = float('inf')
        min_s = None

        # sscillation threshold: if a node is revisited more than this, force movement
        oscillation_threshold = 3

        # backtracking limit: do not go back more than 3 vertices
        backtracking_limit = 3

        # define a tolerance for rhs values
        rhs_tolerance = 2  # Treat nodes with `rhs` values within ±2 as equivalent

        # track the previous direction to apply direction change penalties
        prev_direction = (self.G.start[0] - self.last[0], self.G.start[1] - self.last[1])

        # detect oscillation: count how many times nodes in recently_visited repeat
        oscillating_nodes = [s for s in self.recently_visited if self.recently_visited.count(s) > oscillation_threshold]

        # backtracking logic: check if the current node is already in the backtracking list
        if len(self.recently_visited) > backtracking_limit:
            backtracking_nodes = self.recently_visited[-backtracking_limit:]
        else:
            backtracking_nodes = self.recently_visited

        # iterate over all traversable adjacent nodes
        for s in self.G.GetTraversableAdjacent(self.G.start):
            # check if the node is part of oscillation or backtracking
            if s in oscillating_nodes or s in backtracking_nodes:
                # if oscillating or excessive backtracking, deprioritize this node unless no other options exist
                oscillation_penalty = 100
                backtracking_penalty = 50
            else:
                oscillation_penalty = 0
                backtracking_penalty = 0

            # default exploration reward for nodes with inf g-values
            exploration_reward = 0
            if self.g[s] == float('inf'):
                exploration_reward = 50  # Strongly reward unexplored nodes

            # encourage progression to higher rhs if it resolves oscillation or backtracking
            if self.rhs[s] > self.rhs[self.G.start] and self.g[s] == float('inf'):
                if s in oscillating_nodes or s in backtracking_nodes:  # Force breaking oscillation/backtracking
                    exploration_reward += 50
                elif self.rhs[s] - self.rhs[self.G.start] <= rhs_tolerance:
                    exploration_reward += 20  # Moderate reward for reasonable progression

            # apply penalty for revisiting recently visited nodes
            revisit_count = self.recently_visited.count(s)
            revisit_penalty = 5 * (2 ** (revisit_count - 1)) if revisit_count > 0 else 0

            # apply penalty for direction changes
            curr_direction = (s[0] - self.G.start[0], s[1] - self.G.start[1])
            direction_change_penalty = 0.2 if prev_direction != curr_direction else 0

            # add a progress reward for moving closer to the goal
            progress_reward = 1.0 / (1 + self.heuristic(s, self.G.goal))  # Reward nodes closer to the goal

            # add a distance-based reward for nodes closer to the start
            distance_reward = 1.0 / (1 + self.heuristic(self.G.start, s))  # Reward nodes closer to the start

            # add stochastic noise to break ties
            noise = random.uniform(0, 0.01)

            # calculate the total value for this successor
            heuristic_weight = 1.5  # Stronger heuristic weight for progress
            curr_val = (self.G.GetCost(self.G.start, s) + 
                        self.g[s] + 
                        revisit_penalty + 
                        direction_change_penalty + 
                        heuristic_weight * self.heuristic(s, self.G.goal) -
                        progress_reward -
                        distance_reward -
                        exploration_reward +  # Exploration is rewarded
                        oscillation_penalty +
                        backtracking_penalty +
                        noise)

            # tie-breaking: prefer nodes with lower heuristic values within the rhs_tolerance
            if curr_val < val or (
                abs(curr_val - val) <= 1e-6 and (min_s is None or 
                abs(self.rhs[s] - self.rhs[min_s]) <= rhs_tolerance and
                self.heuristic(s, self.G.goal) < self.heuristic(min_s, self.G.goal))
            ):
                val, min_s = curr_val, s

        # handle cases with oscillation/backtracking or no clear progression
        if min_s is None or min_s in oscillating_nodes or min_s in backtracking_nodes:
            # force movement to a node outside the oscillating/backtracking set
            unexplored = [s for s in self.G.GetTraversableAdjacent(self.G.start) if s not in oscillating_nodes and s not in backtracking_nodes]
            if unexplored:
                min_s = random.choice(unexplored)
            else:
                # if all nodes are part of oscillation/backtracking, pick the least-visited node
                min_s = min(self.G.GetTraversableAdjacent(self.G.start), key=self.recently_visited.count)

        # add the chosen successor to recently visited nodes
        self.recently_visited.append(min_s)
        # limit the size of recently visited nodes to maintain a sliding window
        if len(self.recently_visited) > 10:
            self.recently_visited.pop(0)

        return min_s
    
    def AdaptToChanges(self, changed_edges: List[Tuple[int, int]]) -> Tuple[int, int]:
        self.k_m += self.heuristic(self.last, self.G.start)  # Update heuristic shift
        self.last = self.G.start

        # update affected vertices and neighbors
        affected_vertices = set()
        for e in changed_edges:
            for s, u in self.G.GetVerticesConnectedByEdge(e):
                affected_vertices.update([s, u])
                for (a, b) in [(s, u), (u, s)]:
                    if self.rhs[a] == self.G.GetCost(a, b) + self.g[b]:
                        if a != self.G.goal:
                            self.rhs[a] = min([float('inf')] + [self.G.GetCost(a, c) + self.g[c] for c in self.G.GetAdjacent(a)])
                    self.UpdateVertex(a)
        
        # force recomputation of paths if a significant change is detected
        if len(affected_vertices) > 5:  # threshold for significant change
            for vertex in affected_vertices:
                for neighbor in self.G.GetAdjacent(vertex):
                    self.UpdateVertex(neighbor)
            self.ComputePath()