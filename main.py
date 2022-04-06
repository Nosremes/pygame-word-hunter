import pygame
from pygame.locals import *
import sys
import random

colors = {
    "white":(255,255,255),
    "black":(0,0,0)}

words = [
    "amor","cachorro","cama","luz",
    "armario","sofa"]

pygame.init()
x,y = (800,600)
window = pygame.display.set_mode((x,y))
pygame.display.set_caption("Formando palavras")


class DrawMainWord:
    def __init__(self,margin_y,all_words):
        self.margin_x = None
        self.margin_y = margin_y
        self.all_words = all_words
        self.word = None
        self.letter_index = None
        self.win = False
        self.font = pygame.font.SysFont("Arial",100,True)
        self.update_word()

    def draw(self,window):
        if self.win:
            surface = self.font.render(self.word,True,colors["black"])
            self.margin_x = 800 / 2 - surface.get_width()/2
            window.blit(surface,(self.margin_x,self.margin_y))
        else:
            word = list(self.word)
            word[self.letter_index] = "_"
            word = "".join(word)
            surface = self.font.render(word,True,colors["black"])
            self.margin_x = 800 / 2 - surface.get_width()/2
            window.blit(surface,(self.margin_x,self.margin_y))

    def track_keys(self,event):
        if event.key == K_SPACE:
            self.update_word()
        if pygame.key.name(event.key) == self.word[self.letter_index]:
            self.win = True

    def update_word(self):
        new_word = random.choice(self.all_words)
        if new_word != self.word:
            self.word = new_word
            self.letter_index = random.randint(0,len(new_word) - 1)
            self.win = False
        else:
            self.update_word()

class Letters:
    def __init__(self,word):
        self.alphabet = [
                "A","B","C","D","E","F","G",
                "H","I","J","K","L","M","N",
                "O","P","Q","R","S","T","U",
                "V","W","X","Y","Z"]
        self.mode = "dica"
        self.word = word
        self.x = 100
        self.y = 300
        self.space_between = 20
        self.font = pygame.font.SysFont("Arial",35,True)
        self.all_surfaces = [self.font.render(x,True,colors["black"]) for x in self.alphabet]
    
    def draw(self,window):
        x = self.x 
        y = self.y
        for surface in self.all_surfaces:
            if (x + surface.get_width() + self.space_between) > 700:
                y += 100
                x = self.x

            window.blit(surface,(x,y))
            x += surface.get_width() + self.space_between
    
    def opstions_alpha(self):
        self.opstions_alpha = None

word = DrawMainWord(100,words)
letters_buttons = Letters(word)
while True:
    window.fill(colors["white"])
    word.draw(window)
    letters_buttons.draw(window)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            word.track_keys(event)
    pygame.display.update()    



