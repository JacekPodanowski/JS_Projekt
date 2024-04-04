import pygame
import sys
import MapGen
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class MapRenderer:
    def __init__(self, map, cell_size, padding=2):
        self.map = map
        self.cell_size = cell_size
        self.padding = padding
        self.screen_width = map.width * (cell_size + padding) - padding  
        self.screen_height = map.height * (cell_size + padding) - padding  

        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Labirynt")

    def render(self):
        self.screen.fill(BLACK)

        for y, row in enumerate(self.map.fields):
            for x, field in enumerate(row):
                rect = pygame.Rect(x * (self.cell_size + self.padding), y * (self.cell_size + self.padding),self.cell_size, self.cell_size)
                
                if isinstance(field, MapGen.VoidField):
                    pygame.draw.rect(self.screen, BLACK, rect)  # Pustka
                    # Generowanie szumu na polach typu VoidField
                    if random.random() < 0.25:
                        dot_size = 1
                        dot_x = random.randint(rect.left, rect.right - dot_size)
                        dot_y = random.randint(rect.top, rect.bottom - dot_size)
                        pygame.draw.circle(self.screen, WHITE, (dot_x, dot_y), dot_size)
                
                elif isinstance(field, MapGen.LockedField):
                    pygame.draw.rect(self.screen, WHITE, rect)  # Rysowanie zablokowanego pola
                
                else:
                    pygame.draw.rect(self.screen, BLACK, rect)  # Rysowanie odblokowanego pola
                    pygame.draw.rect(self.screen, WHITE, rect, 1) 

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.render()

        pygame.quit()

