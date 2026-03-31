import pygame
import global_vars as gv
import various_functions as f


class CatBusRoom:
    def __init__(self):
        self.intro_complete = False
        # gv.last_time_check_dialogue = pygame.time.get_ticks()
        self.last_time_check = pygame.time.get_ticks()
        self.last_time_check_book = pygame.time.get_ticks()
        self.book_counter = 0
        self.book_down = False
        self.success = False

    # def run(self):
    #     """ self-contained loop in main game loop """
    #     if gv.holding_object == 105:
    #         gv.success_sfx.play()
    #         self.success = True
    #
    #     img_flip = True
    #
    #     while gv.world_level == "cat_bus_room":
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 pygame.quit()
    #             elif event.type == pygame.KEYDOWN:
    #                 if event.key == pygame.locals.K_SPACE:
    #                     gv.world_level = "top"
    #                     gv.door_sfx.play()
    #
    #         if pygame.time.get_ticks() - self.last_time_check_book > gv.DIALOGUE_INTERVAL / 2:
    #             self.book_down = not self.book_down
    #             self.last_time_check_book = pygame.time.get_ticks()
    #
    #         if pygame.time.get_ticks() - self.last_time_check > gv.ANIMATION_INTERVAL:
    #             self.last_time_check = pygame.time.get_ticks()
    #             img_flip = not img_flip
    #
    #         if img_flip:
    #             gv.screen.blit(gv.cat_bus_img, (0, 0))
    #         else:
    #             gv.screen.blit(gv.cat_bus2_img, (0, 0))
    #
    #         if gv.to_do["deliver cat"]:
    #             if self.book_down:
    #                 gv.screen.blit(gv.large_cat_img, (60, 175))
    #             else:
    #                 gv.screen.blit(gv.large_cat_img, (60, 170))
    #         else:
    #             if self.success:
    #                 self.give_book()
    #             elif self.book_down:
    #                 gv.screen.blit(gv.book_hands_img, (80, 360))
    #             else:
    #                 gv.screen.blit(gv.book_hands_img, (80, 340))
    #
    #             # if self.book_counter < 3500:
    #             if gv.dialogue_counter < len(gv.dialogue["hippie_book_success"]):
    #                 self.dialogue()
    #
    #         if not self.intro_complete:
    #             if gv.intro_fade.fade():
    #                 self.intro_complete = True
    #
    #         pygame.display.update()

    def dialogue(self):
        if self.success:
            temp_dialogue = gv.dialogue["hippie_book_success"][gv.dialogue_counter % len(gv.dialogue["hippie_book_success"])][:]
        else:
            temp_dialogue = gv.dialogue["hippie_book"][gv.dialogue_counter % len(gv.dialogue["hippie_book"])][:]

        f.draw_dialogue(temp_dialogue, 280, 250)

        if pygame.time.get_ticks() - gv.last_time_check_dialogue > gv.DIALOGUE_INTERVAL:
            gv.last_time_check_dialogue = pygame.time.get_ticks()
            gv.dialogue_counter_flag = True
            gv.dialogue_counter += 1  # update outside main game loop needed because we are in self-contained loop
            gv.speech_sfx.play()

    def give_book(self):
        """ sort of like a generator or iterator that returns one thing each time...
        draws one background, then another, and then changes state if enough time has passed..."""
        if gv.dialogue_counter < len(gv.dialogue["hippie_book_success"]):
            gv.screen.blit(gv.book_hands_img, (80, 380))
        elif self.book_counter < 350:
            pygame.draw.rect(gv.screen, gv.BLACK, pygame.Rect(0, 0, 750, 750))
            gv.screen.blit(gv.book_img, (260, 320))
            self.book_counter += 1
        else:
            pygame.draw.rect(gv.screen, gv.BLACK, pygame.Rect(0, 0, 750, 750))
            gv.screen.blit(gv.book_img, (260, 320))
            gv.holding_object = 99
            gv.moving_right = False
            gv.moving_left = False
            gv.to_do["deliver cat"] = True
            gv.world_level = "movie"
            gv.movie_idx = 0
            gv.success_sfx.play()


# def create():
#     room = CatBusRoom()
#     room.run()
