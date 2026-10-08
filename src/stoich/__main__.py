from stoich.equation_parser import parse_reaction, balance_equation

def main():
    reaction = "Pb(NO3)2 + KI -> PbI2 + KNO3"
    print(balance_equation(parse_reaction(reaction)))

if __name__ == "__main__":
    main()