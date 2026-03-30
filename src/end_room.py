import pygame
import global_vars as gv
import various_functions as f

pygame.init()


class EndRoom:
    def __init__(self) -> None:
        """this class is used to run a self-contained game loop for a 'room' in the game"""
        self.intro_complete = False
        # gv.last_time_check_dialogue = pygame.time.get_ticks()
        self.success = False
        self.success_font = pygame.font.Font(gv.resource_path("fonts/kongtext.ttf"), 16)
        self.success_text1 = self.success_font.render("Congratulations!", True, gv.WHITE)
        self.success_text2 = self.success_font.render("You Won a Free Movie Rental!", True, gv.WHITE)
        self.success_text3 = self.success_font.render("Codes:", True, gv.WHITE)
        self.success_text4 = self.success_font.render("strange_loop      (Free RENT)", True, gv.WHITE)
        self.success_text5 = self.success_font.render("33                 (-33% BUY)", True, gv.WHITE)
        self.success_text6 = self.success_font.render("Press SPACEBAR to watch movie.", True, gv.WHITE)
        # print("end room, in briefcase", gv.in_briefcase)

    def dialogue(self) -> None:
        """loops (over many calls) dialogue and draws on screen"""
        if self.success:
            temp_dialogue = gv.dialogue["band_member_success"][gv.dialogue_counter][:]
        elif gv.first_time:
            # used to determine what should be on the computer screen on first level after transition
            temp_dialogue = gv.dialogue["band_member"][gv.dialogue_counter % len(gv.dialogue["band_member"])][:]
        elif sum([1 if val else 0 for val in gv.to_do.values()]) > 6 and (
                    gv.in_briefcase["book"] and gv.in_briefcase["shirt"] and gv.in_briefcase["printout"]) and (
                    gv.holding_object == 98):
            temp_dialogue = gv.dialogue["band_member_feedback"][gv.dialogue_counter % len(gv.dialogue["band_member_feedback"])][:]
        elif gv.to_do["explore feedback"] and (gv.in_briefcase["book"] and gv.in_briefcase["shirt"] and gv.in_briefcase["printout"]) and (
                    gv.holding_object == 98):
            temp_dialogue = gv.dialogue["band_member_low_count"][gv.dialogue_counter % len(gv.dialogue["band_member_low_count"])][:]
        elif (gv.in_briefcase["book"] and gv.in_briefcase["shirt"] and gv.in_briefcase["printout"]) and gv.holding_object == 98:
            temp_dialogue = gv.dialogue["band_member_feedback"][gv.dialogue_counter % len(gv.dialogue["band_member_feedback"])][:]
        elif gv.holding_object == 98:
            temp_dialogue = gv.dialogue["band_member_briefcase"][gv.dialogue_counter % len(gv.dialogue["band_member_briefcase"])][:]
        elif gv.holding_object == 99:
            temp_dialogue = gv.dialogue["band_member_book"][gv.dialogue_counter % len(gv.dialogue["band_member_book"])][:]
        elif gv.holding_object == 123:
            temp_dialogue = gv.dialogue["band_member_shirt"][gv.dialogue_counter % len(gv.dialogue["band_member_shirt"])][:]
        elif gv.holding_object == 186:
            temp_dialogue = gv.dialogue["band_member_printout"][gv.dialogue_counter % len(gv.dialogue["band_member_printout"])][:]
        elif gv.holding_object in [77, 78, 105]:
            temp_dialogue = gv.dialogue["band_member_other"][gv.dialogue_counter % len(gv.dialogue["band_member_other"])][:]
        elif gv.holding_object is None:
            temp_dialogue = gv.dialogue["band_member"][gv.dialogue_counter % len(gv.dialogue["band_member"])][:]

        f.draw_dialogue(temp_dialogue, 375, 250)
        if pygame.time.get_ticks() - gv.last_time_check_dialogue > gv.DIALOGUE_INTERVAL:
            gv.dialogue_counter_flag = True
            gv.dialogue_counter += 1  # update outside main game loop needed because we are in self-contained loop
            gv.speech_sfx.play()
            gv.last_time_check_dialogue = pygame.time.get_ticks()

    # def run(self) -> None:
    #     """ self-contained game loop"""
    #     last_counter = 0
    #
    #     if sum([1 if val else 0 for val in gv.to_do.values()]) > 6 and gv.to_do["explore feedback"] and (
    #             gv.in_briefcase["book"] and gv.in_briefcase["shirt"] and gv.in_briefcase["printout"]) and (
    #             gv.holding_object == 98):
    #         self.success = True
    #
    #     while gv.world_level == "end_room":
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 pygame.quit()
    #             elif event.type == pygame.KEYDOWN:
    #                 if event.key == pygame.locals.K_SPACE:
    #                     gv.world_level = "top"
    #
    #         if self.success and gv.dialogue_counter == 0:
    #             pygame.mixer.music.unload()
    #             pygame.mixer.music.load(gv.resource_path("audio/ending_music.mp3"))
    #             pygame.mixer.music.set_volume(0.1)
    #             pygame.mixer.music.play(-1, 0.0, 1000)
    #
    #         if self.success and gv.dialogue_counter >= 3:
    #             self.end_scene()
    #
    #         gv.screen.blit(gv.end_bg_img, (0, 0))
    #
    #         if last_counter == gv.dialogue_counter:
    #             gv.screen.blit(gv.end_band2_img, (200, 270))
    #         elif pygame.time.get_ticks() - gv.last_time_check_dialogue > gv.DIALOGUE_INTERVAL/2:
    #             last_counter += 1
    #             gv.screen.blit(gv.end_band_img, (200, 270))
    #         else:
    #             gv.screen.blit(gv.end_band_img, (200, 270))
    #
    #         gv.screen.blit(gv.letter_box_img, (0, 0))
    #
    #         self.dialogue()
    #
    #         if not self.intro_complete:
    #             if gv.intro_fade.fade():
    #                 self.intro_complete = True
    #
    #         pygame.display.update()
    #
    #         if not self.intro_complete:
    #             if gv.intro_fade.fade():
    #                 self.intro_complete = True
    #         pygame.display.update()

    # def end_scene(self) -> None:
    #     """we run this celebration scene when all the goals have been met"""
    #     movie.play(7)
    #
    #     while gv.world_level == "end_room":
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
    #                 pygame.quit()
    #             elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
    #                 webbrowser.open("https://vimeo.com/ondemand/digitalphysics")
    #
    #         gv.screen.blit(self.success_text, (120, 300))
    #         gv.screen.blit(self.success_text2, (120, 330))
    #         gv.screen.blit(self.success_text3, (120, 360))
    #         gv.screen.blit(self.success_text4, (120, 400))
    #         pygame.display.update()


# def create() -> None:
#     """creates an instance of the room and kicks it off"""
#     room = EndRoom()
#     room.run()
