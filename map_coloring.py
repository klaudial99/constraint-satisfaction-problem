from typing import Dict, List, Optional

from Board import Board
from csp import Constraint, CSP


class MapColoringConstraint(Constraint[str, str]):
    def __init__(self, point1: str, point2: str) -> None:
        super().__init__([point1, point2])
        self.point1: str = point1
        self.point2: str = point2

    def satisfied(self, assignment: Dict[str, str]) -> bool:
        if self.point1 not in assignment or self.point2 not in assignment:
            return True
        return assignment[self.point1] != assignment[self.point2]


if __name__ == "__main__":
    board = Board(20, 20)
    board.make_points(5)
    board.make_links()

    variables: List[str] = board.points
    domains: Dict[str, List[str]] = {}
    for variable in variables:
        domains[variable] = ["red", "green", "blue"]
    csp: CSP[str, str] = CSP(variables, domains)

    for link in board.links:
        csp.add_constraint(MapColoringConstraint(link[0], link[1]))

    solution: Optional[List[Dict[str, str]]] = csp.backtracking_search()
    if not solution:
        print("No solution found!")
    else:
        print("SOLUTIONS AMOUNT:", len(solution))
        for s in solution:
            board.draw_board(s)




