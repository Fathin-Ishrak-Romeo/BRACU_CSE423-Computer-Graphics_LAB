import glfw
from OpenGL.GL import *
import sys
import random
import time

width, height = 800, 600
points = []
blink = False
frozen = False
speed = 1.0
last_blink_time = 0

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glPointSize(5.0)

def display():
    global blink, points, last_blink_time
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glBegin(GL_POINTS)
    current_time = time.time()
    for point in points:
        x, y, r, g, b, dx, dy = point
        if blink and (current_time - last_blink_time) >= 0.5:
            point[2:5] = (0.0, 0.0, 0.0) if (r, g, b) != (0.0, 0.0, 0.0) else (random.random(), random.random(), random.random())
            last_blink_time = current_time
        glColor3f(r, g, b)
        glVertex2f(x, y)
    glEnd()
    glfw.swap_buffers(window)

def update_points():
    global points, speed
    if not frozen:
        for point in points:
            point[0] += point[5] * speed * 0.01
            point[1] += point[6] * speed * 0.01
            if point[0] >= 1 or point[0] <= -1:
                point[5] *= -1
            if point[1] >= 1 or point[1] <= -1:
                point[6] *= -1

def mouse_click(window, button, action, mods):
    if button == glfw.MOUSE_BUTTON_RIGHT and action == glfw.PRESS:
        x, y = glfw.get_cursor_pos(window)
        x = (x / width) * 2 - 1
        y = 1 - (y / height) * 2
        points.append([x, y, random.random(), random.random(), random.random(), random.choice([-1, 1]), random.choice([-1, 1])])
    elif button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
        global blink
        blink = not blink

def key_pressed(window, key, scancode, action, mods):
    global speed, frozen
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)
    elif key == glfw.KEY_UP and action == glfw.PRESS:
        speed += 0.1
    elif key == glfw.KEY_DOWN and action == glfw.PRESS:
        speed = max(0.1, speed - 0.1)
    elif key == glfw.KEY_SPACE and action == glfw.PRESS:
        frozen = not frozen

if not glfw.init():
    sys.exit()

window = glfw.create_window(width, height, "Amazing Box", None, None)
if not window:
    glfw.terminate()
    sys.exit()

glfw.make_context_current(window)
glfw.set_mouse_button_callback(window, mouse_click)
glfw.set_key_callback(window, key_pressed)

init()

while not glfw.window_should_close(window):
    display()
    update_points()
    glfw.poll_events()

glfw.terminate()
