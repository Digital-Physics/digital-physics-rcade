import global_vars as gv
import water as wa
import ufo as u
import real as r
import exit as e
import decoration as d
import character as c
import cat as ca
import blob as b
import random


class World:
    def __init__(self):
        gv.obstacle_list = []  # obstacle list are tiles you can't move through; used for checking collisions in character move methods
        # variables related to the level 2 Cellular Automaton (CA) game
        self.ca_rules = [0]*8  # these are the current rules to apply to the rows
        self.ca_state = "1"  # string representing starting tape (all 0s to left and right)
        self.ca_row = 24
        self.ca_col = 7
        self.ca_next_string = ""
        self.ca_lever = False
        self.ca_rules_updated = False
        self.ca_last_row_complete = False
        self.ca_success = False
        self.level_length = None
        self.random_door_bit = random.randint(0, 1)

    # tiles can be hard objects like ground, non-interacting decoration, starting positions for Characters, dangerous water, etc.
    def process_data(self, data):
        """future update: instead of if statements, should we do a dictionary mapping from tile number to unique code?"""
        ufo = None
        hippie = None
        notkhatchig = None
        # real = None
        cat = None

        self.level_length = len(data[0])  # put in initialization

        for i, row in enumerate(data):
            for j, tile in enumerate(row):
                # some tiles are procedurally generated from the random CA rules
                if gv.level == 2 and 32 <= i <= 131:
                    if gv.continued_CA[i-32][j] == "0":
                        tile = 1020
                    elif gv.continued_CA[i-32][j] == "1":
                        tile = 1019
                # target solution row for display
                if gv.level == 2 and i == 17:
                    if gv.ca_solution[j] == "0":
                        tile = 1020
                    elif gv.ca_solution[j] == "1":
                        tile = 1019
                # most tiles are determined ahead of time in the CSV layout
                if tile != -1:  # -1 is an empty tile in the board layout csv
                    # adjust ground tile number based on goals achieved
                    if 135 <= tile <= 140:
                        # tile += (171-135)
                        tile = tile + 6 * min(sum([1 if val else 0 for val in gv.to_do.values()]), 6)
                    # define tile image
                    if tile < gv.TILE_TYPES:
                        img = gv.img_list[tile]
                    # tiles we don't want to collide with are numbered 1000 greater than the collidable obstacle versions of the same image
                    elif tile > 1000:
                        img = gv.img_list[tile - 1000]
                    # define initial tile position
                    img_rect = img.get_rect()
                    img_rect.x = j * gv.TILE_SIZE
                    img_rect.y = i * gv.TILE_SIZE

                    # tile_data list is used for obstacles; Decorations and Characters reference subset of those elements
                    # image, current position on screen, tile position in level layout, flip image list, flip message, CA rule or flip_idx
                    tile_data = [img, img_rect, [i, j], None, None, None]

                    if tile == 0:  # monitor = level exit (for testing purposes; to get to other levels quickly)
                        if gv.dev_mode == 0:
                            exit_obj = e.Exit(img, j * gv.TILE_SIZE, i * gv.TILE_SIZE)
                            gv.exit_group.add(exit_obj)
                        else:
                            decoration = d.Decoration(img, j * gv.TILE_SIZE, i * gv.TILE_SIZE)
                            gv.decoration_group.add(decoration)
                    elif tile == 1:  # Escher wire ground tiles
                        gv.obstacle_list.append(tile_data)
                    elif tile in [2, 75]:  # decoration grass
                        decoration = d.Decoration(img, j * gv.TILE_SIZE, i * gv.TILE_SIZE, collidable=True, type="grass")
                        gv.decoration_group.add(decoration)
                    elif tile == 3:  # grass-with-mushroom decoration tiles
                        decoration = d.Decoration(img, j * gv.TILE_SIZE, i * gv.TILE_SIZE, collidable=True, type="mushroom")
                        gv.decoration_group.add(decoration)
                    # tile 4 is grass without mushroom; it gets used only when tile 3 is updated
                    elif tile == 5:  # lever to start Cellular Automaton
                        decoration = d.Decoration(img, j * gv.TILE_SIZE, i * gv.TILE_SIZE, collidable=True, type="lever off")
                        gv.decoration_group.add(decoration)
                    elif 6 <= tile <= 10:  # CA pipes
                        # need to load on CA pipes that will be swapped in, tiles 56-60
                        tile_data[3] = gv.img_list[tile + 50]
                        tile_data[4] = "flip on lever"
                        gv.obstacle_list.append(tile_data)
                    # tiles 11-18 is off
                    elif tile == 19:  # CA tile on
                        tile_data[3] = gv.img_list[20]
                        tile_data[4] = "CA tile"
                        gv.obstacle_list.append(tile_data)
                    elif tile == 20:  # CA tile off
                        tile_data[3] = gv.img_list[19]
                        tile_data[4] = "CA tile"
                        gv.obstacle_list.append(tile_data)
                    elif 21 <= tile <= 28:  # decoration computer tiles
                        decoration = d.Decoration(img, j * gv.TILE_SIZE, i * gv.TILE_SIZE)
                        gv.decoration_group.add(decoration)
                    elif tile in [29, 30, 70, 71]:  # Escher block building background
                        decoration = d.Decoration(img, j * gv.TILE_SIZE, i * gv.TILE_SIZE)
                        gv.decoration_group.add(decoration)
                    elif 31 <= tile <= 38:  # CA rule tiles (off set)
                        # need to load CA images that will be swapped in, tiles 11-18
                        tile_data[3] = gv.img_list[tile - 20]
                        tile_data[4] = "flip when hit with head"
                        tile_data[5] = tile-31  # 31 is rule 000, 32 is 001, etc.
                        gv.obstacle_list.append(tile_data)
                    elif tile == 40:  # Escher bird and fish
                        gv.obstacle_list.append(tile_data)
                    elif 41 <= tile <= 53:  # computer ground tiles
                        gv.obstacle_list.append(tile_data)
                    elif tile == 54:  # black door
                        if gv.level == 0:
                            if j < 5:
                                door_name = "neural_cellular_automata_room_dist"
                                gv.door_dict[door_name] = True
                            elif j < 25:
                                door_name = "monitor_room"
                                gv.door_dict[door_name] = True
                            elif j < 100:
                                door_name = "computer_room"
                                gv.door_dict[door_name] = True
                            elif j < 125:
                                door_name = "tai_chi"
                                gv.door_dict[door_name] = True
                            else:
                                door_name = "soccer_room"
                                gv.door_dict[door_name] = True
                        if gv.level == 1:
                            if j < 50:
                                door_name = "environment_control_room"
                                gv.door_dict[door_name] = True
                            elif j < 100:
                                door_name = "cat_bus_room"
                                gv.door_dict[door_name] = True
                            else:
                                door_name = "ascii_room"
                                gv.door_dict[door_name] = True
                        if gv.level == 2:
                            if i < 75 and j < 8:
                                door_name = "particle_affinity_room"
                                gv.door_dict[door_name] = True
                            elif i < 75 and j >= 8:
                                door_name = "briefcase_room"
                                gv.door_dict[door_name] = True
                            elif j > 8:
                                if self.random_door_bit == 0:
                                    door_name = "end_room"
                                    gv.door_dict[door_name] = True
                                else:
                                    door_name = "behind_computer"
                                    gv.door_dict[door_name] = True
                            else:
                                if self.random_door_bit == 0:
                                    door_name = "behind_computer"
                                    gv.door_dict[door_name] = True
                                else:
                                    door_name = "end_room"
                                    gv.door_dict[door_name] = True
                        decoration = d.Decoration(img, j * gv.TILE_SIZE, i * gv.TILE_SIZE, collidable=True, type=door_name)
                        gv.decoration_group.add(decoration)
                    elif tile == 55:  # extra on lever that stays on
                        decoration = d.Decoration(img, j * gv.TILE_SIZE, i * gv.TILE_SIZE)
                        gv.decoration_group.add(decoration)
                    elif tile in [61, 74, 120, 125, 133, 189, 193]:  # this is a non-moving dialogue character bottom
                        decoration = d.Decoration(img, j * gv.TILE_SIZE, i * gv.TILE_SIZE)
                        gv.decoration_group.add(decoration)
                    elif tile in [62, 73, 192]:  # this is a non-moving dialogue character head
                        decoration = d.Decoration(img, j * gv.TILE_SIZE, i * gv.TILE_SIZE, collidable=True, type="first dead_head")
                        gv.decoration_group.add(decoration)
                    elif tile in [119, 124, 188]:  # second head of the level; distinguished to help w/ dialogue
                        decoration = d.Decoration(img, j * gv.TILE_SIZE, i * gv.TILE_SIZE, collidable=True, type="second dead_head")
                        gv.decoration_group.add(decoration)
                    elif tile in [132]:
                        decoration = d.Decoration(img, j * gv.TILE_SIZE, i * gv.TILE_SIZE, collidable=True, type="third dead_head")
                        gv.decoration_group.add(decoration)
                    elif tile == 63:  # mobius strip
                        tile_data[3] = [gv.img_list[tile], gv.img_list[tile+1]]
                        tile_data[4] = "flip each step"
                        tile_data[5] = 0  # image in list idx
                        gv.obstacle_list.append(tile_data)
                    elif tile == 65:  # water
                        water = wa.Water(img, j * gv.TILE_SIZE, i * gv.TILE_SIZE, flip_image=gv.img_list[tile+1])
                        gv.water_group.add(water)
                    elif tile == 67:  # book
                        decoration = d.Decoration(img, j * gv.TILE_SIZE, i * gv.TILE_SIZE, collidable=True, type="book")
                        gv.decoration_group.add(decoration)
                    elif tile == 68:  # shirt
                        decoration = d.Decoration(img, j * gv.TILE_SIZE, i * gv.TILE_SIZE, collidable=True, type="shirt")
                        gv.decoration_group.add(decoration)
                    elif tile == 69:  # non-updating ground
                        gv.obstacle_list.append(tile_data)
                    elif tile == 76:  # level exit
                        exit = e.Exit(img, j * gv.TILE_SIZE, i * gv.TILE_SIZE)
                        gv.exit_group.add(exit)
                    elif tile == 79:  # camera
                        decoration = d.Decoration(img, j * gv.TILE_SIZE, i * gv.TILE_SIZE, collidable=True, type="camera")
                        gv.decoration_group.add(decoration)
                    elif tile == 80:  # hot dog
                        decoration = d.Decoration(img, j * gv.TILE_SIZE, i * gv.TILE_SIZE, collidable=True, type="hot_dog")
                        gv.decoration_group.add(decoration)
                    elif 81 <= tile <= 92:  # cat bus
                        decoration = d.Decoration(img, j * gv.TILE_SIZE, i * gv.TILE_SIZE)
                        gv.decoration_group.add(decoration)
                    # non-tile numbers in CSV
                    elif tile == 94:  # create player/khatchig
                        if gv.level == 0:
                            gv.khatchig = c.Character("khatchig", j * gv.TILE_SIZE, i * gv.TILE_SIZE, 2.5, 7, self)
                        elif gv.level == 1:
                            gv.khatchig = c.Character("khatchig", j * gv.TILE_SIZE, i * gv.TILE_SIZE, 2.25, 6, self)
                        else:
                            gv.khatchig = c.Character("khatchig", j * gv.TILE_SIZE, i * gv.TILE_SIZE, 2, 5, self)
                    elif tile == 95:
                        hippie = c.Character("hippie", j * gv.TILE_SIZE, i * gv.TILE_SIZE, 2.5, 1, self)
                    elif tile == 96:
                        ufo = u.Ufo(600, 200, 2, 1)
                    elif tile == 97:
                        # make sure we aren't at a checkpoint away from the start of the board
                        if gv.bg_scroll == 0:
                            notkhatchig = c.Character("notkhatchig", j * gv.TILE_SIZE, i * gv.TILE_SIZE, 2.5, 6, self)
                    # non-collidable decoration tiles that look like collidable obstacles
                    elif tile == 100:  # nca logo
                        tile_data[3] = [gv.img_list[tile], gv.img_list[tile+1], gv.img_list[tile+2], gv.img_list[tile+3]]
                        tile_data[4] = "flip each step"
                        tile_data[5] = 0  # image list idx
                        gv.obstacle_list.append(tile_data)
                    elif tile == 104:
                        real = r.Real(j * gv.TILE_SIZE, i * gv.TILE_SIZE, 2, 1)
                        gv.real_group.add(real)
                    elif tile == 105:
                        cat = ca.Cat(j * gv.TILE_SIZE, i * gv.TILE_SIZE, gv.TILE_SIZE/32, 3)
                    elif 106 <= tile <= 111:  # food truck
                        decoration = d.Decoration(img, j * gv.TILE_SIZE, i * gv.TILE_SIZE, collidable=False, type="hot dog truck")
                        gv.decoration_group.add(decoration)
                    elif tile == 112:  # food truck ledge bottom
                        gv.obstacle_list.append(tile_data)
                    elif tile == 113:  # food truck ledge top
                        decoration = d.Decoration(img, j * gv.TILE_SIZE, i * gv.TILE_SIZE, collidable=True, type="flip on hot dog drop")
                        gv.decoration_group.add(decoration)
                    elif 115 <= tile <= 117:  # phone
                        if tile == 116:
                            decoration = d.Decoration(img, j * gv.TILE_SIZE, i * gv.TILE_SIZE, collidable=False, type="phone_bottom")
                            gv.decoration_group.add(decoration)
                        else:
                            decoration = d.Decoration(img, j * gv.TILE_SIZE, i * gv.TILE_SIZE, collidable=True, type="phone")
                            gv.decoration_group.add(decoration)
                    elif tile == 118:
                        blob = b.Blob(j * gv.TILE_SIZE, i * gv.TILE_SIZE, 2, 1)
                        gv.blob_group.add(blob)
                    elif tile == 126:  # dancing dead head
                        decoration = d.Decoration(img, j * gv.TILE_SIZE, i * gv.TILE_SIZE, collidable=True, type="flip dead_head",
                                                  flip_image=gv.img_list[tile + 2])
                        gv.decoration_group.add(decoration)
                    elif tile == 127:  # dancing dead head
                        decoration = d.Decoration(img, j * gv.TILE_SIZE, i * gv.TILE_SIZE, collidable=True, type="flip dead_head bottom",
                                                  flip_image=gv.img_list[tile + 2])
                        gv.decoration_group.add(decoration)
                    elif 135 <= tile <= 176:  # ground
                        gv.obstacle_list.append(tile_data)
                    elif tile == 177:  # mirror
                        decoration = d.Decoration(img, j * gv.TILE_SIZE, i * gv.TILE_SIZE, collidable=True, type="mirror")
                        gv.decoration_group.add(decoration)
                    elif 178 <= tile <= 185:  # mirror sides
                        decoration = d.Decoration(img, j * gv.TILE_SIZE, i * gv.TILE_SIZE, collidable=True, type="mirror side")
                        gv.decoration_group.add(decoration)
                    elif tile > 1000:  # to make an object a non-interacting decoration just add +1000 to the tile #
                        decoration = d.Decoration(img, j * gv.TILE_SIZE, i * gv.TILE_SIZE)
                        gv.decoration_group.add(decoration)
        return gv.khatchig, ufo, hippie, notkhatchig, cat  # real, cat

    # update rectangle positions and draw obstacle tiles that aren't in a sprite group
    def draw(self):
        for i, tile_data in enumerate(gv.obstacle_list):
            if gv.level == 2:
                tile_data[1][1] += int(gv.screen_scroll)  # y value of rectangle
                gv.screen.blit(tile_data[0], tile_data[1])
            else:
                tile_data[1][0] += gv.screen_scroll  # x value of rectangle
                gv.screen.blit(tile_data[0], tile_data[1])
