from pico2d import *
from math import *

open_canvas()
grass = load_image('grass.png')
character = load_image('character.png')

r = 100
theta = 0
x, y = 300, 200
dir = 4
def MoveRect():
    global dir, x, y
    if dir == 1:
        if x < 500: x += 1
        else: dir = 2
    if dir == 2:
        if y > 200: y -= 1
        else: dir = 3
    if dir == 3:
        if x > 300: x -= 1
        else: dir = 4
    if dir == 4:
        if y < 400: y += 1
        else: dir = 1


while True:
    clear_canvas()
    grass.draw(400,30)
    character.draw(400 + r * cos(theta),300 + r*sin(theta))
    character.draw(x, y)
    

    update_canvas()

    theta += 0.1
    MoveRect()  

    delay(0.016)
    if theta >= 1000:
        break
close_canvas()
