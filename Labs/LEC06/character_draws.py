# 실습 과제 진행
from pico2d import *

# TODO: 캐릭터 클래스 제작
# 인스턴스 속성
# - 캐릭터 이미지
# - 중심 좌표 x, y
# - Move에 대한 플래그
# 메서드
# - __init__: 인스턴스 속성 지정
#    - 인수
#       - imagefilename: 이미지 파일 이름
#       - x: 중심점 x좌표
#       - y: 중심점 y좌표
# - draw: 그리기 함수 호출
# - moveRectangle: 사각형 경로로 이동
# - moveCircle: 원 경로로 이동
# - moveTriangle: 삼각형 경로로 이동
class Character:
    pass

# TODO: 배경매니저 클래스 제작
# 인스턴스 속성
# - 배경을 담을 공간: 리스트
# 메서드
# - __init__: 인스턴스 속성 지정
# - append: 배경 추가하기
#   - 인수
#       - imagefilename: 이미지 파일 이름
#       - x: 중심점 x좌표
#       - y: 중심점 y좌표
# - draw: 배경 그리기
class BgManager:
    pass

open_canvas(800, 600)

# TODO: 원 -> 사각형 -> 삼각형 운동 반복하는 코드 만들기
# 구현 아이디어: Character의 움직임 플래그를 이용하여 작동 시켜라
# 원 - 1, 사각형 - 2, 삼각형 - 3으로 두고 원래 자리로 돌아올 때마다 플래그를 바꿔준다

while True:
    clear_canvas()
    update_canvas()
    
    delay(0.01)
close_canvas()