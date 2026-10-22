from src.stoich.table import table
import re

POLYATOMIC_IONS = frozendict(
    {
        "NH4": ("Ammonium", 1),
        "NO2": ("Nitrite", -1),
        "NO3": ("Nitrate", -1),
        "SO3": ("Sulfite", -2),
        "SO4": ("Sulfate", -2),
        "HSO4": ("Hydrogen Sulfate", -1),
        "S2O3": ("Thiosulfate", -2),
        "C2O4": ("Oxalate", -2),
        "OH": ("Hydroxide", -1),
        "PO3": ("Phosphite", -3),
        "PO4": ("Phosphate", -3),
        "HPO4": ("Hydrogen Phosphate", -2),
        "H2PO4": ("Diydrogen Phosphate", -1),
        "ClO4": ("Perchlorate", -1),
        "ClO3": ("Chlorate", -1),
        "ClO2": ("Chlorite", -1),
        "ClO": ("Hypochlorite", -1),
        "BrO3": ("Bromate", -1),
        "IO3": ("Iodate", -1),
        "C2H3O2": ("Acetate", -1),
        "CO3": ("Carbonate", -2),
        "HCO3": ("Bicarbonate", -1),
        "CrO4": ("Chromate", -2),
        "Cr2O7": ("Dichromate", -2),
        "MnO4": ("Permanganate", -1),
        "CN": ("Cyanide", -1),
        "OCN": ("Cyanate", -1),
        "SCN": ("Thiocyanate", -1),
        "Hg2": ("Mercury(I)", 2),
        "O2": ("Peroxide", -2),
    }
)
ELEMENT_SYMBOLS = tuple(
    [
        "H",
        "He",
        "Li",
        "Be",
        "B",
        "C",
        "N",
        "O",
        "F",
        "Ne",
        "Na",
        "Mg",
        "Al",
        "Si",
        "P",
        "S",
        "Cl",
        "Ar",
        "K",
        "Ca",
        "Sc",
        "Ti",
        "V",
        "Cr",
        "Mn",
        "Fe",
        "Co",
        "Ni",
        "Cu",
        "Zn",
        "Ga",
        "Ge",
        "As",
        "Se",
        "Br",
        "Kr",
        "Rb",
        "Sr",
        "Y",
        "Zr",
        "Nb",
        "Mo",
        "Tc",
        "Ru",
        "Rh",
        "Pd",
        "Ag",
        "Cd",
        "In",
        "Sn",
        "Sb",
        "Te",
        "I",
        "Xe",
        "Cs",
        "Ba",
        "La",
        "Ce",
        "Pr",
        "Nd",
        "Pm",
        "Sm",
        "Eu",
        "Gd",
        "Tb",
        "Dy",
        "Ho",
        "Er",
        "Tm",
        "Yb",
        "Lu",
        "Hf",
        "Ta",
        "W",
        "Re",
        "Os",
        "Ir",
        "Pt",
        "Au",
        "Hg",
        "Tl",
        "Pb",
        "Bi",
        "Po",
        "At",
        "Rn",
        "Fr",
        "Ra",
        "Ac",
        "Th",
        "Pa",
        "U",
        "Np",
        "Pu",
        "Am",
        "Cm",
        "Bk",
        "Cf",
        "Es",
        "Fm",
        "Md",
        "No",
        "Lr",
        "Rf",
        "Db",
        "Sg",
        "Bh",
        "Hs",
        "Mt",
        "Ds",
        "Rg",
        "Cn",
        "Nh",
        "Fl",
        "Mc",
        "Lv",
        "Ts",
        "Og",
    ]
)
ELEMENT_NAMES = []
for symbol in ELEMENT_SYMBOLS:
    ELEMENT_NAMES.append(table.symbol(symbol).name)
ELEMENT_NAMES = tuple(ELEMENT_NAMES)

# This module contains functions to parse chemical formulas into dictionaries of elements and/or polyatomic ions and their counts
# This module also contains functions to determine characteristics of chemical formulas, such as whether they contain polyatomic ions

# Parsing Functions:


# For Parsing Elements in a formula, default to get_poly_element
# get_element_dict is used for calculate_molar_mass
def get_element_dict(formula: str) -> dict[str, int]:
    if re.search(r"\(", formula):
        return get_element_with_parentheses(formula)
    else:
        return get_element_no_parentheses(formula)


def get_element_with_parentheses(formula: str) -> dict[str, int]:
    # remove the whitespace from the formula
    formula = re.sub(r"\s+", "", formula)
    # find all the parentheses in the formula
    parentheses = re.findall(r"\((.*?)\)(\d*)", formula)
    # create a dictionary to store the elements and their counts
    element_dict = {}
    # iterate through the parentheses and their counts
    for subformula, count in parentheses:
        # get the count of the poly atomic ion, defaulting to 1 if no count is provided
        poly_count = count if count else 1
        # parse the group of elements inside the parentheses
        subformula_dict = get_element_no_parentheses(subformula)
        # multiply the counts of the elements in the group by the count of the parentheses
        for element, element_count in subformula_dict.items():
            if element in element_dict:
                element_dict[element] += element_count * int(poly_count)
            else:
                element_dict[element] = element_count * int(poly_count)
        # remove the parsed group from the formula
        formula = formula.replace(f"({subformula}){poly_count}", "")
    # parse any remaining elements outside of parentheses
    remaining_dict = get_element_no_parentheses(formula)
    for element, count in remaining_dict.items():
        if element in element_dict:
            element_dict[element] += count
        else:
            element_dict[element] = count
    return element_dict


def get_element_no_parentheses(formula: str) -> dict[str, int]:
    # remove the whitespace from the formula
    formula = re.sub(r"\s+", "", formula)
    # add a space before each element symbol to separate them
    formula = re.sub(r"([A-Z][a-z]?)", r" \1", formula).strip()
    # split the formula into a list of elements and their counts
    elements = re.split(r"\s", formula)
    # create a dictionary to store the elements and their counts
    element_dict = {}
    # separate the elements and their counts
    for element in elements:
        # use regex to separate the element symbol and its count
        element_symbol = re.match(r"([A-Z][a-z]?)(\d*)", element)
        if element_symbol.group(1) not in ELEMENT_SYMBOLS:
            raise ValueError(f"Invalid element symbol: {element_symbol.group(1)}")
        # separate the count from the element symbol, defaulting to 1 if no count is provided
        count = element_symbol.group(2) if element_symbol.group(2) else 1
        # storing the element symbol and its count in the dictionary
        element_dict[element_symbol.group(1)] = int(count)
    return element_dict


def get_polyatomic_ions(formula: str) -> dict[str, int]:
    # check if the formula contains parentheses, which indicates the presence of polyatomic ions
    if bool(re.search(r"\(", formula)):
        # find all the parentheses in the formula
        parentheses = re.findall(r"\((.*?)\)(\d*)", formula)
        # create a list to store the polyatomic ions
        polyatomic_ions = {}
        # iterate through the parentheses and their counts
        for subformula, count in parentheses:
            # get the count of the polyatomic ion, defaulting to 1 if no count is provided
            poly_count = count if count else 1
            # add the polyatomic ion to the list, along with its count
            polyatomic_ions[subformula] = int(poly_count)
        return polyatomic_ions
    else:
        polyatomic_ions = {}
        for polyatomic_ion in POLYATOMIC_IONS:
            if polyatomic_ion in formula:
                polyatomic_ions[polyatomic_ion] = 1
                formula = formula.replace(f"{polyatomic_ion}", "")
        return polyatomic_ions


def get_poly_element(formula: str) -> dict[str, int]:
    # check if the formula contains parentheses, which indicates the presence of polyatomic ions
    if bool(re.search(r"\(", formula)):
        # find all the parentheses in the formula
        parentheses = re.findall(r"\((.*?)\)(\d*)", formula)
        # create a list to store the polyatomic ions
        poly_element_dict = {}
        # iterate through the parentheses and their counts
        for subformula, count in parentheses:
            # get the count of the poly atomic ions, defaulting to 1 if no count is provided
            poly_count = count if count else 1
            # add the polyatomic ion to the list, along with its count
            poly_element_dict[subformula] = int(poly_count)
            formula = formula.replace(f"({subformula}){poly_count}", "")
        # parse any remaining elements outside of parentheses
        remaining_dict = get_element_no_parentheses(formula)
        for element, count in remaining_dict.items():
            poly_element_dict[element] = count
        return poly_element_dict
    else:
        poly_element_dict = {}
        for ion in POLYATOMIC_IONS:
            if ion in formula:
                poly_element_dict[ion] = 1
                formula = formula.replace(f"{ion}", "")
        if formula == "":
            return poly_element_dict
        remaining_dict = get_element_no_parentheses(formula)
        for element, count in remaining_dict.items():
            poly_element_dict[element] = count
        return poly_element_dict


def get_charge(formula: str) -> int:
    # returns the charge of an ion based on its formula
    match = re.search(r"(\+|-)(\d*)", formula)
    if not match:
        return 0
    return int(match.group(2))


# Characteristic Functions:
def is_ion(formula: str) -> bool:
    return bool(re.search(r"(\+|-)", formula))


def is_polyatomic_ion(formula: str) -> bool:
    return formula in POLYATOMIC_IONS


def contains_polyatomic_ions(formula: str) -> bool:
    # check if the formula contains parentheses, which indicates the presence of polyatomic ions
    if bool(re.search(r"\(", formula)):
        return True

    # check if the formula contains any known polyatomic ions
    for ion in POLYATOMIC_IONS:
        if ion in formula:
            return True
    return False


def is_ionic(poly_element_dict: dict[str, int]) -> bool:
    if len(poly_element_dict) == 1:
        return is_ion(list(poly_element_dict.keys())[0])
    # check if the substance is ionic based on the presence of a polyatomic ions or metals
    for poly_element in poly_element_dict:
        if poly_element in POLYATOMIC_IONS:
            return True
        else:
            try:
                element_instance = table.symbol(poly_element)
                if element_instance.series in [
                    "Alkali metals",
                    "Alkaline earth metals",
                    "Transition metals",
                    "Poor metals",
                    "Lanthanides",
                    "Actinides",
                ]:
                    return True
            except ValueError:
                raise ValueError(
                    f"Polyatomic ion or element is invalid: {poly_element}"
                )
    return False


# Molar Mass Function:
def calculate_molar_mass(element_dict: dict[str, int]) -> float:
    molar_mass = 0.0
    # iterate through the element dictionary and calculate the molar mass
    for element, count in element_dict.items():
        try:
            # get the element instance from periodictable
            element_instance = table.symbol(element)
        except ValueError:
            raise ValueError(f"Invalid element symbol: {element}")
        # add the atomic weight of the element multiplied by its count to the molar mass
        molar_mass += element_instance.mass * count
    return molar_mass
