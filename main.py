import pygame
from pygame.locals import *
import sys
import random

colors = {
    "white":(255,255,255),"black":(0,0,0),
    "red":(255,0,0),"green":(0,255,0),"blue":(0,0,255)}

words_teste = [
    "amor","cachorro","cama","luz",
    "armario","sofa"]

with open("database.txt") as f:
    words = f.readline().split(" ")
    #print(words)

pygame.init()
x,y = (800,600)
window = pygame.display.set_mode((x,y))
pygame.display.set_caption("Word hunter")

class DrawMainWord:
    def __init__(self,margin_y,all_words):
        self.margin_x = None
        self.margin_y = margin_y
        self.all_words = all_words
        self.word = None
        self.letter = None
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


    def update_word(self):
        new_word = random.choice(self.all_words)
        if new_word != self.word:
            self.word = new_word
            self.letter_index = random.randint(0,len(new_word) - 1)
            self.letter = self.word[self.letter_index]
            self.win = False
        else:
            self.update_word()

    def try_letter(self,letter):
        if letter.upper() == self.word[self.letter_index].upper():
            global points
            if not self.win:
                points += 1
            self.win = True
            return True
        return False

class Letters:
    ALPHABET = [
                "A","B","C","D","E","F","G",
                "H","I","J","K","L","M","N",
                "O","P","Q","R","S","T","U",
                "V","W","X","Y","Z"]
    
    def __init__(self,word):
        self.alphabet = type(self).ALPHABET.copy()
        self.wrongs = []
        self.word = word
        self.font = pygame.font.SysFont("Arial",35,True)
        self.all_surfaces = [
                self.font.render(x,True,colors["black"])for x in self.alphabet]
        self.rects = []
        x = 100
        y = 300
        space_between = 20
        for surface in self.all_surfaces:
            rect = surface.get_rect()
            if (x + surface.get_width() + space_between) > 700:
                y += 100
                x = 100
            rect.x = x 
            rect.y = y
            x += surface.get_width() + space_between
            self.rects.append(rect)

    def draw(self,window):
        for i,surface in enumerate(self.all_surfaces):
            window.blit(surface,self.rects[i])
            mouse_pos = pygame.mouse.get_pos()
            if self.rects[i].collidepoint(mouse_pos):
                rect = self.rects[i]
                rect = pygame.Rect.inflate(rect,15,10)
                pygame.draw.rect(window,colors["blue"],rect,2)
    
    def track_inputs(self,event):
        if event.type == MOUSEBUTTONDOWN:
            for i,rect in enumerate(self.rects):
                if rect.collidepoint(event.pos):
                    #if chose wrong letter
                    try_letter = self.word.try_letter(self.alphabet[i])
                    if not try_letter:
                        global points 
                        points -= 1
                        self.alphabet.pop(i)
                        self.update_alpha()
    def update_alpha(self):
        self.all_surfaces = [
                self.font.render(x,True,colors["black"]) for x in self.alphabet]
        x = 100
        y = 300
        space_between = 20
        self.rects = [] 
        for surface in self.all_surfaces:
            rect = surface.get_rect()
            if (x + surface.get_width() + space_between) > 700:
                y += 100
                x = 100
            
            rect.x = x
            rect.y = y
            x += surface.get_width() + space_between
            self.rects.append(rect)
    
    def reset_alpha(self):
        self.alphabet = type(self).ALPHABET.copy()
        self.update_alpha()
    
word = DrawMainWord(100,words)
letters_buttons = Letters(word)
points = 0
font = pygame.font.SysFont("Arial",20,True,True)

while True:
    window.fill(colors["white"])
    word.draw(window)
    letters_buttons.draw(window)
    points_surface = font.render("POINTS: " + str(points),True,colors["black"])
    window.blit(points_surface,(20,20))
    for event in pygame.event.get():
        # track mouse
        letters_buttons.track_inputs(event)
        
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                word.update_word()
                letters_buttons.reset_alpha()
            #try key typed
            word.try_letter(pygame.key.name(event.key))

    pygame.display.update()    

pygame.quit()
