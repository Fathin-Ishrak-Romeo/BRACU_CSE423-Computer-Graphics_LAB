import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shoot the Circles!")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
TEAL = (0, 255, 255)
AMBER = (255, 191, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Shooter properties
shooter_radius = 25
shooter_speed = 5
shooter_x = WIDTH // 2
shooter_y = HEIGHT - shooter_radius - 10

# Circle properties
falling_circles = []
max_falling_circles = 2
circle_speed = 2

# Projectile properties
projectiles = []
projectile_radius = 5
projectile_speed = 5
misfire_count = 0

# Game state variables
score = 0
lives = 3
game_over = False
paused = False

# Fonts
font = pygame.font.SysFont(None, 40)

# Functions to draw objects
def draw_circle(x, y, radius, color):
    pygame.draw.circle(screen, color, (x, y), radius, 1)

def draw_shooter(x, y, radius, color):
    pygame.draw.circle(screen, color, (x, y), radius, 1)

def draw_projectile(x, y, radius, color):
    pygame.draw.circle(screen, color, (x, y), radius, 1)

# Function to display text
def display_text(text, font, color, x, y):
    render = font.render(text, True, color)
    screen.blit(render, (x, y))

# Function to reset game
def reset_game():
    global score, falling_circles, projectiles, lives, game_over, paused, shooter_speed, circle_speed, max_falling_circles
    score = 0
    falling_circles.clear()
    projectiles.clear()
    lives = 3
    game_over = False
    paused = False
    shooter_speed = 5
    circle_speed = 2
    max_falling_circles = 2
    print("Starting Over")

# Function to check for collisions
def has_collided(circle_x, circle_y, circle_radius, proj_x, proj_y, proj_radius):
    distance = ((circle_x - proj_x) ** 2 + (circle_y - proj_y) ** 2) ** 0.5
    return distance < circle_radius + proj_radius

# Function to check if shooter collides with any falling circle
def check_shooter_collision():
    for circle in falling_circles:
        if has_collided(circle[0], circle[1], circle[2], shooter_x, shooter_y, shooter_radius):
            return True
    return False

# Function to end game
def end_game():
    global game_over
    print(f"Game Over! Final Score: {score}")
    game_over = True

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

    # If not paused and not game over
    if not paused and not game_over:
        # Move shooter left and right with 'a' and 'd' keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and shooter_x > shooter_radius:
            shooter_x -= shooter_speed
        if keys[pygame.K_d] and shooter_x < WIDTH - shooter_radius:
            shooter_x += shooter_speed
        if keys[pygame.K_SPACE]:
            projectiles.append([shooter_x, shooter_y])

        # Move projectiles
        for projectile in projectiles[:]:
            projectile[1] -= projectile_speed
            if projectile[1] < 0:
                projectiles.remove(projectile)

        # Move falling circles and increase difficulty over time
        if len(falling_circles) < max_falling_circles:
            radius = random.randint(10, 30)  # Randomize the size of circles
            x_position = random.randint(radius, WIDTH - radius)
            falling_circles.append([x_position, 0, radius])

        for circle in falling_circles[:]:
            circle[1] += circle_speed
            if circle[1] > HEIGHT:
                falling_circles.remove(circle)
                lives -= 1
                if lives == 0:
                    end_game()

        # Check for shooter collision
        if check_shooter_collision():
            end_game()

        # Check for collisions with projectiles
        for projectile in projectiles[:]:
            for circle in falling_circles[:]:
                if has_collided(circle[0], circle[1], circle[2], projectile[0], projectile[1], projectile_radius):
                    projectiles.remove(projectile)
                    falling_circles.remove(circle)
                    score += 1
                    print(f"Score: {score}")

        # Increase difficulty based on score
        if score % 5 == 0 and score > 0:
            shooter_speed += 0.5
            circle_speed += 0.5
            max_falling_circles += 1

    # Draw shooter
    draw_shooter(shooter_x, shooter_y, shooter_radius, YELLOW)

    # Draw projectiles
    for projectile in projectiles:
        draw_projectile(projectile[0], projectile[1], projectile_radius, WHITE)

    # Draw falling circles
    for circle in falling_circles:
        draw_circle(circle[0], circle[1], circle[2], YELLOW)

    # Draw UI buttons
    pygame.draw.polygon(screen, TEAL, [(10, 30), (30, 10), (30, 50)])  # Left arrow button (restart)
    pygame.draw.polygon(screen, AMBER, [(180, 10), (220, 30), (180, 50)])  # Play/pause button
    pygame.draw.line(screen, RED, (360, 10), (390, 40), 2)  # Cross button (exit)
    pygame.draw.line(screen, RED, (390, 10), (360, 40), 2)  # Cross button (exit)

    # Draw score and lives
    display_text(f"Score: {score}", font, WHITE, 10, 70)
    display_text(f"Lives: {lives}", font, WHITE, 10, 100)

    pygame.display.update()

    # Limit the frame rate
    pygame.time.Clock().tick(60)
 