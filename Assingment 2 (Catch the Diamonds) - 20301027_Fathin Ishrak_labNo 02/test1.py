import random
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *

# Global Variables
catcher_x = 0
catcher_width = 100
diamond_x = 0
diamond_y = 500
diamond_speed = 0.1
score = 0
game_over = False
paused = False

# Colors for diamonds
colors = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (1, 0, 1), (0, 1, 1)]

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, 800, 0, 600)

def draw_catcher():
    global catcher_x
    glColor3f(1, 1, 1)
    glBegin(GL_QUADS)
    glVertex2f(catcher_x, 50)
    glVertex2f(catcher_x + catcher_width, 50)
    glVertex2f(catcher_x + catcher_width, 60)
    glVertex2f(catcher_x, 60)
    glEnd()

def draw_diamond():
    global diamond_x, diamond_y
    glColor3f(*random.choice(colors))  # Random color for the diamond
    glBegin(GL_QUADS)
    glVertex2f(diamond_x, diamond_y)
    glVertex2f(diamond_x + 20, diamond_y)
    glVertex2f(diamond_x + 20, diamond_y + 20)
    glVertex2f(diamond_x, diamond_y + 20)
    glEnd()

def update_diamond():
    global diamond_y, diamond_speed, diamond_x, game_over, score
    if not paused and not game_over:
        diamond_y -= diamond_speed
        if diamond_y < 50 and catcher_x < diamond_x < catcher_x + catcher_width:
            # Caught the diamond
            score += 1
            print(f"Score: {score}")
            reset_diamond()
        elif diamond_y < 0:
            # Missed the diamond
            game_over = True
            print(f"Game over! Score: {score}")
        # Increase diamond speed
        diamond_speed += 0.001

def reset_diamond():
    global diamond_y, diamond_x
    diamond_y = 600
    diamond_x = random.randint(0, 780)

def draw_buttons():
    # Left restart button
    glColor3f(0, 1, 1)
    glBegin(GL_QUADS)
    glVertex2f(50, 550)
    glVertex2f(80, 550)
    glVertex2f(80, 580)
    glVertex2f(50, 580)
    glEnd()

    # Pause/play button
    glColor3f(1, 0.5, 0)
    glBegin(GL_QUADS)
    glVertex2f(380, 550)
    glVertex2f(420, 550)
    glVertex2f(420, 580)
    glVertex2f(380, 580)
    glEnd()

    # Quit button
    glColor3f(1, 0, 0)
    glBegin(GL_QUADS)
    glVertex2f(700, 550)
    glVertex2f(730, 550)
    glVertex2f(730, 580)
    glVertex2f(700, 580)
    glEnd()

def restart_game():
    global score, game_over, diamond_speed, catcher_x
    score = 0
    game_over = False
    diamond_speed = 0.1
    catcher_x = 400
    reset_diamond()
    print("Starting over!")

def toggle_pause():
    global paused
    paused = not paused
    print("Game Paused" if paused else "Game Resumed")

def quit_game():
    print(f"Goodbye! Final Score: {score}")
    pygame.quit()
    quit()

def handle_mouse_click(x, y):
    if 50 < x < 80 and 550 < y < 580:  # Restart button
        restart_game()
    elif 380 < x < 420 and 550 < y < 580:  # Pause/Play button
        toggle_pause()
    elif 700 < x < 730 and 550 < y < 580:  # Quit button
        quit_game()

def main():
    global catcher_x
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    init()

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    catcher_x -= 10
                if event.key == pygame.K_RIGHT:
                    catcher_x += 10
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                handle_mouse_click(mouse_x, 600 - mouse_y)

        glClear(GL_COLOR_BUFFER_BIT)

        if not game_over:
            update_diamond()

        draw_catcher()
        draw_diamond()
        draw_buttons()

        pygame.display.flip()
        clock.tick(60)  # Set frame rate to 60 FPS

if __name__ == '__main__':
    main()
