import pygame
import random
import itertools

import various_functions


class ParticleGridRoom:
    def __init__(self, kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def try_replace_particle(self):
        x, y = self.pos
        p_type = self.type_grid[x][y]
        for row in [[(i, j, self.type_grid[i][j]) for i in range(max(x - 1, 0), min(x + 2, self.length))] for j in
                    range(max(x - 1, 0), min(x + 2, self.length))]:
            for i, j, cell_type in row:
                if cell_type == self.copy_type[p_type]:
                    for row2 in [[(k, l, self.type_grid[k][l]) for k in range(max(x - 1, 0), min(x + 2, self.length))] for l in
                                 range(max(x - 1, 0), min(x + 2, self.length))]:
                        for k, l, cell_type2 in row2:
                            if cell_type2 == self.replace_type[p_type]:
                                self.type_grid[k][l] = self.copy_type[p_type]

    # each open adjacent cell is given a score representing the total pos/neg affinity within a rectangular radius
    def score_within_radius(self):
        x, y = self.pos
        p_type = self.type_grid[x][y]
        self.best_idx = self.pos
        best = -1000000
        tiebreak_set = [[x, y]]  # if there are no open cells, we don't want an empty set to choose from

        # only check cell score in adjacent cells if it's open, but then consider all cells in that cell's "radius" when determining score
        # could we vectorize this code in numpy or jax to speed it up?
        for row in [[(i, j) for i in range(max(x - 1, 0), min(x + 2, self.length)) if self.type_grid[i][j] == 0] for j in
                    range(max(y - 1, 0), min(y + 2, self.length))]:
            for i, j in row:
                score = 0
                cell_count = 0
                for row2 in [[(k, l, self.type_grid[k][l]) for k in range(max(i - self.radius, 0), min(i + self.radius + 1, self.length))]
                             for l in range(max(j - self.radius, 0), min(j + self.radius + 1, self.length))]:
                    for k, l, cell_type in row2:
                        cell_count += 1
                        if cell_type != 0:  # don't add the spurious affinity data associated with open cells (type 0)
                            if self.affinity[p_type][cell_type] == 1:
                                score += 1
                            else:
                                score -= 1
                # normalize score for edge (of grid) cases
                score = score / cell_count
                if score > best:
                    best = score
                    tiebreak_set = [[i, j]]
                elif score == best:
                    tiebreak_set.append([i, j])
        # break tie or choose only item
        best_cell = random.choice(range(len(tiebreak_set)))
        self.best_idx = tiebreak_set[best_cell]

    def move_particle(self):
        x, y = self.pos
        p_type = self.type_grid[x][y]

        # updates best_idx based on current position of particle
        self.score_within_radius()
        best_x, best_y = self.best_idx

        if x == best_x and y == best_y:
            pass  # the particle didn't find a better adjacent cell to move to
        else:  # move particle
            self.type_grid[best_x][best_y] = p_type
            self.type_grid[x][y] = 0

    # this is an asynchronous computation in the sense that not all particles update at each step
    # each step in the simulation updates a bunch of randomly selected particles
    def step(self):
        for t in range(int(0.2 * self.density * (self.length ** 2) // 1)):
            particles = [[x, y] for x, y in list(itertools.product(range(self.length), range(self.length))) if self.type_grid[x][y] != 0]
            rand_particle_idx = random.choice(range(len(particles)))
            self.pos = particles[rand_particle_idx]
            self.try_replace_particle()
            self.move_particle()

    def print(self, surface):
        self.printout = pygame.transform.scale(surface, (50, 66))
        self.counter = 0

    # def run(self):
    #     """ self-contained loop in main game loop """
    #
    #     img_flip = True
    #
    #     color_shift = random.uniform()
    #
    #     while gv.world_level == "particle_affinity_room":
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 pygame.quit()
    #             elif event.type == pygame.KEYDOWN:
    #                 if event.key == pygame.locals.K_SPACE:
    #                     gv.world_level = "top"
    #                     gv.door_sfx.play()
    #                 elif event.key == pygame.K_p:
    #                     self.print(gv.surf)
    #                 elif event.key == pygame.K_RETURN:
    #                     gv.switch_sfx.play()
    #                     self.reset = True
    #
    #         self.step()
    #
    #         # gv.surf = pygame.surfarray.make_surface(np.array(self.type_grid) / self.num_types * 255 * color_shift)
    #         gv.surf = pygame.surfarray.make_surface(self.type_grid / self.num_types * 255 * color_shift)
    #         gv.surf = pygame.transform.scale(gv.surf, (255, 170))
    #
    #         self.stars_counter += 0.1
    #         gv.screen.blit(gv.stars_img, [(self.stars_counter % gv.stars_img.get_width()) - gv.stars_img.get_width(), 155])
    #         gv.screen.blit(gv.stars_img, [self.stars_counter % gv.stars_img.get_width(), 155])
    #
    #         if pygame.time.get_ticks() - self.last_time_check > gv.ANIMATION_INTERVAL:
    #             self.last_time_check = pygame.time.get_ticks()
    #             img_flip = not img_flip
    #
    #         if img_flip:
    #             gv.screen.blit(gv.escher7_img, (0, 0))
    #         else:
    #             gv.screen.blit(gv.escher8_img, (0, 0))
    #
    #         gv.screen.blit(gv.surf, (70, 303))
    #
    #         if self.printout:
    #             self.counter += 1
    #             if self.counter % 30 == 0 and self.counter <= 30*64:
    #                 gv.printer_sfx.play()
    #             if self.counter >= 30*64 and self.first_sfx:
    #                 gv.success_sfx.play()
    #                 gv.to_do["print printout"] = True
    #                 self.first_sfx = False
    #                 if gv.holding_object == 98:
    #                     gv.in_briefcase["printout"] = True
    #                     gv.briefcase_open_sfx.play()
    #                 elif gv.holding_object == 99:
    #                     gv.holding_object = 186
    #                     for tile in gv.decoration_group:
    #                         if tile.type == "grass":
    #                             new_decoration = d.Decoration(gv.img_list[67], tile.rect.x, tile.rect.y, collidable=True, type="book")
    #                             tile.kill()
    #                             gv.decoration_group.add(new_decoration)
    #                             break
    #                 else:
    #                     gv.holding_object = 186
    #
    #             gv.screen.blit(gv.paper_img, (530, 445 - min(self.counter//30, 64)))
    #             gv.screen.blit(self.printout, (540, 450 - min(self.counter//30, 64)))
    #             gv.screen.blit(gv.printer_img, (490, 440))
    #         else:
    #             gv.screen.blit(gv.printer_img, (490, 440))
    #
    #         gv.screen.blit(gv.letter_box_img, (0, 0))
    #
    #         pygame.display.update()
    #
    #         if self.reset:
    #             # create()
    #             params = {"length": random.randint(20, 40),
    #                       "num_types": random.randint(3, 15),
    #                       "density": random.choice([i * 0.05 for i in range(3, 12)]),
    #                       "radius": random.choice([1, 2]),
    #                       "pos": [0, 0],
    #                       "best_idx": [0, 0],
    #                       "intro_complete": False,
    #                       "printout": None,
    #                       "first_sfx": True,
    #                       "reset": False}
    #
    #             params_dict = dict_creator(params)
    #             self.__init__(params_dict)
    #             self.run()


# type 0 represents a blank cell, which is not really a particle; some of idx/range() references below reflect this
def dict_creator(params):
    # initialize grid of particles
    params["type_grid"] = [random.choices(population=[i for i in range(params['num_types'] + 1)],
                                          weights=[1-params['density']] + [params['density']/params['num_types']]*params['num_types'],
                                          k=params['length']) for _ in range(params['length'])]

    # make particles randomly attracted to all types including their own type
    params["affinity"] = [random.choices(population=[0, 1], weights=[0.5, 0.5], k=params["num_types"] + 1)
                          for _ in range(params["num_types"] + 1)]

    # sim rule: can't copy self => remove type_index of self
    params["copy_type"] = [random.choice([i for i in range(params['num_types'] + 1) if i != type_idx and i != 0])
                           for type_idx in range(params['num_types'] + 1)]

    # sim rule: replace type also can't be the same type as the particle itself
    params["replace_type"] = [random.choice([i for i in range(1, params['num_types'] + 1) if i != type_idx and (
            i != params["copy_type"][type_idx])]) for type_idx in range(params['num_types'] + 1)]

    params["colors"] = various_functions.get_colors(params["num_types"])

    return params


def create():
    params = {"length": random.randint(20, 40),
              "num_types": random.randint(3, 15),
              "density": random.choice([i * 0.05 for i in range(3, 10)]),
              "radius": random.choice([1, 2]),
              "pos": [0, 0],
              "best_idx": [0, 0],
              # "intro_complete": False,
              "printout": None,
              "first_sfx": True,
              "reset": False,
              "stars_counter": 0,
              "last_time_check": pygame.time.get_ticks()}

    params_dict = dict_creator(params)
    return ParticleGridRoom(params_dict)
    # room.run()




