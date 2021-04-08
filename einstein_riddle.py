from typing import List, Dict, Optional

from csp import CSP, Constraint


# unique values in category
class AllDifferentConstraint(Constraint[str, int]):
    def __init__(self, category: List[str]) -> None:
        super().__init__([var for var in category])
        self.category: List[str] = category

    def satisfied(self, assignment: Dict[str, int]) -> bool:
        vals = [] # taken values in category
        for key, value in assignment.items():
            if key in self.category:
                if value in vals: # if it repeats
                    return False
                vals.append(value)
        return True


# particular value (house number) to variable
class HouseNumberConstraint(Constraint[str, int]):
    def __init__(self, var: str, number: int) -> None:
        super().__init__([var])
        self.var: str = var
        self.number: int = number

    def satisfied(self, assignment: Dict[str, int]) -> bool:
        if self.var not in assignment:
            return True
        return assignment[self.var] == self.number


# two variables - same house number
class SameHouseNumberConstraint(Constraint[str, int]):
    def __init__(self, var1: str, var2: str) -> None:
        super().__init__([var1, var2])
        self.var1: str = var1
        self.var2: str = var2

    def satisfied(self, assignment: Dict[str, int]) -> bool:
        if self.var1 in assignment and self.var2 in assignment: # if both are in assignment
            return assignment[self.var1] == assignment[self.var2]
        return True # if one is not in assignment


# two variables in neighbourhood
class NeighbourConstraint(Constraint[str, int]):
    def __init__(self, var1: str, var2: str, side: str) -> None:
        super().__init__([var1, var2])
        self.var1: str = var1
        self.var2: str = var2
        self.side: str = side

    def satisfied(self, assignment: Dict[str, int]) -> bool:
        if self.var1 in assignment and self.var2 in assignment: # if both are in assignment
            if self.side == "left": # (LEFT - var1 - var2 - RIGHT)
                return assignment[self.var1]+1 == assignment[self.var2]
            elif self.side == "?":
                return abs(assignment[self.var1] - assignment[self.var2]) == 1
        return True # if one is not in assignment


if __name__ == "__main__":

    nationality = ["Norweg", "Anglik", "Dunczyk", "Niemiec", "Szwed"]
    color = ["Czerwony", "Bialy", "Zolty", "Niebieski", "Zielony"]
    cigarette = ["Light", "Cygaro", "Fajka", "Bez_filtra", "Mentolowe"]
    drink = ["Herbata", "Mleko", "Woda", "Piwo", "Kawa"]
    pet = ["Kot", "Ptak", "Pies", "Kon", "Rybki"]

    variables: List[str] = nationality + color + cigarette + drink + pet
    domains: Dict[str, List[int]] = {}
    for variable in variables:
        domains[variable] = [1, 2, 3, 4, 5]

    csp: CSP[str, int] = CSP(variables, domains)

    csp.add_constraint(AllDifferentConstraint(nationality))
    csp.add_constraint(AllDifferentConstraint(color))
    csp.add_constraint(AllDifferentConstraint(cigarette))
    csp.add_constraint(AllDifferentConstraint(drink))
    csp.add_constraint(AllDifferentConstraint(pet))

    csp.add_constraint(HouseNumberConstraint("Norweg", 1))
    csp.add_constraint(SameHouseNumberConstraint("Anglik", "Czerwony"))
    csp.add_constraint(NeighbourConstraint("Zielony", "Bialy", "left"))
    csp.add_constraint(SameHouseNumberConstraint("Dunczyk", "Herbata"))
    csp.add_constraint(NeighbourConstraint("Light", "Kot", "?"))
    csp.add_constraint(SameHouseNumberConstraint("Zolty", "Cygaro"))
    csp.add_constraint(SameHouseNumberConstraint("Niemiec", "Fajka"))
    csp.add_constraint(HouseNumberConstraint("Mleko", 3))
    csp.add_constraint(NeighbourConstraint("Light", "Woda", "?"))
    csp.add_constraint(SameHouseNumberConstraint("Bez_filtra", "Ptak"))
    csp.add_constraint(SameHouseNumberConstraint("Szwed", "Pies"))
    csp.add_constraint(NeighbourConstraint("Norweg", "Niebieski", "?"))
    csp.add_constraint(NeighbourConstraint("Kon", "Zolty", "?"))
    csp.add_constraint(SameHouseNumberConstraint("Mentolowe", "Piwo"))
    csp.add_constraint(SameHouseNumberConstraint("Zielony", "Kawa"))

    solution: Optional[List[Dict[str, int]]] = csp.backtracking_search(True)
    #solution: Optional[List[Dict[str, int]]] = csp.mac(csp.domains)
    if not solution:
        print("There is no solution!")
    else:
        print("Steps:", csp.steps)
        for sol in solution:
            for val in set(sol.values()):
                result = []
                for k, v in sol.items():
                    if val == v:
                        result.append(k)
                print(str(val) + ":", result)

