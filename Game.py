import pygame
import sys
import MapGen
import Player
import Gui
import random
import Asteroid
import database
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

def generate_new_asteroid():
    # Losujemy sektor (1 = lewy górny, 2 = górny środek-lewy, 3 = górny środek-prawy, 4 = prawy górny)
    sector = random.choice([1, 2, 3, 4])

    if sector == 1:
        x = 0
        y = random.uniform(0, HEIGHT / 2)
        x_speed = random.uniform(ASTEROID_SPEED_MIN, ASTEROID_SPEED_MAX)
        y_speed = random.uniform(ASTEROID_SPEED_MIN, ASTEROID_SPEED_MAX)
    elif sector == 2:
        x = random.uniform(0, WIDTH / 3)
        y = 0
        x_speed = random.uniform(ASTEROID_SPEED_MIN, ASTEROID_SPEED_MAX)
        y_speed = random.uniform(ASTEROID_SPEED_MIN, ASTEROID_SPEED_MAX)
    elif sector == 3:
        x = random.uniform(2 * WIDTH / 3, WIDTH)
        y = 0
        x_speed = random.uniform(-ASTEROID_SPEED_MAX, -ASTEROID_SPEED_MIN)
        y_speed = random.uniform(ASTEROID_SPEED_MIN, ASTEROID_SPEED_MAX)
    else:  # sector == 4
        x = WIDTH
        y = random.uniform(0, HEIGHT / 2)
        x_speed = random.uniform(-ASTEROID_SPEED_MAX, -ASTEROID_SPEED_MIN)
        y_speed = random.uniform(ASTEROID_SPEED_MIN, ASTEROID_SPEED_MAX)

    asteroid_type = random.choice(["BIG", "SMALL","SMALL","SMALL"])
    new_asteroid = Asteroid.Asteroid(x, y, x_speed, y_speed, asteroid_type)
    
    return new_asteroid

def start_mission(day,player):
    asteorides = False
    asteroid_delay = 0
    if (day >= ASTEROID_DAY):
        asteorides = True
        asteroid_delay = ASTEROID_BASIC_DELAY - day*50 if day<=30 else 500 

    # Mapa
    landing_zone_id, line_points = MapGen.generate_random_map(WIDTH, HEIGHT, day)
    draw_lines(line_points, landing_zone_id)

    player.x_speed = random.uniform(-SIDE_SPEED, SIDE_SPEED)  # Losowa prędkość boczna
    
    clock = pygame.time.Clock()
    last_asteroid_spawn_time = pygame.time.get_ticks()

    asteroids = []

    running = True
    while running:
        current_time = pygame.time.get_ticks()
        
        # Generowanie nowej asteroidy co określony czas
        if asteorides and current_time - last_asteroid_spawn_time > asteroid_delay:
            new_asteroid = generate_new_asteroid()
            asteroids.append(new_asteroid)
            last_asteroid_spawn_time = current_time

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
        collision_with_line = player.check_collision_with_line(line_points, landing_zone_id, LANDING_SPEED_LIMIT)

        # Sprawdzenie kolizji
        if collision_with_line == "collision":
            text = font.render("Loose", True, RED)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, text_rect)
            pygame.display.flip()
            pygame.time.delay(2000)
            running = False

        elif collision_with_line == "too fast":
            text = font.render("you hit the spot with brutal speed", True, ORANGE)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, text_rect)
            pygame.display.flip()
            pygame.time.delay(3000)
            running = False

        elif collision_with_line == "win":
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
        draw_lines(line_points, landing_zone_id)
        draw_info(player, LANDING_SPEED_LIMIT)

        # Rysowanie i aktualizacja asteroid
        for asteroid in asteroids:
            asteroid.update(DRAG, GRAVITY_FORCE)
            asteroid.draw(screen, GREY)
            collision_with_asteroid = player.check_collision_with_asteroid(asteroid)
            
            if collision_with_asteroid == "BIG_collision":
                text = font.render("Collision with big asteroid!", True, RED)
                text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                screen.blit(text, text_rect)
                pygame.display.flip()
                pygame.time.delay(2000)
                running = False
            
            if collision_with_asteroid == "SMALL_collision":
                    player.handle_asteroid_collision(asteroid)
                    asteroids.remove(asteroid)
            
            if asteroid.check_collision_with_line(line_points):
                asteroids.remove(asteroid)

        # Aktualizacja ekranu
        pygame.display.flip()

        # Ograniczenie liczby klatek na sekundę
        clock.tick(60)

    if collision_with_line in ["win", "collision", "too fast"]:
        return collision_with_line


def game_loop(day, player):
    current_menu = Gui.hangar_menu(screen, day)
    
    while current_menu in ["start_mission", "save_and_exit", "upgrades","black_market"]:
        if current_menu == "start_mission":
            start_mission(day, player)
            player.set_position(WIDTH // 2, START_HEIGHT, ENTRY_SPEED)
            day += 1
            current_menu = Gui.hangar_menu(screen, day)
        elif current_menu == "save_and_exit":
            slot = Gui.save_game_menu(screen)
            if slot is not None:
                database.save_game_state(slot, day, player)
                print("Zapisano grę i wyjście.")
                current_menu = Gui.main_menu(screen)
        elif current_menu == "upgrades":
            current_menu = Gui.upgrade_menu(screen, player)
            if current_menu == "hangar_menu":
                current_menu = Gui.hangar_menu(screen, day)
        elif current_menu == "black_market":
            current_menu = Gui.black_market_menu(screen, player)
            if current_menu == "hangar_menu":
                current_menu = Gui.hangar_menu(screen, day)
    
    return current_menu

def main():
    database.initialize_database()
    while True:
        current_menu = Gui.main_menu(screen)

        if current_menu == "new_game":
            day = 1
            player = Player.Player(WIDTH // 2, START_HEIGHT, ENTRY_SPEED)
            current_menu = game_loop(day, player)

        elif current_menu == "load_game":
            slot = Gui.load_game_menu(screen)
            if slot is not None:
                game_state = database.load_game_state(slot)
                if game_state:
                    day = game_state['day']
                    player = Player.Player(WIDTH // 2, START_HEIGHT, ENTRY_SPEED)
                    player.player_upgrades["Left_maneuvering_engine"] = game_state['upgrades']["Left_maneuvering_engine"]
                    player.player_upgrades["Right_maneuvering_engine"] = game_state['upgrades']["Right_maneuvering_engine"]
                    player.player_upgrades["Engine_efficiency"] = game_state['upgrades']["Engine_efficiency"]
                    player.player_upgrades["Engine_power"] = game_state['upgrades']["Engine_power"]
                    player.money = game_state['money']
                    current_menu = game_loop(day, player)
                else:
                    print("Nie można załadować gry. Brak zapisanego stanu gry.")



if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Kosmiczny Kurier Kombinant")
    font = pygame.font.Font(None, FONT_SIZE)
    main()
