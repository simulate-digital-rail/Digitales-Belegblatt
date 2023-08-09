from  datetime import datetime
from xml.dom import minidom

from digitales_belegblatt.digitales_belegblatt import DigitalesBelegblatt

class TimerMock():

    def __init__(self):
        self._now = datetime.now()

    def now(self):
        return self._now

    def set_time(self,time_string : str):
        self._now = datetime.strptime(time_string, '%m/%d/%y %H:%M:%S')

def test_empty_belegblatt():

    timer_mock = TimerMock()
    digitales_belegblatt = DigitalesBelegblatt(["Schwarze Pumpe","Boxberg","Cottbus"])
    digitales_belegblatt.timer = timer_mock

    timer_mock.set_time('09/19/22 13:55:26')

    xml = digitales_belegblatt.generate_image()
    with open("tmp/empty.svg","w",encoding="UTF-8") as f:
        f.write(xml)

    doc = minidom.parse("tmp/empty.svg")
    assert len(doc.getElementsByTagName('line')) == 5
    assert len(doc.getElementsByTagName('text')) == 7
    doc.unlink()


def test_zug_position():

    timer_mock = TimerMock()
    digitales_belegblatt = DigitalesBelegblatt(["Schwarze Pumpe","Boxberg","Cottbus"])
    digitales_belegblatt.timer = timer_mock

    timer_mock.set_time('09/19/22 13:55:26')
    digitales_belegblatt.set_zug_position(101,"Schwarze Pumpe")
    digitales_belegblatt.set_zug_position(102,"Cottbus")

    assert "Schwarze Pumpe" == digitales_belegblatt.get_zug_position(101)
    assert "Cottbus" == digitales_belegblatt.get_zug_position(102)

    digitales_belegblatt.block_strecke_for_zugnummer(102,"Schwarze Pumpe")

    timer_mock.set_time('09/19/22 14:10:26')
    digitales_belegblatt.set_zug_position(102,"Boxberg")

    timer_mock.set_time('09/19/22 14:13:00')
    digitales_belegblatt.set_zug_position(102,"Schwarze Pumpe")

    timer_mock.set_time('09/19/22 14:15:00')
    digitales_belegblatt.block_strecke_for_zugnummer(101,"Boxberg")

    timer_mock.set_time('09/19/22 14:30:26')
    digitales_belegblatt.set_zug_position(101,"Boxberg")

    xml = digitales_belegblatt.generate_image()
    with open("tmp/test.svg","w",encoding="UTF-8") as f:
        f.write(xml)

    doc = minidom.parse("tmp/test.svg")
    assert len(doc.getElementsByTagName('line')) == 20
    assert len(doc.getElementsByTagName('text')) == 13
    doc.unlink()

    trains = digitales_belegblatt.get_trains()
    assert trains == {101,102}

    assert "Boxberg" == digitales_belegblatt.get_zug_position(101)
    assert "Schwarze Pumpe" == digitales_belegblatt.get_zug_position(102)


def test_zug_position_stretched():

    timer_mock = TimerMock()
    digitales_belegblatt = DigitalesBelegblatt(["Schwarze Pumpe","Boxberg"])
    digitales_belegblatt.timer = timer_mock

    timer_mock.set_time('09/19/22 13:55:00')
    digitales_belegblatt.set_zug_position(1,"Schwarze Pumpe")
    digitales_belegblatt.set_zug_position(2,"Boxberg")

    assert "Schwarze Pumpe" == digitales_belegblatt.get_zug_position(1)
    assert "Boxberg" == digitales_belegblatt.get_zug_position(2)

    timer_mock.set_time('09/19/22 13:55:26')
    digitales_belegblatt.block_strecke_for_zugnummer(2,"Schwarze Pumpe")

    timer_mock.set_time('09/19/22 13:56:26')
    digitales_belegblatt.set_zug_position(2,"Schwarze Pumpe")



    timer_mock.set_time('09/19/22 13:57:15')
    digitales_belegblatt.block_strecke_for_zugnummer(1,"Boxberg")

    timer_mock.set_time('09/19/22 13:57:30')
    digitales_belegblatt.set_zug_position(1,"Boxberg")

    xml = digitales_belegblatt.generate_image(minutes=1)
    with open("tmp/stretched.svg","w",encoding="UTF-8") as f:
        f.write(xml)

    doc = minidom.parse("tmp/stretched.svg")
    assert len(doc.getElementsByTagName('line')) == 16
    assert len(doc.getElementsByTagName('text')) == 10
    doc.unlink()




def test_zug_position_offset():

    timer_mock = TimerMock()
    digitales_belegblatt = DigitalesBelegblatt(["Schwarze Pumpe","Boxberg"])
    digitales_belegblatt.timer = timer_mock

    timer_mock.set_time('09/19/22 13:55:00')
    digitales_belegblatt.set_zug_position(1,"Schwarze Pumpe")
    digitales_belegblatt.set_zug_position(2,"Boxberg")

    assert "Schwarze Pumpe" == digitales_belegblatt.get_zug_position(1)
    assert "Boxberg" == digitales_belegblatt.get_zug_position(2)

    timer_mock.set_time('09/19/22 13:55:26')
    digitales_belegblatt.block_strecke_for_zugnummer(2,"Schwarze Pumpe")

    timer_mock.set_time('09/19/22 14:02:26')
    digitales_belegblatt.set_zug_position(2,"Schwarze Pumpe")



    timer_mock.set_time('10/19/22 13:40:15')
    digitales_belegblatt.block_strecke_for_zugnummer(1,"Boxberg")

    timer_mock.set_time('10/19/22 13:58:30')
    digitales_belegblatt.set_zug_position(1,"Boxberg")

    xml = digitales_belegblatt.generate_image(offset=datetime.strptime('10/19/22 13:00:00', '%m/%d/%y %H:%M:%S'))
    with open("tmp/offset.svg","w",encoding="UTF-8") as f:
        f.write(xml)

    doc = minidom.parse("tmp/offset.svg")
    assert len(doc.getElementsByTagName('line')) == 10
    assert len(doc.getElementsByTagName('text')) == 8
    doc.unlink()