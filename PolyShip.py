import math
import time
import sys
## pip show pygame
## pygame path follows Location:
## escape \ characters as necessary
sys.path.append("c:\\users\\neil\\appdata\\local\\packages\\pythonsoftwarefoundation.python.3.7_qbz5n2kfra8p0\\localcache\\local-packages\\python37\\site-packages")
import pygame

# Global Constants

HEIGHT = 600
WIDTH = 800

# Ignore these 3 functions. Scroll down for the relevant code.

def create_background(width, height):
        colors = [(255, 255, 255), (212, 212, 212)]
        background = pygame.Surface((width, height))
        tile_width = 20
        y = 0
        while y < height:
                x = 0
                while x < width:
                        row = y // tile_width
                        col = x // tile_width
                        pygame.draw.rect(
                                background, 
                                colors[(row + col) % 2],
                                pygame.Rect(x, y, tile_width, tile_width))
                        x += tile_width
                y += tile_width
        return background

def is_trying_to_quit(event):
        pressed_keys = pygame.key.get_pressed()
        alt_pressed = pressed_keys[pygame.K_LALT] or pressed_keys[pygame.K_RALT]
        x_button = event.type == pygame.QUIT
        altF4 = alt_pressed and event.type == pygame.KEYDOWN and event.key == pygame.K_F4
        escape = event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        return x_button or altF4 or escape

def run_demos(width, height, fps):
        pygame.init()
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('press space to see next demo')
        background = create_background(width, height)
        clock = pygame.time.Clock()
        demos = [
                do_line_demo
                ]
        the_world_is_a_happy_place = 0
        while True:
                the_world_is_a_happy_place += 1
                for event in pygame.event.get():
                        if is_trying_to_quit(event):
                                return
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                                demos = demos[1:]
                screen.blit(background, (0, 0))
                if len(demos) == 0:
                        return
                demos[0](screen, the_world_is_a_happy_place)
                pygame.display.flip()
                clock.tick(fps)

## Normal Functions lifted from tuinbels, Sept 2003, https://blenderartists.org/t/getting-face-normals-from-python/309648/3

# vector substration
def vecsub(a, b):
    return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]

# vector crossproduct
def veccross(x, y):
    v = [0, 0, 0]
    v[0] = x[1]*y[2] - x[2]*y[1]
    v[1] = x[2]*y[0] - x[0]*y[2]
    v[2] = x[0]*y[1] - x[1]*y[0]
    return v

# calculate normal from 3 verts
def Normal(v0, v1, v2):
    return veccross(vecsub(v0, v1),vecsub(v0, v2))

# calculate normal from 4 verts
# found in the blender sources in arithb.c 
# (bl-blender\blender\source\blender\blenlib\intern\arithb.c)
def Normal4(v0, v1, v2, v3):
    return veccross(vecsub(v0, v2),vecsub(v1, v3))

def rotate_3d_points(points, angle_x, angle_y, angle_z):
        new_points = []
        for point in points:
                x = point[0]
                y = point[1]
                z = point[2]
                new_y = y * math.cos(angle_x) - z * math.sin(angle_x)
                new_z = y * math.sin(angle_x) + z * math.cos(angle_x)
                y = new_y
                # isn't math fun, kids?
                z = new_z
                new_x = x * math.cos(angle_y) - z * math.sin(angle_y)
                new_z = x * math.sin(angle_y) + z * math.cos(angle_y)
                x = new_x
                z = new_z
                new_x = x * math.cos(angle_z) - y * math.sin(angle_z)
                new_y = x * math.sin(angle_z) + y * math.cos(angle_z)
                x = new_x
                y = new_y
                new_points.append([x, y, z])
        return new_points

##
##      Problem: Polygons must be drawn back to front to avoid visual glitching
##      Problem: There is no trivial way to determine which polygon should be in front
##
##      Hypothesis: It should be adequate to prove that the vertices of one polygon fall
##              entirely on one side of the plane of another polygon.


def layer_polygons(polygons):
        polygons_plus_midpoint = []
        polygons_plus_midpoint_sorted = []

        for polygon in polygons:
                count = 0
                width_sum = 0
                height_sum = 0
                depth_sum = 0

                # sum the x, y, and z coordinates
                for vertex in polygon:
                        width_sum += vertex[0]
                        height_sum += vertex[1]
                        depth_sum += vertex[2]
                        count += 1

                # Calculate the midpoint of the polygon
                x = width_sum / count
                y = height_sum / count
                z = depth_sum / count

                polygons_plus_midpoint.append(( (polygon),(x,y,z) ))

        for polygon in polygons_plus_midpoint:
                ## colliderect() to test if two rectangles overlap
                ##
                pass

        return polygons_plus_midpoint_sorted

def do_line_demo(surface, counter):
        color = (0, 0, 0) # black
        cube_points = [
                [0, 2, 0],              #Nose
                [.5, 1, .5],            #Base of Nosecone
                [-.5, 1, .5],
                [-.5, 1, -.5],
                [.5, 1, -.5],
                [.5, -1.5, .25],        #Back End
                [.5, -1.5, -.25],
                [-.5, -1.5, .25],
                [-.5, -1.5, -.25],
                [.5, 1, 0],             #Right Wing
                [.5, -1, 0],
                [2, -1.75, -.25],
                [-.5, 1, 0],            #Left Wing
                [-.5, -1, 0],
                [-2, -1.75, -.25],
                [0, 0, .4],             #Vertical Stabilizer
                [0, -1.5, .25],
                [0, -1.75, 1]
                
                ]
                
        connections = [
                (0, 1),
                (0, 2),
                (0, 3),
                (0, 4),
                (1, 2),
                (2, 3),
                (3, 4),
                (4, 1),
                (1, 5),
                (2, 7),
                (3, 8),
                (4, 6),
                (5, 7),
                (7, 8),
                (8, 6),
                (6, 5),
                (9, 10),
                (10, 11),
                (11, 9),
                (12, 13),
                (13, 14),
                (14, 12),
                (15, 16),
                (16, 17),
                (17, 15)
                ]

        polygons = [
                
                ((0, 2, 3),(144,144,144)),      #Left Front
                ((0, 3, 4),(90, 90, 90)),       #Bottom Front
                ((0, 4, 1),(144,144,144)),      #Right Front
                ((0, 1, 2),(0, 0, 255)),        #Top Front
                ((1, 2, 7, 5),(192,192,192)),   #Top
                ((2, 3, 8, 7),(128,128,128)),   #Right
                ((3, 4, 6, 8),(64, 64, 64)),    #Bottom
                ((4, 1, 5, 6),(128,128,128)),   #Left
                ((5, 6, 8, 7),(255,185,0)),     #Engine
                ((9, 10, 11),(128,0,0)),        #Right Wing
                ((12, 13, 14),(0,0,128)),       #Left Wing
                ((15, 16, 17),(0,128,0))        #Vertical Stabilizer
                ]
                
        t = counter * 2 * 3.14159 / 60 # this angle is 1 rotation per second
        
        # rotate about x axis every 2 seconds
        # rotate about y axis every 4 seconds
        # rotate about z axis every 6 seconds
        points = rotate_3d_points(cube_points, t / 2, t / 4, t / 6)
        flattened_points = []
        for point in points:
                flattened_points.append(
                        (point[0] * (1 + 1.0 / (point[2] + 3)),
                         point[1] * (1 + 1.0 / (point[2] + 3))))
        
        for con in connections:
                p1 = flattened_points[con[0]]
                p2 = flattened_points[con[1]]
                x1 = p1[0] * 60 + WIDTH/2
                y1 = p1[1] * 60 + HEIGHT/2
                x2 = p2[0] * 60 + WIDTH/2
                y2 = p2[1] * 60 + HEIGHT/2
                
                # This is the only line that really matters
                pygame.draw.line(surface, color, (x1, y1), (x2, y2), 4)

        for pol in polygons:
                vertices = []
                for p in pol[0]:
                        p1 = flattened_points[p]
                        x1 = p1[0] * 60 + WIDTH/2
                        y1 = p1[1] * 60 + HEIGHT/2
                        vertices.append((x1, y1))
                #
                #
                #       NEXT STEP: SORTING POLYGON DRAW ORDER
                #
                #
                # Need to sort polygons back to front before drawing!
                pygame.draw.polygon(surface, pol[1], vertices, 0)
                
        
run_demos(WIDTH, HEIGHT, 30)
