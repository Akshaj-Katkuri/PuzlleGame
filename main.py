import pygame
from pygame import Surface
import sys


# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BUTTON_WIDTH, BUTTON_HEIGHT = 3/17 * WIDTH, 1/11 * HEIGHT
LEVEL_BUTTON_COLOR = (0, 128, 255)
LEVEL_HOVER_COLOR = (0, 255, 255)
LEVEL_LOCKED_COLOR = (128, 128, 128)
LEVEL_1_IMAGE_WIDTH, LEVEL_1_IMAGE_HEIGHT = 353, 344
TEXT_COLOR = (255, 255, 255)
BG_COLOR = (28, 170, 156)
LEVEL_3_IMAGE_WIDTH, LEVEL_3_IMAGE_HEIGHT = 992, 985

# Images
wrong_image = pygame.image.load("Red_X.svg.png")
wrong_image = pygame.transform.scale(wrong_image, (.1 * WIDTH, .1 * HEIGHT))
right_image = pygame.image.load("Green_check.svg.png")
right_image = pygame.transform.scale(right_image, (.1 * WIDTH, .1 * HEIGHT))
lvl1_image = pygame.image.load("level_1.png")
lvl1_image = pygame.transform.scale(lvl1_image, (LEVEL_1_IMAGE_WIDTH, LEVEL_1_IMAGE_HEIGHT))
lvl3_image = pygame.image.load("chesspuzlle.png")
lvl3_image = pygame.transform.scale(lvl3_image, (LEVEL_3_IMAGE_WIDTH/3, LEVEL_3_IMAGE_HEIGHT/3))

# User info
levels_unlocked = [1]

# screen info
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen_state = 'main_menu'
pygame.display.set_caption("Puzzle Game Level Selector")

# Font setup
font = pygame.font.Font(None, 40)

user_input = ""

# Function to draw buttons
def draw_button(text, x, y, unlocked):
    # Draw the button
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if not unlocked: # If the level is locked, draw a grey button
        pygame.draw.rect(screen, LEVEL_LOCKED_COLOR, (x, y, BUTTON_WIDTH, BUTTON_HEIGHT))
    elif x < mouse_x < x + BUTTON_WIDTH and y < mouse_y < y + BUTTON_HEIGHT:
        pygame.draw.rect(screen, LEVEL_HOVER_COLOR, (x, y, BUTTON_WIDTH, BUTTON_HEIGHT))
    else:
        pygame.draw.rect(screen, LEVEL_BUTTON_COLOR, (x, y, BUTTON_WIDTH, BUTTON_HEIGHT))
  
    # Render text and place it on the button
    text_surface = font.render(text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(x + BUTTON_WIDTH // 2, y + BUTTON_HEIGHT // 2))
    screen.blit(text_surface, text_rect)

def draw_level_buttons():
    for x in range(4):
        for y in range(5):
            draw_button(f"Level {x*5+y+1}", 1/17 * WIDTH + x*4/17 * WIDTH, 2*y*BUTTON_HEIGHT + BUTTON_HEIGHT, x*5+y+1 in levels_unlocked)

# Main menu loop
def main_menu():
    global screen_state

    screen.fill(BG_COLOR)
    draw_level_buttons()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            for x in range(4):
                for y in range(5):
                    level = x * 5 + y + 1
                    button_x = 1/17 * WIDTH + x * 4/17 * WIDTH
                    button_y = 2 * y * BUTTON_HEIGHT + BUTTON_HEIGHT
                    if button_x < mouse_x < button_x + BUTTON_WIDTH and button_y < mouse_y < button_y + BUTTON_HEIGHT:
                        if level in levels_unlocked:
                            set_screen_state(f'level_{level}')


def level_1():
    screen.fill(BG_COLOR)
    x = (WIDTH-LEVEL_1_IMAGE_WIDTH)/2
    y = (HEIGHT-LEVEL_1_IMAGE_HEIGHT)/2
    screen.blit(lvl1_image, ((WIDTH-LEVEL_1_IMAGE_WIDTH)/2, (HEIGHT-LEVEL_1_IMAGE_HEIGHT)/2))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                set_screen_state('main_menu')
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if (x) < mouse_x < (1/3 * LEVEL_1_IMAGE_WIDTH + x) and (2/3 * LEVEL_1_IMAGE_HEIGHT + y) < mouse_y < (LEVEL_1_IMAGE_HEIGHT + y):
                popup(right_image, 1000)
                unlock_level(2)
                set_screen_state('main_menu')
            else: 
                popup(wrong_image, 1000)

def handle_user_input(clue_text: list[str]):
    global user_input
    user_input = ""
    input_box_y = int(HEIGHT * 0.5)  # Static y-coordinate proportional to screen height
    input_box = pygame.Rect(WIDTH//2 - 100, input_box_y, 200, 40)
    clue_font = pygame.font.Font(None, 36)

    while True:
        screen.fill(BG_COLOR)
        
        # Display the clue text
        display_clue(clue_text)
        
        # Draw the input box and user input
        pygame.draw.rect(screen, LEVEL_BUTTON_COLOR, input_box, 2)
        input_text = clue_font.render(user_input.upper(), True, TEXT_COLOR)
        screen.blit(input_text, (input_box.x+5, input_box.y+5))
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    set_screen_state('main_menu')
                    return ""
                elif event.key == pygame.K_RETURN:
                    return user_input
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode

def display_clue(clue_text: list[str]):
    clue_font = pygame.font.Font(None, 36)
    for i, line in enumerate(clue_text):
        text_surface = clue_font.render(line, True, TEXT_COLOR)
        screen.blit(text_surface, (WIDTH//2 - text_surface.get_width()//2, HEIGHT//6 + i * 40))

def level_2():
    global user_input
    screen.fill(BG_COLOR)

    clue_text = [
        "Remove the first letter, I sound the same.",
        "Then remove the last letter, I still sound the same.",
        "Then remove the middle letter, and I still sound the same again.", 
        "What word am I?"
    ]

    user_input = handle_user_input(clue_text)
    if user_input.upper() == "EMPTY":
        unlock_level(3)
        set_screen_state('main_menu')
    else:
        popup(wrong_image, 1000)

def level_3():
    screen.fill(BG_COLOR)
    screen.blit(lvl3_image)

def popup(img: Surface, duration):
    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < duration:
        screen.blit(img, (WIDTH/2 - img.get_width()/2, .1*HEIGHT - img.get_height()/2))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def unlock_level(level):
    if level not in levels_unlocked:   
        levels_unlocked.append(level)

def center_image(img_width, img_height):
    return (WIDTH - img_width) / 2, (HEIGHT - img_height) / 2

def set_screen_state(state):
    global screen_state
    screen_state = state

while True: 
    match screen_state: 
        case 'main_menu':
            main_menu()
        
        case 'level_1':
            level_1()

        case 'level_2': 
            level_2()

    pygame.display.update()
