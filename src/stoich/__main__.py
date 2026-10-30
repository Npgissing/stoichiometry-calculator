from src.stoich.gui import run
import src.stoich.equation_parser as ep
from src.stoich.substance import Substance
import re


def main():
    ep.generate_equation_image(
        ep.format_equation_latex(
            ep.format_reaction(
                ep.balance_equation(ep.parse_equation("K+1 + NO3-1 -> KNO3"))
            )
        )
    )
    # run()


if __name__ == "__main__":
    main()
