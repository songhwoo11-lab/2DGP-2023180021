# 실습 과제 진행
from pico2d import *
import math

def move_circle():
    
    for degree in range(360):
        clear_canvas()
        theta = math.radians(degree)
        x = 400 + 100 * math.cos(theta)
        y = 300 + 100 * math.sin(theta)
        boy.draw(x, y)
        delay(0.1)
        update_canvas()

def move_top():
    print("top")
def move_right():
    print("right")
def move_bottom():
    print("bottom")
def move_left():
    print("left")

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
    move_circle()
    move_rectangle()
    move_triangle()
    break
close_canvas()
