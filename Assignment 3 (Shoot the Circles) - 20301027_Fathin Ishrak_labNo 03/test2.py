import pygame
import random
import sys
import time

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shoot The Circles")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
TEAL = (0, 255, 255)
AMBER = (255, 191, 0)
BLACK = (0, 0, 0)

# Fonts
font = pygame.font.SysFont(None, 40)

# Shooter settings
shooter_radius = 20
shooter_speed = 5
shooter_color = AMBER
shooter_x = WIDTH // 2
shooter_y = HEIGHT - shooter_radius - 20
shots_fired = 0
missed_shots = 0
max_misses = 3

# Falling circles settings
falling_circles = []
initial_circle_speed = 1
max_circle_speed = 5
falling_circle_min_radius = 10
falling_circle_max_radius = 20
level_threshold = 200

# Score
score = 0
game_over = False
paused = False
delta_time = 0
last_frame_time = time.time()

# Button settings
button_size = 20
restart_button = (10, 10, 20)
pause_button = (180, 10, 20)
exit_button = (360, 10, 20)

# Function to draw the shooter circle
def draw_shooter(x, y, color):
    pygame.draw.circle(screen, color, (x, y), shooter_radius, 2)

# Function to draw the falling circles
def draw_circle(x, y, radius, color):
    pygame.draw.circle(screen, color, (x, y), radius, 2)

# Function to create new falling circles
def create_falling_circle():
    radius = random.randint(falling_circle_min_radius, falling_circle_max_radius)
    x = random.randint(radius, WIDTH - radius)
    return [x, 0, radius, initial_circle_speed + random.uniform(0, 1), WHITE]

# Function to manage falling circles and increase difficulty
def manage_falling_circles():
    global score, game_over
    if len(falling_circles) < 3 + score // 50:  # Gradually increase the number of circles
        falling_circles.append(create_falling_circle())

    for circle in falling_circles:
        circle[1] += circle[3] * delta_time * 60  # Move circles down
        if circle[1] - circle[2] > HEIGHT:  # Circle passed the bottom
            falling_circles.remove(circle)
            missed_shot()

        if shooter_x - shooter_radius <= circle[0] <= shooter_x + shooter_radius and circle[1] >= shooter_y - shooter_radius:
            game_over = True

# Function for shooting mechanics
def fire_shot():
    global shots_fired, score, missed_shots
    shots_fired += 1
    hit = False
    for circle in falling_circles:
        if shooter_x - shooter_radius <= circle[0] <= shooter_x + shooter_radius and shooter_y - 100 <= circle[1] <= shooter_y:
            score += 1
            hit = True
            falling_circles.remove(circle)
            break
    if not hit:
        missed_shots += 1

    if missed_shots >= max_misses:
        game_over()

# Function to reset the game
def reset_game():
    global score, falling_circles, shooter_x, game_over, missed_shots
    score = 0
    missed_shots = 0
    falling_circles.clear()
    shooter_x = WIDTH // 2
    game_over = False

# Function to pause the game
def toggle_pause():
    global paused
    paused = not paused

# Function to calculate delta time
def calculate_delta_time():
    global delta_time, last_frame_time
    current_time = time.time()
    delta_time = current_time - last_frame_time
    last_frame_time = current_time

# Function to display text
def display_text(text, font, color, x, y):
    render = font.render(text, True, color)
    screen.blit(render, (x, y))

# Function to draw buttons
def draw_buttons():
    pygame.draw.line(screen, TEAL, (10 + button_size, 10), (10, 10 + button_size // 2), 2)  # Restart button
    pygame.draw.line(screen, AMBER, (180, 10), (200, 20), 2)  # Play button
    pygame.draw.line(screen, RED, (360, 10), (380, 30), 2)  # Exit button

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
            if 10 <= mouse_x <= 30 and 10 <= mouse_y <= 30:
                reset_game()
            if 180 <= mouse_x <= 200 and 10 <= mouse_y <= 30:
                toggle_pause()
            if 360 <= mouse_x <= 380 and 10 <= mouse_y <= 30:
                print(f"Goodbye! Final Score: {score}")
                pygame.quit()
                sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                fire_shot()

    if not game_over and not paused:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and shooter_x > shooter_radius:
            shooter_x -= shooter_speed * delta_time * 60
        if keys[pygame.K_d] and shooter_x < WIDTH - shooter_radius:
            shooter_x += shooter_speed * delta_time * 60

        manage_falling_circles()

    # Draw game elements
    draw_shooter(shooter_x, shooter_y, shooter_color)
    for circle in falling_circles:
        draw_circle(circle[0], circle[1], circle[2], circle[4])

    draw_buttons()
    display_text(f"Score: {score}", font, WHITE, 10, 70)

    pygame.display.update()
    pygame.time.Clock().tick(60)
     