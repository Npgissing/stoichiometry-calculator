from src.stoich.substance_name import name_compound_simple

def test_name_compound_simple():
    assert name_compound_simple({"O": 2}) == "Oxygen"
    assert name_compound_simple({"H": 2, "O": 1}) == "Dihydrogen monoxide"
    assert name_compound_simple({"Na": 1, "Cl": 1}) == "Sodium chloride"
    assert name_compound_simple({"Ca": 1, "CO3": 1}) == "Calcium carbonate"
    assert name_compound_simple({"NH4": 1, "NO3": 1}) == "Ammonium nitrate"
    assert name_compound_simple({"Fe": 2, "O": 3}) == "Iron(III) oxide"
    assert name_compound_simple({"Pb": 1, "NO3": 2}) == "Lead(II) nitrate"