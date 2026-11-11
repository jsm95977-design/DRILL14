from pico2d import load_image

import game_framework

# ----------------------------------------------------------------------
# 새 크기/속도 (물리 단위 기반, boy.py 와 같은 PIXEL_PER_METER 사용)
# ----------------------------------------------------------------------
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm

BIRD_SIZE_M = 2.5  # 화면에 그려지는 새의 가로 크기 (m) - 눈에 잘 띄도록 과장
BIRD_DRAW_W = int(BIRD_SIZE_M * PIXEL_PER_METER)  # 약 83 px
BIRD_DRAW_H = int(BIRD_DRAW_W * 168 / 183)        # 원본 비율 유지

# ----------------------------------------------------------------------
# 스프라이트 시트 정보 (bird_animation.png : 5열 x 3행, 총 14 프레임)
# ----------------------------------------------------------------------
SHEET_COLS, SHEET_ROWS = 5, 3
FRAME_W, FRAME_H = 183, 168
SHEET_H = 506


class Bird:
    image = None  # 모든 새가 하나의 이미지를 공유

    def __init__(self, x=800, y=450):
        if Bird.image is None:
            Bird.image = load_image('bird_animation.png')

        self.x, self.y = x, y
        self.frame = 0

    def update(self):
        pass

    def draw(self):
        # 첫 번째 프레임(좌상단)만 그림
        bottom = SHEET_H - FRAME_H  # pico2d 는 좌하단이 원점
        Bird.image.clip_draw(0, bottom, FRAME_W, FRAME_H,
                             self.x, self.y, BIRD_DRAW_W, BIRD_DRAW_H)
