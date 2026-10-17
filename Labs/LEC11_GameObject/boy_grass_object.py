from pico2d import *
import random


# Game object class here
class Grass:
    def __init__(self):
        self.image = load_image('grass.png')

    def draw(self):
        self.image.draw(400, 30)

    def update(self): pass

class Boy:
    def __init__(self):
        self.x, self.y = random.randint(0,400), 90
        self.frame = random.randint(0, 7)
        self.speed = random.randint(5, 10)
        self.image = load_image('run_animation.png')

    def update(self):
        self.frame = (self.frame + 1) % 8
        self.x += self.speed
        if self.x >= get_canvas_width() + 50:
            self.x = -50

    def draw(self):
        self.image.clip_draw(self.frame*100, 0, 100, 100, self.x, self.y)

class Zombie:
    def __init__(self):
        self.x, self.y = 100, 170
        self.frame = 0
        self.image = load_image('zombie_run_animation.png')

    def update(self):
        self.frame = (self.frame + 1) % 10
        self.x += 5
        if self.x >= get_canvas_width() + 50:
                    self.x = -50

    def draw(self):
        frame_width = self.image.w // 10
        frame_height = self.image.h
        self.image.clip_draw(self.frame*frame_width, 0, frame_width, frame_height, self.x, self.y, frame_width // 2, frame_height // 2)


def reset_world():
    global running, grass, team, world, zombie
    running = True
    world = []
    grass = Grass() # Grass 클래스 이용해서, grass 객체 생성
    world.append(grass)
    team = [Boy() for _ in range(11)]
    world += team
    zombie = Zombie()
    world.append(zombie)


def update_world():
    for obj in world: obj.update() 

def render_world():
    clear_canvas()
    for obj in world: obj.draw() 
    update_canvas()

def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

running = None
grass = None
team = []
world = None
zombie = None
open_canvas()

# 초기화 코드
reset_world()

# 게임 루프 코드
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.05)

# 종료 코드
close_canvas()
