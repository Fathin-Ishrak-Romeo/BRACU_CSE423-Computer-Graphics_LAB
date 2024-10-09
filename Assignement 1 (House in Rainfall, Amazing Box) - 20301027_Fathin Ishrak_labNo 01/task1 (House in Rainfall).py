import glfw
from OpenGL.GL import *
import numpy as np
import time

# Initialize the library
if not glfw.init():
    raise Exception("glfw can not be initialized!")

# Create a windowed mode window and its OpenGL context
window = glfw.create_window(800, 600, "House in Rainfall", None, None)
if not window:
    glfw.terminate()
    raise Exception("glfw window can not be created!")

# Make the window's context current
glfw.make_context_current(window)

# Set the viewport size
glViewport(0, 0, 800, 600)

def draw_house():
    # Draw the base of the house
    glBegin(GL_QUADS)
    glColor3f(0.8, 0.6, 0.4)  # Wall color (light brown)
    glVertex2f(-0.5, -0.5)
    glVertex2f(0.5, -0.5)
    glVertex2f(0.5, 0.2)
    glVertex2f(-0.5, 0.2)
    glEnd()

    # Draw the roof
    glBegin(GL_TRIANGLES)
    glColor3f(0.5, 0.1, 0.1)  # Roof color (dark red)
    glVertex2f(-0.5, 0.2)
    glVertex2f(0, 0.7)
    glVertex2f(0.5, 0.2)
    glEnd()

    # Draw the door
    glBegin(GL_QUADS)
    glColor3f(0.3, 0.2, 0.1)  # Door color (dark brown)
    glVertex2f(-0.1, -0.5)
    glVertex2f(0.1, -0.5)
    glVertex2f(0.1, -0.1)
    glVertex2f(-0.1, -0.1)
    glEnd()

    # Draw the window
    glBegin(GL_QUADS)
    glColor3f(0.7, 0.9, 1.0)  # Window color (light blue)
    glVertex2f(0.2, 0.0)
    glVertex2f(0.4, 0.0)
    glVertex2f(0.4, 0.2)
    glVertex2f(0.2, 0.2)
    glEnd()
    
    glBegin(GL_LINES)
    glColor3f(0.0, 0.0, 0.0)  # Window frame color (black)
    glVertex2f(0.3, 0.0)
    glVertex2f(0.3, 0.2)
    glVertex2f(0.2, 0.1)
    glVertex2f(0.4, 0.1)
    glEnd()

# Increase the number of raindrops
num_raindrops = 300
rain_positions = np.random.rand(num_raindrops, 2) * 2 - 1

def draw_rain():
    global rain_positions
    glPointSize(3)  # Increase raindrop size
    glBegin(GL_POINTS)
    glColor3f(0, 0, 1)
    for pos in rain_positions:
        glVertex2f(pos[0], pos[1])
    glEnd()

    # Update rain positions
    rain_positions[:, 1] -= 0.01
    rain_positions[rain_positions[:, 1] < -1, 1] = 1

rain_angle = 0

def draw_bent_rain():
    global rain_positions, rain_angle
    glPointSize(3)  # Increase raindrop size
    glBegin(GL_POINTS)
    glColor3f(0, 0, 1)
    for pos in rain_positions:
        bent_x = pos[0] + np.sin(rain_angle) * (1 - pos[1])
        glVertex2f(bent_x, pos[1])
    glEnd()

    # Update rain positions
    rain_positions[:, 1] -= 0.01
    rain_positions[rain_positions[:, 1] < -1, 1] = 1

background_color = [0.0, 0.0, 0.2]

def change_background_color():
    glClearColor(background_color[0], background_color[1], background_color[2], 1.0)

def change_color_to_day():
    global background_color
    background_color = [0.5, 0.8, 1.0]  # Light blue for daytime

def change_color_to_night():
    global background_color
    background_color = [0.0, 0.0, 0.2]  # Dark blue for nighttime

def key_callback(window, key, scancode, action, mods):
    global rain_angle
    if key == glfw.KEY_LEFT and (action == glfw.PRESS or action == glfw.REPEAT):
        rain_angle -= 0.1
    elif key == glfw.KEY_RIGHT and (action == glfw.PRESS or action == glfw.REPEAT):
        rain_angle += 0.1
    elif key == glfw.KEY_D and action == glfw.PRESS:
        change_color_to_day()
    elif key == glfw.KEY_N and action == glfw.PRESS:
        change_color_to_night()

glfw.set_key_callback(window, key_callback)

# Loop until the user closes the window
while not glfw.window_should_close(window):
    # Render here, e.g. using pyOpenGL
    glClear(GL_COLOR_BUFFER_BIT)

    change_background_color()
    draw_house()
    draw_bent_rain()

    # Swap front and back buffers
    glfw.swap_buffers(window)

    # Poll for and process events
    glfw.poll_events()
    time.sleep(0.01)

glfw.terminate()
