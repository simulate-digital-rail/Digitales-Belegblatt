from datetime import datetime, timedelta
from typing import List
from PIL import Image , ImageDraw , ImageFont, ImageColor
import aggdraw

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
        
        #font = 'Roboto-Bold.ttf'
        #font_size = 14
        #font = ImageFont.truetype(font,size=font_size)
        font = ImageFont.load_default()

        img  = Image.new( mode = "RGB", size = (width, height) , color = (255, 255, 255))
        draw = ImageDraw.Draw(img)

        # draw Betriebsstellen
        l = len(self.betriebsstellen)
        w = (width - 2 * woff) / (l - 1)

        x_p = lambda i : woff + i * w

        for i in range(l):
            
            # Betriebsstellentext
            text = self.betriebsstellen[i]
            (left, top, right, bottom) = draw.textbbox((0,0),text, font)
            draw.text((x_p(i) - (right - left)/2, (hoff - (bottom - top))/2), text, fill=(0,0,0), font=font)
            
            # Vertikale Linie
            draw.line((x_p(i),hoff, x_p(i),height), fill=ImageColor.getrgb("lightgrey"))

        #draw time
        min_t , max_t = self._get_min_max_time()
        start_t = rounded_to_the_last_15th_minute_epoch(min_t)
        end_t = rounded_to_the_next_30th_minute_epoch(max_t)
        x_t = start_t   

        y_t = lambda dt : hoff + ((dt - start_t) / timedelta(minutes=15)) * toff

        while x_t <= end_t:

            text = x_t.strftime("%H:%M")
            (left, top, right, bottom) = draw.textbbox((0,0),text, font)
           
            # Zeittext
            draw.text(((woff - (right-left))/2, y_t(x_t) - (bottom- top)/2), text, fill=(0,0,0), font=font)

            # Horizontale Line
            draw.line((woff,y_t(x_t), width - woff,y_t(x_t)), fill=ImageColor.getrgb("lightgrey"))

            x_t = x_t + timedelta(minutes=15)
            
        # paint Blocks
        red_pen = aggdraw.Pen("red", 2)
        for dt, zugnummer , from_pos , to_pos in self.strecken_block:
           
            y = y_t(dt)

            from_i = self.betriebsstellen.index(from_pos)
            to_i = self.betriebsstellen.index(to_pos)
            from_x = x_p(from_i)
            to_x = x_p(to_i)

            # trainnummber
            text = str(zugnummer)
            (left, top, right, bottom) = draw.textbbox((0,0),text, font)
            t_x = woff + abs(from_x - to_x)/2 - (right - left)/2
            t_y = y - (bottom - top) - 2

            draw.text( (t_x , t_y), text, fill=ImageColor.getrgb("red"), font=font)


            draw2 = aggdraw.Draw(img)
            draw2.line((from_x,y, to_x,y), red_pen)
            #draw arrow
            a = 10
            if from_x < to_x: a = -10
            draw2.line((to_x+a,y-5, to_x,y), red_pen)
            draw2.line((to_x+a,y+5, to_x,y), red_pen)
            draw2.flush()
         

        # draw trains 
        green_pen = aggdraw.Pen("green", 1)
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

                draw2 = aggdraw.Draw(img)
                draw2.line((from_x,from_y, to_x,to_y), green_pen)
                draw2.flush()

        return img
