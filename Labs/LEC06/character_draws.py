# 실습 과제 진행
from pico2d import *

def move_circle():
    print('circle')

def move_rectangle():
    print('rectangle')

def move_triangle():
    print('triangle')

open_canvas(800, 600)
update_canvas()
close_canvas()

while True:
    move_circle()
    move_rectangle()
    move_triangle()