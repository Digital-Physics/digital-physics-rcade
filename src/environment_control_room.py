import pygame
import global_vars as gv
import random


class ControlEnvRoom:
    def __init__(self):
        self.intro_complete = False
        self.last_time_check = pygame.time.get_ticks()
        self.pos_wallpaper = [random.choice([5*i for i in range(150)]), random.choice([5*i for i in range(150)])]
        self.first_sfx = True
        self.last_move_time = pygame.time.get_ticks()  # rate-limit d-pad movement

    def translate(self, direction, dist):
        if direction == "x":
            self.pos_wallpaper[0] = (self.pos_wallpaper[0]+dist)%gv.SCREEN_WIDTH
        else:
            self.pos_wallpaper[1] = (self.pos_wallpaper[1]+dist)%gv.SCREEN_WIDTH