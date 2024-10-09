import pygame
import random
import sys
import time

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Diamonds")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
TEAL = (0, 255, 255)
AMBER = (255, 191, 0)
BLACK = (0, 0, 0)
DIAMOND_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]

# Fonts
font = pygame.font.SysFont(None, 40)

# Catcher settings (Increased size by 1.5x)
catcher_width = 120  # Increased size
catcher_height = 18
catcher_speed = 7
catcher_color = WHITE
catcher_x = WIDTH // 2 - catcher_width // 2
catcher_y = HEIGHT - catcher_height - 10

# Diamond settings
diamond_size = 20
diamond_speed = 2
diamond_color = random.choice(DIAMOND_COLORS)
diamond_x = random.randint(0, WIDTH - diamond_size)
diamond_y = 0

# Game state variables
score = 0
game_over = False
paused = False
delta_time = 0
last_frame_time = time.time()

# Function to draw the catcher as a plate
def draw_catcher_plate(x, y, color):
    pygame.draw.line(screen, color, (x + 15, y + catcher_height), (x + catcher_width - 15, y + catcher_height), 2)  # Bottom line
    pygame.draw.line(screen, color, (x + 15, y + catcher_height), (x, y), 2)  # Left diagonal
    pygame.draw.line(screen, color, (x + catcher_width - 15, y + catcher_height), (x + catcher_width, y), 2)  # Right diagonal
    pygame.draw.line(screen, color, (x, y), (x + catcher_width, y), 2)  # Top line

# Function to draw the diamond using mid-point lines
def draw_diamond(x, y, color):
    pygame.draw.line(screen, color, (x, y), (x + diamond_size // 2, y + diamond_size), 2)
    pygame.draw.line(screen, color, (x + diamond_size // 2, y + diamond_size), (x + diamond_size, y), 2)
    pygame.draw.line(screen, color, (x + diamond_size, y), (x + diamond_size // 2, y - diamond_size), 2)
    pygame.draw.line(screen, color, (x + diamond_size // 2, y - diamond_size), (x, y), 2)

# Function to display text
def display_text(text, font, color, x, y):
    render = font.render(text, True, color)
    screen.blit(render, (x, y))

# AABB collision detection
def has_collided(catcher_x, catcher_y, diamond_x, diamond_y):
    return (diamond_x < catcher_x + catcher_width and
            diamond_x + diamond_size > catcher_x and
            diamond_y < catcher_y + catcher_height and
            diamond_y + diamond_size > catcher_y)

# Function to reset game
def reset_game():
    global score, diamond_speed, diamond_x, diamond_y, game_over, paused, catcher_color
    score = 0
    diamond_speed = 2
    diamond_x = random.randint(0, WIDTH - diamond_size)
    diamond_y = 0
    game_over = False
    paused = False
    catcher_color = WHITE
    print("Starting Over")

# Function to calculate delta time for frame-independent movement
def calculate_delta_time():
    global delta_time, last_frame_time
    current_time = time.time()
    delta_time = current_time - last_frame_time
    last_frame_time = current_time

# Function to draw left arrow button using mid-point line
def draw_left_arrow(x, y, size, color):
    pygame.draw.line(screen, color, (x + size, y), (x, y + size // 2), 2)  # Left diagonal
    pygame.draw.line(screen, color, (x, y + size // 2), (x + size, y + size), 2)  # Right diagonal

# Function to draw play/pause button
def draw_play_pause(x, y, size, color, is_paused):
    if is_paused:
        # Draw play icon (triangle)
        pygame.draw.line(screen, color, (x, y), (x, y + size), 2)
        pygame.draw.line(screen, color, (x, y), (x + size, y + size // 2), 2)
        pygame.draw.line(screen, color, (x + size, y + size // 2), (x, y + size), 2)
    else:
        # Draw pause icon (two lines)
        pygame.draw.line(screen, color, (x, y), (x, y + size), 2)
        pygame.draw.line(screen, color, (x + size, y), (x + size, y + size), 2)

# Function to draw the red cross button using midpoint lines
def draw_cross(x, y, size, color):
    pygame.draw.line(screen, color, (x, y), (x + size, y + size), 2)
    pygame.draw.line(screen, color, (x + size, y), (x, y + size), 2)

# Main game loop
while True:
    calculate_delta_time()
    
    screen.fill(BLACK)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Restart button (teal arrow)
            if 10 <= mouse_x <= 40 and 10 <= mouse_y <= 40:
                reset_game()
            # Play/Pause button (amber, center)
            if 180 <= mouse_x <= 220 and 10 <= mouse_y <= 40:
                paused = not paused
            # Exit button (red, right)
            if 360 <= mouse_x <= 390 and 10 <= mouse_y <= 40:
                print(f"Goodbye! Final Score: {score}")
                pygame.quit()
                sys.exit()

    # Check if game is paused
    if not paused and not game_over:
        # Move the catcher
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and catcher_x > 0:
            catcher_x -= catcher_speed * delta_time * 60  # Adjust with delta time
        if keys[pygame.K_RIGHT] and catcher_x < WIDTH - catcher_width:
            catcher_x += catcher_speed * delta_time * 60  # Adjust with delta time

        # Move the diamond
        diamond_y += diamond_speed * delta_time * 60  # Adjust with delta time

        # Check if the diamond is caught
        if has_collided(catcher_x, catcher_y, diamond_x, diamond_y):
            score += 1
            diamond_speed += 0.3  # Increase diamond speed for more challenge
            catcher_speed += 0.5  # Increase catcher_speed to cope up with the increasing diamond_speed
            diamond_x = random.randint(0, WIDTH - diamond_size)
            diamond_y = 0
            diamond_color = random.choice(DIAMOND_COLORS)
            print(f"Score: {score}")

        # Check if the diamond missed the catcher
        if diamond_y > HEIGHT:
            game_over = True
            catcher_color = RED
            print(f"Game Over! Score: {score}")

    # Draw catcher plate
    draw_catcher_plate(catcher_x, catcher_y, catcher_color)

    # Draw diamond
    if not game_over:
        draw_diamond(diamond_x, diamond_y, diamond_color)

    # Draw UI buttons with reduced size and correct restart arrow
    draw_left_arrow(10, 10, 20, TEAL)  # Left arrow button (restart)
    draw_play_pause(180, 10, 20, AMBER, paused)  # Play/pause button
    draw_cross(360, 10, 20, RED)  # Cross button (exit)

    # Draw side score counter
    display_text(f"Score: {score}", font, WHITE, 10, 70)

    pygame.display.update()

    # Limit the frame rate
    pygame.time.Clock().tick(60)
