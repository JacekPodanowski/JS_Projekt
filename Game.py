import pygame
import sys
import MapGen
import Player
import Gui
from Settings import *

def draw_lines(line_points,landing_zone_id):
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
    text_speed_x = font.render(f"Speed X: {speed_x:.2f}", True, WHITE)
    screen.blit(text_speed_x, (10, 50))

    # kontrola predkosci
    if speed_y > landing_speed_limit:
        speed_y_color = RED
    else:
        speed_y_color = WHITE

    # y speed
    text_speed_y = font.render(f"Speed Y: {(-speed_y):.2f}", True, speed_y_color)
    screen.blit(text_speed_y, (10, 70))

    # fuel bar
    pygame.draw.rect(screen, GREEN, (10, 20, int(fuel), 20))
    pygame.draw.rect(screen, GREY, (10, 20, int(fuel), 20), 2)

def start_mission(day):
    
    #mapa
    landing_zone_id, line_points = MapGen.generate_random_map(WIDTH, HEIGHT,day)
    draw_lines(line_points,landing_zone_id)
    player = Player.Player(WIDTH // 2, -50, ENTRY_SPEED)  # startowa pozycja gracza i prędkość wlotowa

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

        player.update(DRAG, GRAVITY_FORCE)
        collision = player.check_collision_with_line(line_points, landing_zone_id, LANDING_SPEED_LIMIT)



        # Sprawdzenie kolizji
        if collision == "collision":
            text = font.render("Loose", True, RED)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, text_rect)
            pygame.display.flip()
            pygame.time.delay(2000)
            running = False

        elif collision == "too fast":
            text = font.render("you hit the spot with brutal speed", True, ORANGE)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, text_rect)
            pygame.display.flip()
            pygame.time.delay(3000)
            running = False

        elif collision == "win":
            text = font.render("win", True, GREEN)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, text_rect)
            pygame.display.flip()
            pygame.time.delay(2000)
            running = False

        # Wyczyszczenie ekranu
        screen.fill(BLACK)

        # Narysowanie gracza
        player.draw(screen, GREY, RED)
        draw_lines(line_points,landing_zone_id)
        draw_info(player, LANDING_SPEED_LIMIT)

        # Aktualizacja ekranu
        pygame.display.flip()

        # Ograniczenie liczby klatek na sekundę
        pygame.time.Clock().tick(60)

    if collision in ["win", "collision","too fast"]:
        return collision

def main():
    day = 1
    while True:
        current_menu = Gui.main_menu(screen)

        if current_menu == "new_game":
            current_menu = Gui.hangar_menu(screen, day)

            while current_menu in ["start_mission", "save_and_exit", "upgrades"]:
                if current_menu == "start_mission":
                    start_mission(day)
                    day += 1
                    current_menu = Gui.hangar_menu(screen, day)
                elif current_menu == "save_and_exit":
                    # Zapis
                    print("Zapisano grę i wyjście.")
                    current_menu = Gui.main_menu(screen)
                elif current_menu == "upgrades":
                    current_menu = Gui.upgrade_menu(screen)
                    if current_menu == "hangar_menu":
                        current_menu = Gui.hangar_menu(screen, day)

        elif current_menu == "load_game":
            # Ładowanie gry...
            print("Ładowanie gry...")

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Kosmiczny Kurier Kombinant")
    font = pygame.font.Font(None, FONT_SIZE)
    main()
