import math
import pygame
import sys
import MapGen
import Player

pygame.init()

# Ustawienia okna
WIDTH, HEIGHT = 1280, 720
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREY = (128, 128, 128)
ORANGE = (255,165,0) 
FONT_SIZE = 40

# Utworzenie okna gry
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ruch gracza")


# Ustawienia czcionki
font = pygame.font.Font(None, FONT_SIZE)

#mapa
landing_zone_id, line_points = MapGen.generate_random_map(WIDTH, HEIGHT, 20, 30)

def draw_line():
    pygame.draw.lines(screen, RED, False, line_points[:landing_zone_id], 3)
    pygame.draw.line(screen, GREEN, line_points[landing_zone_id - 1], line_points[landing_zone_id], 5)
    pygame.draw.lines(screen, RED, False, line_points[landing_zone_id:], 3)


def draw_info(player, landing_speed_limit):
    fuel, max_fuel = player.fuel, player.max_fuel
    speed_x, speed_y = player.x_speed, player.y_speed
    
    font = pygame.font.Font(None, 24)
    
    # stan paliwa
    text_fuel_amount = font.render(f"Fuel: {int(fuel)}/{int(max_fuel)}", True, WHITE)
    screen.blit(text_fuel_amount, (10, 2))
    
    # x speed
    text_speed_x = font.render(f"Speed X: {speed_x:.3f}", True, WHITE)
    screen.blit(text_speed_x, (10, 50))
    
    # kontrola predkosci
    if speed_y > landing_speed_limit:
        speed_y_color = RED
    else:
        speed_y_color = WHITE

    # y speed
    text_speed_y = font.render(f"Speed Y: {(-speed_y):.3f}", True, speed_y_color)
    screen.blit(text_speed_y, (10, 70))
    
    # fuel bar
    pygame.draw.rect(screen, GREEN, (10, 20, int(fuel), 20))
    pygame.draw.rect(screen, GREY, (10, 20, int(fuel), 20), 2)





# Główna pętla gry
gravity_force = 0.003
entry_speed = 1
drag = 0.999
player = Player.Player(WIDTH // 2, -100, entry_speed) #startowa pozycja gracza i prędkośc wlotowa
landing_speed_limit= 1

running = True
while running:
    # Obsługa zdarzeń
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Sprawdzenie wciśniętych klawiszy
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_w] or keys[pygame.K_UP]) and player.fuel > 0:
        player.fuel = player.adjust_thrust(player.fuel)

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player.rotate_left()

    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player.rotate_right()

    player.update(drag,gravity_force)
    collision = player.check_collision_with_line(line_points,landing_zone_id,landing_speed_limit)

    draw_line()

    # Sprawdzenie kolizji
    if collision == "collision":
        text = font.render("Loose", True, RED)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(2000)  # Czekaj 2 sekundy przed zakończeniem gry
        running = False

    elif collision == "too fast":
        text = font.render("you hit the spot with brutal speed", True, ORANGE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(3000)  # Czekaj 3 sekundy przed zakończeniem gry
        running = False
        
    elif collision == "win":
        text = font.render("win", True, GREEN)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(2000)  # Czekaj 2 sekundy przed zakończeniem gry
        running = False

    # Wyczyszczenie ekranu
    screen.fill(BLACK)

    # Narysowanie gracza
    player.draw(screen,GREY,RED)
    draw_line()
    draw_info(player,landing_speed_limit)

    # Aktualizacja ekranu
    pygame.display.flip()

    # Ograniczenie liczby klatek na sekundę
    pygame.time.Clock().tick(60)

# Wyjście z programu
pygame.quit()
sys.exit()