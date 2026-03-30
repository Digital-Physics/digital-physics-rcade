import pygame
import global_vars as gv


class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y, collidable=False, type=None, flip_image=None):
        pygame.sprite.Sprite.__init__(self)
        self.collidable = collidable
        self.image = img
        self.type = type
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + gv.TILE_SIZE // 2, y + (gv.TILE_SIZE - self.image.get_height()))
        self.flip_image = flip_image

    def update(self):
        if gv.level == 2:
            # print("decoration.py, update method, x,y pos", self.rect.x, self.rect.y)
            self.rect.y += int(gv.screen_scroll)
        else:
            self.rect.x += gv.screen_scroll
