from pico2d import load_image, get_canvas_width

import game_framework

# ----------------------------------------------------------------------
# 새 크기/속도 (물리 단위 기반, boy.py 와 같은 PIXEL_PER_METER 사용)
# ----------------------------------------------------------------------
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm

BIRD_SIZE_M = 2.5  # 화면에 그려지는 새의 가로 크기 (m) - 눈에 잘 띄도록 과장
BIRD_DRAW_W = int(BIRD_SIZE_M * PIXEL_PER_METER)  # 약 83 px
BIRD_DRAW_H = int(BIRD_DRAW_W * 168 / 183)        # 원본 비율 유지

FLY_SPEED_KMPH = 30.0  # 새의 기본 비행 속도 (Km / Hour)
FLY_SPEED_MPM = (FLY_SPEED_KMPH * 1000.0 / 60.0)
FLY_SPEED_MPS = (FLY_SPEED_MPM / 60.0)
FLY_SPEED_PPS = (FLY_SPEED_MPS * PIXEL_PER_METER)

# ----------------------------------------------------------------------
# 날갯짓 애니메이션 (bird_animation.png : 5열 x 3행, 총 14 프레임)
# ----------------------------------------------------------------------
TIME_PER_ACTION = 0.6                    # 한 번 날갯짓하는 데 걸리는 시간 (초)
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION  # 초당 날갯짓 횟수
FRAMES_PER_ACTION = 14                   # 한 번 날갯짓에 사용되는 프레임 수

SHEET_COLS, SHEET_ROWS = 5, 3
FRAME_W, FRAME_H = 183, 168
SHEET_H = 506


class Bird:
    image = None  # 모든 새가 하나의 이미지를 공유

    def __init__(self, x=800, y=450):
        if Bird.image is None:
            Bird.image = load_image('bird_animation.png')

        self.x, self.y = x, y
        self.dir = 1                # -1: 왼쪽, 1: 오른쪽
        self.speed = FLY_SPEED_PPS
        self.frame = 0

    def update(self):
        dt = game_framework.frame_time

        # 날갯짓 프레임 진행
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * dt) % FRAMES_PER_ACTION

        # 좌우 이동 및 화면 끝에서 방향 전환
        self.x += self.dir * self.speed * dt
        half_w = BIRD_DRAW_W / 2
        right_limit = get_canvas_width() - half_w
        if self.x > right_limit:
            self.x = right_limit
            self.dir = -1
        elif self.x < half_w:
            self.x = half_w
            self.dir = 1

    def draw(self):
        index = int(self.frame)
        col = index % SHEET_COLS
        row = index // SHEET_COLS                 # 위에서부터 몇 번째 행인지
        left = col * FRAME_W
        bottom = SHEET_H - (row + 1) * FRAME_H     # pico2d 는 좌하단이 원점

        Bird.image.clip_draw(left, bottom, FRAME_W, FRAME_H,
                             self.x, self.y, BIRD_DRAW_W, BIRD_DRAW_H)
