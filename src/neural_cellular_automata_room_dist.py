import pygame
import global_vars as gv
import various_functions as f
# import random


class NcaRoomDist:
    def __init__(self):
        self.control = pygame.Rect(3, 3, 10, 10)
        self.intro_complete = False
        gv.last_time_check_dialogue = pygame.time.get_ticks()  # so we get the first "..." in the dialogue
        self.last_time_check = pygame.time.get_ticks()
        self.counter = 0
        self.temp_message = False
        self.key_to_function = {
            pygame.K_LEFT: (lambda x: x.translate('left')),
            pygame.K_RIGHT: (lambda x: x.translate('right')),
            pygame.K_UP: (lambda x: x.translate('up')),
            pygame.K_DOWN: (lambda x: x.translate('down')),
            pygame.K_SLASH: (lambda x: x.translate('clear')),
            pygame.K_PERIOD: (lambda x: x.translate("add"))}

    def translate(self, direction):
        if direction == "right":
            self.control.x = (self.control.x+1)%29  # 59
        elif direction == "left":
            self.control.x = (self.control.x-1)%29  # 59
        elif direction == "up":
            self.control.y = (self.control.y-1)%29  # 59
        elif direction == "down":
            self.control.y = (self.control.y+1)%29  # 59

    def temp_dialogue(self):
        if self.temp_message:
            temp_dialogue = gv.dialogue["notkhatchig_temp"][gv.dialogue_counter % len(gv.dialogue["notkhatchig_temp"])][:]
        else:
            temp_dialogue = gv.dialogue["notkhatchig"][gv.dialogue_counter % len(gv.dialogue["notkhatchig"])][:]

        f.draw_dialogue(temp_dialogue, 180, 250)
        if pygame.time.get_ticks() - gv.last_time_check_dialogue > gv.DIALOGUE_INTERVAL:
            gv.dialogue_counter_flag = True
            gv.dialogue_counter += 1  # update outside main game loop needed because we are in self-contained loop
            gv.speech_sfx.play()
            gv.last_time_check_dialogue = pygame.time.get_ticks()

#     def run(self):
#         """ self-contained loop in main game loop """
#         img_flip = True
#         img_num = 0
#
#         while gv.world_level == "neural_cellular_automata_room_dist":
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     pygame.quit()
#                 elif event.type == pygame.KEYDOWN:
#                     if event.key == pygame.locals.K_SPACE:
#                         gv.world_level = "top"
#                         gv.door_sfx.play()
#                     if event.key in self.key_to_function:
#                         self.temp_message = True
#                         gv.dialogue_counter = 0
#                         self.key_to_function[event.key](self)
#
#             if pygame.time.get_ticks() - self.last_time_check > gv.ANIMATION_INTERVAL/2:
#                 self.last_time_check = pygame.time.get_ticks()
#                 img_flip = not img_flip
#                 self.counter += 1
#
#                 if self.counter > 149:
#                     img_num = random.choice(range(140, 150))
#                 else:
#                     img_num = self.counter
#
#             if self.temp_message and gv.dialogue_counter >= len(gv.dialogue["notkhatchig_temp"]):
#                 self.temp_message = False
#                 gv.dialogue_counter = 0
#
#             if img_flip:
#                 gv.screen.blit(gv.escher3_img, (0, 0))
#             else:
#                 gv.screen.blit(gv.escher4_img, (0, 0))
#
#             gv.screen.blit(gv.nca_movie[img_num], (116, 310))
#
#             pygame.draw.rect(surface=gv.screen, color=(125, 55, 200),
#                              rect=pygame.Rect(self.control.x*5+116, self.control.y*5+310, 25, 25), width=1)
#
#             self.temp_dialogue()
#
#             pygame.display.update()
#
#
# def create():
#     room = NcaRoomDist()
#     room.run()
