# 실습 과제 진행
from pico2d import *
import math

stride = 5
rectangleX = 50
rectangleY = 50
rectangleWidth = 700
rectangleHeight = 500

def move_circle():
    for degree in range(0, 360, stride):
        theta = math.radians(degree)
        x = 400 + 100 * math.cos(theta)
        y = 300 + 100 * math.sin(theta)
        draw_boy(x, y)

def move_top():
    print("top")
    for x in range(rectangleX, rectangleX + rectangleWidth, stride):
        draw_boy(x, rectangleY + rectangleHeight)

def draw_boy(x, y):
    clear_canvas()
    boy.draw(x, y)
    update_canvas()
    delay(0.01)

def move_right():
    print("right")
    for y in range(rectangleY + rectangleHeight, rectangleY, -stride):
        draw_boy(rectangleX + rectangleWidth, y)
def move_bottom():
    print("bottom")
    for x in range(rectangleX + rectangleWidth, rectangleX, -stride):
        draw_boy(x, rectangleY)
def move_left():
    print("left")
    for y in range(rectangleY, rectangleY + rectangleHeight, stride):
            draw_boy(rectangleX, y)

def move_rectangle():
    move_top()
    move_right()
    move_bottom()
    move_left()

def move_topright():
    print("topright")
    for y in range(550, 50, -stride):
        draw_boy(400 + 3.5 * (550 - y) // stride, y)
def move_topleft():
    print("topleft")
    for y in range(50, 550, stride):
        draw_boy(50 + 3.5 * (y - 50) // stride, y)

def move_triangle():
    print('triangle')
    move_topright()
    move_bottom()
    move_topleft()

open_canvas(800, 600)
boy = load_image('character.png')

while True:
    # move_circle()
    # move_rectangle()
    move_triangle()
    break
close_canvas()
