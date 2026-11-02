import re
import sympy as sp
import matplotlib as mpl
import src.stoich.formula_parser as fp
from src.stoich.substance import Substance
from matplotlib.mathtext import math_to_image
from pathlib import Path
from matplotlib.font_manager import FontProperties

# This module contains functions for parsing and balancing chemical equations.


def parse_equation(equation: str) -> list[Substance]:
    if re.search(r"(<=>|<->)", equation):
        return parse_equilibrium(equation)
    elif re.search(r"->", equation):
        return parse_reaction(equation)
    else:
        raise ValueError(f"Equation not formatted correctly: {equation}")


def parse_equilibrium(equation: str) -> list[Substance]:
    pass


def parse_reaction(equation: str) -> list[Substance]:
    prod_react_split = re.split(r"->", equation)
    reactant_string = prod_react_split[0].strip()
    product_string = prod_react_split[1].strip()
    reactant_list = re.split(r" \+ ", reactant_string)
    products_list = re.split(r" \+ ", product_string)
    prod_react_list = []
    for reactant in reactant_list:
        prod_react_list.append(Substance(reactant, is_reactant=True))
    for product in products_list:
        prod_react_list.append(Substance(product, is_product=True))
    return prod_react_list


def balance_equation(prod_react_list: list[Substance]) -> dict[Substance, int]:
    # create a set order of polyatomic ions/elements so that the matrix can be constructed consistently
    poly_element_ordered_list = []
    # iterate through all substances and add just one instance of a polyatomic ion/element to the ordered list
    for substance in prod_react_list:
        poly_element_dict = substance.poly_element_dict
        for poly_element in poly_element_dict:
            if poly_element not in poly_element_ordered_list:
                poly_element_ordered_list.append(poly_element)
    # create a list of lists to store the counts of each polyatomic ion/element for each substance
    matrix_list = [[] for _ in range(len(poly_element_ordered_list))]

    # fill the matrix with the counts of each polyatomic ion/element for each substance
    for i in range(len(prod_react_list)):
        substance = prod_react_list[i]
        for j in range(len(poly_element_ordered_list)):
            poly_element = poly_element_ordered_list[j]
            if substance.is_reactant:
                matrix_list[j].append(substance.get_count(poly_element))
            else:
                matrix_list[j].append(-substance.get_count(poly_element))

    # convert the list of lists to a sympy Matrix
    matrix = sp.Matrix(matrix_list)
    null_vectors = matrix.nullspace()
    if len(null_vectors) == 0:
        raise ValueError("No solution found for the given equation.")
    for i in range(len(null_vectors[0])):
        null_vectors[0][i] = sp.Abs(null_vectors[0][i])
    denoms = [
        null_vectors[0][i].as_numer_denom()[1] for i in range(len(null_vectors[0]))
    ]
    lcm = sp.lcm(denoms)
    for i in range(len(null_vectors[0])):
        null_vectors[0][i] = null_vectors[0][i] * lcm
    balanced_dict = {}
    for i in range(len(prod_react_list)):
        balanced_dict[prod_react_list[i]] = int(null_vectors[0][i])
    return balanced_dict


def format_reaction(balanced_dict: dict[Substance, int]) -> str:
    react_list = []
    prod_list = []
    for substance, count in balanced_dict.items():
        if substance.is_reactant:
            if count == 1:
                react_list.append(substance.formula)
            else:
                react_list.append(f"{count} {substance.formula}")
        elif substance.is_product:
            if count == 1:
                prod_list.append(substance.formula)
            else:
                prod_list.append(f"{count} {substance.formula}")
    react_str = " + ".join(react_list)
    prod_str = " + ".join(prod_list)
    return f"{react_str} -> {prod_str}"


def format_equation_latex(equation: str) -> str:
    equation = re.sub(r"([A-Z][a-z]?)(\d+)", r"\1_{\2}", equation)
    equation = re.sub(r"\((.*?)\)(\d+)", r"(\1)_{\2}", equation)
    equation = re.sub(r"->", r"\\rightarrow", equation)
    equation = re.sub(r"(<->)|(<=>)", r"\\rightleftharpoons", equation)
    equation = re.sub(r"([+-])(1\d{0})", r"^{\1}", equation)
    equation = re.sub(r"([+-])(\d+)", r"^{\2\1}", equation)
    return f"${equation}$"


def get_multi_dict(list: list[str]) -> dict[str, int]:
    final_dict = {}
    for element in list:
        if fp.contains_polyatomic_ions(element):
            element_dict = fp.get_poly_element(element)
            for poly_element, count in element_dict.items():
                if poly_element in final_dict:
                    final_dict[poly_element] += count
                else:
                    final_dict[poly_element] = count
        else:
            element_dict = fp.get_element_dict(element)
            for subelement, count in element_dict.items():
                if subelement in final_dict:
                    final_dict[subelement] += count
                else:
                    final_dict[subelement] = count
    return final_dict


def generate_equation_image(formatted_equation: str):
    old = mpl.rcParams["savefig.transparent"]
    mpl.rcParams["savefig.transparent"] = True
    image_file_light = Path.cwd() / "assets" / "images" / "equation_light.png"
    image_file_dark = Path.cwd() / "assets" / "images" / "equation_dark.png"
    try:
        math_to_image(
            formatted_equation,
            image_file_light,
            prop=FontProperties(math_fontfamily="cm"),
            dpi=500,
            format="png",
        )
        math_to_image(
            formatted_equation,
            image_file_dark,
            prop=FontProperties(math_fontfamily="cm"),
            dpi=500,
            format="png",
            color="white",
        )
    finally:
        mpl.rcParams["savefig.transparent"] = old
