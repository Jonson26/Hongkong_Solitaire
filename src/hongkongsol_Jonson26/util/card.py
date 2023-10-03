import pygame
import random
from util.spritesheet import SpriteSheet

class Deck:
    """Class managing the cards and the table"""
    def __init__(self, settings, screen):
        self.settings = settings
        self.screen = screen
        self.card_types = {
            'RR0':  0,
            'GG0':  1,
            'BB0':  2,
            'F0':  3,
            'BG0': 4, 'BG1': 5, 'BG2': 6, 'BG3': 7,
            'BD0': 8,
            'R1':  9, 'R2': 10, 'R3': 11, 'R4': 12, 'R5': 13, 'R6': 14, 'R7': 15, 'R8': 16, 'R9': 17,
            'G1': 18, 'G2': 19, 'G3': 20, 'G4': 21, 'G5': 22, 'G6': 23, 'G7': 24, 'G8': 25, 'G9': 26,
            'B1': 27, 'B2': 28, 'B3': 29, 'B4': 30, 'B5': 31, 'B6': 32, 'B7': 33, 'B8': 34, 'B9': 35
            }

        self.card_sheet = []
        self.card_deck = []

        self.card_back = None
        self.card_backdrop = None

        self._loadCards()

        self.board = Board(self)

        self.shuffle()

    def _loadCards(self):
        cardsheet = SpriteSheet(self.settings.card_picture)

        w, h, tc = self.settings.card_width, self.settings.card_height, self.settings.tr_color
        for i in range(4):
            for j in range(9):
                self.card_sheet.insert(len(self.card_sheet), cardsheet.image_at((w*j, h*i, w, h), tc))

        playable_card_types = set(self.card_types.keys()).difference({'BG0', 'BG1', 'BG2', 'BG3', 'BD0'})
        for card_type in playable_card_types:
            self.card_deck.insert(len(self.card_deck), Card(card_type, self))
        for x in range(3):
            self.card_deck.insert(len(self.card_deck), Card('RR0', self))
            self.card_deck.insert(len(self.card_deck), Card('GG0', self))
            self.card_deck.insert(len(self.card_deck), Card('BB0', self))

        self.card_back = Card(self.settings.card_back, self)
        self.card_backdrop = Card('BD0', self)

    def shuffle(self):
        random.shuffle(self.card_deck)

    def draw(self):
        self.board.draw()

class Card:
    """Class representing individual cards"""

    def __init__(self, card_type, deck):
        self.card_type = card_type
        self.deck = deck
        self.allowed = {'BD0'}
        if len(self.card_type)==2:
            colours = {'R', 'G', 'B'}
            colours.discard(self.card_type[0])
            num = int(self.card_type[1])+1
            if num>=0:
                for colour in colours:
                    self.allowed.add(colour+str(num))

    #Checks whether this card can be placed on top of another
    def check(self, card):
        return card.card_type in self.allowed

    def draw(self, x, y, scale = 1):
        image = pygame.transform.scale(
            self.deck.card_sheet[self.deck.card_types[self.card_type]],
            (self.deck.settings.card_width*scale,
             self.deck.settings.card_height*scale))
        rect = image.get_rect()
        rect.topleft = x, y
        self.deck.screen.blit(image, rect)

    #Animate a card flying from one point to another
    def animate(self, start_x, start_y, dest_x, dest_y, time=10, scale=1):
        c_x, c_y = start_x, start_y
        len_w = dest_x-start_x
        len_h = dest_y-start_y
        step = 0
        capture = pygame.Surface((self.deck.settings.screen_width, self.deck.settings.screen_height))
        capture.blit(self.deck.screen, (0, 0))
        while step <= time:
            c_x = start_x+int(len_w*(step/time))
            c_y = start_y+int(len_h*(step/time))
            
            self.deck.screen.blit(capture, (0, 0))
            self.draw(c_x, c_y, scale)
            pygame.display.flip()
            pygame.time.wait(1)
            
            step = step+1

class Board:
    """Class representing the board; manages all the piles on it"""
    def __init__(self, deck):
        self.deck = deck
        self.resetPiles()
        
    def resetPiles(self):
        self.piles = []
        width = self.deck.settings.card_width
        height = self.deck.settings.card_height
        for i in range(3):
            self.piles.insert(len(self.piles), Pile(self, (width+5)*i+5, 5, 0, 0))
        for i in range(2):
            self.piles.insert(len(self.piles), Pile(self, (width+5)*(i+3)+5, 5, 0, 3))
        for i in range(3):
            self.piles.insert(len(self.piles), Pile(self, (width+5)*(i+5)+5, 5, 0, 2))
        self.piles[3].stack = []
        self.piles[4].stack.insert(1, self.deck.card_back)
        for i in range(8):
            self.piles.insert(len(self.piles), Pile(self, (width+5)*i+5, height+10, 8, 1))

    def draw(self):
        for pile in self.piles:
            pile.draw()
            
    def clickCheck(self, x, y):
        index = 0
        for pile in self.piles:
            r = pile.clickCheck(x, y)
            if r>0:
                return (index, r)
            index = index+1
        return (-1, -1)
    
class Pile:
    """Class representing a pile of cards"""
    #Pile types:
    #0 - Can hold 1 card
    #1 - Can hold unlimited cards
    #2 - Discard pile
    #3 - Immutable pile
    def __init__(self, board, x, y, stack_offset=0, pile_type=0):
        self.stack_offset = stack_offset;
        self.pile_type = pile_type
        self.board = board
        self.x = x
        self.y = y
        self.stack = [board.deck.card_backdrop]

    def draw(self):
        scale = self.board.deck.settings.scale
        for i in range(len(self.stack)):
            self.stack[i].draw(self.x*scale, (self.y+self.stack_offset*max(0,i-1))*scale, scale)

    #Check if pile clicked
    #Return 0 if not
    #If yes, return how many cards were selected, counting from the top of the pile
    def clickCheck(self, x, y):
        settings = self.board.deck.settings
        scale = settings.scale
        l_x, l_y = self.x*scale, self.y*scale
        w = settings.card_width*scale
        h = settings.card_height*scale + self.stack_offset*(max(0,len(self.stack)-2))*scale

        clickdepth = 0
        while ((l_x <= x and x <= l_x+w) and (l_y <= y and y <= l_y+h)):
            clickdepth = clickdepth+1
            h = self.stack_offset*(max(0,len(self.stack)-(clickdepth+1)))*scale
            if clickdepth>len(self.stack)-2:
                return clickdepth
        return clickdepth

    def getPile(self, depth):
        out = Pile(self.board, 0, 0, self.stack_offset)
        out.stack = []

        if depth == 0 or self.pile_type>=2:
            return out

        if len(self.stack)>1:
            out.stack.insert(len(out.stack), self.stack.pop())
            depth = depth-1

        while depth>0 and len(self.stack)>1:
            if out.stack[-1].check(self.stack[-1]):
                out.stack.insert(len(out.stack), self.stack.pop())
                depth = depth-1
            else:
                depth = 0

        out.stack.insert(len(out.stack), self.board.deck.card_backdrop)
        out.stack.reverse()
        
        return out

    def putPile(self, pile):
        pile.stack.pop(0)
        for card in pile.stack:
            self.stack.insert(len(self.stack), card)
        






        



