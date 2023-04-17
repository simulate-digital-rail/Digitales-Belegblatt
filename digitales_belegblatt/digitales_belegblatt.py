from datetime import datetime, timedelta
from typing import List
from PIL import Image , ImageDraw , ImageFont, ImageColor


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
        
        from_position = self.get_zug_position(zugnummer,)
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
        
        woff = 80
        hoff = 50
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
        for i in range(l):
            x = woff + i * w

            text = self.betriebsstellen[i]
            t_width, t_height = draw.textsize(text, font)
            draw.text((x - t_width/2, (hoff - t_height)/2), text, fill=(0,0,0), font=font)

            draw.line((x,hoff, x,height), fill=(0,0,0))

        #draw time

        min_t , max_t = self._get_min_max_time()
        start_t = rounded_to_the_last_15th_minute_epoch(min_t)
        end_t = rounded_to_the_next_30th_minute_epoch(max_t)
        x_t = start_t   
        while x_t <= end_t:

            text = x_t.strftime("%H:%M")
            t_width, t_height = draw.textsize(text, font)
            i = (x_t - start_t) / timedelta(minutes=15)
            y = hoff +  i * toff
            draw.text(((woff - t_width)/2, y - t_height/2), text, fill=(0,0,0), font=font)
            draw.line((woff,y, width - woff,y), fill=(0,0,0))

            x_t = x_t + timedelta(minutes=15)
            
        # paint Blocks
        for dt, zugnummer , from_pos , to_pos in self.strecken_block:
            #dt -> y
            i = (dt - start_t) / timedelta(minutes=15)
            y = hoff +  i * toff

            from_i = self.betriebsstellen.index(from_pos)
            to_i = self.betriebsstellen.index(to_pos)
            from_x = woff + from_i * w
            to_x = woff + to_i * w

            # trainnummber
            text = str(zugnummer)
            t_width, t_height = draw.textsize(text, font)
            t_x = woff + abs(from_x - to_x)/2 - t_width/2
            t_y = y - t_height - 2
            draw.text( (t_x , t_y), text, fill=ImageColor.getrgb("red"), font=font)

            draw.line((from_x,y, to_x,y), fill=ImageColor.getrgb("red"), width=3)
            #draw arrow
            if from_x < to_x:
                draw.line((to_x-10,y-10, to_x,y), fill=ImageColor.getrgb("red"), width=3)
                draw.line((to_x-10,y+10, to_x,y), fill=ImageColor.getrgb("red"), width=3)
            else:
                draw.line((to_x+10,y-10, to_x,y), fill=ImageColor.getrgb("red"), width=3)
                draw.line((to_x+10,y+10, to_x,y), fill=ImageColor.getrgb("red"), width=3)

        # züge eintragen
        for _, positions in self.zug_positionen.items(): 
            for i in range(1,len(positions)):
                dt_from , from_pos = positions[i-1]
                dt_to , to_pos = positions[i]

                from_i = self.betriebsstellen.index(from_pos)
                to_i = self.betriebsstellen.index(to_pos)
                from_x = woff + from_i * w
                to_x = woff + to_i * w

                i = (dt_from - start_t) / timedelta(minutes=15)
                from_y = hoff +  i * toff
                
                i = (dt_to - start_t) / timedelta(minutes=15)
                to_y = hoff +  i * toff

                draw.line((from_x,from_y, to_x,to_y), fill=ImageColor.getrgb("green"), width=3)



        return img
