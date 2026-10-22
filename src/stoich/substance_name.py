from src.stoich.table import table
import re
import src.stoich.formula_parser as fp
POLYATOMIC_IONS = fp.POLYATOMIC_IONS
SET_CHARGE_CATIONS = frozendict(
    {"Al": 3, 
     "Zn": 2, 
     "Cd": 2, 
     "Ag": 1, 
     "Sc": 3, 
     "Y": 3, 
     "La": 3, 
     "Ac": 3})
ELEMENT_STEMS = frozendict(
    {"H" : "Hydr", 
     "N" : "Nitr", 
     "O" : "Ox", 
     "F" : "Fluor", 
     "P" : "Phosph", 
     "S" : "Sulf", 
     "Cl" : "Chlor", 
     "Se" : "Selen", 
     "Br" : "Brom",
     "I" : "Iod"})

# This module contains functions to name chemical compounds based on their a list of the elements and polyatomic ions present

# Currently doesn't support ions, only non charged compounds, also no polyatomic ions
def name_compound_simple(poly_element_dict : dict[str, int]) -> str:
    if (len(poly_element_dict) == 1):
        key = list(poly_element_dict.keys())[0]
        element_instance = table.symbol(key)
        return element_instance.name.capitalize()
    # iterate through the elements in the compound and check if any of them are metals
    elif fp.is_ionic(poly_element_dict):
        return name_ionic_compound(poly_element_dict)
    # if the compound does not contain a metal or a polyatomic ion, it is a covalent compound
    else:
        return name_covalent_compound(poly_element_dict)

def name_ionic_compound(poly_element_dict : dict[str, int]) -> str:
    # returns the name of an ionic compound (cation and anion)
    # separate the cation and anion based on the elements present
    cation = ""
    anion = ""
    for poly_element in poly_element_dict:
        if poly_element in POLYATOMIC_IONS:
            if poly_element == "NH4" or poly_element == "Hg2":
                cation = poly_element
            else:
                anion = poly_element
        else:
            try:
                element_instance = table.symbol(poly_element)
            except ValueError:
                raise ValueError(f"Invalid element symbol: {poly_element}")
            if element_instance.series in ["Alkali metals", "Alkaline earth metals", "Transition metals", "Poor metals", "Lanthanides", "Actinides"]:
                cation = poly_element
            else:
                anion = poly_element
    if not cation:
        raise ValueError("Invalid ionic compound: missing cation")
    if not anion:
        raise ValueError("Invalid ionic compound: missing anion")
    if cation and anion:
        return f"{name_cation(cation, anion, poly_element_dict)} {name_anion(anion)}"
 
def name_covalent_compound(poly_element_dict : dict[str, int]) -> str:
    # returns the name of a covalent compound
    prefixes = ("Mono", "Di", "Tri", "Tetra", "Penta", "Hexa", "Hepta", "Octa", "Nona", "Deca")
    covalent_name = ""
    element_place = 1
    # iterate through the element symbols and counts
    for element, count in poly_element_dict.items():
        try:
            element_instance = table.symbol(element)
        except ValueError:
            raise ValueError(f"Invalid element symbol: {element}")
        # if the element is the first one
        if element_place == 1:
            # if the count is 1, leave off the prefix
            if count == 1:
                covalent_name += element_instance.name.capitalize()
            # otherwise include the prefix
            else:
                covalent_name += f"{prefixes[count - 1].capitalize()}{element_instance.name.lower()} "
        else:
            #include the prefix for the second element
            covalent_name += f"{prefixes[count - 1].lower()}{ELEMENT_STEMS[element].lower()}ide"
        element_place += 1
    # remove the double vowels
    covalent_name = re.sub(r"(oo|ao)", r"o", covalent_name).strip()
    return covalent_name

def name_cation(cation : str, anion : str, poly_element_dict : dict[str, int]) -> str:
    # returns the name of a cation
    polyatomic_ion_cation_info = POLYATOMIC_IONS.get(cation)
    if polyatomic_ion_cation_info:
        return polyatomic_ion_cation_info[0]
    else:
        try:
            element_instance = table.symbol(cation)
        except ValueError:
            raise ValueError(f"Invalid element symbol: {cation}")
        if element_instance.symbol in SET_CHARGE_CATIONS or element_instance.series in ("Alkali metals", "Alkaline earth metals"):
            return f"{element_instance.name.capitalize()}"
        else:
            return f"{element_instance.name.capitalize()}({roman_numeral(get_cation_charge(cation, anion, poly_element_dict))})"

def name_anion(anion : str) -> str:
    # returns the name of an anion
    polyatomic_ion_anion_info = POLYATOMIC_IONS.get(anion)
    if polyatomic_ion_anion_info:
            return polyatomic_ion_anion_info[0].lower()
    else:
        try:
            element_instance = table.symbol(anion)
        except ValueError:
            raise ValueError(f"Invalid element symbol: {anion}")
        if element_instance.symbol in ELEMENT_STEMS:
            return f"{ELEMENT_STEMS[element_instance.symbol].lower()}ide"
        else:
            raise ValueError(f"Element stem not known: {anion}")

def get_cation_charge(cation : str, anion : str, poly_element_dict : dict[str, int]) -> int:
    # returns the charge of a cation based on the anion and the polyatomic ions present in the compound
    anion_charge = 0
    # if the cation is a polyatomic ion, get its charge from the POLYATOMIC_IONS list
    polyatomic_ion_cation_info = POLYATOMIC_IONS.get(cation)
    if polyatomic_ion_cation_info:
        return polyatomic_ion_cation_info[1]
    # if the cation is an element, check if it is in the SET_CHARGE_CATIONS dictionary or if it is an alkali or alkaline earth metal
    elif cation in SET_CHARGE_CATIONS:
        return SET_CHARGE_CATIONS[cation]
    else:
        try:
            cation_element_instance = table.symbol(cation)
        except ValueError:
            raise ValueError(f"Invalid element symbol: {cation}")
        # if the cation is an alkali or alkaline earth metal, get its charge from its group number
        if cation_element_instance.series in ("Alkali metals", "Alkaline earth metals"):
            return cation_element_instance.group
    # if the anion is a polyatomic ion, get its charge from the POLYATOMIC_IONS list
    polyatomic_ion_anion_info = POLYATOMIC_IONS.get(anion)
    if polyatomic_ion_anion_info:
        anion_charge = polyatomic_ion_anion_info[1]
    # if the anion is an element, get its charge from its group number (subtracting 8 to get the negative charge)
    else:
        try:
            anion_element_instance = table.symbol(anion)
        except ValueError:
            raise ValueError(f"Invalid element symbol: {anion}")
        anion_charge = anion_element_instance.group - 18
    if cation not in poly_element_dict:
        raise ValueError(f"Invalid cation: {cation}")
    elif anion not in poly_element_dict:
        raise ValueError(f"Invalid anion: {anion}")
    else:
        cation_count = poly_element_dict[cation]
        anion_count = poly_element_dict[anion]
    # calculate the total charge of the cation and anion
    total_anion_charge = anion_charge * anion_count
    cation_charge = -1 * (total_anion_charge // cation_count)
    return cation_charge

def roman_numeral(num : int) -> str:
    # returns the roman numeral representation of a number
    roman_numerals = frozendict({50 : "L", 40 : "XL", 10 : "X", 9 : "IX", 5 : "V", 4 : "IV", 1 : "I"})

    roman_num = ""
    for roman_number in roman_numerals:
        count = num // roman_number
        roman_num += roman_numerals[roman_number] * count
        num -= (count * roman_number)
    return roman_num