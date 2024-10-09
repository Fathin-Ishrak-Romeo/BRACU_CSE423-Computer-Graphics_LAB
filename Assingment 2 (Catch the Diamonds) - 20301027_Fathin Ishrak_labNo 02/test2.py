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

# Fonts
font = pygame.font.SysFont(None, 40)

# Catcher settings
catcher_width = 60
catcher_height = 20
catcher_speed = 5
catcher_color = WHITE
catcher_x = WIDTH // 2 - catcher_width // 2
catcher_y = HEIGHT - catcher_height - 10

# Diamond settings
diamond_size = 20
diamond_speed = 2
diamond_color = random.choice([RED, TEAL, AMBER])
diamond_x = random.randint(0, WIDTH - diamond_size)
diamond_y = 0

# Game state variables
score = 0
game_over = False
paused = False

# Function to draw the catcher
def draw_catcher(x, y, color):
    pygame.draw.rect(screen, color, (x, y, catcher_width, catcher_height))

# Function to draw the diamond
def draw_diamond(x, y, color):
    pygame.draw.polygon(screen, color, [(x, y), (x + diamond_size // 2, y + diamond_size), (x + diamond_size, y), (x + diamond_size // 2, y - diamond_size)])

# Function to display score
def display_text(text, font, color, x, y):
    render = font.render(text, True, color)
    screen.blit(render, (x, y))

# AABB collision detection
def has_collided(catcher_x, catcher_y, diamond_x, diamond_y):
    return (diamond_x < catcher_x + catcher_width and
            diamond_x + diamond_size > catcher_x and
            diamond_y < catcher_y + catcher_height and
            diamond_y + diamond_size > catcher_y)

# Main game loop
while True:
    screen.fill(BLACK)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if 10 <= mouse_x <= 60 and 10 <= mouse_y <= 60:
                score = 0
                diamond_speed = 2
                diamond_x = random.randint(0, WIDTH - diamond_size)
                diamond_y = 0
                game_over = False
                paused = False
                catcher_color = WHITE
                print("Starting Over")

            if 160 <= mouse_x <= 240 and 10 <= mouse_y <= 60:
                paused = not paused

            if 310 <= mouse_x <= 360 and 10 <= mouse_y <= 60:
                print(f"Goodbye! Final Score: {score}")
                pygame.quit()
                sys.exit()

    # Check if game is paused
    if not paused and not game_over:
        # Move the catcher
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and catcher_x > 0:
            catcher_x -= catcher_speed
        if keys[pygame.K_RIGHT] and catcher_x < WIDTH - catcher_width:
            catcher_x += catcher_speed

        # Move the diamond
        diamond_y += diamond_speed

        # Check if the diamond is caught
        if has_collided(catcher_x, catcher_y, diamond_x, diamond_y):
            score += 1
            diamond_speed += 0.5  # Increase diamond speed for more challenge
            diamond_x = random.randint(0, WIDTH - diamond_size)
            diamond_y = 0
            diamond_color = random.choice([RED, TEAL, AMBER])
            print(f"Score: {score}")

        # Check if the diamond missed the catcher
        if diamond_y > HEIGHT:
            game_over = True
            catcher_color = RED
            print(f"Game Over! Score: {score}")

    # Draw catcher
    draw_catcher(catcher_x, catcher_y, catcher_color)

    # Draw diamond
    if not game_over:
        draw_diamond(diamond_x, diamond_y, diamond_color)

    # Draw UI buttons
    pygame.draw.rect(screen, TEAL, (10, 10, 50, 50))
    pygame.draw.rect(screen, AMBER, (160, 10, 80, 50))
    pygame.draw.rect(screen, RED, (310, 10, 50, 50))

    display_text(f"Score: {score}", font, WHITE, 10, 70)

    pygame.display.update()

    # Limit the frame rate
    pygame.time.Clock().tick(60)
