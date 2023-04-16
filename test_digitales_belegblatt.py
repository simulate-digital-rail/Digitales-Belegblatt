

def test_zug_position():
    from digitales_belegblatt.digitales_belegblatt import DigitalesBelegblatt

    db = DigitalesBelegblatt(["AA","BB","CC"])
    db.set_zug_position(101,"AA")
    db.set_zug_position(102,"CC")

    assert "AA" == db.get_zug_position(101)
    assert "CC" == db.get_zug_position(102)