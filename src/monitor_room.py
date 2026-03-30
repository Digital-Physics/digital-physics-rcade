import pygame
import global_vars as gv
# import movie
# import asyncio


class MonitorRoom:
    def __init__(self):
        self.monitor_font = pygame.font.Font(gv.resource_path("fonts/kongtext.ttf"), 6)
        self.monitor_text = self.monitor_font.render("<MONITOR>", True, gv.WHITE)
        self.last_time_check = pygame.time.get_ticks()
        self.intro_complete = True
        self.cam_angle = 0
        self.computer_center = [70 + 255//2, 303 + 170//2]
        self.next_frame = None
        self.counter = 0
        self.cam_zoom = 0
        self.key_to_function = {
            pygame.K_LEFT:   (lambda x: x.rotate(-2)),
            pygame.K_RIGHT:  (lambda x: x.rotate(2)),
            pygame.K_DOWN:   (lambda x: x.zoom(2)),
            pygame.K_UP:     (lambda x: x.zoom(-2))}
        self.cam_img_list = []

        for i in range(3):
            img = pygame.image.load(gv.resource_path(f'img/Background/cam{i}.png'))
            img = pygame.transform.scale(img, (100, 100))
            self.cam_img_list.append(img)

        self.cam_img_count = 0
        self.cam_img = self.cam_img_list[self.cam_img_count]

    def zoom(self, delta):
        self.cam_zoom = min(max(self.cam_zoom + delta, -40), 100)

    def rotate(self, delta):
        # self.cam_angle = min(max(self.cam_angle + delta, 0), 100)
        self.cam_angle += delta
        self.cam_img_count = (self.cam_img_count + 1) % 3
        self.cam_img = self.cam_img_list[self.cam_img_count]

    def get_rotated_subsurface(self, surface):
        w, h = surface.get_width(), surface.get_height()
        img2 = pygame.Surface((w * 2, h * 2), pygame.SRCALPHA)
        img2.blit(surface, (w - self.computer_center[0], h - self.computer_center[1]))
        rotated = pygame.transform.rotate(img2, self.cam_angle)
        sub = rotated.subsurface(rotated.get_rect().center[0] - 255//2 - self.cam_zoom,
                                 rotated.get_rect().center[1] - 170//2 - self.cam_zoom,
                                 255 + 2*self.cam_zoom, 170 + 2*self.cam_zoom)
        return sub

    # def run(self):
    #     """ self-contained loop in main game loop """
    #     if gv.holding_object == 77:
    #         gv.success_sfx.play()
    #         gv.to_do["explore feedback"] = True
    #         movie.play(5)  # need to update video to make it full screen
    #
    #     img_flip = True
    #
    #     while gv.world_level == "monitor_room":
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
    #         if pygame.time.get_ticks() - self.last_time_check > gv.ANIMATION_INTERVAL:
    #             self.last_time_check = pygame.time.get_ticks()
    #             img_flip = not img_flip
    #
    #         if img_flip:
    #             gv.screen.blit(gv.escher15_img, (0, 0))
    #         else:
    #             gv.screen.blit(gv.escher16_img, (0, 0))
    #
    #         if gv.holding_object == 77:
    #             self.counter += 1
    #
    #             if self.next_frame:
    #                 gv.screen.blit(self.next_frame, (70, 303))  # , special_flags=pygame.BLEND_RGBA_MULT)
    #             sub = gv.screen.copy()
    #             sub = self.get_rotated_subsurface(sub)
    #             gv.tile_on_monitor = pygame.transform.scale(sub, (255, 170))
    #             gv.screen.blit(gv.tile_on_monitor, (70, 303))  # , special_flags=pygame.BLEND_RGBA_MULT)
    #             gv.screen.blit(self.monitor_text, (80, 310))
    #             if self.counter % 10 == 0:
    #                 self.next_frame = gv.screen.subsurface(70, 303, 255, 170).copy()
    #                 self.next_frame = pygame.transform.scale(self.next_frame, (255, 170))
    #         else:
    #             gv.screen.blit(gv.tile_on_monitor, (70, 303))
    #             gv.screen.blit(self.monitor_text, (80, 310))
    #
    #         if not self.intro_complete:
    #             if gv.intro_fade.fade():
    #                 self.intro_complete = True
    #         pygame.display.update()


    # def create():
    #     room = MonitorRoom()
    #     # room.run()
