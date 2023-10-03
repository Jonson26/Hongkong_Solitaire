import pygame
from util.spritesheet import SpriteSheet

class UI:
    def __init__(self, settings, screen):
        self.settings = settings
        self.screen = screen
        self.uisheet = SpriteSheet(self.settings.ui_picture)
        self.buttons = []
        self.initButton()

    def initButton(self, bnum=0):
        if bnum == 0:
            self.buttons = []
            self.buttons.insert(len(self.buttons), Button(self.settings.offset*self.settings.scale,
                                       self.settings.screen_height-(self.settings.offset+13)*self.settings.scale,
                                       self.uisheet.image_at((0, 0, 47, 13), self.settings.tr_color),
                                       self))
            self.buttons.insert(len(self.buttons), StackButton((self.settings.offset*4+self.settings.card_width*3+2)*self.settings.scale,
                                       (self.settings.offset+2)*self.settings.scale,
                                       self.uisheet.load_strip((0, 26, 7, 13), 8, self.settings.tr_color),
                                       self))
            self.buttons.insert(len(self.buttons), WinCounter((self.settings.offset*5+self.settings.card_width*5)*self.settings.scale,
                                       self.settings.screen_height-(self.settings.offset+15)*self.settings.scale,
                                       self.settings.score,
                                       self.uisheet.image_at((0, 50, 51, 17), self.settings.tr_color),
                                       self.uisheet.load_strip((0, 39, 7, 11), 10, self.settings.tr_color),
                                       self))
            self.buttons.insert(len(self.buttons), Button((self.settings.offset*2+47)*self.settings.scale,
                                       self.settings.screen_height-(self.settings.offset+13)*self.settings.scale,
                                       self.uisheet.image_at((47, 0, 11, 13), self.settings.tr_color),
                                       self))
        if bnum == 1:
            self.buttons = []
            self.buttons.insert(len(self.buttons), Button(self.settings.screen_width/2-24*self.settings.scale,
                                       self.settings.screen_height/2-7*self.settings.scale,
                                       self.uisheet.image_at((0, 13, 48, 13), self.settings.tr_color),
                                       self))
    def draw(self):
        for button in self.buttons:
            button.draw()

class Button:
    def __init__(self, x, y, image, ui):
        self.x = x
        self.y = y
        self.image = image
        self.ui = ui

    def draw(self):
        scale = self.ui.settings.scale
        image = pygame.transform.scale(self.image,
                                       (self.image.get_width()*scale,
                                        self.image.get_height()*scale))
        rect = image.get_rect()
        rect.topleft = self.x, self.y
        self.ui.screen.blit(image, rect)

    def click(self, x, y):
        scale = self.ui.settings.scale
        return (self.x <= x and x <= self.x+self.image.get_width()*scale) and (self.y <= y and y <= self.y+self.image.get_height()*scale)

class StackButton:
    def __init__(self, x, y, images, ui):
        self.x = x
        self.y = y
        self.images = images
        self.current_image = 0
        self.ui = ui

    def draw(self):
        scale = self.ui.settings.scale
        image = self.images[self.current_image]
        image = pygame.transform.scale(image,
                                       (image.get_width()*scale,
                                        image.get_height()*scale))
        rect = image.get_rect()
        rect.topleft = self.x, self.y
        self.ui.screen.blit(image, rect)

    def setLook(self, look):
        num = 0
        num = num + int(look[2])
        num = num + 2*int(look[1])
        num = num + 4*int(look[0])
        self.current_image = num

class WinCounter:
    
    def __init__(self, x, y, num, image, numimages, ui):
        self.x = x
        self.y = y
        self.num = num
        self.image = image
        self.numimages = numimages
        self.current_image = 0
        self.ui = ui

    def draw(self):
        scale = self.ui.settings.scale
        image = self.image
        image = pygame.transform.scale(image,
                                       (image.get_width()*scale,
                                        image.get_height()*scale))
        rect = image.get_rect()
        rect.topleft = self.x, self.y
        self.ui.screen.blit(image, rect)
        digit = [int(self.num/100)%10+1, int(self.num/10)%10+1, self.num%10+1]
        for i in range(3):
            if digit[0]==1:
                digit[0]=0
                if digit[1]==1:
                    digit[1]=0
            image = self.numimages[digit[i]]
            image = pygame.transform.scale(image,
                                            (image.get_width()*scale,
                                            image.get_height()*scale))
            rect = image.get_rect()
            rect.topleft = self.x+27*scale+image.get_width()*i, self.y+3*scale
            self.ui.screen.blit(image, rect)
