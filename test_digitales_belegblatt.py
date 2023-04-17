from  datetime import datetime
class TimerMock():

    def __init__(self):
        self._now = datetime.now()
    def now(self):
        return self._now
    
def test_zug_position():
    from digitales_belegblatt.digitales_belegblatt import DigitalesBelegblatt
    from PIL import Image 
    timer_mock = TimerMock()
    db = DigitalesBelegblatt(["Schwarze Pumpe","Boxberg","Cottbus"])
    db.timer = timer_mock

    timer_mock._now = datetime.strptime('09/19/22 13:55:26', '%m/%d/%y %H:%M:%S')
    db.set_zug_position(101,"Schwarze Pumpe")
    db.set_zug_position(102,"Cottbus")

    assert "Schwarze Pumpe" == db.get_zug_position(101)
    assert "Cottbus" == db.get_zug_position(102)

    db.block_strecke_for_zugnummer(102,"Schwarze Pumpe")

    timer_mock._now = datetime.strptime('09/19/22 14:10:26', '%m/%d/%y %H:%M:%S')
    db.set_zug_position(102,"Boxberg")
    timer_mock._now = datetime.strptime('09/19/22 14:13:00', '%m/%d/%y %H:%M:%S')
    db.set_zug_position(102,"Schwarze Pumpe")

    timer_mock._now = datetime.strptime('09/19/22 14:20:26', '%m/%d/%y %H:%M:%S')

    db.block_strecke_for_zugnummer(101,"Boxberg")
    
    db.set_zug_position(101,"Schwarze Pumpe") # Simuliert

    timer_mock._now = datetime.strptime('09/19/22 14:30:26', '%m/%d/%y %H:%M:%S')
    db.set_zug_position(101,"Boxberg")


    img : Image = db.generate_image()
    img.save("test.png")