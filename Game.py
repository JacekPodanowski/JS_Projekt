import pygame
import sys
import MapGen

# Inicjalizacja Pygame
pygame.init()

# Ustawienia okna
WIDTH, HEIGHT = 1280, 720
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN=(0,255,0)
PLAYER_SIZE = 10
FONT_SIZE = 40

# Utworzenie okna gry
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ruch gracza")

# startowa pozycja gracza
player_x = WIDTH // 2
player_y = HEIGHT // 4

# Ustawienia czcionki
font = pygame.font.Font(None, FONT_SIZE)

# Funkcja rysująca gracza
def draw_player(x, y):
    pygame.draw.circle(screen, RED, (x, y), PLAYER_SIZE)

landing_zone_id,line_points = MapGen.generate_random_map(WIDTH,HEIGHT,20)

def draw_line():
    pygame.draw.lines(screen, RED, False, line_points[:landing_zone_id], 3)
    pygame.draw.line(screen, GREEN, line_points[landing_zone_id-1],line_points[landing_zone_id], 5)
    pygame.draw.lines(screen, RED, False, line_points[landing_zone_id:], 3)


def check_collision_with_line(player_x, player_y, line_points):
    for i in range(len(line_points) - 1):
        x1, y1 = line_points[i]
        x2, y2 = line_points[i + 1]
        
        # czy gracz znajduje się nad linią
        if x1 <= player_x <= x2 or x2 <= player_x <= x1:
            line_y = y1 + (player_x - x1) * (y2 - y1) / (x2 - x1)
            if player_y >= line_y - PLAYER_SIZE:
                if i == landing_zone_id - 1:
                    return "win"  # Gracz wylądował na zielonej linii - wygrana
                else:
                    return "collision"  # Gracz koliduje z czerwoną linią
    return "no_collision"  # Brak kolizji


# Główna pętla gry
player_x_speed=0
player_y_speed=0
gravity_force=1
drag = 0.999

running = True
while running:
    # Obsługa zdarzeń
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Sprawdzenie wciśniętych klawiszy
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_y_speed -= 0.03
    if keys[pygame.K_s]:
        player_y_speed += 0.03
    if keys[pygame.K_a]:
        player_x_speed -= 0.03
    if keys[pygame.K_d]:
        player_x_speed += 0.03
        
    player_x=player_x+player_x_speed
    player_y=player_y+player_y_speed+gravity_force
    
    player_x_speed=player_x_speed*drag
    player_y_speed=player_y_speed*drag
    
    draw_line()
    
    # Sprawdzenie kolizji
    if check_collision_with_line(player_x, player_y,line_points)=="collision":
        text = font.render("Zderzenie !", True, RED)
        text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(2000)  # Czekaj 2 s przed zakończeniem gry
        running = False

    elif check_collision_with_line(player_x, player_y,line_points)=="win":
        text = font.render("Dobrze ;)", True, GREEN)
        text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(2000)  # Czekaj 2 s przed zakończeniem gry
        running = False

    # Wyczyszczenie ekranu
    screen.fill(BLACK)

    # Narysowanie gracza
    draw_player(player_x, player_y)
    draw_line()

    # Aktualizacja ekranu
    pygame.display.flip()

    # Ograniczenie liczby klatek na sekundę
    pygame.time.Clock().tick(30)

# Wyjście z programu
pygame.quit()
sys.exit()