from abc import ABC, abstractmethod
from typing import List, Tuple

# defines the methods a search algorithm needs to implement
class SearchAlgorithm(ABC):

    @abstractmethod
    def ComputeShortestPath(self) -> None:
        pass

    @abstractmethod
    def PickSuccessor(self) -> Tuple[int, int]:
        pass

    @abstractmethod
    def AdaptToChanges(self, changed_edges : List[Tuple[int, int]]) -> None:
        pass
