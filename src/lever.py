import pygame
import global_vars as gv

class Lever(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + gv.TILE_SIZE // 2, y + (gv.TILE_SIZE - self.image.get_height()))

    def update(self):
        # scroll
        if gv.level == 2:
            self.rect.y += int(gv.screen_scroll)
        else:
            self.rect.x += gv.screen_scroll