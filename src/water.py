import pygame
import global_vars as gv


class Water(pygame.sprite.Sprite):
    def __init__(self, img, x, y, flip_image):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + gv.TILE_SIZE // 2, y + (gv.TILE_SIZE - self.image.get_height()))
        self.flip_image = flip_image

    def update(self):
        # swap images
        if pygame.time.get_ticks() - gv.last_time_check > gv.ANIMATION_INTERVAL * 5:
            temp_img = self.image
            self.image = self.flip_image
            self.flip_image = temp_img
            # gv.last_time_check is a shared global variable (sloppy) updated by the obstacles check so it is not updated here

        # scroll
        if gv.level == 2:
            self.rect.y += gv.screen_scroll
        else:
            self.rect.x += gv.screen_scroll