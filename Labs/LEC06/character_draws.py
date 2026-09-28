# 실습 과제 진행
from pico2d import *
import math

def move_circle():
    for degree in range(360):
        theta = math.radians(degree)
        x = 400 + 100 * math.cos(theta)
        y = 300 + 100 * math.sin(theta)
        draw_boy(x, y)

def move_top():
    print("top")
    for x in range(50, 750, 5):
        draw_boy(x, 550)

def draw_boy(x, y):
    clear_canvas()
    boy.draw(x, y)
    update_canvas()
    delay(0.01)

def move_right():
    print("right")
    for y in range(550, 50, -5):
        draw_boy(750, y)
def move_bottom():
    print("bottom")
    for x in range(750, 50, -5):
        draw_boy(x, 50)
def move_left():
    print("left")
    for y in range(50, 550, 5):
            draw_boy(50, y)

def move_rectangle():
    move_top()
    move_right()
    move_bottom()
    move_left()

def move_triangle():
    print('triangle')

open_canvas(800, 600)
boy = load_image('character.png')


while True:
    # move_circle()
    move_rectangle()
    move_triangle()
    break
close_canvas()
