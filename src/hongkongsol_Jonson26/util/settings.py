import math
import os.path
from configparser import ConfigParser

class Settings:

    def __init__(self, file='hongkong.ini'):
        self.file = file
        if not os.path.isfile(self.file):
            self.scale = 5
            self.card_width, self.card_height = 11, 17
            self.offset = 5
            
            self.screen_width = (self.offset + (self.card_width+self.offset)*8)*self.scale
            self.screen_height = (self.offset*3 + self.card_height*2 + self.card_height*6)*self.scale
            self.bg_color = '#E1E1E1'

            self.tr_color = '#FF00FF'

            self.card_back = 'BG0'
            self.card_picture = 'assets/spritesheet_alt.png'
            self.ui_picture = 'assets/ui.png'
            self.bg_picture = 'assets/bg.jpg'

            self.score = 0
        else:
            config = ConfigParser()
            config.read(file)
            
            self.scale = config.getint('Size', 'scale')
            self.card_width, self.card_height = config.getint('Size', 'card_width'), config.getint('Size', 'card_height')
            self.offset = config.getint('Size', 'offset')
            
            self.screen_width = (self.offset + (self.card_width+self.offset)*8)*self.scale
            self.screen_height = (self.offset*3 + self.card_height*2 + self.card_height*6)*self.scale

            self.bg_color = config.get('Graphics', 'bg_color')
            self.tr_color = config.get('Graphics', 'tr_color')

            self.card_back = config.get('Graphics', 'card_back')
            
            self.card_picture = config.get('Graphics', 'card_picture')
            self.ui_picture = config.get('Graphics', 'ui_picture')
            self.bg_picture = config.get('Graphics', 'bg_picture')

            self.score = config.getint('Game', 'score')

    def quit(self):
        config = ConfigParser()

        config.add_section("""                       Hongkong Solitaire                       ]
#               Shenzhen Solitaire Clone in Python               
#               All Assets (c) 2023 Filip Jamroga                
#    All Code (c) 2023 Filip Jamroga, unless stated otherwise    
#              spritesheet.py (c) 2019 Eric Matthes              
#SHENZHEN SOLITAIRE is (c) 2016 Zachtronics. All rights reserved.
#================================================================

[Settings File""")
        config.add_section('Size')
        config.add_section('Graphics')
        config.add_section('Game')
        
        config.set('Size', 'scale', str(self.scale))
        config.set('Size', 'card_width', str(self.card_width))
        config.set('Size', 'card_height', str(self.card_height))
        config.set('Size', 'offset', str(self.offset))

        config.set('Graphics', 'bg_color', str(self.bg_color))
        config.set('Graphics', 'tr_color', str(self.tr_color))

        config.set('Graphics', 'card_back', str(self.card_back))
        
        config.set('Graphics', 'card_picture', str(self.card_picture))
        config.set('Graphics', 'ui_picture', str(self.ui_picture))
        config.set('Graphics', 'bg_picture', str(self.bg_picture))

        config.set('Game', 'score', str(self.score))
        with open(self.file, 'w') as configfile:
            config.write(configfile)
