import pygame
import global_vars as gv
import random
import computer_room  # for platonic solids
import decoration as d
import csv
import world as w
# import struct
import colorsys


def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    gv.screen.blit(img, (x, y))


def draw_dialogue(text, x, y):
    # set dimensions of dialogue box
    dialogue_surface = pygame.Surface((max([len(line) for line in text])*10, len(text)*13))

    dialogue_font = pygame.font.Font(gv.resource_path("fonts/kongtext.ttf"), 10)

    for i, line in enumerate(text):
        text_surface = dialogue_font.render(line, True, gv.WHITE)
        dialogue_surface.blit(text_surface, (0,i*15))
    dialogue_rect = dialogue_surface.get_rect(midbottom=(x, y))

    bg_rect = dialogue_rect.copy()
    bg_rect.inflate_ip(10, 10)  # enlarge the copy in position

    frame_rect = bg_rect.copy()
    frame_rect.inflate_ip(4, 4)

    pygame.draw.rect(gv.screen, gv.WHITE, frame_rect)
    pygame.draw.rect(gv.screen, gv.BLACK, bg_rect)
    gv.screen.blit(dialogue_surface, dialogue_rect)


# future: add rain sound and Goettsching song at start of game
# show rain in game going away at start of level 0 as Khatchig moves from the city to the surreal world
# def draw_foreground:
def draw_background():
    print(f"bg_scroll: {gv.bg_scroll}")
    # bg loop frequency
    width = 1376
    # copies are made side by side, offset in the x direction 6 times
    # we get a parallax effect with different scroll factors
    # gv.bg_scroll is an aggregate number that reflects where player is in the x direction of the board layout
    
    
    # if gv.level == 0:
    #     for x in range(6):
    #         gv.screen.blit(gv.stars_img, ((x * width) - gv.bg_scroll * 0.5, 0))
    #         gv.screen.blit(gv.pine1_img, ((x * width) - gv.bg_scroll * 0.7, gv.SCREEN_HEIGHT - gv.pine1_img.get_height() - 250))
    #         gv.screen.blit(gv.pine2_img, ((x * width) - gv.bg_scroll * 0.8, gv.SCREEN_HEIGHT - gv.pine2_img.get_height()))
    # elif gv.level == 1:
    #     gv.screen.blit(gv.sun_img, (-1000 - gv.bg_scroll * 0.02, 0))
    #     # tetrahedrons rotating in two directions
    #     computer_room.create_bg(pv=computer_room.proj_viewer1, trans_dist=gv.screen_scroll * 0.08, reverse=-1)
    #     computer_room.create_bg(pv=computer_room.proj_viewer2, trans_dist=gv.screen_scroll * 0.08)
    #     # cubes rotating in two directions
    #     computer_room.create_bg(pv=computer_room.proj_viewer3, obj="cube", trans_dist=gv.screen_scroll * 0.08, reverse=-1)
    #     computer_room.create_bg(pv=computer_room.proj_viewer4, obj="cube", trans_dist=gv.screen_scroll * 0.08)
    #     # two cubes and one tetrahedron
    #     computer_room.create_bg(pv=computer_room.proj_viewer5, obj="cube", trans_dist=gv.screen_scroll * 0.08, reverse=-1)
    #     computer_room.create_bg(pv=computer_room.proj_viewer6, obj="cube", trans_dist=gv.screen_scroll * 0.08)
    #     computer_room.create_bg(pv=computer_room.proj_viewer7, trans_dist=gv.screen_scroll * 0.08)
    #     gv.screen.blit(gv.water_bg_img, (0 - gv.bg_scroll * 0.05, 650))
    #     gv.screen.blit(gv.water_bg2_img, (0 - gv.bg_scroll * 0.1, 675))
    #     gv.screen.blit(gv.water_bg3_img, (0 - gv.bg_scroll * 0.2, 730))
    # elif gv.level == 2:
    #     for x in range(6):
    #         gv.screen.blit(gv.rotated_stars_img, (0, (x * width) - gv.bg_scroll * 0.5 - 300))

    # # no loop for non-repeating background
    # if gv.level == 0:
    #     gv.screen.blit(gv.streets_img, ((0 * width) - gv.bg_scroll * 0.92, gv.SCREEN_HEIGHT - gv.streets_img.get_height() - 40))

    if gv.level == 0:
        # single blit per layer using pre-tiled strips (was 6 blits each)
        _ox_stars = int(-gv.bg_scroll * 0.5) % width - width
        _ox_pine1 = int(-gv.bg_scroll * 0.7) % width - width
        _ox_pine2 = int(-gv.bg_scroll * 0.8) % width - width
        gv.screen.blit(gv.stars_strip, (_ox_stars, 0))
        gv.screen.blit(gv.pine1_strip, (_ox_pine1, gv.SCREEN_HEIGHT - gv.pine1_img.get_height() - 250))
        gv.screen.blit(gv.pine2_strip, (_ox_pine2, gv.SCREEN_HEIGHT - gv.pine2_img.get_height()))
    elif gv.level == 1:
        gv.screen.blit(gv.sun_img, (int(-1000 - gv.bg_scroll * 0.02), 0))
        # tetrahedrons rotating in two directions
        computer_room.create_bg(pv=computer_room.proj_viewer1, trans_dist=gv.screen_scroll * 0.08, reverse=-1)
        computer_room.create_bg(pv=computer_room.proj_viewer2, trans_dist=gv.screen_scroll * 0.08)
        # cubes rotating in two directions
        computer_room.create_bg(pv=computer_room.proj_viewer3, obj="cube", trans_dist=gv.screen_scroll * 0.08, reverse=-1)
        computer_room.create_bg(pv=computer_room.proj_viewer4, obj="cube", trans_dist=gv.screen_scroll * 0.08)
        # two cubes and one tetrahedron
        computer_room.create_bg(pv=computer_room.proj_viewer5, obj="cube", trans_dist=gv.screen_scroll * 0.08, reverse=-1)
        computer_room.create_bg(pv=computer_room.proj_viewer6, obj="cube", trans_dist=gv.screen_scroll * 0.08)
        computer_room.create_bg(pv=computer_room.proj_viewer7, trans_dist=gv.screen_scroll * 0.08)
        gv.screen.blit(gv.water_bg_img, (int(-gv.bg_scroll * 0.05), 650))
        gv.screen.blit(gv.water_bg2_img, (int(-gv.bg_scroll * 0.1), 675))
        gv.screen.blit(gv.water_bg3_img, (int(-gv.bg_scroll * 0.2), 730))
    elif gv.level == 2:
        # single blit using pre-tiled vertical strip (was 6 blits)
        _oy = int(-gv.bg_scroll * 0.5) % width - width
        gv.screen.blit(gv.rotated_stars_strip, (0, _oy - 300))

    # no loop for non-repeating background
    if gv.level == 0:
        gv.screen.blit(gv.streets_img, (int(-gv.bg_scroll * 0.92), gv.SCREEN_HEIGHT - gv.streets_img.get_height() - 40))


def reset_music():
    """used to reset music for the given level in reset_level()"""

    # pygame.mixer.music.fadeout(1000)
    # pygame.mixer.music.unload()
    # pygame.mixer.stop()

    pygame.mixer.music.load(gv.resource_path(f"audio/level{gv.level}_music.ogg"))

    if gv.play_music:
        pygame.mixer.music.set_volume(0.35)
    else:
        pygame.mixer.music.set_volume(0)

    pygame.mixer.music.play(-1, 0.0, 1000)  # loop forever, no delay, audio fade transition in ms


def reset_level(book_flag=False):
    gv.moving_left = False
    gv.moving_right = False
    gv.start_icaros = True
    gv.splash = False
    gv.ufo_present = False
    gv.floating = False

    # print("various func, to do:", gv.to_do.items())

    reset_music()

    gv.decoration_group.empty()
    gv.water_group.empty()
    gv.exit_group.empty()
    gv.real_group.empty()
    gv.blob_group.empty()

    # level 2 is the one vertical level at the moment
    if gv.level == 2:
        gv.ROWS = 150
        gv.COLUMNS = 15
    else:
        gv.ROWS = 15
        gv.COLUMNS = 150

    if gv.level == 2:
        # reset the Cellular Automaton attributes associated with the World object
        # use random 8-bit rule set to generate the solution
        gv.ca_solution_rules = [random.randint(0, 1) for _ in range(8)]
        # initialize the starting state (without appended and prepended 0s) of the CA
        ca_next_string = "1"
        ca_row = 0
        gv.continued_CA = []
        gv.first_ca_block_removal_sfx = True

        # generate cellular automaton solution row of 15 bits and additional decoration details for level
        for _ in range(107):
            ca_row += 1
            # prepend and append just enough 0s for the next row/state to grow by 2 cells
            if len(ca_next_string) <= 13:
                ca_state = "00" + ca_next_string + "00"
            # continue the CA rows in a fixed gv.SCREEN_WIDTH fashion of 15 tiles/row
            else:
                ca_state = "0" + ca_next_string + "0"

            # initialize the computation of the next row of bits
            ca_next_string = ""

            # Checking CA "codons" against rules to determine the cell in the current state
            for i in range(len(ca_state) - 2):
                ca_next_string = ca_next_string + str(gv.ca_solution_rules[int(ca_state[i:i + 3], 2)])

            # it takes 7 computed rows to get to the first row of 15 cells; 3 5 7 9 11 13 15
            if ca_row == 7:
                gv.ca_solution = ca_next_string

            if ca_row >= 8:
                gv.continued_CA.append(ca_next_string)

        # print(gv.ca_solution_rules, gv.ca_solution)

    with open(gv.resource_path(f"levels/level{gv.level}_data.csv"), newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        world_data = [[int(tile) for tile in row] for row in reader]

    # after death, add book to certain spot on level instead of having to deliver cat again to get book
    if book_flag:
        world_data[8][5] = 67
    else:
        # checkpoint
        # lives would only be 3 if they were just reset at a "continue?" screen
        if gv.checkpoint_flag and gv.lives != 3:
            if gv.level == 0:
                gv.bg_scroll, gv.screen_scroll = 3650, -3650
            elif gv.level == 1:
                gv.bg_scroll, gv.screen_scroll = 3200, -3200
            else:
                # checkpoint not needed for third level, level 2
                pass

    # reset now that it has been used to properly set up level
    gv.checkpoint_flag = False

    gv.world_instance = w.World()
    gv.khatchig, gv.ufo, gv.hippie, gv.notkhatchig, gv.cat = gv.world_instance.process_data(world_data)


def level_complete_process():
    gv.start_transition = True
    gv.img_list[0] = gv.nested_levels[gv.level - 1]  # update the ending tile image to reflect the nested tile for the next
    gv.level = (gv.level + 1) % gv.LEVELS

    # first_time is used to identify when inter-level transition reference should be updated (also used for end room dialogue)
    if gv.level == 0:
        gv.first_time = False

    gv.checkpoint_flag = False
    gv.bg_scroll = 0
    reset_level()


def increment_or_reset_dialogue():
    if gv.dialogue_counter_flag:
        gv.dialogue_counter += 1
        gv.last_time_check_dialogue = pygame.time.get_ticks()

    if pygame.time.get_ticks() - gv.last_time_check_dialogue > gv.DIALOGUE_INTERVAL + 10:
        gv.dialogue_counter = 0
        gv.dialogue_counter_flag = False


def post_death_fade_process(inputs):
    if gv.lives == 0:
        draw_text(f"Continue?", gv.font, gv.WHITE, gv.SCREEN_HEIGHT / 2 - 85, gv.SCREEN_WIDTH / 2 - 80)
        gv.restart = True
    else:
        draw_text(f"LEVEL {bin(gv.level + 1)[2:].zfill(2)}", gv.font, gv.WHITE, gv.SCREEN_HEIGHT / 2 - 65, gv.SCREEN_WIDTH / 2 - 80)
        draw_text(f"X {bin(gv.lives)[2:].zfill(2)}", gv.font, gv.WHITE, gv.SCREEN_HEIGHT / 2, gv.SCREEN_WIDTH / 2)
        gv.screen.blit(gv.head_img, (gv.SCREEN_HEIGHT / 2 - 60, gv.SCREEN_WIDTH / 2 - 22))
        gv.restart = True

    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT or (event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_ESCAPE):
            gv.running = False

    # A button or 1P start confirms continue (replaces K_RETURN)
    if inputs["p1"]["a"] or inputs["system"]["start_1p"]:
        if gv.lives == 0:
            gv.lives = 3
            gv.level = 0
            gv.to_do = {task: False for task in gv.to_do_list}
            # refactor: code below; handles a reset; these values were initialized on import, outside of method or function :(
            computer_room.proj_viewer = computer_room.initialize()
            # initialized for 2nd level background design (function used outside of computer room => bad file name.)
            # tetrahedrons rotating in two directions
            computer_room.proj_viewer1 = computer_room.initialize(600, 600 + 1600, 0.25)
            computer_room.proj_viewer2 = computer_room.initialize(600, 600 + 1600, 0.25)
            # cubes rotating in two directions
            computer_room.proj_viewer3 = computer_room.initialize(200, 600 + 1600, 0.25)
            computer_room.proj_viewer4 = computer_room.initialize(200, 600 + 1600, 0.25)
            # two cubes and one tetrahedron
            computer_room.proj_viewer5 = computer_room.initialize(400, 400 + 1600, 0.25)
            computer_room.proj_viewer6 = computer_room.initialize(400, 400 + 1600, 0.25)
            computer_room.proj_viewer7 = computer_room.initialize(400, 400 + 1600, 0.25)

        gv.start_transition = True
        gv.bg_scroll = 0

        # replace the book in the world instead of resetting gv.to_do["deliver cat"] == False
        if (gv.holding_object == 99 or gv.to_do["deliver cat"]) and gv.lives != 3:
            reset_level(book_flag=True)
        else:
            reset_level(book_flag=False)

        # gv.holding_object = None
        gv.holding_object = None
        gv.death_fade.fade_counter = 0
        gv.intro_fade.fade_counter = 0


def transition_process():
    print("TRANSITION PROCESS: restart=", gv.restart, "world_level=", gv.world_level)
    if gv.restart:  # for death and restarting the level
        if gv.intro_fade.fade():  # fade completed
            # reset variables
            gv.start_transition = False
            gv.restart = False
    else:  # first time you start the level
        gv.transition_sfx.play()
        gv.transition_sfx.fadeout(5000)
        # self-contained loop
        # if trans():
        #     gv.start_transition = False
        gv.world_level = "transition"
        gv.start_transition = False


def update_khatchig_action_animation():
    if gv.khatchig.in_air:
        gv.khatchig.update_action(2)  # action 2 is jump
    elif gv.moving_left or gv.moving_right:
        gv.khatchig.update_action(1)  # run
    elif gv.khatchig_is_porting:
        gv.khatchig.update_action(5)  # porting
    else:
        gv.khatchig.update_action(0)  # action 0 is idle


def draw_health_lives():
    draw_text("Health: ", gv.font, gv.WHITE, 10, 35)
    for x in range(gv.khatchig.health - 1):
        gv.screen.blit(gv.heart_img, (150 + (x * 40), 30))

    faded_heart = gv.heart_img.copy()
    faded_heart.fill(((gv.khatchig.health_counter % 350)/350*200, (gv.khatchig.health_counter % 350)/350*200,
                      (gv.khatchig.health_counter % 350)/350*200), special_flags=pygame.BLEND_SUB)
    gv.screen.blit(faded_heart, (150 + ((gv.khatchig.health - 1) * 40), 30))

    for x in range(gv.lives):
        gv.screen.blit(gv.head_img, (550 + (x * 50), 25))


def draw_progress():
    completed_count = min(sum([1 if val else 0 for val in gv.to_do.values()]), 6)
    gv.screen.blit(gv.img_list[194 + completed_count], (450, 25))


def flip_images():
    for idx, tile_data in enumerate(gv.obstacle_list):
        if tile_data[4] == "flip each step":
            mod_len = len(tile_data[3])  # list of images
            gv.obstacle_list[idx][5] = (gv.obstacle_list[idx][5] + 1) % mod_len  # index
            gv.obstacle_list[idx][0] = gv.obstacle_list[idx][3][gv.obstacle_list[idx][5]]  # display this image

    for tile in gv.decoration_group:
        # swap image being used and not being used
        old_image = tile.image
        if tile.type == "cat":
            new_decoration = d.Decoration(tile.flip_image, tile.rect.x, tile.rect.y, collidable=True, type="cat", flip_image=old_image)
            tile.kill()
            gv.decoration_group.add(new_decoration)
            break

    gv.last_time_check = pygame.time.get_ticks()


def update_cellular_automata():
    if gv.world_instance.ca_lever and gv.world_instance.ca_row == 24:
        gv.ca_attempt_sfx.stop()
        gv.ca_attempt_sfx.play()
    elif gv.world_instance.ca_row == 31:
        gv.ca_attempt_sfx.stop()

    # Cellular Automaton (CA) animation
    # step 1: row increment and next state generated
    # while gv.world_instance.ca_lever and gv.world_instance.ca_next_string == "":
    if gv.world_instance.ca_lever and gv.world_instance.ca_next_string == "":
        gv.world_instance.ca_row += 1
        # set starting col (taking into account col increment)
        gv.world_instance.ca_col = max(-1, 32 - gv.world_instance.ca_row - 2)

        # look at neighboring cells on tape which are assumed to be 0s if not explicit
        # the number of next state bits to compute from a n bit string is n - 2
        if len(gv.world_instance.ca_state) <= 13:  # width - 2
            gv.world_instance.ca_state = "00" + gv.world_instance.ca_state + "00"
        else:
            gv.world_instance.ca_state = "0" + gv.world_instance.ca_state + "0"

        # Checking CA "codons" against rules
        for i in range(len(gv.world_instance.ca_state) - 2):
            gv.world_instance.ca_next_string = gv.world_instance.ca_next_string + str(
                gv.world_instance.ca_rules[int(gv.world_instance.ca_state[i:i + 3], 2)])
        gv.world_instance.ca_state = gv.world_instance.ca_next_string

    # step 2: if you are not done writing line of CA cells
    if gv.world_instance.ca_next_string != "":
        if gv.world_instance.ca_last_row_complete:  # only happens after success
            if gv.first_ca_block_removal_sfx:
                gv.ca_block_removal_sfx.play()
                gv.first_ca_block_removal_sfx = False

            break_flag = False
            for idx, tile_data in enumerate(gv.obstacle_list):
                if tile_data[4] == "CA tile":
                    del gv.obstacle_list[idx]
                    break_flag = True
                    break  # we just want to remove one per/step
            if not break_flag:
                gv.ca_block_removal_sfx.stop()
                gv.world_instance.ca_success = False  # so we can know we've finished
        elif gv.world_instance.ca_state == gv.ca_solution and not gv.world_instance.ca_success:
            gv.world_instance.ca_success = True
        else:
            # not solved yet
            next_cell, gv.world_instance.ca_next_string = gv.world_instance.ca_next_string[0], gv.world_instance.ca_next_string[1:]
            gv.world_instance.ca_col += 1

            if next_cell == "0":
                for idx, tile_data in enumerate(gv.obstacle_list):
                    if tile_data[2] == [gv.world_instance.ca_row, gv.world_instance.ca_col]:
                        gv.obstacle_list[idx][0] = gv.img_list[20]
                        gv.obstacle_list[idx][3] = gv.img_list[19]
            elif next_cell == "1":
                for idx, tile_data in enumerate(gv.obstacle_list):
                    if tile_data[2] == [gv.world_instance.ca_row, gv.world_instance.ca_col]:
                        gv.obstacle_list[idx][0] = gv.img_list[19]
                        gv.obstacle_list[idx][3] = gv.img_list[20]

            # end of CA run
            if gv.world_instance.ca_row == 32:
                if gv.world_instance.ca_success:
                    gv.world_instance.ca_last_row_complete = True
                else:
                    # reset to off
                    gv.world_instance.ca_rules_updated = False  # True when gv.khatchig hits head to change rules
                    for tile in gv.decoration_group:
                        if tile.type == "lever on":
                            new_decoration = d.Decoration(gv.img_list[5], tile.rect.x, tile.rect.y, collidable=True, type="lever off")
                            tile.kill()
                            gv.decoration_group.add(new_decoration)

                    # reset CA stuff
                    gv.world_instance.ca_lever = False
                    gv.world_instance.ca_state = "1"  # string representing starting tape (0s in both directions)
                    gv.world_instance.ca_row = 24
                    gv.world_instance.ca_col = 7
                    gv.world_instance.ca_next_string = ""

                    # reset CA pipes to off
                    for idx, tile_data in enumerate(gv.obstacle_list):
                        if tile_data[4] == "flip on lever":
                            gv.obstacle_list[idx][0], gv.obstacle_list[idx][3] = gv.obstacle_list[idx][3], gv.obstacle_list[idx][0]


def get_colors(num_colors):
    colors = [(0, 0, 0)]  # the 0 particle is black
    for _ in range(num_colors):
        hue = random.uniform(0, 1) * 360
        lightness = (50 + random.uniform(0, 1) * 20)/100
        saturation = (70 + random.uniform(0, 1) * 20)/100
        red, green, blue = colorsys.hls_to_rgb(hue, lightness, saturation)
        colors.append((int(red * 255), int(green * 255), int(blue * 255)))
    return colors