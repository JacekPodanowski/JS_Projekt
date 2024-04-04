import random
import sys
import pygame
import numpy as np

class Field:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.canEnter = False

    def display(self):
        print("Pole",end="")


class UnlockedField(Field):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.canEnter = True

    def display(self):
        print(".",end="")


class LockedField(Field):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.canEnter = False

    def display(self):
        print("x",end="")

class VoidField(Field):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.canEnter = False

    def display(self):
        print("o",end="")
        
class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.fields = []

        for y in range(height):
            row = []
            for x in range(width):
                if x == 0 or x == width - 1 or y == 0 or y == height - 1:
                    field = VoidField(x, y)  # Pustka na brzegach
                elif x == 1 or x == width - 2 or y == 1 or y == height - 2:
                    field = LockedField(x, y)  # Zablokowane ściany
                else:
                    field = UnlockedField(x, y) 
                row.append(field)
            self.fields.append(row)

    def display(self):
        for row in self.fields:
            for field in row:
                field.display()
            print()  


