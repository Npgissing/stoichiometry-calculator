import mendeleev as md
import stoich.formula_parser as fp
import stoich.substance_name as name

# Substance class representing a chemical substance with its properties and methods

class Substance:

    def __init__(self, formula, is_reactant=False, is_product=False):
        self.formula = formula
        self.element_dict = fp.get_element_dict(formula)
        self.poly_element_dict = fp.get_poly_element(formula)
        self.molar_mass = fp.calculate_molar_mass(self.element_dict)
        self.charge = fp.get_charge(formula)
        self.name = name.name_compound_simple(self.poly_element_dict)
        self.is_ion = fp.is_ion(formula)
        self.is_polyatomic_ion = fp.is_polyatomic_ion(formula)
        self.is_reactant = is_reactant
        self.is_product = is_product

    def __repr__(self):
        return f"Substance(formula='{self.formula}', molar_mass={self.molar_mass}, charge={self.charge}, name='{self.name}', is_ion={self.is_ion}, is_polyatomic_ion={self.is_polyatomic_ion}, is_reactant={self.is_reactant}, is_product={self.is_product})"

    def get_count(self, poly_element : str) -> int:
        # returns the count of a certain element or polyatomic ion in a substance
        # if the element or polyatomic ion isn't in the substance, return 0
        if poly_element in self.poly_element_dict:
            return self.poly_element_dict[poly_element]
        else:
            return 0
        