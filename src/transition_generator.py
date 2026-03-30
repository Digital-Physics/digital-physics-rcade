import pygame
import csv
import global_vars as gv

pygame.init()

SCREEN_WIDTH = 750
SCREEN_HEIGHT = SCREEN_WIDTH
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
ROWS = 15  # should make rows, columns, and other variables level-specific
COLUMNS = 150
TILE_SIZE = SCREEN_HEIGHT//ROWS
TILE_TYPES = 190
LEVELS = 3
screen_scroll = 0  # delta/change number in normal game play, but aggregate movement in this helper script
bg_scroll = 0  # aggregate number
level = 0
menu_screen = True
start_transition = False
first_time = True  # helps with transitions

stars_img_large = pygame.transform.scale(gv.stars_img, (int(gv.stars_img.get_width()*15), int(gv.stars_img.get_height()*15)))
pine1_img_large = pygame.transform.scale(gv.pine1_img, (int(gv.pine1_img.get_width()*15), int(gv.pine1_img.get_height()*15)))
pine2_img_large = pygame.transform.scale(gv.pine2_img, (int(gv.pine2_img.get_width()*15), int(gv.pine2_img.get_height()*15)))
streets_img_large = pygame.transform.scale(gv.streets_img, (int(gv.streets_img.get_width()*15), int(gv.streets_img.get_height()*15)))
rotated_stars_img_large = pygame.transform.scale(gv.rotated_stars_img, (int(gv.rotated_stars_img.get_width()*15),
                                                                     int(gv.rotated_stars_img.get_height()*15)))
sun_img_large = pygame.transform.scale(gv.sun_img, (int(gv.sun_img.get_width()*15), int(gv.sun_img.get_height()*15)))
water_bg_img_large = pygame.transform.scale(gv.water_bg_img, (int(gv.water_bg_img.get_width()*15), int(gv.water_bg_img.get_height()*15)))
water_bg2_img_large = pygame.transform.scale(gv.water_bg2_img, (int(gv.water_bg2_img.get_width()*15),int(gv.water_bg2_img.get_height()*15)))
water_bg3_img_large = pygame.transform.scale(gv.water_bg3_img, (int(gv.water_bg3_img.get_width()*15),int(gv.water_bg3_img.get_height()*15)))

# create two lists: one will hold the large tiles, and one will hold the small tiles
img_list = []
img_list_large = []

door_dict = {}

for x in range(TILE_TYPES):
    img = pygame.image.load(f'img/tile/{x}.png').convert_alpha()
    img_small = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img = pygame.transform.scale(img, (TILE_SIZE * 15, TILE_SIZE * 15))
    img_list.append(img_small)
    img_list_large.append(img)


# note the level+1 difference from main.py code
def draw_background(scale=1):
    # width = pine2_img.get_width()*scale  # repeating frequency
    width = 1376*scale  # repeating frequency
    for x in range(6):  # repeat 6 times
        if scale == 1:
            if (level+1) % LEVELS == 0:
                screen.blit(gv.stars_img, ((x * width) - bg_scroll * 0.5, 0))
                screen.blit(gv.pine1_img, ((x * width) - bg_scroll * 0.7, SCREEN_HEIGHT - gv.pine1_img.get_height() - 250))
                screen.blit(gv.pine2_img, ((x * width) - bg_scroll * 0.8, SCREEN_HEIGHT - gv.pine2_img.get_height()))
            elif (level+1) % LEVELS == 1:
                screen.blit(gv.sun_img, (-1000 - bg_scroll * 0.02, 0))
                screen.blit(gv.water_bg_img, (0 - bg_scroll * 0.05, 650))
                screen.blit(gv.water_bg2_img, (0 - bg_scroll * 0.1, 675))
                screen.blit(gv.water_bg3_img, (0 - bg_scroll * 0.2, 730))
            elif (level + 1) % LEVELS == 2:
                for im in range(6):
                    screen.blit(gv.rotated_stars_img, (0, (im * width) - bg_scroll * 0.5 - 300))
        else:
            if (level+1) % LEVELS == 0:
                screen.blit(stars_img_large, ((x * width) - bg_scroll * 0.5, 0))
                screen.blit(pine1_img_large, ((x * width) - bg_scroll * 0.7, SCREEN_HEIGHT - pine1_img_large.get_height() - 250*scale))
                screen.blit(pine2_img_large, ((x * width) - bg_scroll * 0.8, SCREEN_HEIGHT - pine2_img_large.get_height()))
            elif (level+1)%LEVELS == 1:
                screen.blit(sun_img_large, (-1000*scale - bg_scroll * 0.02, 0))
                screen.blit(water_bg_img_large, (0 - bg_scroll * 0.05, 650*scale))
                screen.blit(water_bg2_img_large, (0 - bg_scroll * 0.1, 675*scale))
                screen.blit(water_bg3_img_large, (0 - bg_scroll * 0.2, 730*scale))
            elif (level+1) % LEVELS == 2:
                for x in range(6):
                    screen.blit(rotated_stars_img_large, (0, (x * width) - bg_scroll * 0.5 - 300*scale))

    # no loop needed for non-repeating background elements
    # the streets are in level 0, but the for loop in the level constructor is indexed based on nested level (n-1)
    if (level+1)%LEVELS == 0:
        screen.blit(streets_img_large, (0, SCREEN_HEIGHT - streets_img_large.get_height() - 40*scale))


# reset level function
def reset_level(meta_ind=False):
    decoration_group.empty()
    water_group.empty()
    exit_group.empty()
    lever_group.empty()


class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y, collidable=False, type=None, flip_image=None):
        pygame.sprite.Sprite.__init__(self)
        self.collidable = collidable
        self.image = img
        self.type = type
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
        self.flip_image = flip_image

    def update(self):
        # scroll
        if (level+1) == 2:
            self.rect.y += screen_scroll
        else:
            self.rect.x += screen_scroll


class Water(pygame.sprite.Sprite):
    def __init__(self, img, x, y, flip_image):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
        self.flip_image = flip_image

    def update(self):
        # scroll
        if (level+1) == 2:
            self.rect.y += screen_scroll
        else:
            self.rect.x += screen_scroll


class Exit(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        # scroll
        if (level+1) == 2:
            self.rect.y += screen_scroll
        else:
            self.rect.x += screen_scroll


class Lever(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        # scroll
        if (level+1) == 2:
            self.rect.y += screen_scroll
        else:
            self.rect.x += screen_scroll


class World():
    def __init__(self):
        self.obstacle_list = []
        self.level_length = None
        self.level_length_vert = None

    def process_data(self, data, size="small"):
        """
        we take the level data in the csv and initialize the tiles, etc. based on the matrix of numbers and what they represent.
        tiles (images & position) can be ground, non-interacting decoration, starting positions for agents, dangerous water, etc.
        some tile images/numbers will be associated with "sprite" objects with collision & other methods associated with them.
        ground tiles will be put in the obstacle list (although collision checks aren't needed for this helper script)
        """
        # number of tiles wide
        self.level_length = len(data[0])
        # number of tiles high
        self.level_length_vert = len(data)

        for i, row in enumerate(data):
            for j, tile in enumerate(row):
                if tile >= 0:  # -1 is an empty tile
                    if tile < TILE_TYPES:
                        if size == "small":
                            img = img_list[tile]
                        elif size == "large":
                            img = img_list_large[tile]
                    # nothing to do for player and entity start pos (i.e. player, ufo, hippie)
                    elif tile < 1000:
                        pass
                    # tiles we don't want to collide with are indexed 100 more than the tile they look like
                    else:
                        if size == "small":
                            img = img_list[tile-1000]
                        elif size == "large":
                            img = img_list_large[tile-1000]

                    img_rect = img.get_rect()
                    img_rect.x = j * TILE_SIZE
                    img_rect.y = i * TILE_SIZE

                    # tile_data list is used for obstacles; Decorations and Characters reference subset of those elements
                    # image, current position on screen, tile position in level layout, flip image, flip message, CA rule
                    tile_data = [img, img_rect, [i, j], None, None, None]

                    # most tiles are determined ahead of time in the CSV layout
                    if tile != -1:  # -1 is an empty tile in the board layout csv
                        # adjust ground tile number based on goals achieved
                        # if 135 <= tile <= 140:
                        #     # tile += (171-135)
                        #     tile = tile + 6 * min(sum([1 if val else 0 for val in to_do.values()]), 6)
                        # define tile image
                        # if tile < TILE_TYPES:
                        #     img = img_list[tile]
                        # # tiles we don't want to collide with are numbered 1000 greater than the collidable obstacle versions of the same image
                        # elif tile > 1000:
                        #     img = img_list[tile - 1000]
                        # # define initial tile position
                        # img_rect = img.get_rect()
                        # img_rect.x = j * TILE_SIZE
                        # img_rect.y = i * TILE_SIZE

                        # tile_data list is used for obstacles; Decorations and Characters reference subset of those elements
                        # image, current position on screen, tile position in level layout, flip image list, flip message, CA rule or flip_idx
                        # tile_data = [img, img_rect, [i, j], None, None, None]

                        if tile == 0:  # monitor = level exit (for testing purposes; to get to other levels quickly)
                            # if dev_mode:
                            #     exit_obj = Exit(img, j * TILE_SIZE, i * TILE_SIZE)
                            #     exit_group.add(exit_obj)
                            # else:
                            decoration = Decoration(img, j * TILE_SIZE, i * TILE_SIZE)
                            decoration_group.add(decoration)
                        elif tile == 1:  # Escher wire ground tiles
                            self.obstacle_list.append(tile_data)
                        elif tile in [2, 75]:  # decoration grass
                            decoration = Decoration(img, j * TILE_SIZE, i * TILE_SIZE, collidable=True, type="grass")
                            decoration_group.add(decoration)
                        elif tile == 3:  # grass-with-mushroom decoration tiles
                            decoration = Decoration(img, j * TILE_SIZE, i * TILE_SIZE, collidable=True, type="mushroom")
                            decoration_group.add(decoration)
                        # tile 4 is grass without mushroom; it gets used only when tile 3 is updated
                        elif tile == 5:  # lever to start Cellular Automaton
                            decoration = Decoration(img, j * TILE_SIZE, i * TILE_SIZE, collidable=True, type="lever off")
                            decoration_group.add(decoration)
                        elif 6 <= tile <= 10:  # CA pipes
                            # need to load on CA pipes that will be swapped in, tiles 56-60
                            tile_data[3] = img_list[tile + 50]
                            tile_data[4] = "flip on lever"
                            self.obstacle_list.append(tile_data)
                        # tiles 11-18 is off
                        elif tile == 19:  # CA tile on
                            tile_data[3] = img_list[20]
                            tile_data[4] = "CA tile"
                            self.obstacle_list.append(tile_data)
                        elif tile == 20:  # CA tile off
                            tile_data[3] = img_list[19]
                            tile_data[4] = "CA tile"
                            self.obstacle_list.append(tile_data)
                        elif 21 <= tile <= 28:  # decoration computer tiles
                            decoration = Decoration(img, j * TILE_SIZE, i * TILE_SIZE)
                            decoration_group.add(decoration)
                        elif tile in [29, 30, 70, 71]:  # Escher block building background
                            decoration = Decoration(img, j * TILE_SIZE, i * TILE_SIZE)
                            decoration_group.add(decoration)
                        elif 31 <= tile <= 38:  # CA rule tiles (off set)
                            # need to load CA images that will be swapped in, tiles 11-18
                            tile_data[3] = img_list[tile - 20]
                            tile_data[4] = "flip when hit with head"
                            tile_data[5] = tile - 31  # 31 is rule 000, 32 is 001, etc.
                            self.obstacle_list.append(tile_data)
                        elif tile == 40:  # Escher bird and fish
                            self.obstacle_list.append(tile_data)
                        elif 41 <= tile <= 53:  # computer ground tiles
                            self.obstacle_list.append(tile_data)
                        elif tile == 54:  # black door
                            door_name = "whatever"
                            # if level == 0:
                            #     if j < 5:
                            #         door_name = "neural_cellular_automata_room"
                            #         door_dict[door_name] = True
                            #     elif j < 25:
                            #         door_name = "monitor_room"
                            #         door_dict[door_name] = True
                            #     elif j < 100:
                            #         door_name = "computer_room"
                            #         door_dict[door_name] = True
                            #     elif j < 125:
                            #         door_name = "door4"
                            #     else:
                            #         door_name = "soccer_room"
                            #         door_dict[door_name] = True
                            # if level == 1:
                            #     if j < 50:
                            #         door_name = "environment_control_room"
                            #         door_dict[door_name] = True
                            #     elif j < 100:
                            #         door_name = "cat_bus_room"
                            #         door_dict[door_name] = True
                            #     elif j < 120:
                            #         door_name = "door4"
                            #     else:
                            #         door_name = "ascii_room"
                            #         door_dict[door_name] = True
                            # if level == 2:
                            #     if i < 75 and j < 8:
                            #         door_name = "particle_affinity_room"
                            #         door_dict[door_name] = True
                            #     elif i < 75 and j >= 8:
                            #         door_name = "briefcase_room"
                            #         door_dict[door_name] = True
                            #     elif j > 8:
                            #         door_name = "end_room"
                            #         door_dict[door_name] = True
                            #     else:
                            #         door_name = "door6"
                            decoration = Decoration(img, j * TILE_SIZE, i * TILE_SIZE, collidable=True, type=door_name)
                            decoration_group.add(decoration)
                        elif tile == 55:  # extra on lever that stays on
                            decoration = Decoration(img, j * TILE_SIZE, i * TILE_SIZE)
                            decoration_group.add(decoration)
                        elif tile in [61, 74, 120, 125, 133, 189]:  # this is a non-moving dialogue character bottom
                            decoration = Decoration(img, j * TILE_SIZE, i * TILE_SIZE)
                            decoration_group.add(decoration)
                        elif tile in [62, 73, 132]:  # this is a non-moving dialogue character head
                            decoration = Decoration(img, j * TILE_SIZE, i * TILE_SIZE, collidable=True, type="first dead_head")
                            decoration_group.add(decoration)
                        elif tile in [119, 124, 188]:  # second head of the level; distinguished to help w/ dialogue
                            decoration = Decoration(img, j * TILE_SIZE, i * TILE_SIZE, collidable=True, type="second dead_head")
                            decoration_group.add(decoration)
                        elif tile == 63:  # mobius strip
                            tile_data[3] = [img_list[tile], img_list[tile + 1]]
                            tile_data[4] = "flip each step"
                            tile_data[5] = 0  # image in list idx
                            self.obstacle_list.append(tile_data)
                        elif tile == 65:  # water
                            water = Water(img, j * TILE_SIZE, i * TILE_SIZE, flip_image=img_list[tile + 1])
                            water_group.add(water)
                        elif tile == 67:  # book
                            decoration = Decoration(img, j * TILE_SIZE, i * TILE_SIZE, collidable=True, type="book")
                            decoration_group.add(decoration)
                        elif tile == 68:  # shirt
                            decoration = Decoration(img, j * TILE_SIZE, i * TILE_SIZE, collidable=True, type="shirt")
                            decoration_group.add(decoration)
                        elif tile == 69:  # non-updating ground
                            self.obstacle_list.append(tile_data)
                        elif tile == 76:  # level exit
                            exit = Exit(img, j * TILE_SIZE, i * TILE_SIZE)
                            exit_group.add(exit)
                        elif tile == 79:  # camera
                            decoration = Decoration(img, j * TILE_SIZE, i * TILE_SIZE, collidable=True, type="camera")
                            decoration_group.add(decoration)
                        elif tile == 80:  # hot dog
                            decoration = Decoration(img, j * TILE_SIZE, i * TILE_SIZE, collidable=True, type="hot_dog")
                            decoration_group.add(decoration)
                        elif 81 <= tile <= 92:  # cat bus
                            decoration = Decoration(img, j * TILE_SIZE, i * TILE_SIZE)
                            decoration_group.add(decoration)
                        # non-tile numbers in CSV
                        # elif tile == 94:  # create player/khatchig
                        #     if level != 2:
                        #         khatchig = c.Character("khatchig", j * TILE_SIZE, i * TILE_SIZE, 2.5, 7, self)
                        #     else:
                        #         khatchig = c.Character("khatchig", j * TILE_SIZE, i * TILE_SIZE, 2, 7, self)
                        # elif tile == 95:
                        #     hippie = c.Character("hippie", j * TILE_SIZE, i * TILE_SIZE, 2.5, 1, self)
                        # elif tile == 96:
                        #     ufo = u.Ufo(600, 200, 2, 1)
                        # elif tile == 97:
                        #     notkhatchig = c.Character("notkhatchig", j * TILE_SIZE, i * TILE_SIZE, 2.5, 5, self)
                        # non-collidable decoration tiles that look like collidable obstacles
                        elif tile == 100:  # nca logo
                            tile_data[3] = [img_list[tile], img_list[tile + 1], img_list[tile + 2], img_list[tile + 3]]
                            tile_data[4] = "flip each step"
                            tile_data[5] = 0  # image list idx
                            self.obstacle_list.append(tile_data)
                        # elif tile == 104:
                        #     real = r.Real(j * TILE_SIZE, i * TILE_SIZE, 2, 1)
                        #     real_group.add(real)
                        # elif tile == 105:
                        #     cat = ca.Cat(j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE / 32, 3)
                        elif 106 <= tile <= 111:  # food truck
                            decoration = Decoration(img, j * TILE_SIZE, i * TILE_SIZE, collidable=False, type="hot dog truck")
                            decoration_group.add(decoration)
                        elif tile == 112:  # food truck ledge bottom
                            self.obstacle_list.append(tile_data)
                        elif tile == 113:  # food truck ledge top
                            decoration = Decoration(img, j * TILE_SIZE, i * TILE_SIZE, collidable=True, type="flip on hot dog drop")
                            decoration_group.add(decoration)
                        elif 115 <= tile <= 117:  # phone
                            if tile == 116:
                                decoration = Decoration(img, j * TILE_SIZE, i * TILE_SIZE, collidable=False, type="phone_bottom")
                                decoration_group.add(decoration)
                            else:
                                decoration = Decoration(img, j * TILE_SIZE, i * TILE_SIZE, collidable=True, type="phone")
                                decoration_group.add(decoration)
                        # elif tile == 118:
                        #     blob = b.Blob(j * TILE_SIZE, i * TILE_SIZE, 2, 1)
                        #     blob_group.add(blob)
                        elif tile == 126:  # dancing dead head
                            decoration = Decoration(img, j * TILE_SIZE, i * TILE_SIZE, collidable=True, type="flip dead_head",
                                                    flip_image=img_list[tile + 2])
                            decoration_group.add(decoration)
                        elif tile == 127:  # dancing dead head
                            decoration = Decoration(img, j * TILE_SIZE, i * TILE_SIZE, collidable=True,
                                                    type="flip dead_head bottom", flip_image=img_list[tile + 2])
                            decoration_group.add(decoration)
                        elif 135 <= tile <= 176:  # ground
                            self.obstacle_list.append(tile_data)
                        elif tile == 177:  # mirror
                            decoration = Decoration(img, j * TILE_SIZE, i * TILE_SIZE, collidable=True, type="mirror")
                            decoration_group.add(decoration)
                        elif 178 <= tile <= 185:  # mirror sides
                            decoration = Decoration(img, j * TILE_SIZE, i * TILE_SIZE, collidable=True, type="mirror side")
                            decoration_group.add(decoration)
                        elif tile > 1000:  # to make an object a non-interacting decoration just add +1000 to the tile #
                            decoration = Decoration(img, j * TILE_SIZE, i * TILE_SIZE)
                            decoration_group.add(decoration)

    # draw method for obstacles, not sprite groups like decorations
    def draw(self):  # and update position
        for i, tile in enumerate(self.obstacle_list):
            if (level+1) == 2:
                tile[1][1] += screen_scroll  # y value of rectangle
                screen.blit(tile[0], tile[1])
            else:
                tile[1][0] += screen_scroll  # x value of rectangle
                screen.blit(tile[0], tile[1])


def transition(steps, image):
    # get factor that when raised to the nth power gives you an image that is 1/15 of the original
    factor = (1/15)**(1/steps)

    # for trail effect
    trail_buffer = []
    pic = img_list_large[0]

    for step in range(steps+40):
        if step<steps:
            snapshot_img = pygame.transform.scale(image,(int(image.get_width() * factor ** step), int(image.get_height() * factor ** step)))
            trail_img = pygame.transform.scale(pic,(int(pic.get_width() * factor ** step), int(pic.get_height() * factor ** step)))
        else:
            snapshot_img = pygame.transform.scale(image, (int(image.get_width() * factor ** steps), int(image.get_height() * factor ** steps)))
            trail_img = pygame.transform.scale(pic, (int(pic.get_width() * factor ** steps), int(pic.get_height() * factor ** steps)))
        trail_buffer = [trail_img] + trail_buffer
        trail_buffer = trail_buffer[:40]

        # center the big picture in the middle of the smaller screen by calculating where upper left point is off screen
        screen.blit(snapshot_img, (int(SCREEN_WIDTH / 2 - snapshot_img.get_width() / 2),
                                   int(SCREEN_HEIGHT / 2 - snapshot_img.get_height() / 2)))

        # make trail of nested images
        for i, trail in enumerate(trail_buffer):
            if i % 4 == 0:
                trail.set_alpha(200 * 0.92 ** i)
                screen.blit(trail, (int(SCREEN_WIDTH / 2 - trail.get_width() / 2), int(SCREEN_HEIGHT / 2 - trail.get_height() / 2)))

        # overlay opaque original nested image
        screen.blit(trail_img, (int(SCREEN_WIDTH / 2 - trail_img.get_width() / 2), int(SCREEN_HEIGHT / 2 - trail_img.get_height() / 2)))

        pygame.image.save(screen, f"img/transition/level_{level}/{step}.png")

# create sprite group objects
# all sprite objects in the group update when a single group method for "update" and "draw" are called
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
lever_group = pygame.sprite.Group()

# run the main image construction function
# make sure the menu screen is in the tile image folder as a png with the last/largest tile number
for level in range(-1, LEVELS):
    reset_level(True)

    # load meta level (csv) which will wrap around the nested image
    # the nested image was initialized as the menu image or created at the end of the last loop iteration
    print()
    print("load meta level csv, level", (level + 1) % LEVELS)
    with open(f"levels/level{(level + 1) % LEVELS}_data.csv", newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        meta_world_data = [[int(tile) for tile in row] for row in reader]
        world_data = meta_world_data

    # make screen bigger for large screenshot of image
    # large, nested png will be the asset for creating the transition animation
    SCREEN_WIDTH = SCREEN_WIDTH * 15
    SCREEN_HEIGHT = SCREEN_WIDTH
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    TILE_SIZE = SCREEN_HEIGHT // ROWS

    # create group objects containing images of tiles and coordinates
    meta_world = World()
    meta_world.process_data(meta_world_data, "large")

    # regardless of level, we won't need to scroll the tiles to get the snapshot we need
    # we want a large png of the *start* of the meta level, not the end frame in the nested level
    bg_scroll = 0
    screen_scroll = -bg_scroll

    print("draw meta level background, obj list, sprite groups")
    draw_background(15)
    meta_world.draw()

    # we don't need to use the update method since nothing needs to move, but we do need to draw them
    decoration_group.draw(screen)
    water_group.draw(screen)
    exit_group.draw(screen)
    lever_group.draw(screen)

    pygame.display.update()

    print("save screen shot, and then load the png image for transition.")
    pygame.image.save(screen, f"img/meta_level/meta_level_{level}.png")
    meta_level_img = pygame.image.load(f"img/meta_level/meta_level_{level}.png").convert_alpha()

    # we need the screen to be the normal size before running the transition generator
    SCREEN_WIDTH = int(SCREEN_WIDTH / 15)
    SCREEN_HEIGHT = SCREEN_WIDTH
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    TILE_SIZE = SCREEN_HEIGHT // ROWS

    print("run transition generator on meta w/ nested image")
    transition(100, meta_level_img)

    # step 2: make the image that will be nested in the next layer
    # that is, get a png of the screen after you scroll to and construct the image of the end of the level
    world = World()
    reset_level()
    world.process_data(world_data)

    # determine scroll amount to move the images to represent the last frame of the level
    # level 2 is a vertical scroll
    if level+1 == 2:  # the meta level is loaded, hence "level+1"
        # at some point, update the background scroll direction for level 2 in the main game app, and then update this
        bg_scroll = ((world.level_length_vert * TILE_SIZE) - SCREEN_HEIGHT//2)
        screen_scroll = -bg_scroll
    else:
        bg_scroll = (world.level_length * TILE_SIZE) - SCREEN_WIDTH
        screen_scroll = -bg_scroll

    draw_background()
    world.draw()

    decoration_group.update()
    water_group.update()
    exit_group.update()
    lever_group.update()

    # decoration_group.draw(screen)
    water_group.draw(screen)
    exit_group.draw(screen)
    lever_group.draw(screen)
    decoration_group.draw(screen)

    # update tile for nesting in the next step of the oop
    pygame.display.update()

    print("png of screen for nesting saved in folder for use during game play.")
    pygame.image.save(screen, f"img/nested_level/{level}.png")
    end_shot = pygame.image.load(f"img/nested_level/{level}.png").convert_alpha()

    print("In prep for next loop iteration, new nested image overwrites previous nested images in lists.")
    end_shot = pygame.transform.scale(end_shot, (TILE_SIZE*15, TILE_SIZE*15))
    end_shot_small = pygame.transform.scale(end_shot, (TILE_SIZE, TILE_SIZE))
    img_list[0] = end_shot_small
    img_list_large[0] = end_shot

pygame.quit()
