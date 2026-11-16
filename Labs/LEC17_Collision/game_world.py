world = [[], [], []]  # 0: 배경, 1: 오브젝트, 2: UI
collision_pairs = {}

def add_oject(o, depth=1):
    world[depth].append(o)

def add_objects(ol, depth=1):
    world[depth] += ol

def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            remove_collision_object(o)
            return

def update():
    for layer in world:
        for o in layer[:]:
            o.update()

def render():
    for layer in world:
        for o in layer[:]:
            o.draw()

def clear():
    for layer in world:
        layer.clear()

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a <left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True

def add_collision_pair(group, a, b):
    if group not in collision_pairs: # 처음 등록하는 충돌 그룹이면, 충돌 그룸을 생성한다.
        collision_pairs[group] = [[], []] # a와 b를 담을 리스트 2개를 생성
    if a:
        collision_pairs[group][0].append(a) # a를 group에 추가
    if b:
        collision_pairs[group][1].append(b) # b를 group에 추가

def handle_collisions():
    for group, pairs in collision_pairs.items():
        for a in pairs[0]:
            for b in pairs[1]: 
                if collide(a, b):
                    a.handle_collision(group, b) # 충돌 정보와 충돌된 상대 객체를 넘겨줘서 충돌 처리함
                    b.handle_collision(group, a)

def remove_collision_object(o):
    for pairs in collision_pairs.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)
    