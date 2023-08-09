from datetime import datetime, timedelta
from typing import List
import svgwrite

def rounded_to_the_last_15th_minute_epoch(dt):
    rounded = dt - (dt - datetime.min) % timedelta(minutes=15)
    return rounded

def rounded_to_the_next_30th_minute_epoch(dt):
    rounded = dt + (datetime.min - dt) % timedelta(minutes=30)
    return rounded

class DigitalesBelegblatt:

    def __init__(self,betriebsstellen : List[str]):
        self.betriebsstellen = betriebsstellen
        self.zug_positionen = {}
        self.strecken_block = []
        self.timer = datetime

    def set_zug_position(self,zugnummer : int, position : str):
        """ Zugposition dem Digitalen Belegblatt bekannt geben, Im Belegblatt wird eine grüne Line, von der 
            letzten Position bis jetzt gezeichnet"""
        if position not in self.betriebsstellen:
            raise ValueError(f"Betriebsstelle {position} nicht bekannt")
        if zugnummer not in self.zug_positionen:
            self.zug_positionen[zugnummer] = []
        
        self.zug_positionen[zugnummer].append((self.timer.now(),position))

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
        
        from_position = self.get_zug_position(zugnummer)

        #Update Zugposition
        self.set_zug_position(zugnummer,from_position)

        self.strecken_block.append((self.timer.now(),zugnummer,from_position,to_position))


    def _get_min_max_time(self):
        times = []
        for _, positions in self.zug_positionen.items(): 
            for dt , _ in positions:
                times.append(dt)

        for dt, _ , _ , _ in self.strecken_block:
                times.append(dt)
    	
        times.sort()
        return times[0] , times[-1]

    def generate_image(self):

        width = 800
        height = 600
        
        woff = 80 # Rand rechts und Links
        hoff = 50 # Rand oben
        toff = 50 # horizontaler Abstand der 15 Minutenlinien 
        



        svg_document = svgwrite.Drawing(size = ("800px", "600px"))


        # draw Betriebsstellen
        l = len(self.betriebsstellen)
        w = (width - 2 * woff) / (l - 1)

        x_p = lambda i : woff + i * w

        for i in range(l):
            
            # Betriebsstellentext
            text = self.betriebsstellen[i]
            svg_document.add(svg_document.text(text, insert = (x_p(i) , hoff/2),  style = "font-size:10px; font-family:Arial; text-anchor: middle;dominant-baseline: middle;"))
            
            # Vertikale Linie
            svg_document.add(svg_document.line((x_p(i),hoff), (x_p(i),height), stroke=svgwrite.rgb(83, 83, 83, '%')))

        

        #draw time
        min_t , max_t = self._get_min_max_time()
        start_t = rounded_to_the_last_15th_minute_epoch(min_t)
        end_t = rounded_to_the_next_30th_minute_epoch(max_t)
        x_t = start_t   

        y_t = lambda dt : hoff + ((dt - start_t) / timedelta(minutes=15)) * toff

        while x_t <= end_t:

            text = x_t.strftime("%H:%M")
           
            # Zeittext
            svg_document.add(svg_document.text(text, insert = (woff/2 , y_t(x_t)),  style = "font-size:10px; font-family:Arial; text-anchor: middle;dominant-baseline: middle;"))

           

            # Horizontale Line
            svg_document.add(svg_document.line((woff,y_t(x_t)), (width - woff,y_t(x_t)), stroke=svgwrite.rgb(83, 83, 83, '%')))

            x_t = x_t + timedelta(minutes=15)
            

        # paint Blocks
        for dt, zugnummer , from_pos , to_pos in self.strecken_block:
           
            y = y_t(dt)

            from_i = self.betriebsstellen.index(from_pos)
            to_i = self.betriebsstellen.index(to_pos)
            from_x = x_p(from_i)
            to_x = x_p(to_i)

            # trainnummber
            text = str(zugnummer)
            t_x = woff + abs(from_x - to_x)/2
            t_y = y - 5

            #Train Number
            svg_document.add(svg_document.text(text, insert = (t_x , t_y),  style = "font-size:10px; font-family:Arial; text-anchor: middle;dominant-baseline: middle;"))


            # Red line 
            svg_document.add(svg_document.line((from_x,y), (to_x,y), stroke=svgwrite.rgb(100, 0, 0, '%')))

         
            #draw arrow
            a = 10
            if from_x < to_x: a = -10
            svg_document.add(svg_document.line((to_x+a,y-5), (to_x,y), stroke=svgwrite.rgb(100, 0, 0, '%')))
            svg_document.add(svg_document.line((to_x+a,y+5), (to_x,y), stroke=svgwrite.rgb(100, 0, 0, '%')))



        # draw trains 
        for _, positions in self.zug_positionen.items(): 
            for i in range(1,len(positions)):
                dt_from , from_pos = positions[i-1]
                dt_to , to_pos = positions[i]

                from_i = self.betriebsstellen.index(from_pos)
                to_i = self.betriebsstellen.index(to_pos)
                from_x = x_p(from_i)
                to_x = x_p(to_i)

                i = (dt_from - start_t) / timedelta(minutes=15)
                from_y = hoff +  i * toff
                
                i = (dt_to - start_t) / timedelta(minutes=15)
                to_y = hoff +  i * toff


                svg_document.add(svg_document.line((from_x,from_y), (to_x,to_y), stroke=svgwrite.rgb(0, 39, 0, '%')))

               

        return svg_document.tostring()
