import pygame
import global_vars as gv
import decoration as d
import random


class Cat(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed  # in pixels/step when moving left or right
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
                    img = pygame.image.load(gv.resource_path(f"img/cat/{animation}/{i}.png")).convert_alpha()
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
        self.x_velocity = self.direction*self.speed*random.uniform(0, 3)

        # apply gravity
        self.y_velocity += gv.GRAVITY
        self.y_velocity = min(self.y_velocity, 17)

        dx = self.x_velocity
        dy = self.y_velocity

        for tile in gv.decoration_group:
            if tile.collidable:
                if tile.type == "hot_dog":
                    if tile.rect.colliderect(self.rect.x + dx, self.rect.y + dy, self.width, self.height):
                        img = gv.img_list[131]
                        img_rect = img.get_rect()
                        img_rect.right = self.rect.right
                        img_rect.bottom = self.rect.bottom
                        decoration = d.Decoration(img, img_rect.x, img_rect.y, collidable=True, type="cat", flip_image=gv.img_list[130])
                        gv.decoration_group.add(decoration)
                        gv.cat = None

        # check for collisions in the x and y direction before moving
        # for tile_data in gv.world_instance.obstacle_list:
        for tile_data in gv.obstacle_list:
            # check x direction collision before it occurs w/ dx move (3x to prevent tunneling when moving w/ khatchig?)
            if tile_data[1].colliderect(self.rect.x + dx*3, self.rect.y, self.width, self.height):
                dx = 0  # isn't the minimal dx distance
                self.direction *= -1
            if tile_data[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.y_velocity >= 0:
                    # prevent feet going through object
                    self.y_velocity = 0
                    # self.in_air = False
                    # self.update_action(0)
                    dy = tile_data[1].top - self.rect.bottom

        if self.rect.colliderect(gv.khatchig.rect) and gv.khatchig.vulnerable:
            gv.cat_hiss_sfx.play()
            gv.khatchig.health -= 1
            gv.khatchig.vulnerable = False
            # gv.cat_sfx.play()
            gv.hit_sfx.play()

        # now that the dx and dy have been calculated and potentially 0'd for collisions
        self.rect.x += dx
        self.rect.y += dy

        # scroll based on khatchig's movement
        self.rect.x += gv.screen_scroll

    # def auto(self):
    def update_animation(self):
        self.image = self.animation_list[self.action][self.anim_index]

        if pygame.time.get_ticks() - self.last_time_check > gv.ANIMATION_INTERVAL:
            self.last_time_check = pygame.time.get_ticks()
            self.anim_index = (self.anim_index + 1) % len(self.animation_list[self.action])

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.anim_index = 0
            self.last_time_check = pygame.time.get_ticks()

    # this was put in to handle multiple updates at once; it also overwrites update() method in Sprite
    def update(self):
        self.move()
        self.update_animation()

    def draw(self):
        gv.screen.blit(pygame.transform.flip(self.image, (lambda x: False if x == 1 else True)(self.direction), False), self.rect)