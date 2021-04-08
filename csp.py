import copy
from itertools import permutations
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


class Arc(Generic[V]):

    def __init__(self, start: V, end: V, const: Constraint) -> None:
        self.start = start
        self.end = end
        self.const = const


class CSP(Generic[V, D]):
    def __init__(self, variables: List[V], domains: Dict[V, List[D]]) -> None:
        self.variables: List[V] = variables
        self.domains: Dict[V, List[D]] = domains
        self.constraints: Dict[V, List[Constraint[V, D]]] = {}
        for variable in self.variables:
            self.constraints[variable] = []
            if variable not in self.domains:
                raise LookupError("Every variable should have a domain.")
        self.steps = 0

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

    def backtracking_search(self, variable_bool: bool, value_bool: bool, assignment=None) -> Optional[List[Dict[V, D]]]:

        results = []
        if assignment is None:
            assignment = {}
        # all variables are assigned
        if len(assignment) == len(self.variables):
            return [assignment]

        # unassigned variables
        unassigned: List[V] = [v for v in self.variables if v not in assignment]

        # VARIABLE
        first: V = unassigned[0]
        if variable_bool:
            first: V = self.minimum_remaining_values_heuristic(unassigned, self.domains)[0]

        #VALUE
        values = self.domains[first]
        if value_bool:
            values = self.least_constraining_value_heuristic(first, self.domains, assignment)

        for value in values:
            local_assignment = assignment.copy()
            local_assignment[first] = value
            self.steps += 1

            if self.check_consistency(first, local_assignment):
                result: Optional[List[Dict[V, D]]] = self.backtracking_search(variable_bool, value_bool, local_assignment)

                # add new solution to results
                if result is not None:
                    results.extend(result)
        if results is not None:
            return results
        else:
            return None

    def mac(self, variable_bool: bool, value_bool: bool, domains, assignment=None) -> Optional[List[Dict[V, D]]]:
        results = []
        if assignment is None:
            assignment = {}
        # all variables are assigned
        if len(assignment) == len(self.variables):
            return [assignment]

        # unassigned variables
        unassigned: List[V] = [v for v in self.variables if v not in assignment]

        # VARIABLE
        first: V = unassigned[0]
        if variable_bool:
            first: V = self.minimum_remaining_values_heuristic(unassigned, domains)[0]

        # VALUE
        values = domains[first]
        if value_bool:
            values = self.least_constraining_value_heuristic(first, domains, assignment)

        for value in values:
            dom = copy.deepcopy(domains)
            local_assignment = assignment.copy()
            local_assignment[first] = value
            self.steps += 1
            dom[first] = [value]

            if not self.ac_3(dom, local_assignment): # next value if not satisfied
                continue
            else:
                result: Optional[List[Dict[V, D]]] = self.mac(variable_bool, value_bool, dom, local_assignment)

                # add new solution to results
                if result is not None:
                    results.extend(result)
        if len(results) != 0:
            return results
        else:
            return None

    def ac_3(self, domains, assignment) -> bool:

        unary = []
        arcs = set()
        queue = set()

        for var, constraints in self.constraints.items():
            for constr in constraints:
                if len(constr.variables) > 1:
                    multi = list(permutations(constr.variables, 2)) # list of pairs of variables in constraint
                    for arc in multi: # adding arcs
                        new = Arc(arc[0], arc[1], constr)
                        arcs.add(new)
                        queue.add(new)
                else:
                    unary.append(constr)

        for con in unary:
            new_domain = []
            var = con.variables[0]
            for val in domains[var]:
                local_assignment = {var: val}
                if con.satisfied(local_assignment):
                    new_domain.append(val)
            domains[var] = new_domain # setting new domains for unary constraints

        while len(queue) > 0:
            actual_arc = list(queue)[0] # dequeue
            queue.remove(actual_arc)
            if self.remove_inconsistent_values(actual_arc, domains, assignment): # if removed
                if len(domains[actual_arc.start]) == 0: # no possible values -> failure
                    return False
                for arc in arcs:
                    if arc.start != actual_arc.end and arc.end == actual_arc.start: # adding neghbours to queue
                        queue.add(arc)

        return True # satisfied

    def remove_inconsistent_values(self, arc: Arc, domains, assignment) -> bool:
        removed = False
        for x in domains[arc.start]:
            local_assignment = assignment.copy()
            local_assignment[arc.start] = x
            satisfy = [] # does each value satisfy constraint
            for y in domains[arc.end]:
                local_assignment[arc.end] = y
                if arc.const.satisfied(local_assignment):
                    satisfy.append(True)
                    break # at least one possible value -> stop checking
                else:
                    satisfy.append(False)

            if not any(satisfy): # all false - not satisfied
                domains[arc.start].remove(x) # delete value from domain
                removed = True

        return removed

    # VALUE HEURISTIC
    def least_constraining_value_heuristic(self, variable: V, domains: Dict[V, List[D]], assignment):

        neighbours = []
        for constr in self.constraints[variable]:
            if len(constr.variables) > 1:
                multi = list(permutations(constr.variables, 2)) # list of pairs of variables in constraint
                for arc in multi: # adding arcs
                    if arc[1] not in assignment.keys():

                        new_arc = Arc(arc[0], arc[1], constr)
                        #neighbours[arc[1]] = len(domains[arc[1]])
                        neighbours.append(new_arc)

        values = {}
        for val in domains[variable]: # possible values for variable
            values[val] = 0 # adding to dict
            new_assignment = assignment.copy()
            new_assignment[variable] = val
            for neighbour in neighbours: # neighbour = arc
                for val_nei in domains[neighbour.end]: # possible values for neighbour
                    new_assignment[neighbour.end] = val_nei
                    if neighbour.const.satisfied(new_assignment):
                        values[val] += 1 # count possible values (for all neighbours per each variable value)
                del new_assignment[neighbour.end]

        return [k for k, v in sorted(values.items(), key=lambda item: item[1], reverse=True)] # list in correct order (most possibilities first)

    # VARIABLE HEURISTIC
    def minimum_remaining_values_heuristic(self, variables: List[V], domains: Dict[V, List[D]]):
        domains_length = {}
        for var in variables:
            domains_length[var] = len(domains[var])

        return [k for k, v in sorted(domains_length.items(), key=lambda item: item[1], reverse=False)] # list in correct order (least possibilities first)





