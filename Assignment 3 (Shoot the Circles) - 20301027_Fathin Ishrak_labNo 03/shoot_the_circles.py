import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Constants for the game
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600
FPS = 60
MIN_CIRCLE_RADIUS = 10
MAX_CIRCLE_RADIUS = 30
PROJECTILE_RADIUS = 5
SHOOTER_RADIUS = 10
SHOOTER_SPEED = 7
PROJECTILE_SPEED = 10
CIRCLE_SPEED = 2
CIRCLE_INTERVAL = 1500  # 1.5 seconds for new circles to appear

# Colors
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
TEAL = (0, 255, 255)
AMBER = (255, 191, 0)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shoot The Circles!")

# Fonts
font = pygame.font.SysFont(None, 36)

# Create a clock object
clock = pygame.time.Clock()

# Game variables
shooter_x = SCREEN_WIDTH // 2
shooter_y = SCREEN_HEIGHT - SHOOTER_RADIUS - 10
score = 0
misses = 0
misfires = 0  # Track number of misfires
game_over = False
paused = False
projectile_fired = False  # Track if a projectile is already fired
game_over_printed = False  # Flag to avoid infinite game over printing
missed_circles = 0  # Track number of missed circles

# Lists to hold falling circles
falling_circles = []

# Timers
last_circle_time = pygame.time.get_ticks()

# Button areas
btn_restart = pygame.Rect(10, 10, 40, 40)
btn_play_pause = pygame.Rect(SCREEN_WIDTH // 2 - 20, 10, 40, 40)
btn_exit = pygame.Rect(SCREEN_WIDTH - 50, 10, 40, 40)

def draw_shooter(x, y):
    pygame.draw.circle(screen, YELLOW, (x, y), int(SHOOTER_RADIUS), 2)

def draw_projectile(x, y):
    pygame.draw.circle(screen, WHITE, (x, y), PROJECTILE_RADIUS)

def draw_circle(x, y, radius):
    pygame.draw.circle(screen, YELLOW, (x, y), radius, 2)

def display_text(text, x, y):
    img = font.render(text, True, WHITE)
    screen.blit(img, (x, y))

def check_collision(projectile, circle):
    distance = ((projectile[0] - circle[0]) ** 2 + (projectile[1] - circle[1]) ** 2) ** 0.5
    return distance < (PROJECTILE_RADIUS + circle[2])

def check_shooter_collision(circle):
    distance = ((shooter_x - circle[0]) ** 2 + (shooter_y - circle[1]) ** 2) ** 0.5
    return distance < (SHOOTER_RADIUS + circle[2])

def restart_game():
    global shooter_x, score, misses, misfires, game_over, paused, projectile_fired, game_over_printed, missed_circles
    shooter_x = SCREEN_WIDTH // 2
    score = 0
    misses = 0
    misfires = 0
    falling_circles.clear()
    missed_circles = 0  # Reset missed circles
    game_over = False
    paused = False
    projectile_fired = False
    game_over_printed = False  # Reset the flag when the game restarts
    print("Starting Over")

def draw_left_arrow(x, y, size, color):
    pygame.draw.line(screen, color, (x + size, y), (x, y + size // 2), 2)
    pygame.draw.line(screen, color, (x, y + size // 2), (x + size, y + size), 2)

def draw_play_pause(x, y, size, color, is_paused):
    if is_paused:
        # Draw play icon (triangle)
        pygame.draw.polygon(screen, color, [(x, y), (x, y + size), (x + size, y + size // 2)], 2)
    else:
        # Draw pause icon (two lines)
        pygame.draw.line(screen, color, (x, y), (x, y + size), 2)
        pygame.draw.line(screen, color, (x + size, y), (x + size, y + size), 2)

def draw_cross(x, y, size, color):
    pygame.draw.line(screen, color, (x, y), (x + size, y + size), 2)
    pygame.draw.line(screen, color, (x + size, y), (x, y + size), 2)

# Main game loop
projectile = None  # Holds the single projectile data
while True:
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Mouse click handling for the buttons
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if btn_restart.collidepoint(mouse_x, mouse_y):
                restart_game()
            elif btn_play_pause.collidepoint(mouse_x, mouse_y):
                paused = not paused
            elif btn_exit.collidepoint(mouse_x, mouse_y):
                print(f"Goodbye! Final Score: {score}")
                pygame.quit()
                sys.exit()

    if not game_over and not paused:
        # Shooter movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and shooter_x - SHOOTER_SPEED - SHOOTER_RADIUS > 0:
            shooter_x -= SHOOTER_SPEED
        if keys[pygame.K_d] and shooter_x + SHOOTER_SPEED + SHOOTER_RADIUS < SCREEN_WIDTH:
            shooter_x += SHOOTER_SPEED
        if keys[pygame.K_SPACE] and not projectile_fired:
            projectile = [shooter_x, shooter_y - SHOOTER_RADIUS]
            projectile_fired = True

        # Spawn falling circles with randomized size
        if pygame.time.get_ticks() - last_circle_time > CIRCLE_INTERVAL:
            new_circle_x = random.randint(MAX_CIRCLE_RADIUS, SCREEN_WIDTH - MAX_CIRCLE_RADIUS)
            new_circle_radius = random.randint(MIN_CIRCLE_RADIUS, MAX_CIRCLE_RADIUS)
            falling_circles.append([new_circle_x, -new_circle_radius, new_circle_radius])
            last_circle_time = pygame.time.get_ticks()

        # Move falling circles
        for circle in falling_circles[:]:
            circle[1] += CIRCLE_SPEED

            # Check if falling circle hits the shooter
            if check_shooter_collision(circle):
                game_over = True
                break  # End the loop if game is over

            if circle[1] - circle[2] > SCREEN_HEIGHT:
                falling_circles.remove(circle)
                missed_circles += 1
                misses = missed_circles  # Update misses with missed_circles
                if missed_circles >= 3:  # Game over after 3 missed circles
                    game_over = True

        # Move projectile
        if projectile:
            projectile[1] -= PROJECTILE_SPEED
            if projectile[1] < 0:
                projectile_fired = False
                projectile = None
                misfires += 1  # Increment misfires on missed shot
                if misfires >= 3:  # Game over after 3 misfires
                    game_over = True

        # Check for collisions between projectile and falling circles
        if projectile:
            for circle in falling_circles[:]:
                if check_collision(projectile, circle):
                    projectile_fired = False
                    projectile = None
                    falling_circles.remove(circle)
                    score += 1
                    print(f"Score: {score}")
                    break

    # Drawing elements
    draw_shooter(shooter_x, shooter_y)

    if projectile:
        draw_projectile(projectile[0], projectile[1])

    for circle in falling_circles:
        draw_circle(circle[0], circle[1], circle[2])

    # Display score and misses
    display_text(f"Score: {score}", 10, 50)
    display_text(f"Misses: {misses}", 10, 80)

    # Handle game over state
    if game_over:
        if not game_over_printed:
            print(f"Game Over! Final Score: {score}")
            game_over_printed = True  # Set the flag to avoid infinite printing
        display_text("GAME OVER", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2)

    # Draw buttons (Restart, Play/Pause, Exit)
    draw_left_arrow(10, 10, 20, TEAL)  # Left arrow button (restart)
    draw_play_pause(SCREEN_WIDTH // 2 - 10, 10, 20, AMBER, paused)  # Play/pause button
    draw_cross(SCREEN_WIDTH - 40, 10, 20, RED)  # Cross button (exit)

    pygame.display.flip()
    clock.tick(FPS)
