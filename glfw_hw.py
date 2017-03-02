#!/usr/bin/env python3

from datetime import datetime
from math import *
from pyglet.gl import *


window = pyglet.window.Window(600, 600, caption="Clock")
glClearColor(1, 1, 1, 1)
hc_r = 0.4
hc_g = 0
hc_b = 1
vertices = 4
circle = False
coords = []
for i in range(3):
    coords.append([0, 0])
angles = [0] * 3
hands_lengths = [245, 220, 175]
plus_symbols = (65363, 65362, 65451)
minus_symbols = (65361, 65364, 65453)


@window.event
def on_draw():
    window.clear()
    glLineWidth(10)
    if circle:
        draw_n_gon(100)
    else:
        draw_n_gon(vertices)
    glLineWidth(5)
    glBegin(GL_LINES)  # notches to indicate hours
    glColor3f(0, 0.6, 0.6)
    for i in range(1, 13):
        xcoord = cos(pi*i/6)
        ycoord = sin(pi*i/6)
        glVertex2f(300 + xcoord*240, 300 + ycoord*240)
        glVertex2f(300 + xcoord*225, 300 + ycoord*225)
    glEnd()
    for i in range(3):  # hands
        glLineWidth(3+2*i)
        glBegin(GL_LINES)
        glColor3f(hc_r, hc_g, hc_b)
        glVertex2f(300 - coords[i][0]/10, 300 - coords[i][1]/10)
        glVertex2f(300 + coords[i][0], 300 + coords[i][1])
        glEnd()
        

def update(dt):
    global ctime, coords  # adding how much time passed since the last frame and updating ctime & coords
    ctime[0] = (ctime[0] + dt) % 60
    ctime[1] = (ctime[1] + dt / 60) % 60
    ctime[2] = (ctime[2] + dt / 3600) % 12
    for i in range(3):
        angles[i] = pi / 2 - pi * ctime[i] / (30 if i < 2 else 6)
    for i in range(3):
        coords[i][0] = hands_lengths[i] * cos(angles[i])
        coords[i][1] = hands_lengths[i] * sin(angles[i])


def draw_n_gon(n):
    glBegin(GL_LINE_LOOP)  # face of the clock
    glColor3f(1, 0, 0.4)
    for i in range(n):
        angle = pi/2 + 2 * pi * i / n - pi / n
        radius = 250 / cos(pi/n)
        glVertex2f(300 + radius  * cos(angle), 300 + (255 / cos(pi/n)) * sin(angle))
    glEnd()


@window.event
def on_mouse_press(x, y, button, modifier):
    global hc_r, hc_g, hc_b  # changing color of hands based of where we clicked
    hc_r = (hc_r + x/600) % 1
    hc_g = (hc_g + y/600) % 1
    hc_b = (hc_b + abs(x - y)/600) % 1


@window.event
def on_key_press(symbol, modifiers):
    global vertices, circle
    if not circle and symbol in plus_symbols:
        if vertices < 100:
            vertices += 1
    elif not circle and symbol in minus_symbols:
        if vertices > 4:
            vertices -= 1
    else:
        circle = not circle


# initial position of clock hands
now = datetime.now()
ctime = [now.second + now.microsecond/1_000_000,
         now.minute + now.second / 60,
         now.hour + now.minute / 60]
for i in range(3):  # damn hours, y r u 12 no 60?
    angles[i] = pi/2 - pi * ctime[i] / (30 if i < 2 else 6)  # finding the angle, at which each hand is pointing
for i in range(3):
    coords[i][0] = hands_lengths[i] * cos(angles[i])  # and here we transform it into normal coords
    coords[i][1] = hands_lengths[i] * sin(angles[i])
pyglet.clock.schedule_interval(update, 1/30)
pyglet.app.run()
