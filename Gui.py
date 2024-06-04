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

        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        start_mission_rect = start_mission_button.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        save_and_exit_rect = save_and_exit_button.get_rect(bottomleft=(10, HEIGHT - 10))

        screen.blit(title, title_rect)
        screen.blit(start_mission_button, start_mission_rect)
        screen.blit(save_and_exit_button, save_and_exit_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_mission_rect.collidepoint(event.pos):
                    return "start_mission"  # Rozpocznij misję
                if save_and_exit_rect.collidepoint(event.pos):
                    return "save_and_exit"  # Zapisz i wyjdź

        pygame.display.flip()
