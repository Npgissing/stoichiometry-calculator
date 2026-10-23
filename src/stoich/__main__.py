from src.stoich.gui import run
import src.stoich.equation_parser as ep
from src.stoich.substance import Substance
from src.stoich.table import table


def main():
    # run()
    equation = "H2 + O2 -> H2O"
    for substance, count in ep.balance_equation(ep.parse_equation(equation)).items():
        print(f"{substance.formula}, {substance.name}: {count}")


if __name__ == "__main__":
    main()
