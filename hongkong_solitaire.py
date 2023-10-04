import sys
import pygame
import random
from threading import Thread
from settings import Settings
from util.spritesheet import SpriteSheet
from util.card import Deck
from util.ui import UI
from util.about import About

class CardGame:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create resources."""
        pygame.init()
        self.settings = Settings('hongkong.ini')

        self.screen = pygame.display.set_mode(
                (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("HongKong Solitaire")
        self.deck = Deck(self.settings, self.screen)
        self.ui = UI(self.settings, self.screen)
        self.bg_img = pygame.image.load(self.settings.bg_picture)
        self.winnable = False

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                command = self.deck.board.clickCheck(event.pos[0], event.pos[1])
                if command[0]>-1:
                    if command[0]==3:
                        self._stackcolours()
                    else:
                        self._move_pile_effect(self.deck.board.piles[command[0]].getPile(command[1]), command[0])
                    self._automove()
                elif self.ui.buttons[0].click(event.pos[0], event.pos[1]):
                    self._deal_effect()
                elif self.ui.buttons[3].click(event.pos[0], event.pos[1]):
                    Thread(target=About).start()

    def _animate_random_card(self, s_x=0, s_y=0, t=10):
        i = random.randrange(0, len(self.deck.card_deck))
        d_x = random.randrange(0, self.settings.screen_width-self.settings.card_width)
        d_y = random.randrange(0, self.settings.screen_height-self.settings.card_height)

        self.deck.card_deck[i].animate(s_x, s_y, d_x, d_y, t, self.settings.scale)

    def _win_effect(self):
        for i in range(random.randint(40, 80)):
            self._animate_random_card(self.settings.screen_width/2, self.settings.offset*self.settings.scale)
        self.ui.initButton(1)
        self.ui.draw()
        pygame.display.flip()
        pygame.time.wait(1000)
        self.settings.score = self.settings.score + 1
        self.winnable = False
        self.ui.initButton(0)
        
    def _deal_effect(self):
        self.deck.shuffle()
        self.deck.board.resetPiles()
        self._update_screen()
        width = self.settings.card_width
        height = self.settings.card_height
        for i in range(len(self.deck.card_deck)):
            pile = int(i/5)
            self.deck.card_deck[i].animate(self.settings.screen_width/2,
                                           self.settings.offset*self.settings.scale,
                                           ((width+5)*pile+5)*self.settings.scale,
                                           (height+10+8*len(self.deck.board.piles[8+pile].stack)*self.settings.scale),
                                           50, self.settings.scale)
            self.deck.board.piles[8+pile].stack.insert(len(self.deck.board.piles[8+pile].stack),
                                                       self.deck.card_deck[i])
            self._update_screen()
        self.deck.board.piles[4].stack.pop()
        self.winnable = True
        self._automove()

    def _move_pile_effect(self, pile, origin):
        #init animation stuff; do not move empty stacks
        if len(pile.stack)<2:
            return
        self._update_screen()
        capture = pygame.Surface((self.deck.settings.screen_width, self.deck.settings.screen_height))
        capture.blit(self.deck.screen, (0, 0))
        pygame.display.flip()

        #animate stack movement
        run, x, y = True, 0, 0
        while run:
            self.deck.screen.blit(capture, (0, 0))
            x, y = pygame.mouse.get_pos()
            pile.x = x/self.settings.scale-self.settings.card_width/2
            pile.y = y/self.settings.scale-self.settings.offset
            pile.draw()
            pygame.display.flip()
            pygame.time.wait(1)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    run = False

        #try to put stack onto another; if not possible, put it back
        command = self.deck.board.clickCheck(x, y)
        if command[0]>7:
            if pile.stack[1].check(self.deck.board.piles[command[0]].stack[-1]):
                self.deck.board.piles[command[0]].putPile(pile)
                return
        if self.deck.board.piles[command[0]].pile_type==0 and len(pile.stack)==2:
            if len(self.deck.board.piles[command[0]].stack)==1:
                self.deck.board.piles[command[0]].putPile(pile)
                return
        if self.deck.board.piles[command[0]].pile_type==2 and len(pile.stack)==2:
            if len(pile.stack[1].card_type)==2 and pile.stack[1].card_type[0]!='F':
                bottom_type = pile.stack[1].card_type[0] + str(int(pile.stack[1].card_type[1])-1)
                if bottom_type==self.deck.board.piles[command[0]].stack[-1].card_type:
                    self.deck.board.piles[command[0]].putPile(pile)
                    return
                if bottom_type in {'R0','G0','B0'} and len(self.deck.board.piles[command[0]].stack)==1:
                    self.deck.board.piles[command[0]].putPile(pile)
                    return
        self.deck.board.piles[origin].putPile(pile)

    def _automove(self):
        change = False
        piles = self.deck.board.piles
        
        #todo: detect if "0" cards can be taken away
        stackbuttonstatus = ''
        for colour in ['GG0', 'BB0', 'RR0']:
            counter = 0
            for pile in piles:
                if pile.pile_type<2:
                    if pile.stack[-1].card_type == colour:
                        counter=counter+1
            stackbuttonstatus = stackbuttonstatus + ('1' if counter==4 else '0')
        self.ui.buttons[1].setLook(stackbuttonstatus)
        
        #try to move the flower to the middle field
        if len(self.deck.board.piles[4].stack)==1:
            change = self._move_card('F0',4)

        #try to move numered cards to the discard piles
        maxcard = max(min(len(piles[5].stack), len(piles[6].stack), len(piles[7].stack)), 2)
        for c in [('R', 5), ('G', 6), ('B', 7)]:
            if len(piles[c[1]].stack)==1:
                change = self._move_card(c[0]+'1',c[1])
            else:
                change = self._move_card(c[0]+str(maxcard), c[1])#int(piles[c[1]].stack[-1].card_type[1])+1), c[1])
            if change:
                break

        #check if won
        if self.winnable and piles[0].pile_type == 3 and piles[1].pile_type == 3 and piles[2].pile_type == 3 and piles[4].stack[-1].card_type == 'F0' and piles[5].stack[-1].card_type == 'R9' and piles[6].stack[-1].card_type == 'G9' and piles[7].stack[-1].card_type == 'B9':
            self._win_effect()
        
        if change:
            self._automove()

    def _move_card(self, card_type, destination):
        piles = self.deck.board.piles
        scale = self.settings.scale
        tosearch = set(range(3)) | set(range(8, 16))
        for i in tosearch:
                if piles[i].stack[-1].card_type==card_type:
                    card = piles[i].stack.pop()
                    self._update_screen()
                    card.animate(
                        piles[i].x*scale,
                        (piles[i].y+
                         self.settings.card_height+
                         piles[i].stack_offset*
                         (max(0,len(piles[i].stack)-2)))*scale,
                        piles[destination].x*scale,
                        piles[destination].y*scale,
                        50,
                        scale)
                    piles[destination].stack.insert(len(piles[destination].stack), card)
                    return True
        return False

    def _stackcolours(self):
        for colour in ['GG0', 'BB0', 'RR0']:
            superbreak = False
            counter = 0
            for pile in self.deck.board.piles:
                if pile.pile_type<2:
                    if pile.stack[-1].card_type == colour:
                        counter=counter+1
            if counter==4:
                for i in range(3):
                    if len(self.deck.board.piles[i].stack)==1 or self.deck.board.piles[i].stack[-1].card_type==colour:
                        for pile in self.deck.board.piles:
                            if pile.pile_type<2:
                                if pile.stack[-1].card_type == colour:
                                    card = pile.stack.pop()
                                    self._update_screen()
                                    card.animate(
                                        pile.x*self.settings.scale,
                                        (pile.y+
                                         self.settings.card_height+
                                         pile.stack_offset*
                                         (max(0,len(pile.stack)-2)))*self.settings.scale,
                                        self.deck.board.piles[i].x*self.settings.scale,
                                        self.deck.board.piles[i].y*self.settings.scale,
                                        50,
                                        self.settings.scale)
                        self.deck.board.piles[i].stack.insert(len(self.deck.board.piles[i].stack), self.deck.card_back)
                        self.deck.board.piles[i].pile_type = 3
                        superbreak = True
                        break
            if superbreak:
                break
    
    def _quit(self):
        self.ui.settings.quit()
        pygame.display.quit()
        pygame.quit()
        sys.exit()

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)

        scale = self.settings.scale
        image = self.bg_img
        image = pygame.transform.scale(image,
                                       (image.get_width()*scale,
                                        image.get_height()*scale))
        rect = image.get_rect()
        rect.topleft = 0, 0
        self.screen.blit(image, rect)

        self.deck.draw()
        self.ui.draw()

        pygame.display.flip()

if __name__ == "__main__":
    game = CardGame()
    game.run_game()
