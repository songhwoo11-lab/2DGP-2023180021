# 실습 과제 진행
from pico2d import *
import math

CircleX, CircleY = 400, 300
CircleRadius = 100
stride = 5
rectangleX = 50
rectangleY = 50
rectangleWidth = 700
rectangleHeight = 500
TriangleX, TriangleY = 400, 550
TriangleBottomDegree = 700
TriangleMINX = 50
TriangleMINY = 50

def move_circle():
    for degree in range(0, 360, stride):
        theta = math.radians(degree)
        x = CircleX + CircleRadius * math.cos(theta)
        y = CircleY + CircleRadius * math.sin(theta)
        draw_boy(x, y)

def move_top():
    print("top")
    for x in range(rectangleX, rectangleX + rectangleWidth, stride):
        draw_boy(x, rectangleY + rectangleHeight)

def draw_boy(x, y):
    clear_canvas()
    sky.draw(400,330)
    grass.draw(400,30)
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
    for y in range(TriangleY, 50, -stride):
        draw_boy(TriangleX + ((TriangleBottomDegree / 2) / ((TriangleY - TriangleMINY) // stride)) * (TriangleY - y) // stride, y)
def move_topleft():
    print("topleft")
    for y in range(TriangleMINY, TriangleY, stride):
        draw_boy(50 + ((TriangleBottomDegree / 2) / ((TriangleY - TriangleMINY) // stride)) * (y - TriangleMINY) // stride, y)
def move_bottomTRIANGLE():
    print("bottom")
    for x in range(TriangleMINX + TriangleBottomDegree, TriangleMINX, -stride):
        draw_boy(x, TriangleMINY)

def move_triangle():
    print('triangle')
    move_topright()
    move_bottomTRIANGLE()
    move_topleft()

open_canvas(800, 600)
boy = load_image('character.png')
sky = load_image('sky.png')
grass = load_image('grass.png')

while True:
    # move_circle()
    # move_rectangle()
    move_triangle()
    break
close_canvas()
