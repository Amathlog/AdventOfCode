from queue import PriorityQueue
import abc
from typing import List, Any, Dict

class StatePriority:
    def __init__(self, state: Any, priority: int):
        self.state = state
        self.priority = priority

    def __lt__(self, other: "StatePriority") -> bool:
        return self.priority < other.priority

# A* solver.
# Nodes needs to support == and be hashable.
# Returns a list of nodes with smallest cost
# By default, A* heuristic is returning 0, which is the equivalent of the Djikstra algorithm,
# but you can re-implement it. Be careful to always have an heuristic that NEVER OVERESTIMATES the real cost.
# Needs to implement a few methods to adapt it to your problem. Start and end states will probably be stored in your __init__ function.
class AStar_Solver(abc.ABC):
    def __init__(self):
        pass

    def heuristic(self, state: Any) -> int:
        return 0
    
    @abc.abstractmethod
    def get_neighbors(self, state: Any) -> List[Any]:
        pass

    @abc.abstractmethod
    def get_cost(self, state: Any) -> int:
        pass

    @abc.abstractmethod
    def is_start(self, state: Any) -> bool:
        pass
    
    @abc.abstractmethod
    def is_end(self, state: Any) -> bool:
        pass
    
    @abc.abstractmethod
    def get_start_states(self) -> List[Any]:
        pass

    # Can re-implement this function if we want to do some pre-processing/post-processing
    def solve(self) -> Any:
        return self.solve_internal()

    def solve_internal(self) -> List[Any]:     
        states = PriorityQueue()
        start_states = self.get_start_states()
        for s in start_states:
            states.put(StatePriority(s, self.heuristic(s)))

        came_from: Dict[Any, Any] = {}
        g_score: Dict[Any, int] = {s: 0 for s in start_states}

        def reconstruct_path(state):
            res = []
            curr = state
            while not self.is_start(curr):
                res.append(curr)
                curr = came_from[curr]
            return [curr] + res[::-1]

        while states.qsize() > 0:
            state = states.get().state
            if self.is_end(state):
                return reconstruct_path(state)
            
            for s in self.get_neighbors(state):
                tentative_gscore = g_score[state] + self.get_cost(s)
                if s not in g_score or tentative_gscore < g_score[s]:
                    came_from[s] = state
                    g_score[s] = tentative_gscore
                    states.put(StatePriority(s, tentative_gscore + self.heuristic(s)))

        # Failed
        return []
