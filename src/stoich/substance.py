import src.stoich.formula_parser as fp
import src.stoich.substance_name as name

# Substance class representing a chemical substance with its properties and methods


class Substance:

    def __init__(self, formula, is_reactant=False, is_product=False):
        self.formula: str = formula
        self.element_dict: dict[str, int] = fp.get_element_dict(formula)
        self.poly_element_dict: dict[str, int] = fp.get_poly_element(formula)
        self.molar_mass: float = fp.calculate_molar_mass(self.element_dict)
        self.charge: int = fp.get_charge(formula)
        self.name: str = name.name_compound_simple(self.poly_element_dict)
        self.is_ion: bool = fp.is_ion(formula)
        self.is_polyatomic_ion: bool = fp.is_polyatomic_ion(formula)
        self.is_reactant: bool = is_reactant
        self.is_product: bool = is_product

    def __repr__(self):
        return f"Substance(formula='{self.formula}', molar_mass={self.molar_mass}, charge={self.charge}, name='{self.name}', is_ion={self.is_ion}, is_polyatomic_ion={self.is_polyatomic_ion}, is_reactant={self.is_reactant}, is_product={self.is_product})"

    def __str__(self):
        return f"Substance: {self.formula}, Name: {self.name}"

    def get_count(self, poly_element: str) -> int:
        # returns the count of a certain element or polyatomic ion in a substance
        # if the element or polyatomic ion isn't in the substance, return 0
        if poly_element in self.poly_element_dict:
            return self.poly_element_dict[poly_element]
        else:
            return 0

    def get_moles(self, mass: float) -> float:
        # returns the number of moles of a substance given the mass in grams
        return mass / self.molar_mass

    def get_mass(self, moles: float) -> float:
        # returns the mass in grams of a substance given the number of moles
        return moles * self.molar_mass
