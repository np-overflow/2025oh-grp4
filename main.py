# main_game.py
import pygame
from pygame import mixer
from fighter import Fighter
import math
from image import create_ui  # Import the photo selector
from comfyui_client import main
import tkinter as tk
from tkinter import PhotoImage
import threading
import time
from PIL import Image, ImageTk  # Pillow library
# remove imaege1.png and image2.png


# Initialize pygame and other libraries
mixer.init()
pygame.init()

# Create the game window

# Get the screen width and height of the computer
infoObject = pygame.display.Info()
SCREEN_WIDTH = infoObject.current_w
SCREEN_HEIGHT = infoObject.current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Photo Fighter")

# Set frame rate
clock = pygame.time.Clock()
FPS = 60

# Define colors
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# Game variables
intro_count = 4
last_count_update = pygame.time.get_ticks()
score = [0, 0]
round_over = False
ROUND_OVER_COOLDOWN = 2000

# Fighter variables (example data)
WARRIOR_SIZE = 162
WARRIOR_SCALE = 6
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 4.5
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

# Music and sound effects
#pygame.mixer.music.load("assets/audio/music.mp3")
#pygame.mixer.music.set_volume(0.5)
#pygame.mixer.music.play(-1, 0.0, 5000)
sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
sword_fx.set_volume(0.5)
magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
magic_fx.set_volume(0.75)

# Background image
bg_image = pygame.image.load("assets/images/background/background2.jpeg").convert_alpha()
win_bg_image = pygame.image.load("assets/images/background/win_screen.jpg").convert_alpha()

# Spritesheets for the fighters
warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()

# Victory image
victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()

# Animation steps for the fighters
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]
# Font definitions
count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)

# Function for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Function for drawing background
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

# Function for drawing victory screen
def draw_win_bg():
    scaled_bg = pygame.transform.scale(win_bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

# Function for drawing health bar
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))

# Get bobbing offset
def get_bobbing_offset(time):
    return math.sin(time * 0.009) * 2

# Open the photo submission window (call function from photo_selector.py)
photo_path_1 = create_ui("image1.png")
photo_path_2 = create_ui("image2.png")

# Load the selected photo (if available)
if photo_path_1:
    print(f"Photo selected: {photo_path_1}")
    photo_image_1 = pygame.image.load(photo_path_1).convert_alpha()
else:
    photo_image_1 = None

# Load the selected photo (if available)
if photo_path_2:
    print(f"Photo selected: {photo_path_2}")
    photo_image_2 = pygame.image.load(photo_path_2).convert_alpha()
else:
    photo_image_2 = None


# Create fighters
fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

# Below process will take some time to process the image, so to open a window to show an loading screen image using tkinter
def run_tkinter():
    """Function to run the Tkinter GUI."""
    window = tk.Tk()
    window.title("Image Viewer")

    # Set a desired maximum size for the image
    max_width, max_height = SCREEN_WIDTH*0.8, SCREEN_HEIGHT*0.8

    try:
        # Open and resize the image
        original_image = Image.open(r"assets\images\background\the_tech_overflow_openhouse_stablediffusion.png")  # Replace with your image path
        original_width, original_height = original_image.size
        
        # Calculate the resize ratio while preserving aspect ratio
        resize_ratio = min(max_width / original_width, max_height / original_height)
        new_width = int(original_width * resize_ratio)
        new_height = int(original_height * resize_ratio)
        
        # Resize the image
        resized_image = original_image.resize((new_width, new_height), Image.LANCZOS)
        image = ImageTk.PhotoImage(resized_image)
        
        # Display the resized image
        image_label = tk.Label(window, image=image)
        image_label.image = image  # Keep a reference to avoid garbage collection
        image_label.pack()
    except Exception as e:
        print(f"Failed to load image: {e}")
        error_label = tk.Label(window, text="Failed to load image")
        error_label.pack()

    # Add a dismiss button
    dismiss_button = tk.Button(window, text="Dismiss", command=window.destroy)
    dismiss_button.pack()

    # Run the Tkinter event loop
    window.mainloop()
# Start the Tkinter GUI in a separate thread
tk_thread = threading.Thread(target=run_tkinter, daemon=True)
tk_thread.start()

# Process the photo image for the fighters
main(photo_path_1,"image1_processed.png")
main(photo_path_2,"image2_processed.png")



# Load the image for the box
box_image_1 = pygame.image.load("image1_processed.png").convert_alpha()
box_image_2 = pygame.image.load("image2_processed.png").convert_alpha()
box_size = 90
scaled_box_image_1 = pygame.transform.scale(box_image_1, (box_size, box_size))
scaled_box_image_2 = pygame.transform.scale(box_image_2, (box_size, box_size))

# Game loop
run = True
start_time = pygame.time.get_ticks()

# Constants for dynamic positioning
HEALTH_BAR_WIDTH = 200  # Width of the health bar
HEALTH_BAR_HEIGHT = 20  # Height of the health bar
MARGIN = 20             # Margin from the edge of the screen

# Dynamic starting positions for fighters
fighter_1_start_x = SCREEN_WIDTH // 4  # 25% of the screen width
fighter_2_start_x = SCREEN_WIDTH * 3 // 4  # 75% of the screen width
fighter_start_y = SCREEN_HEIGHT - 150  # Fixed offset from bottom of the screen

# Initialize fighters
fighter_1 = Fighter(1, fighter_1_start_x, fighter_start_y, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
fighter_2 = Fighter(2, fighter_2_start_x, fighter_start_y, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)


middle_image = pygame.image.load("helper.png").convert_alpha()  # Replace with your actual file path
desired_width = middle_image.get_width() /7.5
desired_height = middle_image.get_height()/7.5
middle_image = pygame.transform.smoothscale(middle_image, (desired_width, desired_height))
while run:
    clock.tick(FPS)

    # Calculate current time for bobbing
    current_time = pygame.time.get_ticks() - start_time
    bob_offset = get_bobbing_offset(current_time)

    # Draw background
    draw_bg()

    # Dynamic health bar and score positions
    health_bar_1_x = MARGIN
    health_bar_1_y = MARGIN 
    health_bar_2_x = SCREEN_WIDTH - HEALTH_BAR_WIDTH*2 - MARGIN
    health_bar_2_y = MARGIN
    score_1_x = MARGIN
    score_1_y = HEALTH_BAR_HEIGHT + MARGIN * 2
    score_2_x = SCREEN_WIDTH - HEALTH_BAR_WIDTH*2 - MARGIN
    score_2_y = HEALTH_BAR_HEIGHT + MARGIN * 2

    # Calculate the position to place the image between the health bars
    middle_image_x = (health_bar_1_x + health_bar_2_x + HEALTH_BAR_WIDTH) // 2 - desired_width // 2 + 100
    middle_image_y = MARGIN + (HEALTH_BAR_HEIGHT // 2) - (desired_height // 2) + 60


    # Draw the PNG image between the health bars
    screen.blit(middle_image, (middle_image_x, middle_image_y))
    # Show player stats
    draw_health_bar(fighter_1.health, health_bar_1_x, health_bar_1_y)
    draw_health_bar(fighter_2.health, health_bar_2_x, health_bar_2_y)
    draw_text("P1: " + str(score[0]), score_font, RED, score_1_x, score_1_y)
    draw_text("P2: " + str(score[1]), score_font, RED, score_2_x, score_2_y)

    if intro_count <= 0:
        fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
        fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
    else:
        draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
        if (pygame.time.get_ticks() - last_count_update) >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()

    # Update fighters
    fighter_1.update()
    fighter_2.update()

    # Draw fighters
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    # Dynamic bobbing box positions
    height_offset = 60  # Base height offset

    # Draw image-filled box on fighter_1's body with bobbing effect
    body_x_1 = fighter_1.rect.centerx
    body_y_1 = fighter_1.rect.centery
    box_y_1 = body_y_1 - box_size // 2 - height_offset + bob_offset
    screen.blit(scaled_box_image_1, (body_x_1 - box_size // 2+20, box_y_1))

    # Draw image-filled box on fighter_2's body with bobbing effect
    body_x_2 = fighter_2.rect.centerx
    body_y_2 = fighter_2.rect.centery
    box_y_2 = body_y_2 - box_size // 2 - height_offset + bob_offset + 10
    screen.blit(scaled_box_image_2, (body_x_2 - box_size // 2 +20, box_y_2))

    # Check for round over conditions
    if not round_over:
        if not fighter_1.alive:
            score[1] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
            scaled_box_image_1.fill((0, 0, 0, 0))
        elif not fighter_2.alive:
            score[0] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
            scaled_box_image_2.fill((0, 0, 0, 0))
    else:
        screen.blit(victory_img, (SCREEN_WIDTH // 2 - victory_img.get_width() // 2, 150))
        if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
            if score[0] + score[1] == 3:
                draw_win_bg()
                if score[0] > score[1]:
                    win_player = pygame.transform.scale(pygame.image.load("image1_processed.png").convert(), (200, 200))
                else:
                    win_player = pygame.transform.scale(pygame.image.load("image2_processed.png").convert(), (200, 200))
                screen.blit(win_player, win_player.get_rect(center=screen.get_rect().center))
                draw_text(f"Player {1 if score[0] > score[1] else 2}", count_font, RED, SCREEN_WIDTH // 2 - 30, 400)
            else:
                round_over = False
                intro_count = 4
                fighter_1 = Fighter(1, fighter_1_start_x, fighter_start_y, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
                fighter_2 = Fighter(2, fighter_2_start_x, fighter_start_y, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)
                scaled_box_image_1 = pygame.transform.scale(box_image_1, (box_size, box_size))
                scaled_box_image_2 = pygame.transform.scale(box_image_2, (box_size, box_size))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()