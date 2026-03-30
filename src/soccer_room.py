import pygame
import global_vars as gv
# import movie
import various_functions as f


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x_velocity = 0
        self.y_velocity = 0
        self.img = gv.soccer_ball_img
        self.rect = self.img.get_rect()
        self.rect.x, self.rect.y = 375, 50
        self.width = self.rect.width
        self.height = self.rect.height
        self.juggle_counter = 0

    def move(self, char_head):
        self.y_velocity += gv.GRAVITY
        self.y_velocity = min(self.y_velocity, 17)

        dx = self.x_velocity
        dy = self.y_velocity

        if char_head.rect.colliderect(self.rect.x + dx, self.rect.y + dy, self.width, self.height):
            self.x_velocity = (self.rect.midbottom[0] - char_head.rect.midtop[0])/10
            self.y_velocity = -17
            gv.header_sfx.play()
            self.juggle_counter += 1
            if self.juggle_counter >= 10:
                gv.success_sfx.play()
                gv.to_do["juggle soccer ball"] = True
                gv.world_level = "movie"
                gv.movie_idx = 1
                # pygame.mixer.music.fadeout(1000)
                # pygame.mixer.music.unload()
                # f.reset_music()

        # update rectangle position of khatchig
        self.rect.x += dx
        self.rect.y += dy

    def draw(self):
        gv.screen.blit(self.img, [self.rect.x, self.rect.y])


class SimpleChar(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 6  # in pixels/step when moving left or right
        self.direction = 1  # facing/moving right
        self.x_velocity = 0
        self.y_velocity = 0
        self.animation_list = []  # a list of action animation lists
        self.anim_index = 0
        self.action = 0  # Run
        self.last_time_check = pygame.time.get_ticks()  # for animation slow down

        animation_types = ["Run"]
        for animation in animation_types:
            temp_list = []
            i = 0
            end_flag = False
            while not end_flag:
                try:
                    # print(f"img/{self.char_type}/{animation}/{i}.png")
                    img = pygame.image.load(gv.resource_path(f"img/notkhatchig/{animation}/{i}.png")).convert_alpha()
                    img = pygame.transform.scale(img, (int(img.get_width() * 1.75), int(img.get_height() * 1.75)))
                    temp_list.append(img)
                    i += 1
                except FileNotFoundError:
                    end_flag = True
            self.animation_list.append(temp_list)

        # update the image variable based on the current action and frame in the animation
        self.image = self.animation_list[self.action][self.anim_index]
        self.rect = self.image.get_rect()
        self.rect.center = (375, 500)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def move(self, moving_left, moving_right):
        if moving_left:
            self.x_velocity = -self.speed
            self.direction = -1
        elif moving_right:
            self.x_velocity = self.speed
            self.direction = 1

        dx = self.x_velocity
        dy = self.y_velocity

        # update rectangle position of khatchig
        self.rect.x += dx
        self.rect.y += dy

    def draw(self):
        gv.screen.blit(pygame.transform.flip(self.image, (lambda x: False if x == 1 else True)(self.direction), False), self.rect)

    def update_animation(self):
        self.image = self.animation_list[self.action][self.anim_index]

        if pygame.time.get_ticks() - self.last_time_check > gv.ANIMATION_INTERVAL:
            self.last_time_check = pygame.time.get_ticks()
            self.anim_index += 1

        if self.anim_index >= len(self.animation_list[self.action]):
            self.anim_index = 0


class SoccerRoom():
    def __init__(self, character, ball):
        self.intro_complete = False
        self.notkhatchig = character
        self.soccer_ball = ball
        self.mov_left = False
        self.mov_right = False
        # self.last_time = 0

    def translate(self, direction):
        if direction == "right":
            self.mov_right, self.mov_left = True, False
        elif direction == "left":
            self.mov_right, self.mov_left = False, True

    # def run(self):
    #     """ self-contained loop in main game loop """
    #     bg_counter = 0
    #
    #     while gv.world_level == "soccer_room":
    #         for event in pygame.event.get():
    #             # should put in the key_up events or turn moving left and right to false
    #             if event.type == pygame.QUIT:
    #                 pygame.quit()
    #             elif event.type == pygame.KEYDOWN:
    #                 if event.key == pygame.locals.K_SPACE:
    #                     gv.world_level = "top"
    #                     pygame.mixer.music.fadeout(1000)
    #                     pygame.mixer.music.unload()
    #                     f.reset_music()
    #                 if event.key in key_to_function:
    #                     # dictionary returns a method (run on itself)
    #                     key_to_function[event.key](self)
    #
    #         bg_counter += 1
    #         bg_idx = int((bg_counter/20)) % 3
    #         gv.screen.blit(gv.campfire_bg[bg_idx], [0, 0])
    #
    #         self.notkhatchig.update_animation()
    #         self.notkhatchig.move(self.mov_left, self.mov_right)
    #         self.notkhatchig.draw()
    #
    #         self.soccer_ball.move(self.notkhatchig)
    #         self.soccer_ball.draw()
    #         gv.screen.blit(gv.pine1_img, (0, 500))
    #         gv.screen.blit(gv.letter_box_img, (0, 0))
    #
    #         if not self.intro_complete:
    #             if gv.intro_fade.fade():
    #                 self.intro_complete = True
    #
    #         # print("soccer room, time interval", time.time() - self.last_time)
    #         # self.last_time = time.time()
    #         pygame.display.update()
    #         gv.clock.tick(gv.FPS)


# key_to_function = {
#     pygame.K_LEFT:   (lambda x: x.translate('left')),
#     pygame.K_RIGHT:  (lambda x: x.translate('right'))}


def init_ball_char():
    soccer_ball = Ball()
    notkhatch = SimpleChar()

    # transition music
    # pygame.mixer.music.fadeout(1000)
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    pygame.mixer.music.load(gv.resource_path("audio/icaros.ogg"))
    pygame.mixer.music.set_volume(0.12)
    pygame.mixer.music.play(-1, 0.0, 1000)

    return SoccerRoom(notkhatch, soccer_ball)


# def create():
#     room = init_ball_char()
#
#     # transition music
#     pygame.mixer.music.fadeout(1000)
#     pygame.mixer.music.unload()
#     pygame.mixer.music.load(gv.resource_path("audio/icaros.wav"))
#     pygame.mixer.music.set_volume(0.12)
#     pygame.mixer.music.play(-1, 0.0, 1000)
#
#     # room.run()
