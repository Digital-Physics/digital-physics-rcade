import pygame
import global_vars as gv
import random


class Ufo(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.x_direction = 1
        self.y_direction = 1
        self.speed = speed  # in pixels when moving left or right
        self.animation_list = []  # a list of action animation lists
        self.anim_index = 0
        self.action = 0  # idle
        self.last_time_check = pygame.time.get_ticks()  # for animation slow down
        # NPC-specific variables (enemies or other characters in the game)
        # should probably just use an itertools cycle instead of creating the one below
        self.beam_alpha_loop_list = list(range(128))
        self.beam_alpha_loop_list.reverse()
        self.beam_alpha_loop_list = list(range(128)) + self.beam_alpha_loop_list
        self.beam_alpha_idx = 0

        animation_types = ["Move", "Disappear"]

        for animation in animation_types:
            temp_list = []
            i = 0
            end_flag = False
            while not end_flag:
                try:
                    img = pygame.image.load(gv.resource_path(f"img/ufo/{animation}/{i}.png")).convert_alpha()
                    img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                    temp_list.append(img)
                    i += 1
                except FileNotFoundError:
                    end_flag = True
            self.animation_list.append(temp_list)

        # get the rectangle that holds the image and center it on x, y
        self.image = self.animation_list[self.action][self.anim_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def move(self):
        dx = -0.2 * (self.rect.x - gv.khatchig.rect.x) + random.uniform(-5, 5)
        dy = self.y_direction * self.speed * random.uniform(0, 1) * 0.8

        if self.rect.colliderect(gv.khatchig.rect) and gv.khatchig.vulnerable:
            gv.khatchig.health -= 1
            gv.hit_sfx.play()
            gv.khatchig.vulnerable = False
            gv.floating = False
            # movie.play(2)  # self-contained loop
            gv.world_level = "movie"
            gv.movie_idx = 2

        if gv.ufo_present:
            self.rect.x += dx
            self.rect.y += dy

    # this method is only used for NPCs
    def auto(self):
        if gv.ufo_present and gv.bg_scroll > 6500:
            gv.ufo_sfx.stop()
            self.update_action(1)  # disappear
            if self.anim_index == len(self.animation_list[1]) - 1:
                gv.ufo_present = False
            gv.floating = False
        elif gv.ufo_present:
            self.move()
            self.update_action(0)
        elif 5400 <= gv.bg_scroll <= 6500:
            gv.ufo_present = True
            gv.ufo_sfx.play()

    def update_animation(self):
        self.image = self.animation_list[self.action][self.anim_index]

        if pygame.time.get_ticks() - self.last_time_check > gv.ANIMATION_INTERVAL:
            self.last_time_check = pygame.time.get_ticks()
            self.anim_index += 1
        if self.anim_index >= len(self.animation_list[self.action]):
            if self.action == 0:  # moving
                self.anim_index = 0
            else:
                self.anim_index = len(self.animation_list[self.action]) - 1

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.anim_index = 0
            self.last_time_check = pygame.time.get_ticks()

    def update(self):
        """this method handles multiple updates at once.
        It also overwrites update() method in Sprite"""
        self.auto()
        self.update_animation()

    def draw(self):
        if gv.ufo_present:
            gv.screen.blit(self.image, self.rect)
            gv.beam_img.set_alpha(self.beam_alpha_loop_list[self.beam_alpha_idx])
            gv.screen.blit(gv.beam_img, (self.rect.x, self.rect.bottom - 15))
            self.beam_alpha_idx = (self.beam_alpha_idx + 1) % 256
