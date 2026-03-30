import pygame
import math
import global_vars as gv


class Node:
    def __init__(self, coordinates: list[float]) -> None:
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.z = coordinates[2]


class Edge:
    def __init__(self, start: int, stop: int) -> None:
        self.start = start
        self.stop = stop


class Wireframe:
    """# the wireframe code was adapted from petercollingridge.go.uk
    https://www.petercollingridge.co.uk/tutorials/3d/pygame/"""
    def __init__(self):
        self.nodes = []
        self.edges = []

    def addNodes(self, nodeList):
        for node in nodeList:
            self.nodes.append(Node(node))

    def addEdges(self, edgeList):
        for (start, stop) in edgeList:
            self.edges.append(Edge(self.nodes[start], self.nodes[stop]))

    def translate(self, axis, d):
        """ Translate each node of a wireframe by d along a given axis. """
        if axis in ['x', 'y', 'z']:
            for node in self.nodes:
                setattr(node, axis, getattr(node, axis) + d)

    def scale(self, center, scale):
        """ Scale the wireframe from the center of the screen. """
        center_x, center_y = center
        for node in self.nodes:
            node.x = center_x + scale * (node.x - center_x)
            node.y = center_y + scale * (node.y - center_y)
            node.z *= scale

    def findcenter(self):
        """ Find the center of the wireframe. """
        num_nodes = len(self.nodes)
        meanX = sum([node.x for node in self.nodes]) / num_nodes
        meanY = sum([node.y for node in self.nodes]) / num_nodes
        meanZ = sum([node.z for node in self.nodes]) / num_nodes
        return (meanX, meanY, meanZ)

    def rotateX(self, center, radians):
        cx, cy, cz = center
        for node in self.nodes:
            y = node.y - cy
            z = node.z - cz
            d = math.hypot(y, z)
            theta = math.atan2(y, z) + radians
            node.z = cz + d * math.cos(theta)
            node.y = cy + d * math.sin(theta)

    def rotateY(self, center, radians):
        cx, cy, cz = center
        for node in self.nodes:
            x = node.x - cx
            z = node.z - cz
            d = math.hypot(x, z)
            theta = math.atan2(x, z) + radians
            node.z = cz + d * math.cos(theta)
            node.x = cx + d * math.sin(theta)

    def rotateZ(self, center, radians):
        cx, cy, cz = center
        for node in self.nodes:
            x = node.x - cx
            y = node.y - cy
            d = math.hypot(y, x)
            theta = math.atan2(y, x) + radians
            node.x = cx + d * math.cos(theta)
            node.y = cy + d * math.sin(theta)

    def outputNodes(self):
        print("\n --- Nodes --- ")
        for i, node in enumerate(self.nodes):
            print(" %d: (%.2f, %.2f, %.2f)" % (i, node.x, node.y, node.z))

    def outputEdges(self):
        print("\n --- Edges --- ")
        for i, edge in enumerate(self.edges):
            print(" %d: (%.2f, %.2f, %.2f)" % (i, edge.start.x, edge.start.y, edge.start.z))
            print("to (%.2f, %.2f, %.2f)" % (edge.stop.x, edge.stop.y, edge.stop.z))


class ProjectionViewer:
    """ Displays 3D objects on a Pygame screen """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.last_time_check = pygame.time.get_ticks()
        self.wireframes = {}
        self.displayNodes = True
        self.displayEdges = True
        self.nodeColor = (11,252,3)
        self.edgeColor = (200,200,200)
        self.nodeRadius = 1
        self.display_obj = "cube"
        self.intro_complete = False
        self.cube_match = False
        self.tet_match = False
        self.solution_points_cube = [(486, 388), (465, 423), (504, 424), (482, 459), (528, 391), (545, 427), (524, 461)]
        self.solution_points_tetrahedron = [(645, 390), (609, 425), (680, 425), (646, 460)]

    def changeObj(self, wireframe_obj):
        self.display_obj = wireframe_obj

    def addWireframe(self, name, wireframe):
        """ Add a named wireframe object. """
        self.wireframes[name] = wireframe

    def translateAll(self, axis, d):
        """ Translate all wireframes along a given axis by d units. """
        for wireframe in self.wireframes.values():
            wireframe.translate(axis, d)

    def scaleAll(self, scale):
        """ Scale all wireframes by a given scale, centerd on the center of the screen. """
        center_x = self.width / 2
        center_y = self.height / 2
        for wireframe in self.wireframes.values():
            wireframe.scale((center_x, center_y), scale)

    def rotateAll(self, axis, theta):
        """ Rotate all wireframe about their center, along a given axis by a given angle. """
        rotateFunction = 'rotate' + axis
        for wireframe in self.wireframes.values():
            center = wireframe.findcenter()
            getattr(wireframe, rotateFunction)(center, theta)

    # for level 1 background, not the computer room
    def run_bg(self, trans_dist, reverse=1):
        self.translateAll("x", trans_dist/3)
        self.translateAll("y", trans_dist)
        self.rotateAll('X', 0.01*reverse)
        self.rotateAll('Y', 0.01*reverse)
        self.rotateAll('Z', 0.01*reverse)
        self.display()

    def display(self):
        """ Draw the wireframes on the screen. """
        if self.displayEdges:
            for edge in self.wireframes[self.display_obj].edges:
                # pygame.draw.aaline(gv.screen, self.edgeColor, (edge.start.x, edge.start.y), (edge.stop.x, edge.stop.y), 1)
                pygame.draw.aaline(gv.screen, self.edgeColor, (edge.start.x, edge.start.y), (edge.stop.x, edge.stop.y))
        if self.displayNodes:
            # print()
            points_match = []
            for node in self.wireframes[self.display_obj].nodes:
                pygame.draw.circle(gv.screen, self.nodeColor, (int(node.x), int(node.y)), self.nodeRadius, 0)
                # print(node.x, node.y)
                if self.point_matches(node.x, node.y):
                    points_match.append(True)
                else:
                    points_match.append(False)
            if all(points_match):
                if self.display_obj == "cube":
                    if not self.cube_match:
                        gv.success_sfx.play()
                        gv.to_do["connect points"] = True
                        self.cube_match = True
                        gv.world_level = "movie"
                        gv.movie_idx = 11
                else:
                    if not self.tet_match:
                        gv.success_sfx.play()
                        gv.to_do["connect points"] = True
                        self.tet_match = True
                        gv.world_level = "movie"
                        gv.movie_idx = 11

    def point_matches(self, x, y):
        if self.display_obj == "cube":
            for point in self.solution_points_cube:
                if abs(point[0]-x) < 5 and abs(point[1]-y) < 5:
                    return True
        else:
            for point in self.solution_points_tetrahedron:
                if abs(point[0]-x) < 5 and abs(point[1]-y) < 5:
                    return True
        return False


key_to_function = {
    pygame.K_LEFT:   (lambda x: x.translateAll('x', -10)),
    pygame.K_RIGHT:  (lambda x: x.translateAll('x',  10)),
    pygame.K_DOWN:   (lambda x: x.translateAll('y',  10)),
    pygame.K_UP:     (lambda x: x.translateAll('y', -10)),
    pygame.K_EQUALS: (lambda x: x.changeObj("cube")),
    pygame.K_MINUS: (lambda x: x.changeObj("tetrahedron")),
    pygame.K_q: (lambda x: x.rotateAll('X', 0.1)),
    pygame.K_w: (lambda x: x.rotateAll('X', -0.1)),
    pygame.K_a: (lambda x: x.rotateAll('Y', 0.1)),
    pygame.K_s: (lambda x: x.rotateAll('Y', -0.1)),
    pygame.K_z: (lambda x: x.rotateAll('Z', 0.1)),
    pygame.K_x: (lambda x: x.rotateAll('Z', -0.1))}


def initialize(x_pos: int = 0, y_pos: int = 0, scale: float = 1) -> ProjectionViewer:
    pv = ProjectionViewer(200, 150)

    cube = Wireframe()
    cube.addNodes([(x, y, z) for x in (200, 250) for y in (400, 450) for z in (150, 200)])
    cube.addEdges([(n, n + 4) for n in range(0, 4)] + [(n, n + 1) for n in range(0, 8, 2)] + [(n, n + 2) for n in (0, 1, 4, 5)])

    tetrahedron = Wireframe()
    tetrahedron.addNodes([(200, 400, 0), (200, 450, 50), (250, 450, 0), (250, 400, 50)])
    tetrahedron.addEdges([(a, b) for a in range(4) for b in range(4) if a != b])

    pv.addWireframe('tetrahedron', tetrahedron)
    pv.addWireframe('cube', cube)
    pv.translateAll("x", x_pos)
    pv.translateAll("y", y_pos)
    pv.scaleAll(scale)
    return pv


# initialized for 2nd level background design (function used outside of computer room => bad file name.)
proj_viewer = initialize()
# tetrahedrons rotating in two directions
proj_viewer1 = initialize(600, 600 + 1600, 0.25)
proj_viewer2 = initialize(600, 600 + 1600, 0.25)
# cubes rotating in two directions
proj_viewer3 = initialize(200, 600 + 1600, 0.25)
proj_viewer4 = initialize(200, 600 + 1600, 0.25)
# two cubes and one tetrahedron
proj_viewer5 = initialize(400, 400 + 1600, 0.25)
proj_viewer6 = initialize(400, 400 + 1600, 0.25)
proj_viewer7 = initialize(400, 400 + 1600, 0.25)


# def create(pv=proj_viewer):
#     pv.run()


def create_bg(pv=proj_viewer1, obj="tetrahedron", trans_dist=0, reverse=1):
    pv.changeObj(obj)
    pv.run_bg(trans_dist, reverse)

