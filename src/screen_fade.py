import pygame
import global_vars as gv


class ScreenFade():
    def __init__(self, direction, color, speed):
        self.direction = direction
        self.color = color
        self.speed = speed
        self.fade_counter = 0

    def fade(self):
        fade_complete = False
        self.fade_counter += self.speed
        # print("fade complete", fade_complete)
        # print("fade count", self.fade_counter)

        if self.direction == 1:  # whole/hole screen fade
            pygame.draw.rect(gv.screen, self.color, (0 - self.fade_counter, 0, gv.SCREEN_WIDTH // 2, gv.SCREEN_HEIGHT))
            pygame.draw.rect(gv.screen, self.color, (gv.SCREEN_WIDTH // 2 + self.fade_counter, 0, gv.SCREEN_WIDTH // 2, gv.SCREEN_HEIGHT))
            pygame.draw.rect(gv.screen, self.color, (0, 0 - self.fade_counter, gv.SCREEN_WIDTH, gv.SCREEN_HEIGHT // 2))
            pygame.draw.rect(gv.screen, self.color, (0, gv.SCREEN_HEIGHT // 2 + self.fade_counter, gv.SCREEN_WIDTH, gv.SCREEN_HEIGHT // 2))
        if self.direction == 2:  # vertical fade
            pygame.draw.rect(gv.screen, self.color, (0, 0, gv.SCREEN_WIDTH, 0 + self.fade_counter))

        if self.fade_counter >= gv.SCREEN_HEIGHT:
            # fade_complete = True
            # we use the same instance, so reset counter for next time if it is the whole-screen fade
            if self.direction == 1:
                self.fade_counter = 0
            return True
        return fade_complete


# # create instances for two kinds of transitions
# # maybe we should add these to the global variable file to be consistent? will it help with circular import avoidance?
# intro_fade = ScreenFade(1, gv.BLACK, 4)
# death_fade = ScreenFade(2, gv.BLACK, 6)