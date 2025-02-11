import pygame
from pygame import Surface
import sys
import random


# Initialize Pygame
pygame.init()

# Constants
# WIDTH, HEIGHT = 1920, 1200
WIDTH, HEIGHT = 800, 600
BUTTON_WIDTH, BUTTON_HEIGHT = 3/17 * WIDTH, 1/11 * HEIGHT
LEVEL_BUTTON_COLOR = (0, 128, 255)
LEVEL_HOVER_COLOR = (0, 255, 255)
LEVEL_LOCKED_COLOR = (128, 128, 128)
LEVEL_1_IMAGE_WIDTH, LEVEL_1_IMAGE_HEIGHT = 353, 344
TEXT_COLOR = (255, 255, 255)
BG_COLOR = (28, 170, 156)
LEVEL_3_IMAGE_WIDTH, LEVEL_3_IMAGE_HEIGHT = 992/3, 985/3
BIG_CLUE_BOX_WIDTH = 0.8 * WIDTH # 46 max characters
SMALL_CLUE_BOX_WIDTH = 0.2 * WIDTH # 9 max characters
LEVEL_5_IMAGE_WIDTH, LEVEL_5_IMAGE_HEIGHT = 643, 444
LEVEL_7_IMAGE_WIDTH, LEVEL_7_IMAGE_HEIGHT = 524, 284
LEVEL_10_IMAGE_WIDTH, LEVEL_10_IMAGE_HEIGHT = 1074 * 2/3 , 379 * 2/3


# Images
wrong_image = pygame.image.load("Red_X.svg.png")
wrong_image = pygame.transform.scale(wrong_image, (.1 * WIDTH, .1 * HEIGHT))
right_image = pygame.image.load("Green_check.svg.png")
right_image = pygame.transform.scale(right_image, (.1 * WIDTH, .1 * HEIGHT))
massive_image = pygame.image.load("massive.png")
lvl1_image = pygame.image.load("level_1.png")
lvl1_image = pygame.transform.scale(lvl1_image, (LEVEL_1_IMAGE_WIDTH, LEVEL_1_IMAGE_HEIGHT))
lvl3_image = pygame.image.load("level_3.png")
lvl3_image = pygame.transform.scale(lvl3_image, (LEVEL_3_IMAGE_WIDTH, LEVEL_3_IMAGE_HEIGHT))
lvl5_image = pygame.image.load("level_5.png")
lvl5_image = pygame.transform.scale(lvl5_image, (LEVEL_5_IMAGE_WIDTH, LEVEL_5_IMAGE_HEIGHT))
lvl7_image = pygame.image.load("level_7.png")
lvl7_image = pygame.transform.scale(lvl7_image, (LEVEL_7_IMAGE_WIDTH, LEVEL_7_IMAGE_HEIGHT))
lvl10_image = pygame.image.load("level_10.png")
lvl10_image = pygame.transform.scale(lvl10_image, (LEVEL_10_IMAGE_WIDTH, LEVEL_10_IMAGE_HEIGHT))

# User info
levels_unlocked = [1,2,3,4,5,6,7,8,9,10]
type_duration = 0

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
    x = find_top_left_x(LEVEL_1_IMAGE_WIDTH)
    y = find_top_left_y(LEVEL_1_IMAGE_HEIGHT)
    screen.blit(lvl1_image, (x, y))
    
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

def handle_user_input(clue_text: list[str], width: float, image=None, clue_box_y: float=(0.5*HEIGHT), image_width: float=None, image_height: float=None, font_size: int = 36, time_limit: int=None) -> str:
    global user_input, type_duration
    start_time = None
    user_input = ""
    input_box_y: float = clue_box_y  # Static y-coordinate proportional to screen height
    input_box = pygame.Rect(WIDTH//2 - (0.5 * width), input_box_y, width, 40)
    clue_font = pygame.font.Font(None, font_size)

    while True:
        screen.fill(BG_COLOR)
        
        # Display the clue text
        display_clue(clue_text, font_size)
        
        # Draw the input box and user input
        pygame.draw.rect(screen, LEVEL_BUTTON_COLOR, input_box, 2)
        input_text = clue_font.render(user_input.upper(), True, TEXT_COLOR)
        screen.blit(input_text, (input_box.x+5, input_box.y+5))
        if image:
            screen.blit(image, (find_top_left_x(image_width), find_top_left_y(image_height)))
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if time_limit and user_input == "":
                    start_time = pygame.time.get_ticks()
                if event.key == pygame.K_ESCAPE:
                    set_screen_state('main_menu')
                    return None
                elif event.key == pygame.K_RETURN:
                    if time_limit:
                        type_duration = pygame.time.get_ticks() - start_time
                    return user_input
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    if width == SMALL_CLUE_BOX_WIDTH and len(user_input) < 9:
                        user_input += event.unicode
                    elif width == BIG_CLUE_BOX_WIDTH and len(user_input) < 70:
                        user_input += event.unicode

        if time_limit and start_time: 
            type_duration = pygame.time.get_ticks() - start_time
            if type_duration > time_limit:
                return user_input

def display_clue(clue_text: list[str], font_size: int = 36):
    clue_font = pygame.font.Font(None, font_size)
    for i, line in enumerate(clue_text):
        text_surface = clue_font.render(line, True, TEXT_COLOR)
        screen.blit(text_surface, (WIDTH//2 - text_surface.get_width()//2, HEIGHT//6 + i * 40))

def find_top_left_x(width) -> float: # Find's correct x coordinate to center image
    return (WIDTH - width) / 2

def find_top_left_y(height) -> float: # Find's correct y coordinate to center image
    return (HEIGHT - height) / 2

def level_2():
    global user_input
    screen.fill(BG_COLOR)

    clue_text = [
        "Remove the first letter, I sound the same.",
        "Then remove the last letter, I still sound the same.",
        "Then remove the middle letter, and I still sound the same again.", 
        "What word am I?"
    ]

    user_input = handle_user_input(clue_text, SMALL_CLUE_BOX_WIDTH)
    if user_input is None:
        return
    if user_input.upper() == "EMPTY":
        unlock_level(3)
        set_screen_state('main_menu')
    else:
        popup(wrong_image, 1000)

def level_3():
    screen.fill(BG_COLOR)
    x = find_top_left_x(LEVEL_3_IMAGE_WIDTH/3)
    y = find_top_left_y(LEVEL_3_IMAGE_HEIGHT/3)
    screen.blit(lvl3_image, (x, y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                set_screen_state('main_menu')
    
    user_input = handle_user_input(["What is the best move for black? (answer in chess notation)"], 
                                   SMALL_CLUE_BOX_WIDTH,
                                   lvl3_image,
                                   0.8*HEIGHT,
                                   LEVEL_3_IMAGE_WIDTH, 
                                   LEVEL_3_IMAGE_HEIGHT)
    if user_input is None:
        return
    if user_input.upper() == "RH2+":
        popup(right_image, 1000)
        set_screen_state('main_menu')
        unlock_level(4)
    else:
        popup(wrong_image, 1000)

    pygame.display.update()

def level_4():
    screen.fill(BG_COLOR)

    clue_text = [
        "-- .- ... ... .. ...- .",
        "Decipher this morse code!"
    ]
    user_input = handle_user_input(clue_text, SMALL_CLUE_BOX_WIDTH)
    if user_input is None:
        return
    if user_input.upper() == "MASSIVE":
        popup(massive_image, 1000)
        unlock_level(5)
        set_screen_state('main_menu')
    else:
        popup(wrong_image, 1000)

def level_5():
    user_input = handle_user_input([""], 
                                   SMALL_CLUE_BOX_WIDTH, 
                                   lvl5_image, 
                                   0.9*HEIGHT, 
                                   LEVEL_5_IMAGE_WIDTH, 
                                   LEVEL_5_IMAGE_HEIGHT)
    if user_input is None:
        return
    if user_input.upper() == "RED":
        popup(right_image, 1000)
        unlock_level(6)
        set_screen_state('main_menu')
    else:
        popup(wrong_image, 1000)

def level_6():
    random_words = get_random_words('words.txt', 7)
    user_input = handle_user_input(["Typing Test!", "Type the words as fast as you can (full accuracy)", random_words], BIG_CLUE_BOX_WIDTH, font_size=24, time_limit=70000)
    if user_input is None:
        return
    if user_input.upper() == random_words.upper() and type_duration <= 70000:
        popup(right_image, 1000)
        unlock_level(7)
        set_screen_state('main_menu')
    else:
        popup(wrong_image, 1000)

def level_7():
    screen.fill(BG_COLOR)
    clue_text = ['Evaluate this integral']
    user_input = handle_user_input(clue_text, SMALL_CLUE_BOX_WIDTH, image=lvl7_image, clue_box_y=0.8*HEIGHT, image_width=LEVEL_7_IMAGE_WIDTH, image_height=LEVEL_7_IMAGE_HEIGHT)
    if user_input is None:
        return
    if user_input == "-20":
        popup(right_image, 1000)
        unlock_level(8)
        set_screen_state('main_menu')
    else:
        popup(wrong_image, 1000)

def level_8():
    screen.fill(BG_COLOR)
    matrix = [[random.randint(1,10) for i in range(4)] for x in range(4)]
    display_clue(''.join(str(row)) for row in matrix)
    pygame.display.update()
    
    pygame.time.wait(4000)

    row = random.randint(0,3)
    column = random.randint(0,3)
    user_input = handle_user_input([f"What was the number in row {row+1} and column {column+1}"], SMALL_CLUE_BOX_WIDTH)

    if user_input is None:
        return
    if user_input == str(matrix[row][column]):
        popup(right_image, 1000)
        unlock_level(9)
        set_screen_state('main_menu')
    else:
        popup(wrong_image, 1000)

def level_10(): 
    screen.fill(BG_COLOR)
    clue_text = ['What song is this?']
    user_input = handle_user_input(clue_text, BIG_CLUE_BOX_WIDTH, image=lvl10_image, clue_box_y=0.8*HEIGHT, image_width=LEVEL_10_IMAGE_WIDTH, image_height=LEVEL_10_IMAGE_HEIGHT)
    if user_input is None:
        return
    if user_input.upper() == "HAPPY BIRTHDAY":
        popup(right_image, 1000)
        unlock_level(11)
        set_screen_state('main_menu')
    else:
        popup(wrong_image, 1000)

def get_random_words(file_path, num_words):
    with open(file_path, 'r') as file:
        words = file.read().splitlines()
    return ' '.join(random.sample(words, num_words))

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

        case 'level_3':
            level_3()

        case 'level_4':
            level_4()

        case 'level_5':
            level_5()

        case 'level_6':
            level_6()

        case 'level_7':
            level_7()

        case 'level_8': 
            level_8()

        case 'level_9':
            pass

        case 'level_10':
            level_10()

    pygame.display.update()
