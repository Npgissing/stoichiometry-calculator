import periodictable as pt

DIATOMIC_ELEMENTS = frozenset(("H", "N", "O", "F", "Cl", "Br", "I"))
GROUP=frozendict(
    {1 : {"H", "Li", "Na", "K", "Rb", "Cs", "Fr"}, 
     2 : {"Be", "Mg", "Ca", "Sr", "Ba", "Ra"}, 
     3 : {"Sc", "Y", "La", "Ac", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr"}, 
     4 : {"Ti", "Zr", "Hf", "Rf"}, 
     5 : {"V", "Nb", "Ta", "Db"}, 
     6 : {"Cr", "Mo", "W", "Sg"}, 
     7 : {"Mn", "Tc", "Re", "Bh"}, 
     8 : {"Fe", "Ru", "Os", "Hs"}, 
     9 : {"Co", "Rh", "Ir", "Mt"}, 
     10 : {"Ni", "Pd", "Pt", "Ds"}, 
     11 : {"Cu", "Ag", "Au", "Rg"}, 
     12 : {"Zn", "Cd", "Hg", "Cn"}, 
     13 : {"B", "Al", "Ga", "In", "Tl", "Nh"}, 
     14 : {"C", "Si", "Ge", "Sn", "Pb", "Fl"}, 
     15 : {"N", "P", "As", "Sb", "Bi", "Mc"}, 
     16 : {"O", "S", "Se", "Te", "Po", "Lv"}, 
     17: {"F", "Cl", "Br", "I", "At", "Ts"}, 
     18: {"He", "Ne", "Ar", "Kr", "Xe", "Rn", "Og"}})
SERIES=frozendict(
    {"Alkali metals" : {"Li", "Na", "K", "Rb", "Cs", "Fr"}, 
     "Alkaline earth metals" : {"Be", "Mg", "Ca", "Sr", "Ba", "Ra"}, 
     "Transition metals" : {"Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds", "Rg", "Cn"}, 
     "Poor metals" : {"Al", "Ga", "In", "Sn", "Tl", "Pb", "Bi", "Po", "Nh", "Fl", "Mc", "Lv"}, 
     "Lanthanides" : {"La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu"}, 
     "Actinides" : {"Ac", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr"}, 
     "Halogens" : {"F", "Cl", "Br", "I", "At", "Ts"}, 
     "Noble gases" : {"He", "Ne", "Ar", "Kr", "Xe", "Rn", "Og"},
     "Metalloids" : {"B", "Si", "Ge", "As", "Sb", "Te"},
     "Nonmetals" : {"H", "C", "N", "O", "P", "S", "Se"}})

# Adding the group and series information to the elements in the periodictable module
# Checking if group has been added as a property
if "group" not in pt.elements.properties:
    pt.elements.properties.append("group")

    # Setting default group
    pt.core.Element.group = 0

    # Loading data from the GROUP dictionary
    for group, element_set in GROUP.items():
        for symbol in element_set:
            element = pt.elements.symbol(symbol)
            element.group = group

# Checking if series has been added as a property
if "series" not in pt.elements.properties:
    pt.elements.properties.append("series")

    # Setting default series
    pt.core.Element.series = "Unknown"

    # Loading data from the SERIES dictionary
    for series, element_set in SERIES.items():
        for symbol in element_set:
            element = pt.elements.symbol(symbol)
            element.series = series

# Checking if diatomic has been added as a property
if "diatomic" not in pt.elements.properties:
    pt.elements.properties.append("diatomic")

    # Setting default value for diatomic
    pt.core.Element.diatomic = False

    # Loading data from DIATOMIC_ELEMENTS set
    for symbol in DIATOMIC_ELEMENTS:
        element = pt.elements.symbol(symbol)
        element.diatomic = True

table = pt.elements