import pygame
import global_vars as gv

# controllable ascii art
# this init was done for loading images and converting alpha
# we don't want to load everything up front, so long as there is no delay in the game play.
pygame.init()


class Ascii_room():
    def __init__(self):
        self.intro_complete = False
        self.control = 0
        self.img_list = []
        self.stars_counter = 0
        self.first_sfx = True

        for i in range(10):
            img = pygame.image.load(gv.resource_path(f'img/ascii_art/{i}.png'))
            img = pygame.transform.scale(img, (112, 272))
            self.img_list.append(img)

        self.last_move_time = pygame.time.get_ticks()  # rate-limit d-pad movement

    def translate(self, direction):
        if direction == "right":
            self.control = (self.control+1) % 10
            self.stars_counter -= 10
        elif direction == "left":
            self.control = (self.control-1) % 10
            self.stars_counter += 10

    # def run(self):
    #     """ self-contained loop in main game loop """
    #
    #     img_flip = True
    #
    #     while gv.world_level == "ascii_room":
    #         for event in pygame.event.get():
    #             # should put in the key_up events or turn moving left and right to false
    #             if event.type == pygame.QUIT:
    #                 pygame.quit()
    #             elif event.type == pygame.KEYDOWN:
    #                 if event.key == pygame.locals.K_SPACE:
    #                     gv.world_level = "top"
    #                     gv.door_sfx.play()
    #                 if event.key in self.key_to_function:
    #                     # dictionary returns a method (run on itself)
    #                     self.key_to_function[event.key](self)
    #
    #         gv.screen.blit(gv.track_img, [(self.stars_counter % gv.track_img.get_width()) - gv.track_img.get_width(), 155])
    #         gv.screen.blit(gv.track_img, [self.stars_counter % gv.track_img.get_width(), 155])
    #
    #         if img_flip:
    #             gv.screen.blit(gv.escher19_img, (0, 0))
    #             img_flip = False
    #         else:
    #             gv.screen.blit(gv.escher20_img, (0, 0))
    #             img_flip = True
    #
    #         # pygame.draw.rect(gv.screen, (255, 255, 255), pygame.Rect(70, 201, 255, 306))
    #         if abs(self.stars_counter) > 300 and self.first_sfx:
    #             self.first_sfx = False
    #             gv.success_sfx.play()
    #             gv.to_do["run ascii"] = True
    #
    #         gv.screen.blit(self.img_list[self.control], (136, 198))
    #         gv.screen.blit(gv.letter_box_img, (0, 0))
    #
    #         if not self.intro_complete:
    #             if gv.intro_fade.fade():
    #                 self.intro_complete = True
    #         pygame.display.update()


# def create():
#     room = Ascii_room()
#     room.run()