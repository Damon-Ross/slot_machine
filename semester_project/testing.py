import random
import pygame
from sys import exit

WIDTH = HEIGHT = 800

reel = ['cherry', 'cherry', 'cherry', 'melon', 'melon', 'melon',
        'lemon', 'lemon', 'lemon', 'apple', 'apple', 'apple', 'star', 'star', 'jackpot']
images = ['cherry', 'melon', 'lemon', 'apple', 'star', 'jackpot']
image_y_coord = [-270, -150, -30, 80, 210, 240]

balance = 100

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Slot Machine')
pygame_icon = pygame.image.load('slot_machine.png')
pygame.display.set_icon(pygame_icon)

backg_colour = pygame.Surface((WIDTH, HEIGHT))
backg_colour.fill('White')

slot_machine_image = pygame.image.load('slot_machine_enhanced.png')
lever_base = pygame.image.load('lever_base.png')
lever_head = pygame.image.load('lever_head.png')
lever_rod = pygame.image.load('lever_rod.png')

scroll_image = pygame.image.load('reel.png').convert_alpha()
reel_width, reel_height = scroll_image.get_size()

font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 30)

current_screen = "start"

start_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 60)
play_again_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 60)

def draw_start_screen():
    screen.fill((255, 255, 255))
    title_text = font.render("Welcome to the Slot Machine!", True, (0, 0, 0))
    instructions = [
        "You start with 100 coins.",
        "Press the lever to gamble 5 coins per spin.",
        "Match three symbols to win coins.",
        "Jackpots give extra rewards!",
    ]
    start_button_text = font.render("Start", True, (255, 255, 255))
    
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 200))
    
    for i, line in enumerate(instructions):
        instruction_text = small_font.render(line, True, (0, 0, 0))
        screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 2 - 120 + i * 30))
    
    pygame.draw.rect(screen, (0, 128, 0), start_button_rect)
    screen.blit(start_button_text, (start_button_rect.centerx - start_button_text.get_width() // 2, start_button_rect.centery - start_button_text.get_height() // 2))

def draw_game_over_screen():
    screen.fill((255, 255, 255))
    game_over_text = font.render("You have no more money!", True, (255, 0, 0))
    play_again_text = font.render("Play Again", True, (255, 255, 255))
    
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 100))
    pygame.draw.rect(screen, (0, 128, 0), play_again_button_rect)
    screen.blit(play_again_text, (play_again_button_rect.centerx - play_again_text.get_width() // 2,
                                  play_again_button_rect.centery - play_again_text.get_height() // 2))

def reel_result():
    result = random.choice(reel)
    return images.index(result), image_y_coord[images.index(result)]

area_rect = pygame.Rect(564, 291, 84, 258)

scroll_speed = 30
reel_x_positions = [189, 315, 439]
reel_y_positions = [225, 225, 225]
reel_final_positions = [None, None, None]
is_reel_stopped = [False, False, False]

clock = pygame.time.Clock()
is_animating = False
start_time = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if current_screen == "start":
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if start_button_rect.collidepoint(mouse_x, mouse_y):
                    current_screen = "main"

        elif current_screen == "main":
            if balance < 0:
                current_screen = "game_over"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if area_rect.collidepoint(mouse_x, mouse_y) and not is_animating:
                    is_animating = True
                    balance -= 5
                    start_time = pygame.time.get_ticks()
                    reel_y_positions = [225, 225, 225]
                    is_reel_stopped = [False, False, False]
                    reel_final_positions = [reel_result() for _ in range(3)]

        elif current_screen == "game_over":
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if play_again_button_rect.collidepoint(mouse_x, mouse_y):
                    balance = 100
                    current_screen = "main"

    if current_screen == "start":
        draw_start_screen()
    elif current_screen == "main":
        screen.blit(backg_colour, (0, 0))
        if is_animating:
            for i in range(3):
                if not is_reel_stopped[i]:
                    reel_y_positions[i] += scroll_speed
                    if reel_y_positions[i] >= reel_height:
                        reel_y_positions[i] -= reel_height
                    if pygame.time.get_ticks() - start_time > (i + 1) * 1000:
                        is_reel_stopped[i] = True
                        reel_y_positions[i] = reel_final_positions[i][1]

            if all(is_reel_stopped):
                is_animating = False

        for i in range(3):
            screen.blit(scroll_image, (reel_x_positions[i], reel_y_positions[i] + reel_height))
            screen.blit(scroll_image, (reel_x_positions[i], reel_y_positions[i]))
            screen.blit(scroll_image, (reel_x_positions[i], reel_y_positions[i] - reel_height))

        screen.blit(slot_machine_image, (0, 0))
        screen.blit(lever_base, (564, 291))
        screen.blit(lever_head, (564, 291))
        screen.blit(lever_rod, (564, 368))

        balance_text = font.render(f"Balance: {balance}", True, (0, 0, 0))
        screen.blit(balance_text, (20, 20))

    elif current_screen == "game_over":
        draw_game_over_screen()

    pygame.display.update()
    clock.tick(60)