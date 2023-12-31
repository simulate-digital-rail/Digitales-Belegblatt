from  datetime import datetime
from xml.dom import minidom
import os

from digitales_belegblatt.digitales_belegblatt import DigitalesBelegblatt


test_path = os.path.dirname(__file__)


class TimerMock():

    def __init__(self):
        self._now = datetime.now()

    def now(self):
        return self._now

    def set_time(self, time_string: str):
        self._now = datetime.strptime(time_string, '%m/%d/%y %H:%M:%S')


def test_empty_belegblatt():

    timer_mock = TimerMock()
    digitales_belegblatt = DigitalesBelegblatt(["Schwarze Pumpe", "Boxberg", "Cottbus"])
    digitales_belegblatt.timer = timer_mock

    timer_mock.set_time('09/19/22 13:55:26')

    xml = digitales_belegblatt.generate_image()
    with open(f"{test_path}/tmp/empty.svg", "w", encoding="UTF-8") as f:
        f.write(xml)

    doc = minidom.parse(f"{test_path}/tmp/empty.svg")
    assert len(doc.getElementsByTagName('line')) == 5
    assert len(doc.getElementsByTagName('text')) == 7
    doc.unlink()


def test_zug_position():

    timer_mock = TimerMock()
    digitales_belegblatt = DigitalesBelegblatt(["Schwarze Pumpe", "Boxberg", "Cottbus"])
    digitales_belegblatt.timer = timer_mock

    timer_mock.set_time('09/19/22 13:55:26')
    digitales_belegblatt.set_zug_position(101, "Schwarze Pumpe")
    digitales_belegblatt.set_zug_position(102, "Cottbus")

    assert "Schwarze Pumpe" == digitales_belegblatt.get_zug_position(101)
    assert "Cottbus" == digitales_belegblatt.get_zug_position(102)

    digitales_belegblatt.block_strecke_for_zugnummer(102, "Schwarze Pumpe")

    timer_mock.set_time('09/19/22 14:10:26')
    digitales_belegblatt.set_zug_position(102, "Boxberg")

    timer_mock.set_time('09/19/22 14:13:00')
    digitales_belegblatt.set_zug_position(102, "Schwarze Pumpe")

    timer_mock.set_time('09/19/22 14:15:00')
    digitales_belegblatt.block_strecke_for_zugnummer(101, "Boxberg")

    timer_mock.set_time('09/19/22 14:30:26')
    digitales_belegblatt.set_zug_position(101, "Boxberg")

    xml = digitales_belegblatt.generate_image()
    with open(f"{test_path}/tmp/test.svg", "w", encoding="UTF-8") as f:
        f.write(xml)

    doc = minidom.parse(f"{test_path}/tmp/test.svg")
    assert len(doc.getElementsByTagName('line')) == 18
    assert len(doc.getElementsByTagName('text')) == 13
    doc.unlink()

    trains = digitales_belegblatt.get_trains()
    assert trains == {101, 102}

    assert "Boxberg" == digitales_belegblatt.get_zug_position(101)
    assert "Schwarze Pumpe" == digitales_belegblatt.get_zug_position(102)


def test_3_out_zug_position():

    timer_mock = TimerMock()
    digitales_belegblatt = DigitalesBelegblatt(["Jöhstadt", "Fahrzeughalle", "Schlössel"])
    digitales_belegblatt.timer = timer_mock

    timer_mock.set_time('09/19/22 13:55:26')
    digitales_belegblatt.set_zug_position(101, "Jöhstadt")

    assert "Jöhstadt" == digitales_belegblatt.get_zug_position(101)

    digitales_belegblatt.block_strecke_for_zugnummer(101, "Fahrzeughalle")

    timer_mock.set_time('09/19/22 14:10:26')
    digitales_belegblatt.set_zug_position(101, "Fahrzeughalle")

    timer_mock.set_time('09/19/22 14:15:00')
    digitales_belegblatt.block_strecke_for_zugnummer(101, "Schlössel")

    timer_mock.set_time('09/19/22 14:30:26')
    digitales_belegblatt.set_zug_position(101, "Schlössel")

    xml = digitales_belegblatt.generate_image()
    with open(f"{test_path}/tmp/joehstadt.svg", "w", encoding="UTF-8") as f:
        f.write(xml)

    doc = minidom.parse(f"{test_path}/tmp/joehstadt.svg")
    assert len(doc.getElementsByTagName('line')) == 17
    assert len(doc.getElementsByTagName('text')) == 13
    doc.unlink()

    trains = digitales_belegblatt.get_trains()
    assert trains == {101}

    assert "Schlössel" == digitales_belegblatt.get_zug_position(101)


def test_3_back_zug_position():

    timer_mock = TimerMock()
    digitales_belegblatt = DigitalesBelegblatt(["Jöhstadt", "Fahrzeughalle", "Schlössel"])
    digitales_belegblatt.timer = timer_mock

    timer_mock.set_time('09/19/22 13:55:26')
    digitales_belegblatt.set_zug_position(101, "Schlössel")

    assert "Schlössel" == digitales_belegblatt.get_zug_position(101)

    digitales_belegblatt.block_strecke_for_zugnummer(101, "Fahrzeughalle")

    timer_mock.set_time('09/19/22 14:10:26')
    digitales_belegblatt.set_zug_position(101, "Fahrzeughalle")
    
    timer_mock.set_time('09/19/22 14:15:00')
    digitales_belegblatt.block_strecke_for_zugnummer(101, "Jöhstadt")

    timer_mock.set_time('09/19/22 14:30:26')
    digitales_belegblatt.set_zug_position(101, "Jöhstadt")

    xml = digitales_belegblatt.generate_image()
    with open(f"{test_path}/tmp/joehstadt2.svg", "w", encoding="UTF-8") as f:
        f.write(xml)

    doc = minidom.parse(f"{test_path}/tmp/joehstadt2.svg")
    assert len(doc.getElementsByTagName('line')) == 17
    assert len(doc.getElementsByTagName('text')) == 13
    doc.unlink()

    trains = digitales_belegblatt.get_trains()
    assert trains == {101}

    assert "Jöhstadt" == digitales_belegblatt.get_zug_position(101)


def test_zug_position_stretched():

    timer_mock = TimerMock()
    digitales_belegblatt = DigitalesBelegblatt(["Schwarze Pumpe", "Boxberg"])
    digitales_belegblatt.timer = timer_mock

    timer_mock.set_time('09/19/22 13:55:00')
    digitales_belegblatt.set_zug_position(1, "Schwarze Pumpe")
    digitales_belegblatt.set_zug_position(2, "Boxberg")

    assert "Schwarze Pumpe" == digitales_belegblatt.get_zug_position(1)
    assert "Boxberg" == digitales_belegblatt.get_zug_position(2)

    timer_mock.set_time('09/19/22 13:55:26')
    digitales_belegblatt.block_strecke_for_zugnummer(2, "Schwarze Pumpe")

    timer_mock.set_time('09/19/22 13:56:26')
    digitales_belegblatt.set_zug_position(2, "Schwarze Pumpe")

    timer_mock.set_time('09/19/22 13:57:15')
    digitales_belegblatt.block_strecke_for_zugnummer(1, "Boxberg")

    timer_mock.set_time('09/19/22 13:57:30')
    digitales_belegblatt.set_zug_position(1, "Boxberg")

    xml = digitales_belegblatt.generate_image(minutes=1)
    with open(f"{test_path}/tmp/stretched.svg", "w", encoding="UTF-8") as f:
        f.write(xml)

    doc = minidom.parse(f"{test_path}/tmp/stretched.svg")
    assert len(doc.getElementsByTagName('line')) == 14
    assert len(doc.getElementsByTagName('text')) == 10
    doc.unlink()


def test_zug_position_offset():

    timer_mock = TimerMock()
    digitales_belegblatt = DigitalesBelegblatt(["Schwarze Pumpe", "Boxberg"])
    digitales_belegblatt.timer = timer_mock

    timer_mock.set_time('09/19/22 13:55:00')
    digitales_belegblatt.set_zug_position(1, "Schwarze Pumpe")
    digitales_belegblatt.set_zug_position(2, "Boxberg")

    assert "Schwarze Pumpe" == digitales_belegblatt.get_zug_position(1)
    assert "Boxberg" == digitales_belegblatt.get_zug_position(2)

    timer_mock.set_time('09/19/22 13:55:26')
    digitales_belegblatt.block_strecke_for_zugnummer(2, "Schwarze Pumpe")

    timer_mock.set_time('09/19/22 14:02:26')
    digitales_belegblatt.set_zug_position(2, "Schwarze Pumpe")

    timer_mock.set_time('10/19/22 13:40:15')
    digitales_belegblatt.block_strecke_for_zugnummer(1, "Boxberg")

    timer_mock.set_time('10/19/22 13:58:30')
    digitales_belegblatt.set_zug_position(1, "Boxberg")

    xml = digitales_belegblatt.generate_image(offset=datetime.strptime('10/19/22 13:00:00', '%m/%d/%y %H:%M:%S'))
    with open(f"{test_path}/tmp/offset.svg", "w", encoding="UTF-8") as f:
        f.write(xml)

    doc = minidom.parse(f"{test_path}/tmp/offset.svg")
    assert len(doc.getElementsByTagName('line')) == 11
    assert len(doc.getElementsByTagName('text')) == 10
    doc.unlink()


def test_fahranfrage_ruecknahme():

    timer_mock = TimerMock()
    digitales_belegblatt = DigitalesBelegblatt(["S-Berg", "C-Stadt"])
    digitales_belegblatt.timer = timer_mock

    timer_mock.set_time('09/19/22 13:55:26')
    digitales_belegblatt.set_zug_position(101, "S-Berg")

    assert "S-Berg" == digitales_belegblatt.get_zug_position(101)

    digitales_belegblatt.block_strecke_for_zugnummer(101, "C-Stadt")

    timer_mock.set_time('09/19/22 13:56:10')
    digitales_belegblatt.revert_strecke_for_zugnummer(101, "C-Stadt")

    timer_mock.set_time('09/19/22 14:03:01')
    digitales_belegblatt.block_strecke_for_zugnummer(101, "C-Stadt")

    xml = digitales_belegblatt.generate_image()
    with open(f"{test_path}/tmp/revert.svg", "w", encoding="UTF-8") as f:
        f.write(xml)

    doc = minidom.parse(f"{test_path}/tmp/revert.svg")
    assert len(doc.getElementsByTagName('line')) == 13
    assert len(doc.getElementsByTagName('text')) == 10
    doc.unlink()

    trains = digitales_belegblatt.get_trains()
    assert trains == {101}

    assert "S-Berg" == digitales_belegblatt.get_zug_position(101)


def test_nothalt_belegblatt():

    timer_mock = TimerMock()
    digitales_belegblatt = DigitalesBelegblatt(["Schwarze Pumpe", "Boxberg", "Cottbus"])
    digitales_belegblatt.timer = timer_mock

    timer_mock.set_time('09/19/22 13:55:26')

    digitales_belegblatt.set_nothalt(True)

    xml = digitales_belegblatt.generate_image()
    with open(f"{test_path}/tmp/nothalt.svg", "w", encoding="UTF-8") as f:
        f.write(xml)

    doc = minidom.parse(f"{test_path}/tmp/nothalt.svg")
    assert len(doc.getElementsByTagName('line')) == 5
    assert len(doc.getElementsByTagName('text')) == 8
    doc.unlink()
