import pygame
from pygame import locals
import global_vars as gv
import decoration as d
import various_functions as f
import asyncio
import random
import os
# import webbrowser
import neural_cellular_automata_room_dist as ncar
import monitor_room as mr
import computer_room as cr
import soccer_room as sr
import environment_control_room as ecr
import cat_bus_room as cbr
import ascii_room as ar
import briefcase_room as br
import end_room as er
import particle_affinity_room as pr


class Game:
    async def run(self):
        pygame.mixer.music.load(gv.resource_path("audio/rain_and_thunder.ogg"))
        pygame.mixer.music.play(-1, 0.0, 0)  # loop forever, no delay, audio fade transition in ms
        # main game loop
        screen_shot_num = 5133
        prev_a = False
        prev_b = False

        while gv.running:
            if gv.menu_screen:  # True while user has not hit enter from the menu screen yet
                ## state ##
                gv.screen.blit(gv.menu_img, (0, 0))
                inputs = _get_input().to_py()
                if inputs["system"]["start_1p"] or inputs["system"]["start_2p"]:
                    gv.menu_screen = False
                    gv.start_transition = True
                    # pygame.mixer.music.fadeout(1000)
                    pygame.mixer.music.stop()
                    pygame.mixer.music.unload()
                    f.reset_music()
                    # seed prev state so first game frame doesn't misfire a press from the menu
                    prev_a = inputs["p1"]["a"]
                    prev_b = inputs["p1"]["b"]
                for event in pygame.event.get():
                    if event.type == pygame.locals.QUIT:
                        gv.running = False
    
            # other game loops that have been inserted in the top level (not nested in functions) 
            # to be compatible w/ how pygbag uses asyncio
            elif gv.world_level != "top":
                ## state ##
                if gv.world_level == "movie":
                    sorted_file_list = sorted(os.listdir(gv.resource_path(f"img/movie_png_seq{gv.movie_idx}")))

                    for file in sorted_file_list:
                        if file.endswith('.jpg'):
                            if gv.movie_idx == 2 and file == "UFO12.jpg":
                                gv.ufo_dump_sfx.play()
                                gv.khatchig.y_velocity = 0
                            gv.screen.blit(
                                pygame.image.load(gv.resource_path(f"img/movie_png_seq{gv.movie_idx}/{file}")).convert_alpha(), (0, 0))
                            pygame.transform.scale(gv.screen, (gv.DISPLAY_WIDTH, gv.DISPLAY_HEIGHT), gv.display_surface); pygame.display.flip()
                            if gv.save_screenshots and gv.master_save_screenshots:
                                screen_shot_num = screen_shot_num + 1
                                pygame.image.save(gv.screen, f"./screenshots/screenshot{screen_shot_num}.jpeg")
                                # pygame.image.save(gv.screen, f"./screenshots/screenshot{screen_shot_num}.png")
                            await asyncio.sleep(0)

                    if gv.movie_idx == 1:  # soccer header
                        # pygame.mixer.music.fadeout(1000)
                        pygame.mixer.music.close()
                        pygame.mixer.music.unload()
                        f.reset_music()
                    # this state plays a loop and then automatically goes back up to the "top" level
                    gv.world_level = "top"
                ## state ##
                elif gv.world_level == "tai_chi":
                    sorted_file_list = sorted(os.listdir(gv.resource_path(f"img/movie_png_seq4")))
                    gv.khatchig.health = min(gv.khatchig.health + 1, gv.MAX_HEALTH)
                    gv.khatchig.health_counter = 0

                    for file in sorted_file_list:
                        if file.endswith('.jpg'):
                            if file == "taichi27.jpg":
                                gv.health_reverse_sfx.play()
                            gv.screen.blit(pygame.image.load(gv.resource_path(f"img/movie_png_seq4/{file}")).convert_alpha(), (0, 0))
                            pygame.transform.scale(gv.screen, (gv.DISPLAY_WIDTH, gv.DISPLAY_HEIGHT), gv.display_surface); pygame.display.flip()
                            if gv.save_screenshots and gv.master_save_screenshots:
                                screen_shot_num = screen_shot_num + 1
                                pygame.image.save(gv.screen, f"./screenshots/screenshot{screen_shot_num}.jpeg")
                                # pygame.image.save(gv.screen, f"./screenshots/screenshot{screen_shot_num}.png")
                            await asyncio.sleep(0)

                    gv.world_level = "top"
                ## state ##
                elif gv.world_level == "behind_computer":
                    sorted_file_list = sorted(os.listdir(gv.resource_path(f"img/movie_png_seq6")))
                    gv.khatchig.health = min(gv.khatchig.health + 1, gv.MAX_HEALTH)

                    for file in sorted_file_list:
                        if file.endswith('.jpg'):
                            gv.screen.blit(pygame.image.load(gv.resource_path(f"img/movie_png_seq6/{file}")).convert_alpha(), (0, 0))
                            pygame.transform.scale(gv.screen, (gv.DISPLAY_WIDTH, gv.DISPLAY_HEIGHT), gv.display_surface); pygame.display.flip()
                            if gv.save_screenshots and gv.master_save_screenshots:
                                screen_shot_num = screen_shot_num + 1
                                pygame.image.save(gv.screen, f"./screenshots/screenshot{screen_shot_num}.jpeg")
                                # pygame.image.save(gv.screen, f"./screenshots/screenshot{screen_shot_num}.png")
                            await asyncio.sleep(0)

                    gv.world_level = "top"
                ## state ##
                elif gv.world_level == "monitor_room":
                    # refactored: kept the monitor_room object, but move the run() method up to the top level (& ref instance not self)
                    # refactored: import images on top level; don't load all images into memory when loading game
                    monitor_rm = mr.MonitorRoom()

                    if gv.holding_object == 77:
                        gv.success_sfx.play()
                        gv.to_do["explore feedback"] = True
                        sorted_file_list = sorted(os.listdir(gv.resource_path(f"img/movie_png_seq5")))
                        # play success movie (png sequence)
                        for file in sorted_file_list:
                            if file.endswith('.jpg'):
                                gv.screen.blit(pygame.image.load(gv.resource_path(f"img/movie_png_seq5/{file}")).convert_alpha(), (0, 0))
                                pygame.transform.scale(gv.screen, (gv.DISPLAY_WIDTH, gv.DISPLAY_HEIGHT), gv.display_surface); pygame.display.flip()
                                if gv.save_screenshots and gv.master_save_screenshots:
                                    screen_shot_num = screen_shot_num + 1
                                    pygame.image.save(gv.screen, f"./screenshots/screenshot{screen_shot_num}.jpeg")
                                    # pygame.image.save(gv.screen, f"./screenshots/screenshot{screen_shot_num}.png")
                                await asyncio.sleep(0)

                    img_flip = True

                    while gv.world_level == "monitor_room":
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                            elif event.type == pygame.KEYDOWN:
                                if event.key == pygame.locals.K_SPACE:
                                    gv.world_level = "top"
                                    gv.door_sfx.play()
                                if event.key in monitor_rm.key_to_function:
                                    # dictionary returns a method (run on itself)
                                    monitor_rm.key_to_function[event.key](monitor_rm)

                        if pygame.time.get_ticks() - monitor_rm.last_time_check > gv.ANIMATION_INTERVAL:
                            monitor_rm.last_time_check = pygame.time.get_ticks()
                            img_flip = not img_flip

                        if img_flip:
                            gv.screen.blit(gv.escher15_img, (0, 0))
                        else:
                            gv.screen.blit(gv.escher16_img, (0, 0))

                        if gv.holding_object == 77:
                            monitor_rm.counter += 1

                            # create feedback
                            if monitor_rm.next_frame:
                                gv.screen.blit(monitor_rm.next_frame, (70, 303))
                            sub = gv.screen.copy()
                            sub = monitor_rm.get_rotated_subsurface(sub)
                            gv.tile_on_monitor = pygame.transform.scale(sub, (255, 170))

                            # new
                            gv.tile_on_monitor.fill((1, 1, 1, 56), special_flags=pygame.BLEND_RGBA_ADD)

                            gv.screen.blit(gv.tile_on_monitor, (70, 303))
                            gv.screen.blit(monitor_rm.monitor_text, (80, 310))
                            if monitor_rm.counter % 4 == 0:
                                monitor_rm.next_frame = gv.screen.subsurface(70, 303, 255, 170).copy()
                                monitor_rm.next_frame = pygame.transform.scale(monitor_rm.next_frame, (255, 170))
                            gv.screen.blit(monitor_rm.cam_img, (170, 500 + monitor_rm.cam_zoom/4))
                            gv.screen.blit(gv.letter_box_img, (0,0))
                        else:
                            gv.screen.blit(gv.tile_on_monitor, (70, 303))
                            gv.screen.blit(monitor_rm.monitor_text, (80, 310))

                        if not monitor_rm.intro_complete:
                            if gv.intro_fade.fade():
                                monitor_rm.intro_complete = True
                        pygame.transform.scale(gv.screen, (gv.DISPLAY_WIDTH, gv.DISPLAY_HEIGHT), gv.display_surface); pygame.display.flip()
                        if gv.save_screenshots and gv.master_save_screenshots:
                            screen_shot_num = screen_shot_num + 1
                            pygame.image.save(gv.screen, f"./screenshots/screenshot{screen_shot_num}.jpeg")
                            # pygame.image.save(gv.screen, f"./screenshots/screenshot{screen_shot_num}.png")
                        await asyncio.sleep(0)
                ## state ##
                elif gv.world_level == "neural_cellular_automata_room_dist":
                    nca_rm = ncar.NcaRoomDist()
                    img_flip = True
                    img_num = 0

                    while gv.world_level == "neural_cellular_automata_room_dist":
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                            elif event.type == pygame.KEYDOWN:
                                if event.key == pygame.locals.K_SPACE:
                                    gv.world_level = "top"
                                    gv.door_sfx.play()
                                if event.key in nca_rm.key_to_function:
                                    # message resets each time the user tries to use unavailable functionality
                                    nca_rm.temp_message = True
                                    gv.dialogue_counter = 0
                                    gv.last_time_check_dialogue = pygame.time.get_ticks()
                                    nca_rm.key_to_function[event.key](nca_rm)

                        if pygame.time.get_ticks() - nca_rm.last_time_check > gv.ANIMATION_INTERVAL / 2:
                            nca_rm.last_time_check = pygame.time.get_ticks()
                            img_flip = not img_flip
                            nca_rm.counter += 1

                            if nca_rm.counter > 149:
                                img_num = random.choice(range(140, 150))
                            else:
                                img_num = nca_rm.counter

                        if nca_rm.temp_message and gv.dialogue_counter >= len(gv.dialogue["notkhatchig_temp"]):
                            nca_rm.temp_message = False
                            gv.dialogue_counter = 0

                        if img_flip:
                            gv.screen.blit(gv.escher3_img, (0, 0))
                        else:
                            gv.screen.blit(gv.escher4_img, (0, 0))

                        nca_img = pygame.image.load(gv.resource_path(f"img/nca_room_movie/{img_num}.jpg")).convert_alpha()
                        nca_img = pygame.transform.scale(nca_img, (163, 163))
                        gv.screen.blit(nca_img, (116, 310))
                           
                        pygame.draw.rect(surface=gv.screen, color=(125, 55, 200),
                                         rect=pygame.Rect(nca_rm.control.x * 5 + 116, nca_rm.control.y * 5 + 310, 25, 25), width=1)

                        nca_rm.temp_dialogue()

                        pygame.transform.scale(gv.screen, (gv.DISPLAY_WIDTH, gv.DISPLAY_HEIGHT), gv.display_surface); pygame.display.flip()
                        if gv.save_screenshots and gv.master_save_screenshots:
                            screen_shot_num = screen_shot_num + 1
                            pygame.image.save(gv.screen, f"./screenshots/screenshot{screen_shot_num}.jpeg")
                            # pygame.image.save(gv.screen, f"./screenshots/screenshot{screen_shot_num}.png")
                        await asyncio.sleep(0)
                ## state ##
                elif gv.world_level == "computer_room":
                    # the import creates the class object; we should update that
                    img_flip = True
                    while gv.world_level == "computer_room":
                        for event in pygame.event.get():
                            # should put in the key_up events or turn moving left and right to false
                            if event.type == pygame.QUIT:
                                pygame.quit()
                            elif event.type == pygame.KEYDOWN:
                                if event.key == pygame.locals.K_SPACE:
                                    gv.world_level = "top"
                                    gv.door_sfx.play()
                                if event.key in cr.key_to_function:
                                    # dictionary returns a method (run on itself) which updates it's own 3d wireframe display
                                    cr.key_to_function[event.key](cr.proj_viewer)

                        if pygame.time.get_ticks() - cr.proj_viewer.last_time_check > gv.ANIMATION_INTERVAL:
                            cr.proj_viewer.last_time_check = pygame.time.get_ticks()
                            img_flip = not img_flip

                        # draw appropriate background
                        if img_flip:
                            if cr.proj_viewer.cube_match and cr.proj_viewer.tet_match:
                                gv.screen.blit(gv.escher_both_img, (0, 0))
                            elif cr.proj_viewer.cube_match:
                                gv.screen.blit(gv.escher_cube_img, (0, 0))
                            elif cr.proj_viewer.tet_match:
                                gv.screen.blit(gv.escher_tet_img, (0, 0))
                            else:
                                gv.screen.blit(gv.escher_img, (0, 0))
                        else:
                            if cr.proj_viewer.cube_match and cr.proj_viewer.tet_match:
                                gv.screen.blit(gv.escher2_both_img, (0, 0))
                            elif cr.proj_viewer.cube_match:
                                gv.screen.blit(gv.escher2_cube_img, (0, 0))
                            elif cr.proj_viewer.tet_match:
                                gv.screen.blit(gv.escher2_tet_img, (0, 0))
                            else:
                                gv.screen.blit(gv.escher2_img, (0, 0))

                        # draw wireframes
                        cr.proj_viewer.display()
                        # the last thing we lay on top before we
                        if not cr.proj_viewer.intro_complete:
                            if gv.intro_fade.fade():
                                cr.proj_viewer.intro_complete = True
                        pygame.transform.scale(gv.screen, (gv.DISPLAY_WIDTH, gv.DISPLAY_HEIGHT), gv.display_surface); pygame.display.flip()
                        if gv.save_screenshots and gv.master_save_screenshots:
                            screen_shot_num = screen_shot_num + 1
                            pygame.image.save(gv.screen, f"./screenshots/screenshot{screen_shot_num}.jpeg")
                            # pygame.image.save(gv.screen, f"./screenshots/screenshot{screen_shot_num}.png")
                        await asyncio.sleep(0)
                ## state ##
                elif gv.world_level == "soccer_room":
                    s_room = sr.init_ball_char()
                    bg_counter = 0
                    prev_b_soccer = False

                    while gv.world_level == "soccer_room":
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()

                        # RCade input for soccer room
                        soccer_inputs = _get_input().to_py()
                        s_room.mov_left = soccer_inputs["p1"]["left"]
                        s_room.mov_right = soccer_inputs["p1"]["right"]

                        # B button exits room
                        curr_b_soccer = soccer_inputs["p1"]["b"]
                        if curr_b_soccer and not prev_b_soccer:
                            gv.world_level = "top"
                            pygame.mixer.music.stop()
                            f.reset_music()
                        prev_b_soccer = curr_b_soccer

                        bg_counter += 1
                        bg_idx = int((bg_counter / 20)) % 3
                        gv.screen.blit(gv.campfire_bg[bg_idx], [0, 0])

                        s_room.notkhatchig.update_animation()
                        s_room.notkhatchig.move(s_room.mov_left, s_room.mov_right)
                        s_room.notkhatchig.draw()

                        s_room.soccer_ball.move(s_room.notkhatchig)
                        s_room.soccer_ball.draw()
                        gv.screen.blit(gv.pine1_img, (0, 500))
                        gv.screen.blit(gv.letter_box_img, (0, 0))

                        if not s_room.intro_complete:
                            if gv.intro_fade.fade():
                                s_room.intro_complete = True

                        pygame.transform.scale(gv.screen, (gv.DISPLAY_WIDTH, gv.DISPLAY_HEIGHT), gv.display_surface); pygame.display.flip()
                        if gv.save_screenshots and gv.master_save_screenshots:
                            screen_shot_num = screen_shot_num + 1
                            pygame.image.save(gv.screen, f"./screenshots/screenshot{screen_shot_num}.jpeg")
                            # pygame.image.save(gv.screen, f"./screenshots/screenshot{screen_shot_num}.png")
                        await asyncio.sleep(0)
                ## state ##
                elif gv.world_level == "environment_control_room":
                    ec_room = ecr.ControlEnvRoom()
                    img_flip = True

                    wallpaper_temp = pygame.Surface((750, 750), pygame.SRCALPHA)

                    for i in range(15):
                        for j in range(15):
                            if j % 4 <= 2:
                                wallpaper_temp.blit(gv.img_list[random.choice([30, 190])], (i * gv.TILE_SIZE, j * gv.TILE_SIZE))
                            else:
                                wallpaper_temp.blit(gv.img_list[random.choice([29, 191])], (i * gv.TILE_SIZE, j * gv.TILE_SIZE))

                    wallpaper = wallpaper_temp.subsurface(0, 0, 750, 750)  # .copy()
                    wallpaper_on_screen_temp = wallpaper.subsurface(0, 0, 750, int(750 * (9 / 15)))
                    wallpaper_on_screen = pygame.transform.scale(wallpaper_on_screen_temp, (255, 170))

                    while gv.world_level == "environment_control_room":
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                            elif event.type == pygame.KEYDOWN:
                                if event.key == pygame.locals.K_SPACE:
                                    gv.world_level = "top"
                                    gv.door_sfx.play()
                                if event.key in ecr.key_to_function:
                                    # dictionary returns a method (run on itself) which updates it's own 3d wireframe display
                                    ecr.key_to_function[event.key](ec_room)

                        # 145 is the height of the y coordinate of the bottom edge of the letter box, which is like the top row of the image
                        if ec_room.pos_wallpaper == [0, 145] and ec_room.first_sfx:
                            ec_room.first_sfx = False
                            gv.success_sfx.play()
                            gv.to_do["match wallpaper"] = True
                            gv.world_level = "movie"
                            gv.movie_idx = 13

                        # four offset images for tiling effect
                        gv.screen.blit(wallpaper, ec_room.pos_wallpaper)
                        gv.screen.blit(wallpaper, [ec_room.pos_wallpaper[0] - gv.SCREEN_WIDTH, ec_room.pos_wallpaper[1]])
                        gv.screen.blit(wallpaper, [ec_room.pos_wallpaper[0], ec_room.pos_wallpaper[1] - gv.SCREEN_HEIGHT])
                        gv.screen.blit(wallpaper, [ec_room.pos_wallpaper[0] - gv.SCREEN_WIDTH, ec_room.pos_wallpaper[1] - gv.SCREEN_HEIGHT])

                        if pygame.time.get_ticks() - ec_room.last_time_check > gv.ANIMATION_INTERVAL:
                            ec_room.last_time_check = pygame.time.get_ticks()
                            img_flip = not img_flip

                        if img_flip:
                            gv.screen.blit(gv.escher17_img, (0, 0))
                        else:
                            gv.screen.blit(gv.escher18_img, (0, 0))

                        gv.screen.blit(wallpaper_on_screen, (70, 303))

                        if not ec_room.intro_complete:
                            if gv.intro_fade.fade():
                                ec_room.intro_complete = True
                        pygame.transform.scale(gv.screen, (gv.DISPLAY_WIDTH, gv.DISPLAY_HEIGHT), gv.display_surface); pygame.display.flip()
                        if gv.save_screenshots and gv.master_save_screenshots:
                            screen_shot_num = screen_shot_num + 1
                            pygame.image.save(gv.screen, f"./screenshots/screenshot{screen_shot_num}.jpeg")
                            # pygame.image.save(gv.screen, f"./screenshots/screenshot{screen_shot_num}.png")
                        await asyncio.sleep(0)
                ## state ##
                elif gv.world_level == "cat_bus_room":
                    cb_room = cbr.CatBusRoom()
                    if gv.holding_object == 105:
                        cb_room.success = True

                    img_flip = True

                    while gv.world_level == "cat_bus_room":
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                            elif event.type == pygame.KEYDOWN:
                                if event.key == pygame.locals.K_SPACE:
                                    gv.world_level = "top"
                                    gv.door_sfx.play()

                        if pygame.time.get_ticks() - cb_room.last_time_check_book > gv.DIALOGUE_INTERVAL / 2:
                            cb_room.book_down = not cb_room.book_down
                            cb_room.last_time_check_book = pygame.time.get_ticks()

                        if pygame.time.get_ticks() - cb_room.last_time_check > gv.ANIMATION_INTERVAL:
                            cb_room.last_time_check = pygame.time.get_ticks()
                            img_flip = not img_flip

                        if img_flip:
                            gv.screen.blit(gv.cat_bus_img, (0, 0))
                        else:
                            gv.screen.blit(gv.cat_bus2_img, (0, 0))

                        # already delivered cat
                        if gv.to_do["deliver cat"]:
                            if cb_room.book_down:
                                gv.screen.blit(gv.large_cat_img, (60, 175))
                            else:
                                gv.screen.blit(gv.large_cat_img, (60, 170))
                        else:
                            if cb_room.success:
                                cb_room.give_book()  # draws one of three steps (lowered hands, show book, play movie)

                                if gv.dialogue_counter < len(gv.dialogue["hippie_book_success"]):
                                    cb_room.dialogue()
                            else:
                                if cb_room.book_down:
                                    gv.screen.blit(gv.book_hands_img, (80, 360))
                                else:
                                    gv.screen.blit(gv.book_hands_img, (80, 340))

                                cb_room.dialogue()

                            # if self.book_counter < 3500:
                            # if gv.dialogue_counter < len(gv.dialogue["hippie_book_success"]):
                            #     cb_room.dialogue()

                        if not cb_room.intro_complete:
                            if gv.intro_fade.fade():
                                cb_room.intro_complete = True

                        pygame.transform.scale(gv.screen, (gv.DISPLAY_WIDTH, gv.DISPLAY_HEIGHT), gv.display_surface); pygame.display.flip()
                        if gv.save_screenshots and gv.master_save_screenshots:
                            screen_shot_num = screen_shot_num + 1
                            pygame.image.save(gv.screen, f"./screenshots/screenshot{screen_shot_num}.jpeg")
                            # pygame.image.save(gv.screen, f"./screenshots/screenshot{screen_shot_num}.png")
                        await asyncio.sleep(0)
                ## state ##
                elif gv.world_level == "ascii_room":
                    a_room = ar.Ascii_room()
                    img_flip = True

                    while gv.world_level == "ascii_room":
                        for event in pygame.event.get():
                            # should put in the key_up events or turn moving left and right to false
                            if event.type == pygame.QUIT:
                                pygame.quit()
                            elif event.type == pygame.KEYDOWN:
                                if event.key == pygame.locals.K_SPACE:
                                    gv.world_level = "top"
                                    gv.door_sfx.play()
                                if event.key in a_room.key_to_function:
                                    a_room.key_to_function[event.key](a_room)

                        gv.screen.blit(gv.track_img, [(a_room.stars_counter % gv.track_img.get_width()) - gv.track_img.get_width(), 155])
                        gv.screen.blit(gv.track_img, [a_room.stars_counter % gv.track_img.get_width(), 155])

                        if img_flip:
                            gv.screen.blit(gv.escher19_img, (0, 0))
                            img_flip = False
                        else:
                            gv.screen.blit(gv.escher20_img, (0, 0))
                            img_flip = True

                        # pygame.draw.rect(gv.screen, (255, 255, 255), pygame.Rect(70, 201, 255, 306))
                        if abs(a_room.stars_counter) > 670 and a_room.first_sfx:
                            a_room.first_sfx = False
                            gv.success_sfx.play()
                            gv.to_do["run ascii"] = True
                            gv.world_level = "movie"
                            gv.movie_idx = 12

                        gv.screen.blit(a_room.img_list[a_room.control], (136, 198))
                        gv.screen.blit(gv.letter_box_img, (0, 0))

                        if not a_room.intro_complete:
                            if gv.intro_fade.fade():
                                a_room.intro_complete = True
                        pygame.transform.scale(gv.screen, (gv.DISPLAY_WIDTH, gv.DISPLAY_HEIGHT), gv.display_surface); pygame.display.flip()
                        if gv.save_screenshots and gv.master_save_screenshots:
                            screen_shot_num = screen_shot_num + 1
                            pygame.image.save(gv.screen, f"./screenshots/screenshot{screen_shot_num}.jpeg")
                            # pygame.image.save(gv.screen, f"./screenshots/screenshot{screen_shot_num}.png")
                        await asyncio.sleep(0)
                ## state ##
                elif gv.world_level == "briefcase_room":
                    b_room = br.BriefcaseRoom()
                    img_flip = True

                    while gv.world_level == "briefcase_room":
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                            elif event.type == pygame.KEYDOWN:
                                if event.key == pygame.locals.K_SPACE:
                                    gv.world_level = "top"
                                    gv.door_sfx.play()
                                if event.key in b_room.key_to_function:
                                    # dictionary returns a method (run on itself)
                                    b_room.key_to_function[event.key](b_room)

                        if b_room.game_loop_counter == 100:
                            b_room.open_try = False
                            b_room.first_sfx = True
                        elif pygame.time.get_ticks() - b_room.last_time_check > gv.DIALOGUE_INTERVAL / 2:
                            b_room.game_loop_counter += 1

                        if img_flip:
                            if b_room.open_try:
                                if b_room.digits == b_room.solution:
                                    if b_room.first_sfx:
                                        if gv.holding_object is not None:
                                            if gv.holding_object == 186:
                                                gv.in_briefcase["printout"] = True
                                            elif gv.holding_object == 123:
                                                gv.in_briefcase["shirt"] = True
                                            elif gv.holding_object == 99:
                                                gv.in_briefcase["book"] = True

                                        gv.briefcase_open_sfx.play()
                                        gv.success_sfx.play()
                                        gv.to_do["get briefcase"] = True
                                        gv.holding_object = 98
                                        b_room.first_sfx = False

                                        gv.world_level = "movie"
                                        gv.movie_idx = 9
                                    gv.screen.blit(gv.escher13_img, (0, 0))
                                else:
                                    if b_room.first_sfx:
                                        gv.briefcase_wrong_sfx.play()
                                        b_room.first_sfx = False
                                    gv.screen.blit(gv.escher11_img, (0, 0))
                            else:
                                gv.screen.blit(gv.escher9_img, (0, 0))
                            img_flip = False
                        else:
                            if b_room.open_try:
                                if b_room.digits == b_room.solution:
                                    if b_room.first_sfx:
                                        gv.briefcase_open_sfx.play()
                                        gv.success_sfx.play()
                                        gv.to_do["get briefcase"] = True
                                        gv.holding_object = 98
                                        b_room.first_sfx = False

                                        gv.world_level = "movie"
                                        gv.movie_idx = 9
                                    gv.screen.blit(gv.escher14_img, (0, 0))
                                else:
                                    if b_room.first_sfx:
                                        gv.briefcase_wrong_sfx.play()
                                        b_room.first_sfx = False
                                    gv.screen.blit(gv.escher12_img, (0, 0))
                            else:
                                gv.screen.blit(gv.escher10_img, (0, 0))
                            img_flip = True

                        b_room.digits_text()

                        if not b_room.intro_complete:
                            if gv.intro_fade.fade():
                                b_room.intro_complete = True
                        pygame.transform.scale(gv.screen, (gv.DISPLAY_WIDTH, gv.DISPLAY_HEIGHT), gv.display_surface); pygame.display.flip()
                        if gv.save_screenshots and gv.master_save_screenshots:
                            screen_shot_num = screen_shot_num + 1
                            pygame.image.save(gv.screen, f"./screenshots/screenshot{screen_shot_num}.jpeg")
                            # pygame.image.save(gv.screen, f"./screenshots/screenshot{screen_shot_num}.png")
                        await asyncio.sleep(0)
                ## state ##
                elif gv.world_level == "end_room":
                    e_room = er.EndRoom()
                    last_counter = 0

                    if sum([1 if val else 0 for val in gv.to_do.values()]) > 6 and gv.to_do["explore feedback"] and (
                            gv.in_briefcase["book"] and gv.in_briefcase["shirt"] and gv.in_briefcase["printout"]) and (
                            gv.holding_object == 98):
                        e_room.success = True

                    while gv.world_level == "end_room":
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                            elif event.type == pygame.KEYDOWN:
                                if event.key == pygame.locals.K_SPACE:
                                    gv.world_level = "top"
                                    gv.first_time = False  # turned off after we gave full dialogue the first time in the room

                        if e_room.success and gv.dialogue_counter == 0:
                            pygame.mixer.music.unload()
                            pygame.mixer.music.load(gv.resource_path("audio/ending_music.ogg"))
                            pygame.mixer.music.set_volume(0.08)
                            pygame.mixer.music.play(-1, 0.0, 1000)

                        if e_room.success and gv.dialogue_counter >= 3:
                            gv.world_level = "end_room_success"

                        gv.screen.blit(gv.end_bg_img, (0, 0))

                        if last_counter == gv.dialogue_counter:
                            gv.screen.blit(gv.end_band2_img, (200, 270))
                        elif pygame.time.get_ticks() - gv.last_time_check_dialogue > gv.DIALOGUE_INTERVAL / 2:
                            last_counter += 1
                            gv.screen.blit(gv.end_band_img, (200, 270))
                        else:
                            gv.screen.blit(gv.end_band_img, (200, 270))

                        gv.screen.blit(gv.letter_box_img, (0, 0))

                        e_room.dialogue()

                        # if not e_room.intro_complete:
                        #     if gv.intro_fade.fade():
                        #         e_room.intro_complete = True
                        #
                        # pygame.transform.scale(gv.screen, (gv.DISPLAY_WIDTH, gv.DISPLAY_HEIGHT), gv.display_surface); pygame.display.flip()

                        if not e_room.intro_complete:
                            if gv.intro_fade.fade():
                                e_room.intro_complete = True
                        pygame.transform.scale(gv.screen, (gv.DISPLAY_WIDTH, gv.DISPLAY_HEIGHT), gv.display_surface); pygame.display.flip()
                        if gv.save_screenshots and gv.master_save_screenshots:
                            screen_shot_num = screen_shot_num + 1
                            pygame.image.save(gv.screen, f"./screenshots/screenshot{screen_shot_num}.jpeg")
                            # pygame.image.save(gv.screen, f"./screenshots/screenshot{screen_shot_num}.png")
                        await asyncio.sleep(0)
                ## state ##
                elif gv.world_level == "particle_affinity_room":
                    p_room = pr.create()
                    img_flip = True

                    while gv.world_level == "particle_affinity_room":
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                            elif event.type == pygame.KEYDOWN:
                                if event.key == pygame.locals.K_SPACE:
                                    gv.world_level = "top"
                                    gv.door_sfx.play()
                                elif event.key == pygame.K_p:
                                    p_room.print(gv.surf)
                                elif event.key == pygame.K_RETURN:
                                    gv.switch_sfx.play()
                                    p_room.reset = True

                        p_room.step()

                        sf = pygame.Surface((p_room.length, p_room.length))

                        for y, row in enumerate(p_room.type_grid):
                            for x, color in enumerate(row):
                                sf.set_at((x, y), p_room.colors[color])

                        gv.surf = pygame.transform.scale(sf, (255, 170))

                        p_room.stars_counter += 0.1
                        gv.screen.blit(gv.stars_img, [(p_room.stars_counter % gv.stars_img.get_width()) - gv.stars_img.get_width(), 155])
                        gv.screen.blit(gv.stars_img, [p_room.stars_counter % gv.stars_img.get_width(), 155])

                        if pygame.time.get_ticks() - p_room.last_time_check > gv.ANIMATION_INTERVAL:
                            p_room.last_time_check = pygame.time.get_ticks()
                            img_flip = not img_flip

                        if img_flip:
                            gv.screen.blit(gv.escher7_img, (0, 0))
                        else:
                            gv.screen.blit(gv.escher8_img, (0, 0))

                        gv.screen.blit(gv.surf, (70, 303))

                        if p_room.printout:
                            p_room.counter += 1
                            if p_room.counter % 10 == 0 and p_room.counter <= 10 * 64:
                                gv.printer_sfx.play()
                            if p_room.counter >= 10 * 64 and p_room.first_sfx:
                                gv.success_sfx.play()
                                gv.to_do["print printout"] = True
                                p_room.first_sfx = False
                                if gv.holding_object == 98:  # briefcase
                                    gv.in_briefcase["printout"] = True
                                    gv.briefcase_open_sfx.play()
                                elif gv.holding_object == 99:  # book
                                    gv.holding_object = 186
                                    for tile in gv.decoration_group:
                                        if tile.type == "grass":
                                            new_decoration = d.Decoration(gv.img_list[67], tile.rect.x, tile.rect.y, collidable=True,
                                                                          type="book")
                                            tile.kill()
                                            gv.decoration_group.add(new_decoration)
                                            break
                                else:
                                    gv.holding_object = 186

                                gv.world_level = "movie"
                                gv.movie_idx = 8

                            gv.screen.blit(gv.paper_img, (530, 445 - min(p_room.counter // 10, 64)))
                            gv.screen.blit(p_room.printout, (540, 450 - min(p_room.counter // 10, 64)))
                            gv.screen.blit(gv.printer_img, (490, 440))
                        else:
                            gv.screen.blit(gv.printer_img, (490, 440))

                        gv.screen.blit(gv.letter_box_img, (0, 0))

                        if p_room.reset:
                            params = {"length": random.randint(20, 40),
                                      "num_types": random.randint(3, 15),
                                      "density": random.choice([i * 0.05 for i in range(3, 10)]),
                                      "radius": random.choice([1, 2]),
                                      "pos": [0, 0],
                                      "best_idx": [0, 0],
                                      # "intro_complete": False,
                                      "printout": None,
                                      "first_sfx": True,
                                      "reset": False}

                            params_dict = pr.dict_creator(params)
                            p_room.__init__(params_dict)

                        pygame.transform.scale(gv.screen, (gv.DISPLAY_WIDTH, gv.DISPLAY_HEIGHT), gv.display_surface); pygame.display.flip()
                        if gv.save_screenshots and gv.master_save_screenshots:
                            screen_shot_num = screen_shot_num + 1
                            pygame.image.save(gv.screen, f"./screenshots/screenshot{screen_shot_num}.jpeg")
                            # pygame.image.save(gv.screen, f"./screenshots/screenshot{screen_shot_num}.png")
                        await asyncio.sleep(0)
                ## state ##
                elif gv.world_level == "end_room_success":
                    e_room = er.EndRoom()

                    sorted_file_list = sorted(os.listdir(gv.resource_path(f"img/movie_png_seq7")))
                    for file in sorted_file_list:
                        if file.endswith('.jpg'):
                            gv.screen.blit(pygame.image.load(gv.resource_path(f"img/movie_png_seq7/{file}")).convert_alpha(), (0, 0))
                            pygame.transform.scale(gv.screen, (gv.DISPLAY_WIDTH, gv.DISPLAY_HEIGHT), gv.display_surface); pygame.display.flip()
                            if gv.save_screenshots and gv.master_save_screenshots:
                                screen_shot_num = screen_shot_num + 1
                                pygame.image.save(gv.screen, f"./screenshots/screenshot{screen_shot_num}.jpeg")
                                # pygame.image.save(gv.screen, f"./screenshots/screenshot{screen_shot_num}.png")
                            await asyncio.sleep(0)

                    while gv.world_level == "end_room_success":
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                                pygame.quit()
                            # elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                            #     webbrowser.open_new_tab("https://vimeo.com/ondemand/digitalphysics")

                        gv.screen.blit(e_room.success_text1, (120, 240))
                        gv.screen.blit(e_room.success_text2, (120, 270))
                        gv.screen.blit(e_room.success_text3, (120, 310))
                        gv.screen.blit(e_room.success_text4, (120, 340))
                        gv.screen.blit(e_room.success_text5, (120, 370))
                        gv.screen.blit(e_room.success_text6, (120, 410))
                        pygame.transform.scale(gv.screen, (gv.DISPLAY_WIDTH, gv.DISPLAY_HEIGHT), gv.display_surface); pygame.display.flip()
                        if gv.save_screenshots and gv.master_save_screenshots:
                            screen_shot_num = screen_shot_num + 1
                            pygame.image.save(gv.screen, f"./screenshots/screenshot{screen_shot_num}.jpeg")
                            # pygame.image.save(gv.screen, f"./screenshots/screenshot{screen_shot_num}.png")
                        await asyncio.sleep(0)
                ## state ##
                # elif gv.world_level == "transition":
                #     for pic_idx in range(gv.TRANSITION_FRAMES):
                #         # transition animations are different after the first loop of the levels
                #         # we won't see menu on computer 2nd time
                #         if gv.level == 0 and gv.first_time is False:
                #             s_img = pygame.image.load(gv.resource_path(f"img/transition/level_2/{pic_idx}.png")).convert_alpha()
                #         else:
                #             s_img = pygame.image.load(gv.resource_path(f"img/transition/level_{gv.level-1}/{pic_idx}.png")).convert_alpha()
                #         gv.screen.blit(s_img, (0, 0))
                #         pygame.transform.scale(gv.screen, (gv.DISPLAY_WIDTH, gv.DISPLAY_HEIGHT), gv.display_surface); pygame.display.flip()
                #         if gv.save_screenshots and gv.master_save_screenshots:
                #             screen_shot_num = screen_shot_num + 1
                #             pygame.image.save(gv.screen, f"./screenshots/screenshot{screen_shot_num}.jpeg")
                #             # pygame.image.save(gv.screen, f"./screenshots/screenshot{screen_shot_num}.png")
                #         await asyncio.sleep(0)

                #     gv.world_level = "top"
                ## state ##
                elif gv.world_level == "transition":
                    # fetch transition frames on demand if not yet in FS
                    from js import fetchFileIntoFS
                    level_key = 2 if (gv.level == 0 and gv.first_time is False) else gv.level - 1
                    for pic_idx in range(gv.TRANSITION_FRAMES):
                        path = f"img/transition/level_{level_key}/{pic_idx}.png"
                        if not os.path.exists(path):
                            await fetchFileIntoFS(path)

                    for pic_idx in range(gv.TRANSITION_FRAMES):
                        if gv.level == 0 and gv.first_time is False:
                            s_img = pygame.image.load(gv.resource_path(f"img/transition/level_2/{pic_idx}.png")).convert_alpha()
                        else:
                            s_img = pygame.image.load(gv.resource_path(f"img/transition/level_{gv.level-1}/{pic_idx}.png")).convert_alpha()
                        gv.screen.blit(s_img, (0, 0))
                        pygame.transform.scale(gv.screen, (gv.DISPLAY_WIDTH, gv.DISPLAY_HEIGHT), gv.display_surface); pygame.display.flip()
                        await asyncio.sleep(0)

                    gv.world_level = "top"
            else:
                f.draw_background()
                gv.world_instance.draw()

                gv.decoration_group.update()
                gv.decoration_group.draw(gv.screen)

                gv.exit_group.update()
                gv.exit_group.draw(gv.screen)

                gv.real_group.update()
                gv.real_group.draw(gv.screen)

                gv.blob_group.update()
                gv.blob_group.draw(gv.screen)

                if gv.mirror:
                    gv.screen.blit(gv.mirror, (gv.mirror_loc[0] + gv.screen_scroll, gv.mirror_loc[1]))
                    gv.screen.blit(gv.img_list[134], (gv.mirror_loc[0] + gv.screen_scroll, gv.mirror_loc[1]))

                # assume it is False at start of game loop; we'll see if it gets turned on
                gv.dialogue_counter_flag = False
                # reset each step and see if it gets turned off in khatchig.move() or hippie.move()
                gv.health_counter_on = True

                gv.khatchig.update()
                gv.khatchig.draw()

                # future update: create NPC groups instead of individual class instance updates
                if gv.hippie is not None:
                    gv.hippie.auto()
                    gv.hippie.update()
                    gv.hippie.draw()

                if gv.notkhatchig is not None:
                    gv.notkhatchig.autonot()
                    gv.notkhatchig.update()
                    gv.notkhatchig.draw()

                if gv.ufo is not None:
                    gv.ufo.update()
                    gv.ufo.draw()

                if gv.cat is not None:
                    gv.cat.update()
                    if gv.cat is not None:
                        gv.cat.draw()

                gv.water_group.update()
                gv.water_group.draw(gv.screen)

                if gv.khatchig.alive:
                    # this line of code prevents the player from jumping after running off a cliff
                    # this would not be a sufficient code design if we had elevators/escalators in the game...
                    # in that situation, there would still be a platform to push off of despite the player "falling" based on y_velocity
                    if gv.khatchig.y_velocity > 1:
                        gv.khatchig.in_air = True

                    f.update_khatchig_action_animation()

                    # calculate movement and see if collision happened w/ exit group
                    gv.screen_scroll, level_complete = gv.khatchig.move(gv.moving_left, gv.moving_right)

                    # now that we've given an opportunity to set dialogue_flag to True, run line below
                    f.increment_or_reset_dialogue()

                    # every 350 game ticks you lose a heart (if you aren't talking to anybody/health counter on)
                    # this is done here instead of in khatchig class...
                    # because hippie.move() and khatchig.move() both could turn the health_counter_on = False
                    if gv.health_counter_on:
                        gv.khatchig.health_counter += 1

                        if gv.khatchig.health_counter % 350 == 349:
                            gv.khatchig.health -= 1
                            gv.health_sfx.play()

                    if gv.level == 2:
                        gv.bg_scroll -= gv.screen_scroll  # aggregate variable is updated by delta variable
                    else:
                        gv.bg_scroll -= gv.screen_scroll
                        # added for hard stop at specific point in level (for level-transition purposes)
                        gv.bg_scroll = min(gv.bg_scroll, gv.COLUMNS * gv.TILE_SIZE - gv.SCREEN_WIDTH)

                        # checkpoint
                        if gv.level == 0 and gv.bg_scroll >= 3500:
                            gv.checkpoint_flag = True
                        elif gv.level == 1 and gv.bg_scroll >= 3000:
                            gv.checkpoint_flag = True

                    if gv.level == 2:
                        f.update_cellular_automata()

                    f.draw_health_lives()
                    f.draw_progress()

                    if level_complete:
                        f.level_complete_process()
                else:
                    gv.screen_scroll = 0  # stop scrolling on death
                    # each method call increments the counter and returns False, until the counter reaches threshold and returns True
                    if gv.death_fade.fade():
                        f.post_death_fade_process(inputs)

            # below: things to do in game loop regardless of whether gv.khatchig is alive or dead:

            # the obstacles that flip do so at a rate five times as slow as the character animation update
            if pygame.time.get_ticks() - gv.last_time_check > gv.ANIMATION_INTERVAL * 5:
                f.flip_images()

            if gv.start_transition:
                f.transition_process()

            # handle quit events only — all game input is via RCade polling below
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gv.running = False

            # RCade input polling
            inputs = _get_input().to_py()
            curr_a = inputs["p1"]["a"]
            curr_b = inputs["p1"]["b"]
            a_pressed = curr_a and not prev_a  # True only on the frame A is first pressed
            b_pressed = curr_b and not prev_b  # True only on the frame B is first pressed

            # left / right: direct hold (replaces K_LEFT / K_RIGHT)
            gv.moving_left = inputs["p1"]["left"]
            gv.moving_right = inputs["p1"]["right"]

            if gv.khatchig.alive:
                # A button: jump and enter rooms (replaces K_UP)
                if a_pressed:
                    gv.khatchig.jump = True

                # B button: pick up / drop / crouch (replaces K_DOWN)
                if b_pressed:
                    if gv.holding_object is None:
                        gv.khatchig.pick = True
                        gv.khatchig.update_action(4)
                    elif gv.pick_flag:  # second B press — drop held object
                        for tile in gv.decoration_group:
                            if tile.collidable and tile.rect.collidepoint(gv.khatchig.rect.midbottom[0], gv.khatchig.rect.midbottom[1]-1):
                                if tile.type in ["grass", "mushroom"]:
                                    if gv.holding_object == 77:  # camera
                                        # get a snapshot of what the camera sees when you put it down to put on the monitor in the monitor room
                                        # the logic is a little messy to avoid range errors on level 3
                                        # and errors at the end of a level if you put cam down on the right side of screen
                                        if tile.rect.x + 100 + 255//2 <= gv.SCREEN_WIDTH and tile.rect.y - 50 + 170//2 <= gv.SCREEN_HEIGHT:
                                            sub = gv.screen.subsurface(tile.rect.x + 100, tile.rect.y - 50, 255//2, 170//2)
                                        else:
                                            sub = gv.screen.subsurface(tile.rect.x - 100, tile.rect.y - 50, 255 // 2, 170 // 2)

                                        gv.tile_on_monitor = pygame.transform.scale(sub, (255, 170))
                                        new_decoration = d.Decoration(gv.img_list[gv.holding_object+2], tile.rect.x, tile.rect.y,
                                                                      collidable=True, type="camera")
                                    elif gv.holding_object == 78:  # hot dog in hand tile
                                        new_decoration = d.Decoration(gv.img_list[80], tile.rect.x, tile.rect.y,
                                                                      collidable=True, type="hot_dog")
                                    elif gv.holding_object == 98:  # suitcase
                                        new_decoration = d.Decoration(gv.img_list[39], tile.rect.x, tile.rect.y,
                                                                      collidable=True, type="suitcase")
                                    elif gv.holding_object == 99:  # book
                                        new_decoration = d.Decoration(gv.img_list[67], tile.rect.x, tile.rect.y,
                                                                      collidable=True, type="book")
                                    elif gv.holding_object == 105:  # cat
                                        new_decoration = d.Decoration(gv.img_list[131], tile.rect.x, tile.rect.y,
                                                                      collidable=True, type="cat", flip_image=gv.img_list[130])
                                    elif gv.holding_object == 123:  # shirt
                                        new_decoration = d.Decoration(gv.img_list[68], tile.rect.x, tile.rect.y,
                                                                      collidable=True, type="shirt")
                                    elif gv.holding_object == 186:  # printout
                                        new_decoration = d.Decoration(gv.img_list[187], tile.rect.x, tile.rect.y,
                                                                      collidable=True, type="printout")

                                    tile.kill()
                                    gv.decoration_group.add(new_decoration)
                                    gv.holding_object = None
                                elif tile.type == "flip on hot dog drop":
                                    if gv.holding_object == 78:  # hot dog tile
                                        gv.success_sfx.play()
                                        gv.to_do["return hot dog"] = True
                                        new_decoration = d.Decoration(gv.img_list[114], tile.rect.x, tile.rect.y,
                                                                      collidable=False, type="hot_dog")
                                        tile.kill()
                                        gv.decoration_group.add(new_decoration)
                                        gv.holding_object = None

                                        gv.world_level = "movie"
                                        gv.movie_idx = 10
                    else:  # holding object, first B press
                        gv.khatchig.pick = True
                        gv.khatchig.update_action(4)
                        gv.pick_flag = True

                # B released: clear pick (replaces K_DOWN KEYUP)
                if not curr_b:
                    gv.khatchig.pick = False

            prev_a = curr_a
            prev_b = curr_b

            pygame.transform.scale(gv.screen, (gv.DISPLAY_WIDTH, gv.DISPLAY_HEIGHT), gv.display_surface); pygame.display.flip()
            if gv.save_screenshots and gv.master_save_screenshots:
                screen_shot_num = screen_shot_num + 1
                pygame.image.save(gv.screen, f"./screenshots/screenshot{screen_shot_num}.jpeg")
                # pygame.image.save(gv.screen, f"./screenshots/screenshot{screen_shot_num}.png")
                print("saving pics")
            gv.clock.tick(gv.FPS)
            await asyncio.sleep(0)


if __name__ == "__main__":
    app = Game()
    asyncio.run(app.run())
    pygame.quit()