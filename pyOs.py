#-*-coding:Utf-8-*-

import time
import pygame
from   pygame.locals import *


class DesktopManager:
    def __init__(self, screen):
        self.screen = screen
        self.windows = []
        self.not_alives = []
        self.tskb_size = (100, self.screen.get_size()[1])
        self.cl_tskb = (45, 167, 37)
        self.main_txt_tsk_bar = font.render("Phoenix!OS", 1, RED)
    
    def _get_active(self, item: int=-1, fen=None) -> bool:
        if item != -1:
            return self.windows[item].visible()
        return fen.visible()
    
    def _get_alive(self, item: int=-1, fen=None) -> bool:
        if item != -1:
            return self.windows[item].alive()
        return fen.alive()
    
    def add_windows(self, *news):
        for new in news:
            self.windows.append(new)
    
    def draw(self):
        poping_to_na = []
        poping = []
        
        pygame.draw.rect(self.screen, (0, 0, 0), (0, 0) + self.screen.get_size())
        
        for tmp in range(len(self.windows)):
            index = len(self.windows) - 1 - tmp
            if not self._get_active(index):
                poping_to_na.append(index)
            if not self._get_alive(index):
                poping.append(index)
            self.windows[index].draw()
        self.draw_task_bar()
        self.main_button_tsk_bar()
        self.print_fps()
        self.print_time()
        
        if poping != None:
            for i in poping[::-1]:
                self.windows.pop(i)
        if poping_to_na != None:
            for i in poping_to_na[::-1]:
                self.not_alives.append(self.windows.pop(i))
    
    def draw_task_bar(self):
        pygame.draw.rect(self.screen, self.cl_tskb, (0, 0) + self.tskb_size)
        y = 40
        for i in self.windows + self.not_alives:
            dispo = (self.tskb_size[0] - 8) // 6
            txt = font_petite.render(i.get_title()[:dispo], 1, WHITE if i in self.windows else GREY)
            self.screen.blit(txt, (4, y))
            y += txt.get_size()[1] + 4
    
    def main_button_tsk_bar(self):
        pygame.draw.rect(self.screen, YELLOW, (0, 0, self.tskb_size[0], 30))
        self.screen.blit(self.main_txt_tsk_bar,
                ((self.tskb_size[0] - self.main_txt_tsk_bar.get_size()[0]) // 2,
                  self.main_txt_tsk_bar.get_size()[1] // 2))
    
    def print_fps(self):
        pass
    
    def select_prog(self, y: int=0):
        real_select = (y - 40) // 14
        print(y, real_select)
        if 0 <= real_select <= len(self.windows) + len(self.not_alives) - 2:
            if real_select < len(self.windows):
                print(self.windows[real_select].get_title())
            elif real_select - len(self.windows) - 1 < len(self.not_alives):
                print(self.not_alives[real_select - len(self.windows) - 1].get_tile())
    
    def print_time(self):
        t = time.strftime("%A")
        self.screen.blit(font_petite.render(t, 1, WHITE), (4, self.screen.get_size()[1] - 42))
        t = time.strftime("%H : %M : %S")
        self.screen.blit(font_petite.render(t, 1, WHITE), (4, self.screen.get_size()[1] - 14))
        t = time.strftime("%d %B")
        self.screen.blit(font_petite.render(t, 1, WHITE), (4, self.screen.get_size()[1] - 28))
    
    def trigger(self, event: pygame.event):
        if event.type == MOUSEBUTTONDOWN and event.pos[0] > self.tskb_size[0] or event.type == KEYDOWN:
            if len(self.windows) >= 1:
                self.windows[0].trigger(event)
        elif event.type == MOUSEBUTTONDOWN and event.pos[0] <= self.tskb_size[0]:
            self.select_prog(event.pos[1])


class Fenetre:
    def __init__(self, screen: pygame.Surface, titre: str="", version: float=1.0, pos: tuple=(0, 0), size: tuple=(0, 0),
                       couleur: tuple=(20, 20, 20), cote_c: int=12):
        self.screen = screen
        self.wscreen, self.hscreen = self.screen.get_size()
        self.titre = titre
        self.version = version
        self.fen_name = "[" + self.titre + "]" + " " + str(self.version)
        self.pos = pos
        self.size = size
        self.couleur = couleur
        self.cote_c = cote_c
        self.active = True
        self.living = True
        self.escape_btn = (self.pos[0] + self.size[0] - (24 - self.cote_c) // 2 - self.cote_c, self.pos[1] + ((24 - self.cote_c) // 2), self.cote_c, self.cote_c)
    
    def draw(self):
        if self.living:
            pygame.draw.rect(self.screen, self.couleur, self.pos + self.size)
            pygame.draw.rect(self.screen, (150, 150, 150), self.pos + (self.size[0], 24))
            self.screen.blit(font.render(self.fen_name, 1, (10, 10, 10)), (self.pos[0] + 2, self.pos[1] + 2))
            pygame.draw.rect(self.screen, RED, self.escape_btn)
     
    def alive(self) -> bool:
        return self.living
     
    def visible(self) -> bool:
        return self.active
    
    def get_title(self) -> str:
        return self.fen_name

    def trigger(self, event: pygame.event):
        if event.type == MOUSEBUTTONDOWN:
            x, y = event.pos
            if self.escape_btn[0] <= x <= self.escape_btn[0] + self.escape_btn[2] \
                    and self.escape_btn[1] <= y <= self.escape_btn[1] + self.escape_btn[3]:
                pygame.draw.rect(self.screen, (0, 0, 0), (0, 0) + self.screen.get_size())
                self.living = False

RED = (180, 20, 20)
GREEN = (20, 180, 20)
BLUE = (20, 20, 180)
YELLOW = (20, 180, 180)
PURPLE = (180, 20, 180)
WHITE = (255, 255, 255)
GREY = (140, 140, 140)

pygame.init()
win = pygame.display.set_mode((0, 0), FULLSCREEN)
font = pygame.font.Font("freesansbold.ttf", 16)
font_petite = pygame.font.Font("freesansbold.ttf", 11)

win_manager = DesktopManager(win)
test = Fenetre(win, "Test", 1.0, size=(540, 480), pos=(120, 120))
other = Fenetre(win, "Une autre fenêtre", size=(200, 300), pos=(200, 160), couleur=(75, 40, 125))
win_manager.add_windows(test, other)

continuer = 1

while continuer:
    for event in pygame.event.get():
        if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == QUIT:
            continuer = 0
        else:
            win_manager.trigger(event)
    win_manager.draw()
    #actualisation de l'écran :
    pygame.display.flip()