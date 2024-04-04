import pygame
import sys
import MapGen
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

class MapRenderer:
    def __init__(self, map, cell_size, Player_x, Player_y, padding=2):
        self.map = map
        self.cell_size = cell_size
        self.padding = padding
        self.screen_width = map.width * (cell_size + padding) - padding  
        self.screen_height = map.height * (cell_size + padding) - padding  
        
        self.player_pos = (Player_x, Player_y) 
        map.fields[Player_x][Player_y] = MapGen.PlayerField(Player_x, Player_y)
        
        # Liczba klatek animacji
        self.animation_frames = 30
        self.current_frame = 0
        
        self.move_delay = 300  # Opóźnienie między ruchami gracza
        self.last_move_time = 0  
        
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
                    
                elif isinstance(field, MapGen.PlayerField):
                    # Interpolacja pośredniego rozmiaru gracza w trakcie animacji
                    player_size = self.cell_size * (self.animation_frames - self.current_frame) / self.animation_frames
                    player_rect = pygame.Rect(rect.centerx - player_size / 2, rect.centery - player_size / 2, player_size, player_size)
                    pygame.draw.rect(self.screen, GREEN, player_rect)  # Rysowanie pola z animowanym graczem
                    pygame.draw.rect(self.screen, WHITE, player_rect, 1)
                
                elif isinstance(field, MapGen.LockedField):
                    pygame.draw.rect(self.screen, WHITE, rect)  # Rysowanie zablokowanego pola
                
                else:
                    pygame.draw.rect(self.screen, BLACK, rect)  # Rysowanie odblokowanego pola
                    pygame.draw.rect(self.screen, WHITE, rect, 1) 

        pygame.display.flip()

    def move_player(self, dx, dy):
        
        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time > self.move_delay:
            new_x = self.player_pos[0] + dx
            new_y = self.player_pos[1] + dy
            if isinstance(self.map.fields[new_y][new_x], MapGen.UnlockedField):
                # Zmniejszanie stopniowo rozmiaru gracza na polu, z którego odchodzi
                for frame in range(self.animation_frames):
                    self.current_frame = frame
                    self.render()
                
                # Aktualizacja pozycji gracza i renderowanie na nowej pozycji
                self.map.fields[self.player_pos[1]][self.player_pos[0]] = MapGen.UnlockedField(self.player_pos[0], self.player_pos[1])
                self.player_pos = (new_x, new_y)
                self.map.fields[self.player_pos[1]][self.player_pos[0]] = MapGen.PlayerField(self.player_pos[0], self.player_pos[1])
                
                # Powiększanie stopniowo rozmiaru gracza na nowym polu
                for frame in range(self.animation_frames,0,-1):
                    self.current_frame = frame
                    self.render()
                
                self.current_frame = 0
                self.last_move_time = current_time

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.move_player(0, -1)
                elif event.key == pygame.K_DOWN:
                    self.move_player(0, 1)
                elif event.key == pygame.K_LEFT:
                    self.move_player(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    self.move_player(1, 0)

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            clock.tick(30)  

            self.handle_events()
            self.render()
