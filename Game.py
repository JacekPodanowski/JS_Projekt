import pygame
import sys
import MapGen


class Player:
    PLAYER_SIZE = 10

    def __init__(self, x, y, fuel):
        self.x = x
        self.y = y
        self.x_speed = 0
        self.y_speed = 0
        self.fuel = fuel
        self.running = True

    def draw(self, screen):
        pygame.draw.circle(screen, GREY, (self.x, self.y), self.PLAYER_SIZE)

        leg_length = self.PLAYER_SIZE * 2
        leg_width = 3
        leg_height = 6

        left_leg = [(self.x - self.PLAYER_SIZE, self.y + self.PLAYER_SIZE),
                    (self.x - self.PLAYER_SIZE - leg_width, self.y + self.PLAYER_SIZE + leg_length),
                    (self.x - self.PLAYER_SIZE - leg_width, self.y + self.PLAYER_SIZE + leg_length + leg_height),
                    (self.x - self.PLAYER_SIZE + leg_width, self.y + self.PLAYER_SIZE + leg_length + leg_height),
                    (self.x - self.PLAYER_SIZE + leg_width, self.y + self.PLAYER_SIZE + leg_length),
                    (self.x - self.PLAYER_SIZE, self.y + self.PLAYER_SIZE)]

        right_leg = [(self.x + self.PLAYER_SIZE, self.y + self.PLAYER_SIZE),
                     (self.x + self.PLAYER_SIZE + leg_width, self.y + self.PLAYER_SIZE + leg_length),
                     (self.x + self.PLAYER_SIZE + leg_width, self.y + self.PLAYER_SIZE + leg_length + leg_height),
                     (self.x + self.PLAYER_SIZE - leg_width, self.y + self.PLAYER_SIZE + leg_length + leg_height),
                     (self.x + self.PLAYER_SIZE - leg_width, self.y + self.PLAYER_SIZE + leg_length),
                     (self.x + self.PLAYER_SIZE, self.y + self.PLAYER_SIZE)]

        pygame.draw.polygon(screen, RED, left_leg)
        pygame.draw.polygon(screen, RED, right_leg)

    def check_collision_with_line(self, line_points):
        leg_length = self.PLAYER_SIZE * 2
        leg_width = 3

        left_leg_x = self.x - self.PLAYER_SIZE - leg_width
        right_leg_x = self.x + self.PLAYER_SIZE + leg_width

        left_leg_y = self.y + self.PLAYER_SIZE + leg_length
        right_leg_y = self.y + self.PLAYER_SIZE + leg_length

        for i in range(len(line_points) - 1):
            x1, y1 = line_points[i]
            x2, y2 = line_points[i + 1]

            # Sprawdzenie czy linia przecina nogi lądownika
            for x, y in [(self.x, self.y), (left_leg_x, left_leg_y), (right_leg_x, right_leg_y)]:
                if x1 <= x <= x2 or x2 <= x <= x1:
                    line_y = y1 + (x - x1) * (y2 - y1) / (x2 - x1)
                    if y >= line_y:
                        if i == landing_zone_id - 1:
                            return "win"  # Gracz ląduje na zielonej linii - wygrana
                        else:
                            return "collision"  # Gracz ląduje na czerwonej linii - przegrana
        return "no_collision"  # Brak kolizji

    def calculate_fuel_usage(self):
        return abs(self.y_speed) / 2

    def move_up(self, fuel, calculate_fuel_usage):
        if fuel > 0:
            self.y_speed -= 0.03
            fuel -= calculate_fuel_usage()
        return fuel

    def move_down(self):
        self.y_speed += 0.03

    def move_left(self):
        self.x_speed -= 0.03

    def move_right(self):
        self.x_speed += 0.03

    def update(self, gravity, drag):
        self.x += self.x_speed
        self.y += self.y_speed + gravity
        self.x_speed *= drag
        self.y_speed *= drag


# Inicjalizacja Pygame
pygame.init()

# Ustawienia okna
WIDTH, HEIGHT = 1280, 720
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREY = (128, 128, 128)
FONT_SIZE = 40

# Utworzenie okna gry
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ruch gracza")

# Pozycja gracza
player = Player(WIDTH // 2, HEIGHT // 4, 100)

# Ustawienia czcionki
font = pygame.font.Font(None, FONT_SIZE)

landing_zone_id, line_points = MapGen.generate_random_map(WIDTH, HEIGHT, 20)


def draw_line():
    pygame.draw.lines(screen, RED, False, line_points[:landing_zone_id], 3)
    pygame.draw.line(screen, GREEN, line_points[landing_zone_id - 1], line_points[landing_zone_id], 5)
    pygame.draw.lines(screen, RED, False, line_points[landing_zone_id:], 3)


def draw_fuel_bar(fuel):
    font = pygame.font.Font(None, 24)
    text = font.render("Fuel", True, WHITE)
    screen.blit(text, (10, 2))
    pygame.draw.rect(screen, GREEN, (10, 20, fuel, 20))
    pygame.draw.rect(screen, GREY, (10, 20, fuel, 20), 2)


# Główna pętla gry
player.player_x_speed = 0
player.player_y_speed = 0
gravity_force = 1
drag = 0.999
fuel = 100

running = True
while running:
    # Obsługa zdarzeń
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Sprawdzenie wciśniętych klawiszy
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_w] or keys[pygame.K_UP]) and fuel > 0:
        fuel = player.move_up(fuel, player.calculate_fuel_usage)

    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        player.move_down()

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player.move_left()

    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player.move_right()

    player.update(gravity_force, drag)
    collision = player.check_collision_with_line(line_points)

    draw_line()

    # Sprawdzenie kolizji
    if collision == "collision":
        text = font.render("Zderzenie !", True, RED)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(2000)  # Czekaj 2 sekundy przed zakończeniem gry
        running = False

    elif collision == "win":
        text = font.render("Dobrze ;)", True, GREEN)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(2000)  # Czekaj 2 sekundy przed zakończeniem gry
        running = False

    # Wyczyszczenie ekranu
    screen.fill(BLACK)

    # Narysowanie gracza
    player.draw(screen)
    draw_line()
    draw_fuel_bar(fuel)

    # Aktualizacja ekranu
    pygame.display.flip()

    # Ograniczenie liczby klatek na sekundę
    pygame.time.Clock().tick(30)

# Wyjście z programu
pygame.quit()
sys.exit()