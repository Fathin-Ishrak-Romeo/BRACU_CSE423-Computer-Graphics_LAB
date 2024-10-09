import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shoot The Circles!")

# Colors
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Shooter settings
shooter_radius = 30
shooter_x = WIDTH // 2
shooter_y = HEIGHT - shooter_radius - 10
shooter_speed = 7

# Projectile settings
projectile_radius = 5
projectile_speed = 10
projectiles = []

# Circle settings
circle_radius = 30
falling_circles = []
circle_speed = 5
circle_interval = 1500  # Time between falling circles (milliseconds)
last_circle_time = pygame.time.get_ticks()

# Score and Game Over settings
score = 0
misses = 0
misfires = 0
game_over = False

# Fonts
font = pygame.font.SysFont(None, 36)

# Button dimensions and positions
btn_size = 50
btn_left = pygame.Rect(10, 10, btn_size, btn_size)
btn_play_pause = pygame.Rect(WIDTH // 2 - btn_size // 2, 10, btn_size, btn_size)
btn_exit = pygame.Rect(WIDTH - btn_size - 10, 10, btn_size, btn_size)

# Game state
paused = False


def draw_circle(x, y, radius, color):
    pygame.draw.circle(screen, color, (x, y), radius, 2)


def draw_projectile(x, y):
    pygame.draw.circle(screen, WHITE, (x, y), projectile_radius)


def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


def check_collision(projectile, circle):
    dx = projectile[0] - circle[0]
    dy = projectile[1] - circle[1]
    distance = (dx**2 + dy**2)**0.5
    return distance < circle_radius + projectile_radius


# Main game loop
running = True
while running:
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            if btn_left.collidepoint(event.pos):
                # Restart the game
                score = 0
                misses = 0
                misfires = 0
                falling_circles = []
                projectiles = []
                game_over = False
                paused = False
            elif btn_play_pause.collidepoint(event.pos):
                # Pause or play the game
                paused = not paused
            elif btn_exit.collidepoint(event.pos):
                # Exit the game
                print(f"Goodbye! Final score: {score}")
                pygame.quit()
                sys.exit()

    if not game_over and not paused:
        # Shooter movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and shooter_x - shooter_speed - shooter_radius > 0:
            shooter_x -= shooter_speed
        if keys[pygame.K_d] and shooter_x + shooter_speed + shooter_radius < WIDTH:
            shooter_x += shooter_speed
        if keys[pygame.K_SPACE]:
            if len(projectiles) < 5:  # Limit the number of projectiles on screen
                projectiles.append([shooter_x, shooter_y - shooter_radius])

        # Circle generation
        if pygame.time.get_ticks() - last_circle_time > circle_interval:
            circle_x = random.randint(circle_radius, WIDTH - circle_radius)
            falling_circles.append([circle_x, circle_radius])
            last_circle_time = pygame.time.get_ticks()

        # Move circles and check for missed circles
        for circle in falling_circles[:]:
            circle[1] += circle_speed
            if circle[1] - circle_radius > HEIGHT:
                misses += 1
                falling_circles.remove(circle)
                if misses >= 3:
                    game_over = True

        # Move projectiles
        for projectile in projectiles[:]:
            projectile[1] -= projectile_speed
            if projectile[1] < 0:
                misfires += 1
                projectiles.remove(projectile)
                if misfires >= 3:
                    game_over = True

        # Check for collisions
        for projectile in projectiles[:]:
            for circle in falling_circles[:]:
                if check_collision(projectile, circle):
                    projectiles.remove(projectile)
                    falling_circles.remove(circle)
                    score += 1
                    break

    # Drawing
    draw_circle(shooter_x, shooter_y, shooter_radius, YELLOW)

    for projectile in projectiles:
        draw_projectile(projectile[0], projectile[1])

    for circle in falling_circles:
        draw_circle(circle[0], circle[1], circle_radius, YELLOW)

    draw_text(f"Score: {score}", font, WHITE, 10, HEIGHT - 40)
    draw_text(f"Misses: {misses}", font, WHITE, 10, HEIGHT - 80)

    if game_over:
        draw_text("Game Over", font, RED, WIDTH // 2 - 100, HEIGHT // 2)
        draw_text(f"Final Score: {score}", font, RED, WIDTH // 2 - 100, HEIGHT // 2 + 50)

    # Draw buttons
    pygame.draw.rect(screen, WHITE, btn_left, 2)
    pygame.draw.polygon(screen, WHITE, [(btn_left.left + 10, btn_left.centery), (btn_left.right - 10, btn_left.centery - 10), (btn_left.right - 10, btn_left.centery + 10)])
    pygame.draw.rect(screen, YELLOW, btn_play_pause, 2)
    pygame.draw.rect(screen, RED, btn_exit, 2)
    pygame.draw.line(screen, WHITE, (btn_exit.left + 10, btn_exit.top + 10), (btn_exit.right - 10, btn_exit.bottom - 10), 2)
    pygame.draw.line(screen, WHITE, (btn_exit.left + 10, btn_exit.bottom - 10), (btn_exit.right - 10, btn_exit.top + 10), 2)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
