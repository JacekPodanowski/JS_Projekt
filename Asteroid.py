import pygame
import math
from Settings import *

class Asteroid:
    def __init__(self, x, y, x_speed, y_speed, type):
        self.x = x
        self.y = y
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.type= type
        if  type=="BIG" :
            self.size = BIG_ASTEROID_SIZE
        elif type=="SMALL" :
            self.size = SMALL_ASTEROID_SIZE
        else:
            print("wrong size parameter")
            self.size = 0
    
    def draw(self, screen, bodyColor):
        pygame.draw.circle(screen, bodyColor, (self.x, self.y), self.size)
    
    def check_collision_with_line(self, line_points):
        for i in range(len(line_points) - 1):
            x1, y1 = line_points[i]
            x2, y2 = line_points[i + 1]
            x, y = self.x, self.y
            
            if x1 <= x <= x2 or x2 <= x <= x1:
                line_y = y1 + (x - x1) * (y2 - y1) / (x2 - x1)
                if y >= line_y:
                    return True
        return False
    
    def update(self, drag, gravity):
        self.y_speed += gravity
        self.x += self.x_speed
        self.y += self.y_speed
        self.x_speed *= drag
        self.y_speed *= drag