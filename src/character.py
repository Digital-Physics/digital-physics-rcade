import pygame
import global_vars as gv
import random
import decoration as d
import various_functions as f


class Character(pygame.sprite.Sprite):
    """this class covers the player (Khatchig) and some NPC/enemies.
    In the future, we should separate classes for player/Khatchig and NPC
    Each should have their own .py file in our opinion
    We can inherit some methods between the classes"""
    def __init__(self, char_type, x, y, scale, speed, world_instance):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed * 2  # pixels/step when moving left or right
        self.direction = 1  # 1 = facing/moving right
        self.health = gv.MAX_HEALTH - 1
        self.x_velocity = 0
        self.y_velocity = 0
        self.jump = False
        self.pick = False
        self.in_air = True
        self.animation_list = []  # a list of action animation lists
        self.anim_index = 0
        self.anim_cycled = False
        self.action = 0  # idle
        self.last_time_check = pygame.time.get_ticks()  # for animation slow down
        gv.last_time_check_dialogue = pygame.time.get_ticks()
        self.last_time_check_flip = pygame.time.get_ticks()
        self.vulnerable = True
        self.vulnerable_counter = 0
        self.world_instance = world_instance
        self.notkhatchig_enters_room = False
        self.phone_flag = False
        self.phone_pos = None
        self.last_moving_right = False
        self.last_moving_left = False
        self.first_sfx = True
        # NPC-specific variables (enemies or other characters in the game)
        self.move_counter = 0
        self.health_counter = 0
        self.idling = False
        self.idling_counter = 0  # for random idling interval
        self.animation_types = ["Idle", "Run", "Jump", "Death", "Pick", "Port",
                                "NK_idle", "NK_run", "NK_jump", "NK_death", "NK_pick"]

        for animation in self.animation_types:
            temp_list = []
            i = 0
            end_flag = False
            while not end_flag:
                try:
                    img = pygame.image.load(gv.resource_path(f"img/{self.char_type}/{animation}/{i}.png")).convert_alpha()
                    img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                    temp_list.append(img)
                    i += 1
                except FileNotFoundError:
                    end_flag = True
            self.animation_list.append(temp_list)

        # update the image variable based on the current action and frame in the animation
        self.image = self.animation_list[self.action][self.anim_index]
        # get the rectangle that holds the image and center it
        # future: if we want to make it so that when he is ducking he is smaller we will...
        # have to make different png heights for "pick" action and adjust the code below
        # perhaps define the rect from the bottom left corner instead of the center...
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def move(self, moving_left, moving_right):
        # reset delta variables associated with each step
        # dx and dy do not need to be reset to 0 because they are defined below
        if self.char_type == "khatchig":
            gv.screen_scroll = 0

        hit_head_flag = False
        door_flag = False
        gv.mirror = None
        gv.mirror_loc = None

        if moving_left:
            # make slightly cartoonish spinning legs for Khatchig changing directions
            # acceleration happens every other step; it takes time to change velocity/direction
            if self.char_type == "khatchig":
                if gv.apply_force:
                    self.x_velocity -= 1 * 4  # leg muscle and frictional force
                    self.x_velocity = max(self.x_velocity, -self.speed)
                    gv.apply_force = False
                else:
                    gv.apply_force = True
            else:  # NPC
                self.x_velocity = -self.speed
            self.direction = -1
        elif moving_right:
            if self.char_type == "khatchig":
                if gv.apply_force:
                    self.x_velocity += 1 * 4
                    self.x_velocity = min(self.x_velocity, self.speed)
                    gv.apply_force = False
                else:
                    # print("moving right, skip applying force. x_velocity", self.x_velocity)
                    gv.apply_force = True
            else:  # NPC
                self.x_velocity = self.speed
            self.direction = 1
        else:
            # friction force reverts player to a stand still over time if not moving left or right
            if self.x_velocity > 0:
                self.x_velocity = max(self.x_velocity - 2, 0)
            elif self.x_velocity < 0:
                self.x_velocity = min(self.x_velocity + 2, 0)

        if self.jump and not self.in_air:
            if gv.ufo_present:
                gv.floating = True
            # code below was put in so Khatchig wouldn't jump when he enters door
            # should/can we add this to the the other for loop of the decoration tiles?
            for tile in gv.decoration_group:
                if tile.collidable:
                    if tile.type in gv.door_dict:
                        if tile.rect.colliderect(self.rect.x, self.rect.y, self.width, self.height):
                            door_flag = True

                    if tile.type == "phone":
                        if tile.rect.colliderect(self.rect.x, self.rect.y, self.width, self.height):
                            if not self.phone_flag:
                                gv.phone_pick_up_sfx.play()
                            self.phone_flag = True
                            self.phone_pos = [tile.rect.x, tile.rect.y]

                            door_flag = True  # avoids jump sound effect

            if not (door_flag or self.phone_flag):
                if self.action == 4:
                    self.y_velocity = -25  # super jump initial velocity
                else:
                    self.y_velocity = -17  # normal jump initial velocity
                self.in_air = True

        if self.phone_flag:
            temp_dialogue = gv.dialogue["phone"][gv.dialogue_counter % len(gv.dialogue["phone"])][:]
            f.draw_dialogue(temp_dialogue, self.phone_pos[0], self.phone_pos[1] - 30)

            if pygame.time.get_ticks() - gv.last_time_check_dialogue > gv.DIALOGUE_INTERVAL:
                gv.dialogue_counter_flag = True
                gv.speech_sfx.play()
                gv.last_time_check_dialogue = pygame.time.get_ticks()

            # we offset the normal increment so we don't penalize the player for listening
            gv.health_counter_on = False

            gv.screen.blit(gv.white_heart_img, (150 + ((gv.khatchig.health - 1) * 40), 30))

        self.y_velocity = min(self.y_velocity + gv.GRAVITY, 17)

        if gv.floating:
            self.x_velocity = 3

            if (moving_left and self.last_moving_right) or (moving_right and self.last_moving_left):
                self.y_velocity -= 4

            if moving_right:
                self.last_moving_right = True
                self.last_moving_left = False
            if moving_left:
                self.last_moving_right = False
                self.last_moving_left = True

        dx = self.x_velocity
        dy = self.y_velocity

        # print("char", self.char_type, gv.world_level)
        if self.char_type == "khatchig":
            # check collidable decoration tiles, and potentially flip or do other actions if khatchig has collided with them
            for tile in gv.decoration_group:
                if tile.collidable:
                    if tile.type == "phone":
                        if tile.rect.colliderect(self.rect.x + dx, self.rect.y + dy, self.width, self.height):
                            # keep phone position up to date for dialogue printing
                            self.phone_pos = [tile.rect.x, tile.rect.y]
                        else:
                            if self.phone_flag:
                                # it's a phone hang-up sound too
                                gv.phone_pick_up_sfx.play()
                            self.phone_flag = False

                        if self.phone_flag:
                            new_decoration = d.Decoration(gv.img_list[117], tile.rect.x, tile.rect.y, collidable=True, type="phone")
                            tile.kill()
                            gv.decoration_group.add(new_decoration)
                        else:
                            new_decoration = d.Decoration(gv.img_list[115], tile.rect.x, tile.rect.y, collidable=True, type="phone")
                            tile.kill()
                            gv.decoration_group.add(new_decoration)
                    if tile.type == "mushroom":
                        if self.pick and tile.rect.colliderect(self.rect.x + dx, self.rect.y + dy, self.width, self.height):
                            # kill grass-with-mushroom tile in the group and add the tile without the mushroom
                            new_decoration = d.Decoration(gv.img_list[4], tile.rect.x, tile.rect.y, collidable=True, type="grass")
                            tile.kill()
                            gv.decoration_group.add(new_decoration)
                            self.health = min(self.health + 1, gv.MAX_HEALTH)  # mushrooms help health
                            self.health_counter = 0  # = 0 would give a bug when mixed w/ dialogue (-=1/step)
                            gv.pick_sfx.play()
                    elif tile.type == "camera":
                        if self.pick and not gv.holding_object and tile.rect.colliderect(
                                self.rect.x + dx, self.rect.y + dy, self.width, self.height):
                            new_decoration = d.Decoration(gv.img_list[2], tile.rect.x, tile.rect.y, collidable=True, type="grass")
                            tile.kill()
                            gv.decoration_group.add(new_decoration)
                            gv.holding_object = 77  # camera tile number
                    elif tile.type == "hot_dog":
                        if self.pick and not gv.holding_object and tile.rect.colliderect(
                                self.rect.x + dx, self.rect.y + dy, self.width, self.height):
                            new_decoration = d.Decoration(gv.img_list[2], tile.rect.x, tile.rect.y, collidable=True, type="grass")
                            tile.kill()
                            gv.decoration_group.add(new_decoration)
                            gv.holding_object = 78  # hot dog
                    elif tile.type == "suitcase":
                        if self.pick and not gv.holding_object and tile.rect.colliderect(
                                self.rect.x + dx, self.rect.y + dy, self.width, self.height):
                            new_decoration = d.Decoration(gv.img_list[2], tile.rect.x, tile.rect.y, collidable=True, type="grass")
                            tile.kill()
                            gv.decoration_group.add(new_decoration)
                            gv.holding_object = 98  # suitcase
                    elif tile.type == "book":
                        if self.pick and not gv.holding_object and tile.rect.colliderect(
                                self.rect.x + dx, self.rect.y + dy, self.width, self.height):
                            new_decoration = d.Decoration(gv.img_list[2], tile.rect.x, tile.rect.y, collidable=True, type="grass")
                            tile.kill()
                            gv.decoration_group.add(new_decoration)
                            gv.holding_object = 99
                        elif self.pick and gv.holding_object == 98 and tile.rect.colliderect(
                                self.rect.x + dx, self.rect.y + dy, self.width, self.height):
                            gv.in_briefcase["book"] = True
                            gv.briefcase_open_sfx.play()
                            new_decoration = d.Decoration(gv.img_list[2], tile.rect.x, tile.rect.y, collidable=True, type="grass")
                            tile.kill()
                            gv.decoration_group.add(new_decoration)
                    elif tile.type == "cat":
                        if self.pick and not gv.holding_object and tile.rect.colliderect(
                                self.rect.x + dx, self.rect.y + dy, self.width, self.height):
                            new_decoration = d.Decoration(gv.img_list[4], tile.rect.x, tile.rect.y, collidable=True, type="grass")
                            tile.kill()
                            gv.decoration_group.add(new_decoration)
                            gv.holding_object = 105
                    elif tile.type == "shirt":
                        if self.pick and not gv.holding_object and tile.rect.colliderect(
                                self.rect.x + dx, self.rect.y + dy, self.width, self.height):
                            new_decoration = d.Decoration(gv.img_list[2], tile.rect.x, tile.rect.y, collidable=True, type="grass")
                            tile.kill()
                            gv.decoration_group.add(new_decoration)
                            gv.holding_object = 123
                        elif self.pick and gv.holding_object == 98 and tile.rect.colliderect(
                                self.rect.x + dx, self.rect.y + dy, self.width, self.height):
                            gv.in_briefcase["shirt"] = True
                            gv.briefcase_open_sfx.play()
                            new_decoration = d.Decoration(gv.img_list[2], tile.rect.x, tile.rect.y, collidable=True, type="grass")
                            tile.kill()
                            gv.decoration_group.add(new_decoration)
                    elif tile.type == "printout":
                        if self.pick and not gv.holding_object and tile.rect.colliderect(
                                self.rect.x + dx, self.rect.y + dy, self.width, self.height):
                            new_decoration = d.Decoration(gv.img_list[2], tile.rect.x, tile.rect.y, collidable=True, type="grass")
                            tile.kill()
                            gv.decoration_group.add(new_decoration)
                            gv.holding_object = 186
                        elif self.pick and gv.holding_object == 98 and tile.rect.colliderect(
                                self.rect.x + dx, self.rect.y + dy, self.width, self.height):
                            gv.in_briefcase["printout"] = True
                            gv.briefcase_open_sfx.play()
                            new_decoration = d.Decoration(gv.img_list[2], tile.rect.x, tile.rect.y, collidable=True, type="grass")
                            tile.kill()
                            gv.decoration_group.add(new_decoration)
                    elif tile.type == "mirror":
                        if tile.rect.colliderect(self.rect.x + dx, self.rect.y + dy, self.width, self.height):
                            mirror_temp = pygame.Surface((750, 750), pygame.SRCALPHA)
                            pygame.draw.rect(mirror_temp, (33, 43, 124), (0, 0, gv.SCREEN_WIDTH, gv.SCREEN_HEIGHT))  # mirror tint bg
                            # NotKhatchig in the mirror
                            mirror_temp.blit(pygame.transform.flip(self.animation_list[(self.action + 6) %
                                                                                       len(self.animation_types)][self.anim_index],
                                                                   (lambda x: False if x == 1 else True)(self.direction), False),
                                             (self.rect.x + dx, self.rect.y + dy))
                            gv.mirror = mirror_temp.subsurface(tile.rect.x - 25, tile.rect.y, 50, 50).copy()
                            gv.mirror_loc = (tile.rect.x, tile.rect.y)
                    elif tile.type == "lever off" and self.world_instance.ca_rules_updated:
                        if tile.rect.colliderect(self.rect.x + dx, self.rect.y + dy, self.width, self.height):
                            gv.ca_lever_sfx.play()
                            self.world_instance.ca_lever = True
                            new_decoration = d.Decoration(gv.img_list[55], tile.rect.x, tile.rect.y, collidable=False, type="lever on")
                            tile.kill()
                            gv.decoration_group.add(new_decoration)
                            self.world_instance.ca_rules_updated = False

                            for idx, tile_data in enumerate(gv.obstacle_list):
                                if tile_data[4] == "flip on lever":
                                    gv.obstacle_list[idx][0], gv.obstacle_list[idx][3] = gv.obstacle_list[idx][3], gv.obstacle_list[idx][0]
                    elif tile.type == "flip on hot dog drop" and gv.holding_object == 78 and self.pick:
                        # this is handled under pick_flag = True, not just collision, in main.py
                        pass
                    # verify that Khatchig has triggered (or recently triggered) the door warp
                    elif (self.jump and tile.type in gv.door_dict) or gv.khatchig_is_porting:
                        if not gv.khatchig_is_porting:
                            if tile.rect.colliderect(self.rect.x + dx, self.rect.y + dy, self.width, self.height):
                                gv.door_sfx.play()
                                gv.khatchig_is_porting = True
                                # gv.room_lib = importlib.import_module(tile.type)  # import room by string name
                                # gv.world_level = tile.type
                                self.anim_index = 0  # anim_index is shared between actions; so reset it here for the logic below
                        elif self.anim_index >= len(self.animation_list[self.action])-1:
                            if tile.rect.colliderect(self.rect.x + dx, self.rect.y + dy, self.width, self.height) and (
                                    tile.type in gv.door_dict):
                                gv.khatchig_is_porting = False
                                gv.world_level = tile.type
                                # gv.room_lib.create()
                                gv.moving_right = False
                                gv.moving_left = False
                                break
                    elif tile.type in ["first dead_head", "second dead_head", "third dead_head"]:
                        if tile.type == "first dead_head":
                            dh_idx = 0
                        elif tile.type == "second dead_head":
                            dh_idx = 1
                        else:
                            dh_idx = 2

                        if tile.rect.colliderect(self.rect.x + dx, self.rect.y + dy, self.width, self.height):
                            f.draw_dialogue(gv.dialogue[f"dead_head{gv.level}{dh_idx}"][gv.dialogue_counter % (
                                len(gv.dialogue[f"dead_head{gv.level}{dh_idx}"]))], tile.rect.x, tile.rect.y)

                            if pygame.time.get_ticks() - gv.last_time_check_dialogue > gv.DIALOGUE_INTERVAL:
                                gv.dialogue_counter_flag = True
                                gv.speech_sfx.play()
                                gv.last_time_check_dialogue = pygame.time.get_ticks()

                            # we offset the normal increment so we don't penalize the player for listening
                            gv.health_counter_on = False

                            gv.screen.blit(gv.white_heart_img, (150 + ((gv.khatchig.health - 1) * 40), 30))

                    elif tile.type in ["flip dead_head", "flip dead_head bottom"]:
                        if tile.rect.colliderect(self.rect.x + dx, self.rect.y + dy, self.width, self.height):
                            if tile.type == "flip dead_head":
                                f.draw_dialogue(gv.dialogue[f"dead_head_flip"][gv.dialogue_counter % len(gv.dialogue[f"dead_head_flip"])],
                                                tile.rect.x, tile.rect.y)

                                if pygame.time.get_ticks() - gv.last_time_check_dialogue > gv.DIALOGUE_INTERVAL:
                                    gv.dialogue_counter_flag = True
                                    gv.speech_sfx.play()
                                    gv.last_time_check_dialogue = pygame.time.get_ticks()

                                # we offset the normal increment so we don't penalize the player for listening
                                gv.health_counter_on = False

                                gv.screen.blit(gv.white_heart_img, (150 + ((gv.khatchig.health - 1) * 40), 30))

                            if pygame.time.get_ticks() - self.last_time_check_flip > gv.DIALOGUE_INTERVAL/48:
                                # swap image being used and not being used
                                old_image = tile.image
                                if tile.type == "flip dead_head":
                                    new_decoration = d.Decoration(tile.flip_image, tile.rect.x, tile.rect.y,
                                                                  collidable=True, type="flip dead_head", flip_image=old_image)
                                else:
                                    new_decoration = d.Decoration(tile.flip_image, tile.rect.x, tile.rect.y,
                                                                  collidable=True, type="flip dead_head bottom", flip_image=old_image)
                                tile.kill()
                                gv.decoration_group.add(new_decoration)
                                self.last_time_check_flip = pygame.time.get_ticks()

            # reset since Khatchig porting animation has looped and he is no longer touching a door
            if self.char_type == "khatchig" and gv.khatchig_is_porting and self.anim_index >= len(self.animation_list[self.action]) - 1:
                gv.khatchig_is_porting = False

            # we use self.jump to enter rooms (see collision handling), not to just jump
            # code below reverts self.jump to False now that the variable has been used for all its purposes
            # allowed it to be True from event handling, through move() method, through decoration collision handling (of one step in loop)
            if self.jump:
                self.jump = False
                if not door_flag:
                    gv.jump_sfx.play()

        # go through all obstacles and check for player collisions before finalizing dx and dy direction updates
        # also see if we need to flip any tiles
        for idx, tile_data in enumerate(gv.obstacle_list):
            # check x direction collision before it occurs, so you can prevent passage through hard object
            if tile_data[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                if self.char_type == "khatchig":
                    if dx > 0:
                        # in the normal case of running and hitting a wall, we get a normal block and dx calculation
                        # in the event khatchig lands on the corner of an object we get a neat "superposition" effect
                        # this is because the collision with this object happens every other step (if the player holds down K_right/left)
                        dx = tile_data[1].left - self.rect.right
                    else:
                        dx = tile_data[1].right - self.rect.left

                # if NPC hits wall, make them change directions
                if self.char_type != 'khatchig':
                    dx = 0
                    self.direction *= -1
                    self.move_counter = 0

            # now check same obstacles for collisions with what will be the y direction move
            # dy analysis also includes the tile flipping check
            if tile_data[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # check if going up
                if self.y_velocity < 0:
                    # add a collision flag so multiple blocks can be checked in for loop before updating dy
                    # this helps with checking to see if multiple CA Rules tiles were hit
                    hit_head_flag = True
                    dy_temp = tile_data[1].bottom - self.rect.top
                    if tile_data[4] == "flip when hit with head":
                        gv.ca_rule_change_sfx.play()
                        # make the reference image the one not being used, and put the other in the reserve spot
                        gv.obstacle_list[idx][0], gv.obstacle_list[idx][3] = gv.obstacle_list[idx][3], gv.obstacle_list[idx][0]
                        self.world_instance.ca_rules[gv.obstacle_list[idx][5]] = (self.world_instance.ca_rules[
                                                                                      gv.obstacle_list[idx][5]] + 1) % 2
                        self.world_instance.ca_rules_updated = True
                # check if falling
                elif self.y_velocity >= 0:
                    # prevent feet going through object
                    self.y_velocity = 0
                    self.in_air = False
                    dy = tile_data[1].top - self.rect.bottom

        # prevent head going through object (now that we've checked all possible objects against collision)
        if hit_head_flag:
            self.y_velocity = 0
            dy = dy_temp

        # check for "superposition" (on/off collision sequence) and flip action/images between khatchig and notkhatchig
        if self.char_type == "khatchig":
            if dx > 0:
                if gv.dx_pos_last_time:
                    gv.collision_on_off_counter = 0
                else:
                    gv.dx_pos_last_time = True
                    gv.collision_on_off_counter += 1
                    if gv.collision_on_off_counter > 50:
                        if self.action == 0:
                            self.action = 6
                        elif self.action == 1 or self.action == 2:  # Khatchig could be landing from a jump(2)
                            self.action = 7
            if dx < 0:
                if not gv.dx_pos_last_time:
                    gv.collision_on_off_counter = 0
                else:
                    gv.dx_pos_last_time = False
                    gv.collision_on_off_counter += 1
                    if gv.collision_on_off_counter > 100:
                        dy = -30
                    elif gv.collision_on_off_counter > 50:
                        if self.action == 6:
                            self.action = 0
                        elif self.action == 7:
                            self.action = 1

            if gv.collision_on_off_counter > 50 and self.first_sfx:
                self.first_sfx = False
                gv.success_sfx.play()
                gv.to_do["superposition"] = True
                gv.world_level = "movie"
                gv.movie_idx = 14

            # check for collision with water tiles
            if pygame.sprite.spritecollide(self, gv.water_group, False):
                if not gv.splash:
                    gv.splash_sfx.play()
                    gv.splash = True
            else:
                # reset sfx flag for next dip in the pool/water
                gv.splash = False

        # check with collision with exit group
        level_complete = False
        if pygame.sprite.spritecollide(self, gv.exit_group, False):
            level_complete = True
            # prevent player movement during transition
            self.alive = False

        # check for falling in pit
        if self.rect.top > gv.SCREEN_HEIGHT:
            self.health = 0

        # check if khatchig is moving off edge of screen
        if self.char_type == 'khatchig':
            if self.rect.left + dx < 0 or self.rect.right + dx > gv.SCREEN_WIDTH:
                self.x_velocity = 0
                dx = 0

        self.rect.x += dx
        self.rect.y += dy
        # for looping player off the top of the screen onto the bottom
        # if self.rect.bottom < 0:
        #     self.rect.y = self.rect.y % gv.SCREEN_HEIGHT - 50

        # update scroll based on change in position of character
        # the "camera dolly" moves when the player/khatchig gets within 200 pixels of the edge of the screen
        # ...except at the start and end of the level
        # this fixes the player's absolute position on screen and moves everything else backwards instead
        if self.char_type == 'khatchig':
            if gv.level == 2:  # vertical level
                if self.rect.bottom > gv.SCREEN_HEIGHT - gv.SCROLL_THRESH - 190:
                    self.rect.y -= dy
                    gv.screen_scroll = -dy
                elif self.rect.top < gv.SCROLL_THRESH and dy < 0:
                    self.rect.y -= dy
                    gv.screen_scroll = -dy
            # keep khatchig/player from going all the way to the edge of the screen
            # too close to the right side of the screen (and not in the final screen rectangle of the level)
            # #or too close to the left side of the screen (and we are beyond the first pixels in terms of scrolling the background)
            elif ((self.rect.right >= gv.SCREEN_WIDTH - gv.SCROLL_THRESH and
                  gv.bg_scroll < (self.world_instance.level_length * gv.TILE_SIZE - gv.SCREEN_WIDTH) -
                   min(0, (gv.bg_scroll-(self.world_instance.level_length * gv.TILE_SIZE - gv.SCREEN_WIDTH)))) or
                  (self.rect.left <= gv.SCROLL_THRESH < gv.bg_scroll)):  # moving left on the first screen
                self.rect.x -= dx  # reverse out the dx to keep player static while screen scrolls
                gv.screen_scroll = -dx
            else:
                pass

        return gv.screen_scroll, level_complete

    # this method is only used for NPCs
    def auto(self):
        if self.alive and gv.khatchig.alive:
            if not self.idling and random.randint(1, 500) == 3:  # 1 in 500 chance
                self.update_action(0)  # idle
                self.idling = True
                self.idling_counter = 50
            if not self.idling:
                if self.direction == 1:
                    agent_moving_right = True
                else:
                    agent_moving_right = False
                agent_moving_left = not agent_moving_right
                # the move method's return value is not needed for the NPC, so it isn't assigned
                self.move(agent_moving_left, agent_moving_right)
                self.update_action(1)  # run

                self.move_counter += 1

                if self.move_counter > 100:
                    self.direction *= -1
                    self.move_counter *= -1
            else:
                self.idling_counter -= 1
                if self.idling_counter <= 0:
                    self.idling = False

        # scroll the NPCs based on Khatchig's movement of the background
        self.rect.x += gv.screen_scroll

    # this method is only used for notkhatchig
    def autonot(self):
        if self.alive and gv.khatchig.alive:
            if not self.notkhatchig_enters_room:
                self.update_action(1)
            if self.direction == 1:
                agent_moving_right = True
            else:
                agent_moving_right = False
            agent_moving_left = not agent_moving_right
            # the move method's return value is not needed for the NPC, so it isn't assigned
            self.move(agent_moving_left, agent_moving_right)

            if not self.notkhatchig_enters_room:
                for tile in gv.decoration_group:
                    if tile.collidable and tile.type in gv.door_dict:
                        if tile.rect.colliderect(self.rect.right, self.rect.y, self.width, self.height):
                            self.notkhatchig_enters_room = True
                            gv.door_sfx.play()
                            self.update_action(0)
                            self.speed = 0

        # scroll the NPCs based on Khatchig's movement
        self.rect.x += gv.screen_scroll

    def update_animation(self):
        self.image = self.animation_list[self.action][self.anim_index]

        # if enough time has passed, update the animation step
        if self.char_type == "hippie":
            if pygame.time.get_ticks() - self.last_time_check > gv.ANIMATION_INTERVAL*3:
                self.last_time_check = pygame.time.get_ticks()
                self.anim_index += 1
        else:
            if pygame.time.get_ticks() - self.last_time_check > gv.ANIMATION_INTERVAL:
                self.last_time_check = pygame.time.get_ticks()
                self.anim_index += 1

        if self.anim_index >= len(self.animation_list[self.action]):
            self.anim_index = 0
            self.anim_cycled = True

        # NPC remains transparent at the end of the door warp dissolve
        if self.char_type == "notkhatchig" and self.action == 0 and self.anim_cycled:
            self.anim_index = -1  # last/blank image

    def update_action(self, new_action):
        # check if action is new before updating
        if new_action != self.action:
            # let picking (action 4) complete
            if self.action == 4 and self.anim_cycled is False:
                pass
            else:
                self.action = new_action
                self.anim_index = 0
                self.anim_cycled = False
                gv.pick_flag = False
                self.last_time_check = pygame.time.get_ticks()

    def check_alive(self):
        if self.vulnerable:
            self.vulnerable_counter = 0
        else:
            self.vulnerable_counter += 1

            if self.vulnerable_counter > 130:
                self.vulnerable = True
                self.vulnerable_counter = 0

        if self.health <= 0 and self.alive:
            gv.gong_sfx.play()
            self.health = 0
            self.speed = 0
            self.alive = False
            gv.lives -= 1
            self.update_action(3)

    def update(self):
        self.update_animation()
        if self.char_type == "khatchig":
            self.check_alive()

    def draw(self):
        if self.vulnerable:
            # flip image, in x direction, y direction
            gv.screen.blit(pygame.transform.flip(self.image, (lambda x: False if x == 1 else True)(self.direction), False), self.rect)
        else:
            if self.vulnerable_counter % 2 == 0:
                muted_image = self.image.copy()
                muted_image.fill((100, 60, 100, 80), special_flags=pygame.BLEND_SUB)
                gv.screen.blit(pygame.transform.flip(muted_image, (lambda x: False if x == 1 else True)(self.direction), False), self.rect)
            else:
                gv.screen.blit(pygame.transform.flip(self.image, (lambda x: False if x == 1 else True)(self.direction), False), self.rect)

        if self.char_type == "khatchig":
            if gv.holding_object:
                # obj_number : pixel_offset_adjustment
                obj_offset = {77: 24,  # camera
                              78: 0,  # hot dog
                              98: 25,  # briefcase
                              99: 20,  # book
                              105: 0,  # cat
                              123: 5,  # shirt
                              186: 20}  # printout

                gv.screen.blit(
                    pygame.transform.flip(gv.img_list[gv.holding_object], (lambda x: False if x == 1 else True)(self.direction), False),
                    (self.rect.x, self.rect.y + obj_offset[gv.holding_object]))

        if self.char_type == "hippie":
            if abs(self.rect.centerx - gv.khatchig.rect.centerx) < 75 and abs(self.rect.centery - gv.khatchig.rect.centery) < 75:
                if gv.to_do["deliver cat"]:
                    f.draw_dialogue(gv.dialogue["hippie2"][gv.dialogue_counter % len(gv.dialogue["hippie2"])], self.rect.midtop[0],
                                    self.rect.midtop[1] - 15)
                else:
                    f.draw_dialogue(gv.dialogue["hippie"][gv.dialogue_counter % len(gv.dialogue["hippie"])], self.rect.midtop[0],
                                    self.rect.midtop[1] - 15)

                if pygame.time.get_ticks() - gv.last_time_check_dialogue > gv.DIALOGUE_INTERVAL:
                    gv.dialogue_counter_flag = True
                    gv.speech_sfx.play()
                    gv.last_time_check_dialogue = pygame.time.get_ticks()

                # we offset the normal increment so we don't penalize the player for listening
                gv.health_counter_on = False

                gv.screen.blit(gv.white_heart_img, (150 + ((gv.khatchig.health - 1) * 40), 30))
