from src.stoich.gui import run
from matplotlib.mathtext import math_to_image
from pathlib import Path


def main():
    # run()
    equation = r"$2 H_{2} + O_{2} \rightarrow 2 H_{2}O$"
    image_file = Path.cwd() / "assets" / "images" / "equation.svg"
    math_to_image(equation, image_file, format="svg")


if __name__ == "__main__":
    main()
