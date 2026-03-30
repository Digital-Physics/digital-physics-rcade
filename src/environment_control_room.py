import pygame
import global_vars as gv
import random


class ControlEnvRoom:
    def __init__(self):
        self.intro_complete = False
        self.last_time_check = pygame.time.get_ticks()
        self.pos_wallpaper = [random.choice([5*i for i in range(150)]), random.choice([5*i for i in range(150)])]
        self.first_sfx = True

    def translate(self, direction, dist):
        if direction == "x":
            self.pos_wallpaper[0] = (self.pos_wallpaper[0]+dist)%gv.SCREEN_WIDTH
        else:
            self.pos_wallpaper[1] = (self.pos_wallpaper[1]+dist)%gv.SCREEN_WIDTH

    # def run(self):
    #     """ self-contained loop in main game loop """
    #     # if intro_fade.fade():
    #     img_flip = True
    #
    #     wallpaper_temp = pygame.Surface((750, 750), pygame.SRCALPHA)
    #
    #     for i in range(15):
    #         for j in range(15):
    #             if j % 4 <= 2:
    #                 wallpaper_temp.blit(gv.img_list[random.choice([30, 190])], (i * gv.TILE_SIZE, j * gv.TILE_SIZE))
    #             else:
    #                 wallpaper_temp.blit(gv.img_list[random.choice([29, 191])], (i * gv.TILE_SIZE, j * gv.TILE_SIZE))
    #
    #     wallpaper = wallpaper_temp.subsurface(0, 0, 750, 750)  # .copy()
    #     wallpaper_on_screen_temp = wallpaper.subsurface(0, 0, 750, int(750 * (9/15)))
    #     wallpaper_on_screen = pygame.transform.scale(wallpaper_on_screen_temp, (255, 170))
    #
    #     # while running:
    #     while gv.world_level == "environment_control_room":
    #         for event in pygame.event.get():
    #             # should put in the key_up events or turn moving left and right to false
    #             if event.type == pygame.QUIT:
    #                 pygame.quit()
    #             elif event.type == pygame.KEYDOWN:
    #                 if event.key == pygame.locals.K_SPACE:
    #                     gv.world_level = "top"
    #                     gv.door_sfx.play()
    #                 if event.key in key_to_function:
    #                     # dictionary returns a method (run on itself) which updates it's own 3d wireframe display
    #                     key_to_function[event.key](self)
    #
    #         # 145 is the height of the y coordinate of the bottom edge of the letter box, which is like the top row of the image
    #         if self.pos_wallpaper == [0, 145] and self.first_sfx:
    #             self.first_sfx = False
    #             gv.success_sfx.play()
    #             gv.to_do["match wallpaper"] = True
    #
    #         # four offset images for tiling effect
    #         gv.screen.blit(wallpaper, self.pos_wallpaper)
    #         gv.screen.blit(wallpaper, [self.pos_wallpaper[0] - gv.SCREEN_WIDTH, self.pos_wallpaper[1]])
    #         gv.screen.blit(wallpaper, [self.pos_wallpaper[0], self.pos_wallpaper[1] - gv.SCREEN_HEIGHT])
    #         gv.screen.blit(wallpaper, [self.pos_wallpaper[0] - gv.SCREEN_WIDTH, self.pos_wallpaper[1] - gv.SCREEN_HEIGHT])
    #
    #         if pygame.time.get_ticks() - self.last_time_check > gv.ANIMATION_INTERVAL:
    #             self.last_time_check = pygame.time.get_ticks()
    #             img_flip = not img_flip
    #
    #         if img_flip:
    #             gv.screen.blit(gv.escher17_img, (0, 0))
    #         else:
    #             gv.screen.blit(gv.escher18_img, (0, 0))
    #
    #         gv.screen.blit(wallpaper_on_screen, (70, 303))
    #
    #         if not self.intro_complete:
    #             if gv.intro_fade.fade():
    #                 self.intro_complete = True
    #         pygame.display.update()


key_to_function = {
    pygame.K_LEFT:   (lambda x: x.translate('x', -5)),
    pygame.K_RIGHT:  (lambda x: x.translate('x',  5)),
    pygame.K_DOWN:   (lambda x: x.translate('y',  5)),
    pygame.K_UP:     (lambda x: x.translate('y', -5))}

# initialize
control_room = ControlEnvRoom()


# def create(room=control_room):
#     room.run()