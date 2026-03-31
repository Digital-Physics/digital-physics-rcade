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
        self.last_move_time = pygame.time.get_ticks()  # rate-limit d-pad movement

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