import math
import pygame
from Settings import *


class Player:
    def __init__(self, x, y,entry_speed):
        self.x = x
        self.y = y
        self.x_speed = 0
        self.y_speed = entry_speed
        self.rotation_speed = ROTATION_SPEED
        self.max_fuel = MAX_FUEL
        self.fuel = self.max_fuel
        self.money= START_MONEY
        self.angle = 0
        self.running = True
        self.player_upgrades = {
            "Left_maneuvering_engine": False,
            "Right_maneuvering_engine": False,
            "Engine_efficiency": False,
            "Engine_power": False
        }

    def upgrade(self, upgrade_name):
        if self.money < UPGRADE_COST:
            return "No money"
        if upgrade_name in self.player_upgrades:
            self.player_upgrades[upgrade_name] = True
            print(f"{upgrade_name} has been upgraded!")
            self.money -= UPGRADE_COST
            return f"{upgrade_name}"
        else:
            print(f"Upgrade {upgrade_name} does not exist.")
            return "No upgrade"

    def rotation_point(self, x, y, angle):
        x -= self.x
        y -= self.y
        qx = x * math.cos(angle) - y * math.sin(angle)
        qy = x * math.sin(angle) + y * math.cos(angle)
        x = qx + self.x
        y = qy + self.y
        return x, y

    def draw(self, screen,bodyColor, legColor):
        pygame.draw.circle(screen, bodyColor, (self.x, self.y), PLAYER_SIZE)

        leg_length = PLAYER_SIZE
        leg_width = 4

        left_leg = [(self.x - PLAYER_SIZE, self.y + PLAYER_SIZE),
                    (self.x - PLAYER_SIZE - leg_width, self.y + PLAYER_SIZE + leg_length),
                    (self.x - PLAYER_SIZE - leg_width, self.y + PLAYER_SIZE + leg_length),
                    (self.x - PLAYER_SIZE + leg_width, self.y + PLAYER_SIZE + leg_length),
                    (self.x - PLAYER_SIZE + leg_width, self.y + PLAYER_SIZE + leg_length),
                    (self.x - PLAYER_SIZE, self.y + PLAYER_SIZE)]

        right_leg = [(self.x + PLAYER_SIZE, self.y + PLAYER_SIZE),
                    (self.x + PLAYER_SIZE + leg_width, self.y + PLAYER_SIZE + leg_length),
                    (self.x + PLAYER_SIZE + leg_width, self.y + PLAYER_SIZE + leg_length),
                    (self.x + PLAYER_SIZE - leg_width, self.y + PLAYER_SIZE + leg_length),
                    (self.x + PLAYER_SIZE - leg_width, self.y + PLAYER_SIZE + leg_length),
                    (self.x + PLAYER_SIZE, self.y + PLAYER_SIZE)]

        left_leg = [self.rotation_point(x, y, self.angle) for x, y in left_leg]
        right_leg = [self.rotation_point(x, y, self.angle) for x, y in right_leg]

        pygame.draw.polygon(screen, legColor, left_leg)
        pygame.draw.polygon(screen, legColor, right_leg)

    def check_collision_with_line(self, line_points,landing_zone_id,landing_speed_limit):
        leg_length = PLAYER_SIZE
        leg_width = 4

        left_leg = [(self.x - PLAYER_SIZE - leg_width, self.y + PLAYER_SIZE + leg_length)]
        right_leg = [(self.x + PLAYER_SIZE + leg_width, self.y + PLAYER_SIZE + leg_length)]

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

    def check_collision_with_asteroid(self, asteroid):
        distance = math.sqrt((self.x - asteroid.x) ** 2 + (self.y - asteroid.y) ** 2)
        if distance < PLAYER_SIZE + asteroid.size:
            if asteroid.type == "BIG":
                return "BIG_collision"
            else:
                return "SMALL_collision"
        return "NO_collision"

    def handle_asteroid_collision(self, asteroid):
        self.x_speed += asteroid.x_speed * SMALL_ASTEROID_TRANSFERRED_SPEED 
        self.y_speed += asteroid.y_speed * SMALL_ASTEROID_TRANSFERRED_SPEED

    def adjust_thrust(self, fuel):
        if fuel > 0:
            
            if(self.player_upgrades["Engine_power"]):
                self.x_speed += THRUST_MULTIPLAYER * math.sin(self.angle) * self.rotation_speed
                self.y_speed -= THRUST_MULTIPLAYER * math.cos(self.angle) * self.rotation_speed
            else:
                self.x_speed += math.sin(self.angle) * self.rotation_speed
                self.y_speed -= math.cos(self.angle) * self.rotation_speed
            
            if(self.player_upgrades["Engine_efficiency"]):
                fuel -= FUEL_USE_MULTIPLAYER * FUEL_USE
            else:
                fuel -= FUEL_USE
        return fuel

    def rotate_left(self):
        if(self.player_upgrades["Right_maneuvering_engine"]):
            self.angle -= ROTATION_MULTIPLAYER * self.rotation_speed
        else:
            self.angle -= self.rotation_speed

    def rotate_right(self):
        if(self.player_upgrades["Left_maneuvering_engine"]):
            self.angle += ROTATION_MULTIPLAYER * self.rotation_speed
        else:
            self.angle += self.rotation_speed

    def update(self, drag, gravity):
        self.y_speed += gravity
        self.x += self.x_speed
        self.y += self.y_speed
        self.x_speed *= drag
        self.y_speed *= drag

    def set_position(self,x, y,entry_speed):
        self.x = x
        self.y = y  
        self.x_speed = 0
        self.y_speed = entry_speed
        self.angle = 0
        self.fuel = self.max_fuel
        self.running = True