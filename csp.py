from typing import Generic, TypeVar, Dict, List, Optional
from abc import abstractmethod

V = TypeVar('V')
D = TypeVar('D')


class Constraint(Generic[V, D]):

    def __init__(self, variables: List[V]) -> None:
        self.variables = variables

    @abstractmethod
    def satisfied(self, assignment: Dict[V, D]) -> bool:
        pass


class CSP(Generic[V, D]):
    def __init__(self, variables: List[V], domains: Dict[V, List[D]]) -> None:
        self.variables: List[V] = variables
        self.domains: Dict[V, List[D]] = domains
        self.constraints: Dict[V, List[Constraint[V, D]]] = {}
        for variable in self.variables:
            self.constraints[variable] = []
            if variable not in self.domains:
                raise LookupError("Every variable should have a domain.")

    def add_constraint(self, constraint: Constraint[V, D]) -> None:
        for variable in constraint.variables:
            if variable not in self.variables:
                raise LookupError("Variable in constraint not in variable list")
            else:
                self.constraints[variable].append(constraint)

    def check_consistency(self, variable: V, assignment: Dict[V, D]) -> bool:
        for constraint in self.constraints[variable]:
            if not constraint.satisfied(assignment):
                return False
        return True

    def backtracking_search(self, assignment=None) -> Optional[List[Dict[V, D]]]:

        results = []
        if assignment is None:
            assignment = {}
        # all variables are assigned
        if len(assignment) == len(self.variables):
            return [assignment]

        # unassigned variables
        unassigned: List[V] = [v for v in self.variables if v not in assignment]

        first: V = unassigned[0]
        for value in self.domains[first]:
            local_assignment = assignment.copy()
            local_assignment[first] = value

            if self.check_consistency(first, local_assignment):
                result: Optional[List[Dict[V, D]]] = self.backtracking_search(local_assignment)

                # add new solution to results
                if result is not None:
                    results.extend(result)
        if results is not None:
            return results
        else:
            return None
