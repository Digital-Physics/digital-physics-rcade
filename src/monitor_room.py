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
        self.last_move_time = pygame.time.get_ticks()  # rate-limit d-pad movement
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