import re
import sympy as sp
import matplotlib as mpl
from src.stoich.substance import Substance
from matplotlib.mathtext import math_to_image
from pathlib import Path
from matplotlib.font_manager import FontProperties

# This module contains functions for parsing and balancing chemical equations.


def parse_equation(equation: str) -> list[Substance]:
    # Search for the type of equation based on the presence of certain symbols and call the appropriate parsing function
    if re.search(r"(<=>|<->)", equation):
        return parse_equilibrium(equation)
    elif re.search(r"->", equation):
        return parse_reaction(equation)
    else:
        raise ValueError(f"Equation not formatted correctly: {equation}")


def parse_equilibrium(equation: str) -> list[Substance]:
    pass


def parse_reaction(equation: str) -> list[Substance]:
    # Split the equation into reactants and products based on the arrow symbol
    prod_react_split = re.split(r"->", equation)
    reactant_string = prod_react_split[0].strip()
    product_string = prod_react_split[1].strip()
    # Split the reactants and products into lists based on plus symbol
    reactant_list = re.split(r" \+ ", reactant_string)
    products_list = re.split(r" \+ ", product_string)
    prod_react_list = []
    # Create Susbtance obejcts and add them to the prod_react_list with the appropriate is_reactant and is_product flags
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
    # find the nullspace of the matrix to get the coefficients for the balanced equation
    null_vectors = matrix.nullspace()
    # if there are no nullspace vectors, raise an error
    if len(null_vectors) == 0:
        raise ValueError("No solution found for the given equation.")
    # make all coefficients positive and convert to integers
    for i in range(len(null_vectors[0])):
        null_vectors[0][i] = sp.Abs(null_vectors[0][i])
    denoms = [null_vectors[0][i].as_numer_denom()[1] for i in range(len(null_vectors[0]))]
    lcm = sp.lcm(denoms)
    for i in range(len(null_vectors[0])):
        null_vectors[0][i] = null_vectors[0][i] * lcm
    # create a dictionary to store the balanced equation with the Substance objects as keys and the coefficients as values
    balanced_dict = {}
    for i in range(len(prod_react_list)):
        balanced_dict[prod_react_list[i]] = int(null_vectors[0][i])
    return balanced_dict


def format_reaction(balanced_dict: dict[Substance, int]) -> str:
    # split the balanced_dict into reactants and products based on the is_reactant and is_product flags of the Substance objects
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
    # join the reactants and products into strings and return the formatted equation
    react_str = " + ".join(react_list)
    prod_str = " + ".join(prod_list)
    return f"{react_str} -> {prod_str}"


def format_equation_latex(equation: str) -> str:
    # format the equation string into LaTeX format for rendering as an image
    equation = re.sub(r"([A-Z][a-z]?)(\d+)", r"\1_{\2}", equation)
    equation = re.sub(r"\((.*?)\)(\d+)", r"(\1)_{\2}", equation)
    equation = re.sub(r"->", r"\\rightarrow", equation)
    equation = re.sub(r"(<->)|(<=>)", r"\\rightleftharpoons", equation)
    equation = re.sub(r"([+-])(1\d{0})", r"^{\1}", equation)
    equation = re.sub(r"([+-])(\d+)", r"^{\2\1}", equation)
    return f"${equation}$"


def generate_equation_image(formatted_equation: str):
    # save old rcParams and set savefig.transparent to True for transparent background
    old = mpl.rcParams["savefig.transparent"]
    mpl.rcParams["savefig.transparent"] = True
    # create file paths for the light and dark images
    image_file_light = Path.cwd() / "assets" / "images" / "equation_light.png"
    image_file_dark = Path.cwd() / "assets" / "images" / "equation_dark.png"
    # create images of the formatted equation in both light and dark modes using math_to_image
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
    # restore the old rcParams after generating the images
    finally:
        mpl.rcParams["savefig.transparent"] = old


def generate_prod_react_image(equation_dict: dict[Substance, int]):
    # save old rcParams and set savefig.transparent to True for transparent background
    old = mpl.rcParams["savefig.transparent"]
    mpl.rcParams["savefig.transparent"] = True
    # create images of the reactants and products in the equation_dict using math_to_image
    try:
        for substance in equation_dict.keys():
            path_light = Path.cwd() / "assets" / "images" / f"{substance.name}_light.png"
            path_dark = Path.cwd() / "assets" / "images" / f"{substance.name}_dark.png"
            math_to_image(
                format_equation_latex(substance.formula),
                path_light,
                prop=FontProperties(math_fontfamily="cm"),
                dpi=500,
                format="png",
            )
            math_to_image(
                format_equation_latex(substance.formula),
                path_dark,
                prop=FontProperties(math_fontfamily="cm"),
                dpi=500,
                format="png",
                color="white",
            )
    # restore the old rcParams after generating the images
    finally:
        mpl.rcParams["savefig.transparent"] = old


def determine_equation_type(formatted_equation: str) -> str:
    # determine the type of equation based on the presence of certain symbols in the formatted_equation
    if "->" in formatted_equation:
        return "reaction"
    elif "<->" in formatted_equation or "<=>" in formatted_equation:
        return "equilibrium"
    else:
        return "unknown"


def parse_amount(substance: Substance, amount: str) -> float:
    # parse the amount string by removing whitespace and converting to lowercase
    amount = amount.strip().lower()
    # find the number in the amount using regex
    match = re.match(r"\d+(\.\d+)?", amount)
    # convert the amount to moles based on the unit specified in the amount string
    if match:
        re.sub(match.group(), "", amount)
        if re.search(r"g", amount) or re.search(r"gram", amount):
            return substance.get_moles(float(match.group()))
        elif re.search(r"mol", amount) or re.search(r"mole", amount):
            return float(match.group())
        else:
            raise ValueError(f"Amount not formatted correctly: {amount}")
    # if no number is found in the amount string, raise an error
    else:
        raise ValueError(f"Amount not formatted correctly: {amount}")


def calculate_equation(
    equation_dict: dict[Substance, int],
    equation_amounts: list[float],
    equation_type: str,
) -> dict[Substance, float]:
    # calculate the final amounts of substances in the equation based on the equation type and the provided amounts
    if equation_type == "reaction":
        return calculate_reaction(equation_dict, equation_amounts)
    elif equation_type == "equilibrium":
        return calculate_equilibrium(equation_dict, equation_amounts)
    else:
        raise ValueError(f"Unknown equation type: {equation_type}")


def calculate_reaction(equation_dict: dict[Substance, int], equation_amounts: list[float]) -> dict[Substance, float]:
    # find the limiting reactant using the get_limiting_reactant function and find its index and amount
    limiting_reactant = get_limiting_reactant(equation_dict, equation_amounts)
    limiting_index = list(equation_dict.keys()).index(limiting_reactant)
    limiting_amount = equation_amounts[limiting_index]
    # calculate the final amounts of each substance in the equation based on the limiting reactant and its amount
    final_results = {}
    for substance, count, amount in zip(equation_dict.keys(), equation_dict.values(), equation_amounts):
        if substance.is_reactant:
            final_results[substance] = amount - (limiting_amount * (count / equation_dict[limiting_reactant]))
        elif substance.is_product:
            final_results[substance] = amount + (limiting_amount * (count / equation_dict[limiting_reactant]))
    return final_results


def calculate_equilibrium(equation_dict: dict[Substance, int], equation_amounts: list[float]) -> dict[Substance, float]:
    pass


def get_limiting_reactant(equation_dict: dict[Substance, int], equation_amounts: list[float]) -> Substance:
    # find the limiting reactant by comparing the ratios of provided amounts to what is required based on the balanced equation
    limiting_reactant = None
    limiting_index = -1
    for i, (substance, count, amount) in enumerate(zip(equation_dict.keys(), equation_dict.values(), equation_amounts)):
        if substance.is_reactant:
            if (
                limiting_reactant is None
                or amount / count
                < list(equation_amounts)[limiting_index] / list(equation_dict.values())[limiting_index]
            ):
                limiting_reactant = substance
                limiting_index = i
    return limiting_reactant
