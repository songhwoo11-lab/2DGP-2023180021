# 실습 과제 진행
from pico2d import *
from math import *

# TODO: 캐릭터 클래스 제작
# 메서드
# - moveRectangle: 사각형 경로로 이동
#   - moveRight: 오른쪽으로 이동
#   - moveUp: 위로 이동
#   - moveLeft: 좌로 이동
#   - moveDown: 아래로 이동
# - moveTriangle: 삼각형 경로로 이동
#   - moveRight: 오른쪽으로 이동
#   - moveUpLeft: 북서 방향으로 이동
#   - moveDownLeft: 남서 방향으로 이동
class Character:
    def __init__(self, imagefilename, x, y):
        self.image = load_image(imagefilename)
        self.x = x
        self.y = y
        self.move_flag = 1

    def draw(self):
        self.image.draw(self.x, self.y)

    def move(self):
        if character.move_flag == 1:
            character.moveCircle()
        elif character.move_flag == 2:
            character.moveRectangle()
        elif character.move_flag == 3:
            character.moveTriangle()
        else:
            pass # 멈춤

    def moveCircle(self):
        global x, y, theta, r
        theta += radians(2)
        self.x = x + r * cos(theta - radians(90))
        self.y = y + r * sin(theta - radians(90))
        if abs(2 * pi - theta) < 1e-10:
            self.x = 400
            self.y = 200
            theta = 0
            self.move_flag = 2
            

    def moveRectangle(self):
        global count
        if count < 100:
            self.moveRight(1)
        elif count < 200:
            self.moveUp(1)
        elif count < 300:
            self.moveLeft(1)
        elif count < 400:
            self.moveDown(1)
        else:
            count = 0
            self.move_flag = 3
            return
        count += 1
    def moveRight(self, x):
        self.x += x
    def moveUp(self, y):
        self.y += y
    def moveLeft(self, x):
        self.x -= x
    def moveDown(self, y):
        self.y -= y

    def moveTriangle(self):
        global count
        if count < 100:
            self.moveRight(1)
        elif count < 150:
            self.moveUpLeft(1)
        elif count < 200:
            self.moveDownLeft(1)    
        else:
            count = 0
            self.move_flag = 1
            return
        count += 1
    def moveUpLeft(self, x):
        self.x -= x
        self.y += 2*x
    def moveDownLeft(self, x):
        self.x -= x
        self.y -= 2*x


class BgManager:
    def __init__(self):
        self.backgrounds = []

    def append(self, imagefilename, x, y):
        image = load_image(imagefilename)
        self.backgrounds.append((image, x, y))

    def draw(self):
        for image, x, y in self.backgrounds:
            image.draw(x, y)

# TODO: 원 -> 사각형 -> 삼각형 운동 반복하는 코드 만들기
# 구현 아이디어: Character의 움직임 플래그를 이용하여 작동 시켜라
# 원 - 1, 사각형 - 2, 삼각형 - 3으로 두고 원래 자리로 돌아올 때마다 플래그를 바꿔준다
open_canvas(800, 600)
character = Character('character.png', 400, 200)
bgmanager = BgManager()
bgmanager.append('sky.png', 400, 300)
bgmanager.append('grass.png', 400, 30)
x, y, theta, r, count = 400, 300, 0, 100, 0

# 테스트용
while True:
    clear_canvas()
    bgmanager.draw()
    character.draw()
    update_canvas()
    print(f"Character Position: ({character.x}, {character.y})")
    print(f"움직임 플래그: {character.move_flag}")

    character.move()

    delay(0.01)
close_canvas()