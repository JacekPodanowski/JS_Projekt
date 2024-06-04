import math
import pygame
import sys
import MapGen
from Settings import *


class Player:
    PLAYER_SIZE = 10

    def __init__(self, x, y,entry_speed):
        self.x = x
        self.y = y
        self.x_speed = 0
        self.y_speed = entry_speed
        self.rotation_speed = 0.02
        self.max_fuel = 100
        self.fuel = self.max_fuel
        self.money= 0
        self.angle = 0
        self.running = True

    def rotation_point(self, x, y, angle):
        x -= self.x
        y -= self.y
        qx = x * math.cos(angle) - y * math.sin(angle)
        qy = x * math.sin(angle) + y * math.cos(angle)
        x = qx + self.x
        y = qy + self.y
        return x, y

    def draw(self, screen,bodyColor, legColor):
        pygame.draw.circle(screen, bodyColor, (self.x, self.y), self.PLAYER_SIZE)

        leg_length = self.PLAYER_SIZE
        leg_width = 4

        left_leg = [(self.x - self.PLAYER_SIZE, self.y + self.PLAYER_SIZE),
                    (self.x - self.PLAYER_SIZE - leg_width, self.y + self.PLAYER_SIZE + leg_length),
                    (self.x - self.PLAYER_SIZE - leg_width, self.y + self.PLAYER_SIZE + leg_length),
                    (self.x - self.PLAYER_SIZE + leg_width, self.y + self.PLAYER_SIZE + leg_length),
                    (self.x - self.PLAYER_SIZE + leg_width, self.y + self.PLAYER_SIZE + leg_length),
                    (self.x - self.PLAYER_SIZE, self.y + self.PLAYER_SIZE)]

        right_leg = [(self.x + self.PLAYER_SIZE, self.y + self.PLAYER_SIZE),
                    (self.x + self.PLAYER_SIZE + leg_width, self.y + self.PLAYER_SIZE + leg_length),
                    (self.x + self.PLAYER_SIZE + leg_width, self.y + self.PLAYER_SIZE + leg_length),
                    (self.x + self.PLAYER_SIZE - leg_width, self.y + self.PLAYER_SIZE + leg_length),
                    (self.x + self.PLAYER_SIZE - leg_width, self.y + self.PLAYER_SIZE + leg_length),
                    (self.x + self.PLAYER_SIZE, self.y + self.PLAYER_SIZE)]

        left_leg = [self.rotation_point(x, y, self.angle) for x, y in left_leg]
        right_leg = [self.rotation_point(x, y, self.angle) for x, y in right_leg]

        pygame.draw.polygon(screen, legColor, left_leg)
        pygame.draw.polygon(screen, legColor, right_leg)

    def check_collision_with_line(self, line_points,landing_zone_id,landing_speed_limit):
        leg_length = self.PLAYER_SIZE
        leg_width = 4

        left_leg = [(self.x - self.PLAYER_SIZE - leg_width, self.y + self.PLAYER_SIZE + leg_length)]
        right_leg = [(self.x + self.PLAYER_SIZE + leg_width, self.y + self.PLAYER_SIZE + leg_length)]

        left_leg = [self.rotation_point(x, y, self.angle) for x, y in left_leg]
        right_leg = [self.rotation_point(x, y, self.angle) for x, y in right_leg]

        for i in range(len(line_points) - 1):
            x1, y1 = line_points[i]
            x2, y2 = line_points[i + 1]

            # Sprawdzenie czy linia przecina nogi lądownika
            for leg in [left_leg[0], right_leg[0]]:
                x, y = leg
                if x1 <= x <= x2 or x2 <= x <= x1:
                    line_y = y1 + (x - x1) * (y2 - y1) / (x2 - x1)
                    if y >= line_y:
                        if i == landing_zone_id - 1:
                            if(self.y_speed>landing_speed_limit):
                                return "too fast"
                            return "win"
                        else:
                            return "collision"

            # Sprawdzenie czy linia przecina kadłub lądownika
            x, y = self.x, self.y
            if x1 <= x <= x2 or x2 <= x <= x1:
                line_y = y1 + (x - x1) * (y2 - y1) / (x2 - x1)
                if y >= line_y:
                    return "collision"

        return "no_collision"

    def adjust_thrust(self, fuel):
        if fuel > 0:
            self.x_speed += math.sin(self.angle) * self.rotation_speed
            self.y_speed -= math.cos(self.angle) * self.rotation_speed
            fuel -= FUEL_USE
        return fuel

    def rotate_left(self):
        self.angle -= self.rotation_speed

    def rotate_right(self):
        self.angle += self.rotation_speed

    def update(self, drag, gravity):
        self.y_speed += gravity
        self.x += self.x_speed
        self.y += self.y_speed
        self.x_speed *= drag
        self.y_speed *= drag