import random
import pygame
from sys import exit

WIDTH = HEIGHT = 800

reel = ['cherry', 'cherry', 'cherry', 'melon', 'melon', 'melon','lemon', 'lemon', 'lemon', 'apple', 'apple', 'apple', 'star', 'star', 'jackpot']
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


def reel_result():
    result = random.choice(reel)
    return images.index(result), image_y_coord[images.index(result)]

slot_machine_image = pygame.image.load('slot_machine_enhanced.png')
lever_base = pygame.image.load('lever_base.png')
lever_head = pygame.image.load('lever_head.png')
lever_rod = pygame.image.load('lever_rod.png')

area_rect = pygame.Rect(564, 291, 84, 258)

scroll_speed = 30
scroll_image = pygame.image.load('reel.png').convert_alpha()
reel_width, reel_height = scroll_image.get_size()

reel_x_positions = [189, 315, 439]
reel_y_positions = [225, 225, 225]
reel_final_positions = [None, None, None]
is_reel_stopped = [False, False, False]

clock = pygame.time.Clock()
is_animating = False
start_time = 0


win = False
jackpot = False
message_flag = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN and balance >0:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if area_rect.collidepoint(mouse_x, mouse_y) and not is_animating:
                is_animating = True
                message_flag = True
                balance -= 5
                start_time = pygame.time.get_ticks()
                reel_y_positions = [225, 225, 225]
                is_reel_stopped = [False, False, False]
                
                if balance <= 20:
                    reel_final_positions[0] = reel_result()
                    chance = random.randint(0, 3)
                    if chance ==0:
                        reel_final_positions[1] = reel_final_positions[2] = reel_final_positions[0]
                else:
                    reel_final_positions = [reel_result() for _ in range(3)]
                
                if (reel_final_positions[0][0] == reel_final_positions[1][0]== reel_final_positions[2][0]):
                    if images[reel_final_positions[0][0]] == 'jackpot':
                        jackpot = True
                    else:
                        win = True


    screen.blit(backg_colour, (0, 0))

    if balance == 0:
        font = pygame.font.Font(None, 100)
        game_over_text = font.render("Game Over!", True, (255, 0, 0))
        restart_text = pygame.font.Font(None, 50).render("Press ESC to Quit", True, (0, 0, 0))
        screen.blit(game_over_text, (WIDTH // 2 - 200, HEIGHT // 2 - 100))
        screen.blit(restart_text, (WIDTH // 2 - 150, HEIGHT // 2))

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
            results = [pos[0] for pos in reel_final_positions]


    for i in range(3):
        screen.blit(scroll_image, (reel_x_positions[i], reel_y_positions[i] + reel_height))
        screen.blit(scroll_image, (reel_x_positions[i], reel_y_positions[i]))
        screen.blit(scroll_image, (reel_x_positions[i], reel_y_positions[i] - reel_height))

    screen.blit(slot_machine_image, (0, 0))
    screen.blit(lever_base, (564, 291))
    screen.blit(lever_head, (564, 291))
    screen.blit(lever_rod, (564, 368))

    if not is_animating and all(is_reel_stopped) and message_flag:
        if jackpot:
            balance += 500  
            print("Jackpot! You won 500 coins!")
            jackpot = False
        elif win:
            balance += 50  
            print("You won 50 coins!")
            win = False
        else:
            print("No win this time.")
        message_flag = False

    font = pygame.font.Font(None, 50)
    balance_text = font.render(f"Balance: {balance}", True, (0, 0, 0))
    screen.blit(balance_text, (20, 20))

    pygame.display.update()
    clock.tick(60)
