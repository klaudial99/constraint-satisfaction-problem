import time
from typing import Dict, List, Optional
from Board import Board
from csp import Constraint, CSP


class MapColoringConstraint(Constraint[str, str]):
    def __init__(self, point1: str, point2: str) -> None:
        super().__init__([point1, point2])
        self.point1: str = point1
        self.point2: str = point2

    def satisfied(self, assignment: Dict[str, int]) -> bool:
        if self.point1 not in assignment or self.point2 not in assignment:
            return True
        return assignment[self.point1] != assignment[self.point2]


if __name__ == "__main__":
    board = Board(30, 30)
    board.make_points(5)
    board.make_links()

    variables: List[str] = board.points
    domains: Dict[str, List[str]] = {}
    for variable in variables:
        domains[variable] = ["red", "green", "blue", "pink"]
    csp: CSP[str, str] = CSP(variables, domains)

    for link in board.links:
        csp.add_constraint(MapColoringConstraint(link[0], link[1]))

    start_time = time.time()
    #solution: Optional[List[Dict[str, str]]] = csp.backtracking_search(False, True, True)
    solution: Optional[List[Dict[str, int]]] = csp.forward_checking(True, True, True, csp.domains)
    #solution: Optional[List[Dict[str, str]]] = csp.mac(False, True, True, csp.domains)
    if not solution:
        print("There is no solution!")
    else:
        print("--- %s seconds ---" % (time.time() - start_time))
        print("Steps:", csp.steps)
        #print("SOLUTIONS AMOUNT:", len(solution))
        #board.draw_board(solution)
        # for s in solution:
        #     board.draw_board(s)
