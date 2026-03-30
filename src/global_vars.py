# import pygame
# import world as w
# import csv
# import screen_fade
# import os
# # import sys
# import dialogue as dl
# # from js import fetch, BASE_URL
# from js import XMLHttpRequest, BASE_URL
# import asyncio


# # initialize global variables that can be referenced across .py files
# # this set of global variables is like the "state" of the game
# world_level = "top"
# movie_idx = None
# SCREEN_WIDTH = 750
# SCREEN_HEIGHT = SCREEN_WIDTH
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# moving_left = False
# moving_right = False
# pygame.display.set_caption("Digital Physics: Part 2 of 1")
# clock = pygame.time.Clock()
# FPS = 30
# GRAVITY = 1.15  # change in velocity in terms of y-pixels/step
# SCROLL_THRESH = 200
# ROWS = 15  # should make ROWS & COLUMNS level-specific at some point
# COLUMNS = 150
# TILE_SIZE = SCREEN_HEIGHT // ROWS
# TILE_TYPES = 201
# MAX_HEALTH = 7
# LEVELS = 3
# TRANSITION_FRAMES = 140
# screen_scroll = 0  # delta number for each step
# bg_scroll = 0  # aggregate, cumulative number over all steps
# level = 0
# menu_screen = True
# start_transition = False
# first_time = True  # helps with transitions
# first_ca_block_removal_sfx = True
# restart = False  # this variable also helps with transitions
# lives = 3
# apply_force = False
# ca_solution_rules = None
# ca_solution = None  # Cellular Automaton solution generated when the board is reset for level 2
# continued_CA = []
# last_time_check = pygame.time.get_ticks()  # for animation update interval measurement
# last_time_check_dialogue = pygame.time.get_ticks()
# BLACK = (0, 0, 0)
# WHITE = (255, 255, 255)
# running = True
# dialogue_counter = 0
# dialogue_counter_flag = False
# ANIMATION_INTERVAL = 75
# DIALOGUE_INTERVAL = 4000
# splash = False  # for sfx
# holding_object = None
# img_list = []
# nested_levels = []
# transition = []
# obstacle_list = []
# ufo_present = False
# floating = False
# khatchig = None
# ufo = None
# hippie = None
# real = None
# cat = None
# notkhatchig = None
# mirror = None
# mirror_loc = None
# world_instance = None
# khatchig_is_porting = False
# door_dict = {}
# surf = None
# pick_flag = False
# collision_on_off_counter = 0
# dx_pos_last_time = False
# room_lib = None
# to_do_list = ["get briefcase", "deliver cat", "connect points", "erase notkhatchig", "return hot dog",
#               "print printout", "juggle soccer ball", "explore feedback", "superposition", "match wallpaper", "run ascii"]
# to_do = {task: False for task in to_do_list}
# in_briefcase = {item: False for item in ["book", "shirt", "printout"]}
# checkpoint_flag = False
# health_counter_on = True
# play_music = True
# save_screenshots = False
# master_save_screenshots = False  # set to False to turn the tab key, which controls image saving, off
# dev_mode = 1  # 0 = dev mode w/ helpful cheats, 1 = user experience w/ no cheats, 2 = exe distribution; user's comp w/ different file path


# # def resource_path(relative_path):
# #     """ Get absolute path to resource, works for dev and for PyInstaller """
# #     if dev_mode != 2:
# #         base_path = os.path.abspath(".")
# #     else:
# #         # PyInstaller creates a temp folder and stores path in _MEIPASS
# #         base_path = sys._MEIPASS

# #     return os.path.join(base_path, relative_path)
# # def resource_path(relative_path):
# #     return "http://localhost:5173/" + relative_path
# # import os

# _cached_paths = set()

# def resource_path(relative_path):
#     return relative_path

# async def prefetch_sequence(seq_path):
#     """Call before iterating a movie_png_seq or transition directory."""
#     from js import fetchFileIntoFS
#     import os
#     files = []
#     # We can't os.listdir a URL, so fetch a known index or try sequential
#     # For now, fetch greedily until 404
#     i = 0
#     for fname in sorted(os.listdir(seq_path)) if os.path.exists(seq_path) else []:
#         files.append(fname)
#     if not files:
#         # Directory not yet in FS — fetch from server
#         # This will be handled per-sequence; see movie loop in main.py
#         pass
#     return files

import pygame
import world as w
import csv
import screen_fade
import os
import dialogue as dl


# initialize global variables that can be referenced across .py files
# this set of global variables is like the "state" of the game
world_level = "top"
movie_idx = None
SCREEN_WIDTH = 750 # need to update
# SCREEN_WIDTH = 480 
SCREEN_HEIGHT = SCREEN_WIDTH
# display_surface is the actual cabinet window (336x262 native CRT resolution)
# screen is the internal game surface — all logic, drawing, and collision stays at 750x750
# each frame, screen is scaled down onto display_surface before flip
# DISPLAY_WIDTH = 336
DISPLAY_WIDTH = 750
# DISPLAY_HEIGHT = 262
DISPLAY_HEIGHT = 750
display_surface = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
moving_left = False
moving_right = False
pygame.display.set_caption("Digital Physics: Part 2 of 1")
clock = pygame.time.Clock()
FPS = 30
GRAVITY = 1.15
SCROLL_THRESH = 200
ROWS = 15
COLUMNS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 201
MAX_HEALTH = 7
LEVELS = 3
TRANSITION_FRAMES = 140
screen_scroll = 0
bg_scroll = 0
level = 0
menu_screen = True
start_transition = False
first_time = True
first_ca_block_removal_sfx = True
restart = False
lives = 3
apply_force = False
ca_solution_rules = None
ca_solution = None
continued_CA = []
last_time_check = pygame.time.get_ticks()
last_time_check_dialogue = pygame.time.get_ticks()
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
running = True
dialogue_counter = 0
dialogue_counter_flag = False
ANIMATION_INTERVAL = 75
DIALOGUE_INTERVAL = 4000
splash = False
holding_object = None
img_list = []
nested_levels = []
transition = []
obstacle_list = []
ufo_present = False
floating = False
khatchig = None
ufo = None
hippie = None
real = None
cat = None
notkhatchig = None
mirror = None
mirror_loc = None
world_instance = None
khatchig_is_porting = False
door_dict = {}
surf = None
pick_flag = False
collision_on_off_counter = 0
dx_pos_last_time = False
room_lib = None
to_do_list = ["get briefcase", "deliver cat", "connect points", "erase notkhatchig", "return hot dog",
              "print printout", "juggle soccer ball", "explore feedback", "superposition", "match wallpaper", "run ascii"]
to_do = {task: False for task in to_do_list}
in_briefcase = {item: False for item in ["book", "shirt", "printout"]}
checkpoint_flag = False
health_counter_on = True
play_music = True
save_screenshots = False
master_save_screenshots = False
dev_mode = 1


def resource_path(relative_path):
    return relative_path


async def fetch_sequence(seq_path):
    """Fetch all frames of a movie/transition sequence into Pyodide FS on demand."""
    from js import fetchFileIntoFS
    if os.path.exists(seq_path):
        return sorted(os.listdir(seq_path))
    # Directory not in FS yet — fetch frames from server until we get a 404
    files = []
    i = 0
    while True:
        fname = f"{i}.png"
        fpath = f"{seq_path}/{fname}"
        try:
            await fetchFileIntoFS(fpath)
            files.append(fname)
            i += 1
        except Exception:
            break
    return files


# a blinking "loading" menu might need multithreading or another set of asyncio
loading_menu = pygame.image.load(resource_path("img/dp_ending_pixel_loading.png")).convert_alpha()
loading_menu = pygame.transform.scale(loading_menu, (SCREEN_WIDTH, SCREEN_HEIGHT))
screen.blit(loading_menu, (0, 0))
pygame.transform.scale(screen, (DISPLAY_WIDTH, DISPLAY_HEIGHT), display_surface)
pygame.display.flip()
pygame.display.set_icon(pygame.image.load(resource_path("img/tile/93.png")))
dialogue = dl.dialogue

# create sprite group objects
# all sprite objects in the group can leverage the group update and draw methods
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
blob_group = pygame.sprite.Group()
real_group = pygame.sprite.Group()

# init and load audio
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init()

# does this help with saving pngs with dialogue/font?
pygame.font.init()

electricity_sfx = pygame.mixer.Sound(resource_path("audio/electricity.ogg"))
electricity_sfx.set_volume(0.6)
ca_block_removal_sfx = pygame.mixer.Sound(resource_path("audio/ca_block_removal.ogg"))
ca_block_removal_sfx.set_volume(0.7)
ca_attempt_sfx = pygame.mixer.Sound(resource_path("audio/ca_attempt.ogg"))
ca_attempt_sfx.set_volume(0.7)
ca_lever_sfx = pygame.mixer.Sound(resource_path("audio/ca_lever.ogg"))
ca_lever_sfx.set_volume(0.8)
ca_rule_change_sfx = pygame.mixer.Sound(resource_path("audio/ca_rule_change.ogg"))
ca_rule_change_sfx.set_volume(0.7)
cat_hiss_sfx = pygame.mixer.Sound(resource_path("audio/cat_hiss.ogg"))
cat_hiss_sfx.set_volume(0.4)
jump_sfx = pygame.mixer.Sound(resource_path("audio/jump.ogg"))
jump_sfx.set_volume(0.9)
splash_sfx = pygame.mixer.Sound(resource_path("audio/splash.ogg"))
splash_sfx.set_volume(0.3)
pick_sfx = pygame.mixer.Sound(resource_path("audio/pick.ogg"))
pick_sfx.set_volume(0.5)
health_sfx = pygame.mixer.Sound(resource_path("audio/health_tick.ogg"))
health_sfx.set_volume(0.6)
health_reverse_sfx = pygame.mixer.Sound(resource_path("audio/health_tick_reverse.ogg"))
health_reverse_sfx.set_volume(0.6)
speech_sfx = pygame.mixer.Sound(resource_path("audio/speech.ogg"))
speech_sfx.set_volume(0.4)
gong_sfx = pygame.mixer.Sound(resource_path("audio/gong_sound.ogg"))
gong_sfx.set_volume(0.5)
ufo_sfx = pygame.mixer.Sound(resource_path("audio/ufo_sound.ogg"))
ufo_sfx.set_volume(0.5)
transition_sfx = pygame.mixer.Sound(resource_path("audio/transition.ogg"))
transition_sfx.set_volume(0.5)
header_sfx = pygame.mixer.Sound(resource_path("audio/header.ogg"))
header_sfx.set_volume(0.6)
door_sfx = pygame.mixer.Sound(resource_path("audio/door.ogg"))
door_sfx.set_volume(0.8)
success_sfx = pygame.mixer.Sound(resource_path("audio/success.ogg"))
success_sfx.set_volume(0.6)
printer_sfx = pygame.mixer.Sound(resource_path("audio/printer.ogg"))
printer_sfx.set_volume(0.98)
ufo_dump_sfx = pygame.mixer.Sound(resource_path("audio/ufo_dump.ogg"))
ufo_dump_sfx.set_volume(0.7)
# for briefcase room
# we should try loading sounds and images on demand, when needed instead of up front, and see how it performs?
switch_sfx = pygame.mixer.Sound(resource_path("audio/switch.ogg"))
switch_sfx.set_volume(0.7)
briefcase_change_sfx = pygame.mixer.Sound(resource_path("audio/briefcase_change_num.ogg"))
briefcase_change_sfx.set_volume(0.7)
briefcase_wrong_sfx = pygame.mixer.Sound(resource_path("audio/briefcase_wrong.ogg"))
briefcase_wrong_sfx.set_volume(0.7)
briefcase_open_sfx = pygame.mixer.Sound(resource_path("audio/briefcase_open.ogg"))
briefcase_open_sfx.set_volume(0.7)
hit_sfx = pygame.mixer.Sound(resource_path("audio/hit.ogg"))
hit_sfx.set_volume(0.7)
phone_pick_up_sfx = pygame.mixer.Sound(resource_path("audio/pick_up.ogg"))
phone_pick_up_sfx.set_volume(0.95)


# load (and transform some) images
tile_on_monitor = pygame.image.load(resource_path("img/original_monitor_screen.png")).convert_alpha()
pine1_img = pygame.image.load(resource_path("img/Background/pine1.png")).convert_alpha()
pine1_img.fill((20, 20, 20, 10), special_flags=pygame.BLEND_SUB)  # darken
pine2_img = pygame.image.load(resource_path("img/Background/pine2.png")).convert_alpha()
stars_img = pygame.image.load(resource_path("img/Background/pixel_stars.png")).convert_alpha()
rotated_stars_img = pygame.transform.rotate(stars_img, 90)
rotated_stars_img = pygame.transform.scale(rotated_stars_img,
                                           (int(rotated_stars_img.get_width() * 0.6), int(rotated_stars_img.get_height() * 0.6)))
stars_img = pygame.transform.scale(stars_img, (int(stars_img.get_width() * 0.4), int(stars_img.get_height() * 0.4)))
track_img = pygame.image.load(resource_path("img/Background/track.png")).convert_alpha()
track_img = pygame.transform.scale(track_img, (int(track_img.get_width() * 0.37), int(track_img.get_height() * 0.37)))
track_img.fill((130, 90, 90, 10), special_flags=pygame.BLEND_SUB)  # darken
sun_img = pygame.image.load(resource_path("img/Background/sun_and_stars.png")).convert_alpha()
sun_img = pygame.transform.scale(sun_img, (int(sun_img.get_width()*0.6), int(sun_img.get_height() * 0.6)))
water_bg_img = pygame.image.load(resource_path("img/Background/water_background.png")).convert_alpha()
water_bg2_img = pygame.image.load(resource_path("img/Background/water_background2.png")).convert_alpha()
water_bg3_img = pygame.image.load(resource_path("img/Background/water_background3.png")).convert_alpha()
streets_img = pygame.image.load(resource_path("img/Background/streets.png")).convert_alpha()
streets_img.fill((130, 90, 90, 10), special_flags=pygame.BLEND_SUB)  # darken
streets_img.set_alpha(60)
large_cat_img = pygame.image.load(resource_path("img/tile/105.png")).convert_alpha()
large_cat_img = pygame.transform.scale(large_cat_img, (300, 300))
heart_img = pygame.image.load(resource_path(f"img/health_heart.png")).convert_alpha()
white_heart_img = heart_img.copy()
white_heart_img = pygame.transform.scale(white_heart_img, (white_heart_img.get_width()*1.05, white_heart_img.get_height()*1.05))
white_heart_img.fill((255, 255, 255), special_flags=pygame.BLEND_ADD)
head_img = pygame.image.load(resource_path("img/khatchig_pixel_head_small.png")).convert_alpha()
menu_img = pygame.image.load(resource_path("img/dp_ending_pixel.png")).convert_alpha()
beam_img = pygame.image.load(resource_path("img/ufo/beam.png")).convert_alpha()
beam_img = pygame.transform.scale(beam_img, (int(beam_img.get_width() * 2), int(beam_img.get_height() * 2)))
menu_img = pygame.transform.scale(menu_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
head_img = pygame.transform.scale(head_img, (int(head_img.get_width() * 0.3), int(head_img.get_height() * 0.3)))

# for particle affinity room
paper_img = pygame.image.load(resource_path("img/Background/printer_paper.png")).convert_alpha()
paper_img = pygame.transform.scale(paper_img, (TILE_SIZE*3//2, TILE_SIZE*3//2))
printer_img = pygame.image.load(resource_path("img/Background/printer_pixel.png")).convert_alpha()
# printer_img = pygame.transform.scale(printer_img, (printer_img.get_width()//2, printer_img.get_height()//2))

# for computer room
escher_img = pygame.image.load(resource_path("img/Background/escher_wallpaper_computer.png")).convert_alpha()
escher_img = pygame.transform.scale(escher_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
escher2_img = pygame.image.load(resource_path("img/Background/escher_wallpaper_computer2.png")).convert_alpha()
escher2_img = pygame.transform.scale(escher2_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
escher_cube_img = pygame.image.load(resource_path("img/Background/escher_wallpaper_computer_cube.png")).convert_alpha()
escher_cube_img = pygame.transform.scale(escher_cube_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
escher2_cube_img = pygame.image.load(resource_path("img/Background/escher_wallpaper_computer2_cube.png")).convert_alpha()
escher2_cube_img = pygame.transform.scale(escher2_cube_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
escher_tet_img = pygame.image.load(resource_path("img/Background/escher_wallpaper_computer_tet.png")).convert_alpha()
escher_tet_img = pygame.transform.scale(escher_tet_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
escher2_tet_img = pygame.image.load(resource_path("img/Background/escher_wallpaper_computer2_tet.png")).convert_alpha()
escher2_tet_img = pygame.transform.scale(escher2_tet_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
escher_both_img = pygame.image.load(resource_path("img/Background/escher_wallpaper_computer_both.png")).convert_alpha()
escher_both_img = pygame.transform.scale(escher_both_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
escher2_both_img = pygame.image.load(resource_path("img/Background/escher_wallpaper_computer2_both.png")).convert_alpha()
escher2_both_img = pygame.transform.scale(escher2_both_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

escher3_img = pygame.image.load(resource_path("img/Background/escher_wallpaper_computer3.png")).convert_alpha()
escher3_img = pygame.transform.scale(escher3_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
escher4_img = pygame.image.load(resource_path("img/Background/escher_wallpaper_computer4.png")).convert_alpha()
escher4_img = pygame.transform.scale(escher4_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

escher5_img = pygame.image.load(resource_path("img/Background/escher_wallpaper_computer_bus.png")).convert_alpha()
escher5_img = pygame.transform.scale(escher5_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
escher6_img = pygame.image.load(resource_path("img/Background/escher_wallpaper_computer_bus2.png")).convert_alpha()
escher6_img = pygame.transform.scale(escher6_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

escher7_img = pygame.image.load(resource_path("img/Background/escher_wallpaper_computer_transparent.png")).convert_alpha()
escher7_img = pygame.transform.scale(escher7_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
escher8_img = pygame.image.load(resource_path("img/Background/escher_wallpaper_computer_transparent2.png")).convert_alpha()
escher8_img = pygame.transform.scale(escher8_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

escher9_img = pygame.image.load(resource_path("img/Background/escher_briefcase.png")).convert_alpha()
escher9_img = pygame.transform.scale(escher9_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
escher10_img = pygame.image.load(resource_path("img/Background/escher_briefcase2.png")).convert_alpha()
escher10_img = pygame.transform.scale(escher10_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
escher11_img = pygame.image.load(resource_path("img/Background/escher_briefcase_open.png")).convert_alpha()
escher11_img = pygame.transform.scale(escher11_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
escher12_img = pygame.image.load(resource_path("img/Background/escher_briefcase2_open.png")).convert_alpha()
escher12_img = pygame.transform.scale(escher12_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
escher13_img = pygame.image.load(resource_path("img/Background/escher_briefcase_open_up.png")).convert_alpha()
escher13_img = pygame.transform.scale(escher13_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
escher14_img = pygame.image.load(resource_path("img/Background/escher_briefcase_open_up2.png")).convert_alpha()
escher14_img = pygame.transform.scale(escher14_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
escher15_img = pygame.image.load(resource_path("img/Background/escher_feedback.png")).convert_alpha()
escher15_img = pygame.transform.scale(escher15_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
escher16_img = pygame.image.load(resource_path("img/Background/escher_feedback2.png")).convert_alpha()
escher16_img = pygame.transform.scale(escher16_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
escher17_img = pygame.image.load(resource_path("img/Background/escher_wallpaper_computer_transparent3.png")).convert_alpha()
escher17_img = pygame.transform.scale(escher17_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
escher18_img = pygame.image.load(resource_path("img/Background/escher_wallpaper_computer_transparent4.png")).convert_alpha()
escher18_img = pygame.transform.scale(escher18_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
escher19_img = pygame.image.load(resource_path("img/Background/escher_wallpaper_computer_transparent5.png")).convert_alpha()
escher19_img = pygame.transform.scale(escher19_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
escher20_img = pygame.image.load(resource_path("img/Background/escher_wallpaper_computer_transparent6.png")).convert_alpha()
escher20_img = pygame.transform.scale(escher20_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

# cat bus room
cat_bus_img = pygame.image.load(resource_path("img/Background/cat_bus_room.png")).convert_alpha()
cat_bus_img = pygame.transform.scale(cat_bus_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
cat_bus2_img = pygame.image.load(resource_path("img/Background/cat_bus_room2.png")).convert_alpha()
cat_bus2_img = pygame.transform.scale(cat_bus2_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
book_hands_img = pygame.image.load(resource_path("img/Background/book_and_hands.png")).convert_alpha()
book_hands_img = pygame.transform.scale(book_hands_img, (int(750/480*book_hands_img.get_width()), int(750/480*book_hands_img.get_height())))
book_img = pygame.image.load(resource_path("img/TM_book.png")).convert_alpha()

# for soccer room
campfire0_img = pygame.image.load(resource_path("img/Background/campfire0.png")).convert_alpha()
campfire0_img = pygame.transform.scale(campfire0_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
campfire1_img = pygame.image.load(resource_path("img/Background/campfire1.png")).convert_alpha()
campfire1_img = pygame.transform.scale(campfire1_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
campfire2_img = pygame.image.load(resource_path("img/Background/campfire2.png")).convert_alpha()
campfire2_img = pygame.transform.scale(campfire2_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
campfire_bg = [campfire0_img, campfire1_img, campfire2_img]
soccer_ball_img = pygame.image.load(resource_path("img/soccer_ball.png")).convert_alpha()
soccer_ball_img = pygame.transform.scale(soccer_ball_img, (20, 20))
letter_box_img = pygame.image.load(resource_path("img/letter_box.png")).convert_alpha()
letter_box_img = pygame.transform.scale(letter_box_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

# for end room
end_bg_img = pygame.image.load(resource_path("img/Background/street_end.png")).convert_alpha()
end_bg_img = pygame.transform.scale(end_bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
end_band_img = pygame.image.load(resource_path("img/Background/band_member.png")).convert_alpha()
end_band_img = pygame.transform.scale(end_band_img, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
end_band2_img = pygame.image.load(resource_path("img/Background/band_member2.png")).convert_alpha()
end_band2_img = pygame.transform.scale(end_band2_img, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))

# load custom font
font = pygame.font.Font(resource_path("fonts/kongtext.ttf"), 20)

# load tile images into list
for x in range(TILE_TYPES):
    img = pygame.image.load(resource_path(f'img/tile/{x}.png')).convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

# tile_on_monitor = img_list[30]
# tile_on_monitor = pygame.transform.scale(tile_on_monitor, (255, 170))

# load nested levels to put on computer screens in each level
# nested_levels = []
for pic in range(LEVELS):
    img = pygame.image.load(resource_path(f"img/nested_level/{pic}.png")).convert_alpha()
    img_small = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    nested_levels.append(img_small)

# load transition images into lists
# list of list: each list corresponds to an animation sequence from level x to level x+1
# transition = []
# for level_load in range(-1, LEVELS):
#     temp = []
#     for pic in range(TRANSITION_FRAMES):
#         img = pygame.image.load(resource_path(f"img/transition/level_{level_load}/{pic}.png")).convert_alpha()
#         temp.append(img)
#     transition.append(temp)
# async def load_transition(level_load):
#     """Load transition frames for a specific level on demand."""
#     from js import fetchFileIntoFS
#     frames = []
#     for pic in range(TRANSITION_FRAMES):
#         path = f"img/transition/level_{level_load}/{pic}.png"
#         if not os.path.exists(path):
#             await fetchFileIntoFS(path)
#         img = pygame.image.load(path).convert_alpha()
#         frames.append(img)
#     return frames

# load neural cellular automata character movie because PyTorch and PyInstaller lead to a Segmentation Fault: 11 error
# for i in range(150):
#     nca_img = pygame.image.load(resource_path(f"img/nca_room_movie/{i}.png")).convert_alpha()
#     nca_img = pygame.transform.scale(nca_img, (163, 163))
#     nca_movie.append(nca_img)

# load first level data from CSV files
with open(resource_path(f"levels/level{level}_data.csv"), newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    world_data = [[int(tile) for tile in row] for row in reader]

# initialize the world instance for the first loop
world_instance = w.World()
khatchig, ufo, hippie, notkhatchig, cat = world_instance.process_data(world_data)

# create instances for two kinds of transitions
intro_fade = screen_fade.ScreenFade(1, BLACK, 16)
death_fade = screen_fade.ScreenFade(2, BLACK, 16)