import pygame
import sys
from Settings import * 

def main_menu(screen):
    title_font = pygame.font.Font(None, 150) 
    subtitle_font = pygame.font.Font(None, 50)
    menu_font = pygame.font.Font(None, 74)
    quit_font = pygame.font.Font(None, 36)

    while True:
        screen.fill(BLACK)
        title = title_font.render("KKK", True, RED)
        subtitle = subtitle_font.render("Kosmiczny Kurier Kombinant", True, WHITE)
        new_game_button = menu_font.render("Nowa Gra", True, GREEN)
        load_game_button = menu_font.render("Wczytaj Grę", True, GREEN)
        quit_button = quit_font.render("Wyjdź", True, RED)

        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 4 - 50))  # Tytuł przesunięty w górę
        subtitle_rect = subtitle.get_rect(center=(WIDTH // 2, HEIGHT // 4 + 25))  # Podtytuł bliżej tytułu
        new_game_rect = new_game_button.get_rect(center=(WIDTH // 2 - 150, HEIGHT // 2))  # Po lewej
        load_game_rect = load_game_button.get_rect(center=(WIDTH // 2 + 150, HEIGHT // 2))  # Po prawej
        quit_rect = quit_button.get_rect(bottomleft=(10, HEIGHT - 10))  # Lewy dolny róg

        screen.blit(title, title_rect)
        screen.blit(subtitle, subtitle_rect)
        screen.blit(new_game_button, new_game_rect)
        screen.blit(load_game_button, load_game_rect)
        screen.blit(quit_button, quit_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if new_game_rect.collidepoint(event.pos):
                    return "new_game"
                if load_game_rect.collidepoint(event.pos):
                    return "load_game"
                if quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

def hangar_menu(screen, day):
    menu_font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 36)
    while True:
        screen.fill(BLACK)
        title = menu_font.render(f"Hangar - Dzień {day}", True, WHITE)
        start_mission_button = small_font.render("Odpal Misję", True, GREEN)
        save_and_exit_button = small_font.render("Wyjdź z zapisem", True, RED)
        upgrades_button = small_font.render("Ulepszenia", True, GREEN)

        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        start_mission_rect = start_mission_button.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        save_and_exit_rect = save_and_exit_button.get_rect(bottomleft=(10, HEIGHT - 10))
        upgrades_rect = upgrades_button.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

        screen.blit(title, title_rect)
        screen.blit(start_mission_button, start_mission_rect)
        screen.blit(save_and_exit_button, save_and_exit_rect)
        screen.blit(upgrades_button, upgrades_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_mission_rect.collidepoint(event.pos):
                    return "start_mission"
                if save_and_exit_rect.collidepoint(event.pos):
                    return "save_and_exit"
                if upgrades_rect.collidepoint(event.pos):
                    return "upgrades"

        pygame.display.flip()

def upgrade_menu(screen, player):
    small_font = pygame.font.Font(None, 36)
    while True:
        screen.fill(BLACK)
        rect_width, rect_height = 300, 100
        spacing = 20

        left_engine_rect = pygame.Rect(WIDTH // 4 - rect_width // 2, HEIGHT // 4 - rect_height // 2, rect_width, rect_height)
        right_engine_rect = pygame.Rect(3 * WIDTH // 4 - rect_width // 2, HEIGHT // 4 - rect_height // 2, rect_width, rect_height)
        engine_efficiency_rect = pygame.Rect(WIDTH // 2 - rect_width // 2, HEIGHT // 2 - rect_height // 2 + rect_height + spacing, rect_width, rect_height)
        engine_power_rect = pygame.Rect(WIDTH // 2 - rect_width // 2, HEIGHT // 2 - rect_height // 2 + 2 * (rect_height + spacing), rect_width, rect_height)

        quit_button = small_font.render("Wróć do hangaru", True, RED)
        quit_rect = quit_button.get_rect(bottomleft=(10, HEIGHT - 10))

        if not player.player_upgrades["Left_maneuvering_engine"]:
            color_left_engine = RED
        else:
            color_left_engine = GREEN

        if not player.player_upgrades["Right_maneuvering_engine"]:
            color_right_engine = RED
        else:
            color_right_engine = GREEN

        if not player.player_upgrades["Engine_efficiency"]:
            color_fuel_tank = RED
        else:
            color_fuel_tank = GREEN

        if not player.player_upgrades["Engine_power"]:
            color_main_engine = RED
        else:
            color_main_engine = GREEN

        pygame.draw.rect(screen, color_left_engine, left_engine_rect)
        pygame.draw.rect(screen, color_right_engine, right_engine_rect)
        pygame.draw.rect(screen, color_fuel_tank, engine_efficiency_rect)
        pygame.draw.rect(screen, color_main_engine, engine_power_rect)

        left_engine_label = small_font.render("Lewy Silnik Manewrowy", True, WHITE)
        right_engine_label = small_font.render("Prawy Silnik Manewrowy", True, WHITE)
        engine_efficiency_label = small_font.render("Efektywność Silnika", True, WHITE)
        engine_power_label = small_font.render("Moc Silnika", True, WHITE)

        screen.blit(left_engine_label, left_engine_label.get_rect(center=left_engine_rect.center))
        screen.blit(right_engine_label, right_engine_label.get_rect(center=right_engine_rect.center))
        screen.blit(engine_efficiency_label, engine_efficiency_label.get_rect(center=engine_efficiency_rect.center))
        screen.blit(engine_power_label, engine_power_label.get_rect(center=engine_power_rect.center))

        screen.blit(quit_button, quit_rect)

        money_label = small_font.render(f"Stan konta: {player.money} ¥", True, WHITE)
        money_rect = money_label.get_rect(topleft=(10, 10))
        screen.blit(money_label, money_rect)
        
        upgrade_cost_label = small_font.render(f"Koszt ulepszenia: {UPGRADE_COST} ¥", True, WHITE)
        upgrade_cost_rect = upgrade_cost_label.get_rect(midbottom=(WIDTH // 2, HEIGHT - 10))
        screen.blit(upgrade_cost_label, upgrade_cost_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if left_engine_rect.collidepoint(event.pos) and not player.player_upgrades["Left_maneuvering_engine"]:
                    player.upgrade("Left_maneuvering_engine")
                if right_engine_rect.collidepoint(event.pos) and not player.player_upgrades["Right_maneuvering_engine"]:
                    player.upgrade("Right_maneuvering_engine")
                if engine_efficiency_rect.collidepoint(event.pos) and not player.player_upgrades["Engine_efficiency"]:
                    player.upgrade("Engine_efficiency")
                if engine_power_rect.collidepoint(event.pos) and not player.player_upgrades["Engine_power"]:
                    player.upgrade("Engine_power")
                if quit_rect.collidepoint(event.pos):
                    return "hangar_menu"

        pygame.display.flip()
