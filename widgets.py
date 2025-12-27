import pygame
from pygame.locals import*

class Label:
    def __init__(self,text,size,pos,font):
        self.pos = pos
        self.text = text
        self.color = (0,0,0)
        self.size = size
        self.font = font

    def show(self,win):
        txt = self.font.render(self.text,True,self.color)
        r = txt.get_rect(center = self.pos)
        win.blit(txt,r)
        return  txt.get_width()

    def show_pos(self,win):
        txt = self.font.render(self.text, True, self.color)
        win.blit(txt,self.pos)
        return txt.get_width()

class Frame:
    def __init__(self,pos,image):
        self.pos = pos
        self.image = pygame.image.load(image).convert_alpha()
        self.size = list(self.image.get_size())

    def show(self,win):
        img = pygame.transform.smoothscale(self.image,self.size)
        win.blit(img,self.pos)
    def show_center(self,win):
        pass