from  datetime import datetime
from PIL import Image 

from digitales_belegblatt.digitales_belegblatt import DigitalesBelegblatt

class TimerMock():

    def __init__(self):
        self._now = datetime.now()

    def now(self):
        return self._now

    def set_time(self,time_string : str):
        self._now = datetime.strptime(time_string, '%m/%d/%y %H:%M:%S')

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

    timer_mock.set_time('09/19/22 14:20:26')

    digitales_belegblatt.block_strecke_for_zugnummer(101,"Boxberg")

    timer_mock.set_time('09/19/22 14:30:26')
    digitales_belegblatt.set_zug_position(101,"Boxberg")


    img : Image = digitales_belegblatt.generate_image()
    img.save("test.png")
