from pico2d import *

open_canvas()

grass = load_image('grass.png')
character = load_image('animation_sheet.png')

# fill here
action = 0
frame = 0
WIDTH = 100
HEIGHT = 100



def RunRight():
    global frame
    for x in range(0, 800, 5):
        clear_canvas()
        grass.draw(400, 30)
        character.clip_draw(
            frame * WIDTH, 1 * HEIGHT,
            WIDTH, HEIGHT, 
            x, 300
        )
        update_canvas()
        frame = (frame + 1) % 8
        delay(0.05)

def StandRight():
    global frame
    for x in range(100):
        clear_canvas()
        grass.draw(400, 30)
        character.clip_draw(
            frame * WIDTH, 3 * HEIGHT,
            WIDTH, HEIGHT, 
            800, 300
        )
        update_canvas()
        frame = (frame + 1) % 8
        delay(0.05)

def RunLeft():
    global frame
    for x in range(800, 0, -5):
        clear_canvas()
        grass.draw(400, 30)
        character.clip_draw(
            frame * WIDTH, 0 * HEIGHT,
            WIDTH, HEIGHT, 
            x, 300
        )
        update_canvas()
        frame = (frame + 1) % 8
        delay(0.05)
    
def StandLeft():
    global frame
    for x in range(100):
        clear_canvas()
        grass.draw(400, 30)
        character.clip_draw(
            frame * WIDTH, 2 * HEIGHT,
            WIDTH, HEIGHT, 
            0, 300
        )
        update_canvas()
        frame = (frame + 1) % 8
        delay(0.05)

while True:
    RunRight()
    StandRight()
    RunLeft()
    StandLeft()

close_canvas()

