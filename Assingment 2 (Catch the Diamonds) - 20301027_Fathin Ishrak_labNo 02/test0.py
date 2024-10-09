

import random
import time
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Game variables
catcher_pos = 0
diamond_x = random.randint(-9, 9)
diamond_y = 10
diamond_speed = 0.02
score = 0
game_over = False
game_paused = False

# Colors
catcher_color = [1.0, 1.0, 1.0]
diamond_color = [random.random(), random.random(), random.random()]

# Window size
window_width = 800
window_height = 600

# Time tracking for delta time
last_time = time.time()


def draw_catcher():
    """Draw the catcher using midpoint line drawing algorithm"""
    glColor3f(*catcher_color)
    glBegin(GL_LINES)
    glVertex2f(catcher_pos - 1.5, -9.5)
    glVertex2f(catcher_pos + 1.5, -9.5)
    glVertex2f(catcher_pos - 1.5, -9)
    glVertex2f(catcher_pos + 1.5, -9)
    glVertex2f(catcher_pos - 1.5, -9.5)
    glVertex2f(catcher_pos - 1.5, -9)
    glVertex2f(catcher_pos + 1.5, -9.5)
    glVertex2f(catcher_pos + 1.5, -9)
    glEnd()


def draw_diamond():
    """Draw the diamond using the midpoint line drawing algorithm"""
    glColor3f(*diamond_color)
    glBegin(GL_LINES)
    glVertex2f(diamond_x, diamond_y)
    glVertex2f(diamond_x - 0.5, diamond_y + 0.5)
    glVertex2f(diamond_x - 0.5, diamond_y + 0.5)
    glVertex2f(diamond_x, diamond_y + 1)
    glVertex2f(diamond_x, diamond_y + 1)
    glVertex2f(diamond_x + 0.5, diamond_y + 0.5)
    glVertex2f(diamond_x + 0.5, diamond_y + 0.5)
    glVertex2f(diamond_x, diamond_y)
    glEnd()


def draw_buttons():
    """Draw buttons using midpoint line algorithm"""
    # Restart button (teal arrow)
    glColor3f(0.0, 1.0, 1.0)
    glBegin(GL_LINES)
    glVertex2f(-9.5, 9)
    glVertex2f(-8.5, 9.5)
    glVertex2f(-8.5, 9.5)
    glVertex2f(-9.5, 10)
    glEnd()

    # Play/Pause button (amber)
    glColor3f(1.0, 0.6, 0.0)
    if game_paused:
        # Play icon
        glBegin(GL_LINES)
        glVertex2f(0.0, 9)
        glVertex2f(0.5, 9.5)
        glVertex2f(0.5, 9.5)
        glVertex2f(0.0, 10)
        glEnd()
    else:
        # Pause icon
        glBegin(GL_LINES)
        glVertex2f(-0.2, 9)
        glVertex2f(-0.2, 10)
        glVertex2f(0.2, 9)
        glVertex2f(0.2, 10)
        glEnd()

    # Quit button (red cross)
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_LINES)
    glVertex2f(8.5, 9)
    glVertex2f(9.5, 10)
    glVertex2f(9.5, 9)
    glVertex2f(8.5, 10)
    glEnd()


def check_collision():
    global score, diamond_y, diamond_x, diamond_color, diamond_speed, game_over, catcher_color
    if -9.5 <= diamond_y <= -9 and abs(catcher_pos - diamond_x) < 1.5:
        score += 1
        print(f"Score: {score}")
        # Reset diamond position and speed
        diamond_y = 10
        diamond_x = random.randint(-9, 9)
        diamond_color = [random.random(), random.random(), random.random()]
        diamond_speed += 0.002
    elif diamond_y <= -10:
        game_over = True
        catcher_color = [1.0, 0.0, 0.0]  # Change catcher color to red
        print(f"Game over! Score: {score}")


def update_diamond():
    global diamond_y
    if not game_over and not game_paused:
        diamond_y -= diamond_speed
        check_collision()


def keyboard_input(key, x, y):
    global catcher_pos
    if not game_over and not game_paused:
        if key == b'a' and catcher_pos > -8.5:
            catcher_pos -= 0.5
        elif key == b'd' and catcher_pos < 8.5:
            catcher_pos += 0.5


def mouse_input(button, state, x, y):
    global game_over, score, diamond_y, diamond_x, diamond_speed, catcher_color, game_paused
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        # Map mouse coordinates to OpenGL coordinates
        mouse_x = (x / window_width) * 20 - 10
        mouse_y = 10 - (y / window_height) * 20
        # Check Restart button click
        if -9.5 <= mouse_x <= -8.5 and 9 <= mouse_y <= 10:
            print("Starting Over!")
            game_over = False
            score = 0
            diamond_y = 10
            diamond_x = random.randint(-9, 9)
            diamond_speed = 0.02
            catcher_color = [1.0, 1.0, 1.0]
        # Check Play/Pause button click
        elif -0.5 <= mouse_x <= 0.5 and 9 <= mouse_y <= 10:
            game_paused = not game_paused
        # Check Quit button click
        elif 8.5 <= mouse_x <= 9.5 and 9 <= mouse_y <= 10:
            print(f"Goodbye! Score: {score}")
            glutLeaveMainLoop()


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_catcher()
    draw_diamond()
    draw_buttons()
    update_diamond()
    glutSwapBuffers()


def timer(value):
    glutPostRedisplay()
    glutTimerFunc(16, timer, 0)


def initialize():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-10, 10, -10, 10, -1.0, 1.0)


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(window_width, window_height)
    glutCreateWindow("Catch the Diamonds!")
    initialize()
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard_input)
    glutMouseFunc(mouse_input)
    glutTimerFunc(16, timer, 0)
    glutMainLoop()


if __name__ == "__main__":
    main()

#python catch_the_diamonds.py
