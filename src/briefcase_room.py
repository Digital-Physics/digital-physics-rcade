import pygame
import global_vars as gv


class BriefcaseRoom:
    def __init__(self):
        self.solution = [1, 0, 1, 0, 1, 0]
        self.control = 0
        self.digits = [1, 2, 3, 4, 5, 6]
        self.open_try = False
        self.game_loop_counter = 0
        self.intro_complete = False
        self.last_time_check = pygame.time.get_ticks()
        self.dialogue_change_state = 0
        self.first_sfx = True
        self.key_to_function = {
            pygame.K_LEFT: (lambda x: x.switch('left')),
            pygame.K_RIGHT: (lambda x: x.switch('right')),
            pygame.K_UP: (lambda x: x.increment()),
            pygame.K_DOWN: (lambda x: x.open())}

    def switch(self, direction):
        gv.switch_sfx.play()
        if direction == "right":
            self.control = (self.control + 1) % 6
        elif direction == "left":
            self.control = (self.control - 1) % 6

    def increment(self):
        self.digits[self.control] = (self.digits[self.control] + 1) % 10
        gv.briefcase_change_sfx.play()

    def digits_text(self):
        digit_font = pygame.font.Font(gv.resource_path("fonts/kongtext.ttf"), 6)
        big_digit_font = pygame.font.Font(gv.resource_path("fonts/kongtext.ttf"), 18)

        for i, digit in enumerate(self.digits):
            digit_text = digit_font.render(str(digit), True, gv.WHITE)
            big_digit_text = big_digit_font.render(str(digit), True, gv.WHITE)
            edge_text = big_digit_font.render(str(digit), True, gv.BLACK)

            if i <= 2:
                gv.screen.blit(digit_text, (98 + i * 14, 400))
            else:
                gv.screen.blit(digit_text, (219 + i * 14, 400))

            if i == self.control:
                gv.screen.blit(edge_text, (140 + i * 20, 452))

            gv.screen.blit(big_digit_text, (138 + i * 20, 450))

    def open(self):
        self.open_try = True
        self.first_sfx = True
        self.game_loop_counter = 0

    # def run(self):
    #     """ self-contained loop in main game loop """
    #
    #     img_flip = True
    #
    #     while gv.world_level == "briefcase_room":
    #         for event in pygame.event.get():
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
    #         if self.game_loop_counter == 200:
    #             self.open_try = False
    #         elif pygame.time.get_ticks() - self.last_time_check > gv.DIALOGUE_INTERVAL/2:
    #             self.game_loop_counter += 1
    #
    #         if img_flip:
    #             if self.open_try:
    #                 if self.digits == self.solution:
    #                     if self.first_sfx:
    #                         if gv.holding_object is not None:
    #                             if gv.holding_object == 186:
    #                                 gv.in_briefcase["printout"] = True
    #                             elif gv.holding_object == 123:
    #                                 gv.in_briefcase["shirt"] = True
    #                             elif gv.holding_object == 99:
    #                                 gv.in_briefcase["book"] = True
    #
    #                         gv.briefcase_open_sfx.play()
    #                         gv.success_sfx.play()
    #                         gv.to_do["get briefcase"] = True
    #                         gv.holding_object = 98
    #                         self.first_sfx = False
    #                     gv.screen.blit(gv.escher13_img, (0, 0))
    #                 else:
    #                     gv.briefcase_wrong_sfx.play()
    #                     gv.screen.blit(gv.escher11_img, (0, 0))
    #             else:
    #                 gv.screen.blit(gv.escher9_img, (0, 0))
    #             img_flip = False
    #         else:
    #             if self.open_try:
    #                 if self.digits == self.solution:
    #                     if self.first_sfx:
    #                         gv.briefcase_open_sfx.play()
    #                         gv.success_sfx.play()
    #                         gv.to_do["get briefcase"] = True
    #                         gv.holding_object = 98
    #                         self.first_sfx = False
    #                     gv.screen.blit(gv.escher14_img, (0, 0))
    #                 else:
    #                     gv.screen.blit(gv.escher12_img, (0, 0))
    #             else:
    #                 gv.screen.blit(gv.escher10_img, (0, 0))
    #             img_flip = True
    #
    #         self.digits_text()
    #
    #         if not self.intro_complete:
    #             if gv.intro_fade.fade():
    #                 self.intro_complete = True
    #         pygame.display.update()


# def create():
#     room = BriefcaseRoom()
#     room.run()
