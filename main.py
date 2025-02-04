import pygame
from pygame import Surface
import sys


# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BUTTON_WIDTH, BUTTON_HEIGHT = 2/13 * WIDTH, 1/11 * HEIGHT
LEVEL_BUTTON_COLOR = (0, 128, 255)
LEVEL_HOVER_COLOR = (0, 255, 255)
LEVEL_LOCKED_COLOR = (128, 128, 128)
LEVEL_1_IMAGE_WIDTH, LEVEL_1_IMAGE_HEIGHT = 353, 344
TEXT_COLOR = (255, 255, 255)
BG_COLOR = (28, 170, 156)

# Images
wrong_image = pygame.image.load("Red_X.svg.png")
wrong_image = pygame.transform.scale(wrong_image, (.1 * WIDTH, .1 * HEIGHT))
right_image = pygame.image.load("Green_check.svg.png")
right_image = pygame.transform.scale(right_image, (.1 * WIDTH, .1 * HEIGHT))
lvl1_image = pygame.image.load("level_1.png")
lvl1_image = pygame.transform.scale(lvl1_image, (LEVEL_1_IMAGE_WIDTH, LEVEL_1_IMAGE_HEIGHT))

# User info
levels_unlocked = [1]

# screen info
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen_state = 'main_menu'
pygame.display.set_caption("Puzzle Game Level Selector")

# Font setup
font = pygame.font.Font(None, 40)

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

    for i in range(1,5): 
        draw_button(f"Level {i}", 1/13 * WIDTH, (2*BUTTON_HEIGHT) + (i-1)*BUTTON_HEIGHT, i in levels_unlocked)

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
            # Check if the player clicked on a button
            if 300 < mouse_x < 500:
                if 150 < mouse_y < 200:
                    set_screen_state('level_1')
                elif 250 < mouse_y < 300:
                    set_screen_state('level_2')
                elif 350 < mouse_y < 400:
                    pass
                elif 450 < mouse_y < 500:
                    pass

def level_1():
    global screen_state

    screen.fill(BG_COLOR)
    x = (WIDTH-LEVEL_1_IMAGE_WIDTH)/2
    y = (HEIGHT-LEVEL_1_IMAGE_HEIGHT)/2
    screen.blit(lvl1_image, ((WIDTH-LEVEL_1_IMAGE_WIDTH)/2, (HEIGHT-LEVEL_1_IMAGE_HEIGHT)/2))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.K_ESCAPE:
            print('key pressed')    
            set_screen_state('main_menu')
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if (x) < mouse_x < (1/3 * LEVEL_1_IMAGE_WIDTH + x) and (2/3 * LEVEL_1_IMAGE_HEIGHT + y) < mouse_y < (LEVEL_1_IMAGE_HEIGHT + y):
                popup(right_image, 1000)
                unlock_level(2)
                set_screen_state('main_menu')
            else: 
                popup(wrong_image, 1000)

def level_2():
    global screen_state
    
    screen.fill(BG_COLOR)
    print("I am thinking of a five letter word. When you remove its first letter, it still sounds the same. When you remove the third letter, it still sounds the same. When you remove the whole word. it's still the same! What’s the word?")
    while True:
        answer = input("What is the five letter word: ")
        if answer == "empty":
            print("You are correct! You can move on to the next level")
            screen_state = 'main_menu'
            levels_unlocked.append(3)
            break
        else:
            print("You are wrong Try again")

def popup(img: Surface, duration): 
    screen.blit(img, (WIDTH/2 - img.get_width()/2, .1*HEIGHT - img.get_height()/2))
    pygame.display.update()
    pygame.time.wait(duration)

def unlock_level(level):
    levels_unlocked.append(level)

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