from datetime import datetime
from typing import List

class DigitalesBelegblatt:

    def __init__(self,betriebsstellen : List[str]):
        self.betriebsstellen = betriebsstellen
        self.zug_positionen = {}
        self.strecken_block = []

    def set_zug_position(self,zugnummer : int, position : str):
        """ Zugposition dem Digitalen Belegblatt bekannt geben, Im Belegblatt wird eine grüne Line, von der 
            letzten Position bis jetzt gezeichnet"""
        if position not in self.betriebsstellen:
            raise ValueError(f"Betriebsstelle {position} nicht bekannt")
        if zugnummer not in self.zug_positionen:
            self.zug_positionen[zugnummer] = []
        
        self.zug_positionen[zugnummer].append((datetime.now(),position))

    def get_zug_position(self,zugnummer : int):
        """ Hilfsfunktion, das das Belegblatt weiß wo sich der Zug befindet """
        if zugnummer not in self.zug_positionen:
            return None
        return self.zug_positionen[zugnummer][-1][1]

    
    def block_strecke_for_zugnummer(self,zugnummer : int,to_position : str):
        """ Es wird im Belegblatt zum aktuellen Zeitpunkt eine rote Line mit Zugnummer von zugposition bis to_position gezeichnet """
        if zugnummer not in self.zug_positionen:
            raise ValueError(f"Zugposition von Zug {zugnummer} nicht bekannt")
        if to_position not in self.betriebsstellen:
            raise ValueError(f"Betriebsstelle {to_position} nicht bekannt")
        
        from_position = self.get_zug_position(zugnummer,)
        self.strecken_block.append((datetime.now(),zugnummer,from_position,to_position))
