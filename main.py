import pygame
import numpy as np

# Pygame 초기화
pygame.init()

# 화면 설정
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Simple Sphere Ray Tracing")

# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# 구 정의
sphere_center = np.array([400, 300, 0])  # 구의 중심
sphere_radius = 100  # 구의 반지름

# 조명 설정
light_pos = np.array([200, 100, -100])  # 광원 위치

# 벡터 정규화 함수 (normalize)
def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v  # 0 벡터는 정규화 불가, 그대로 반환
    return v / norm

# 광선과 구의 충돌 판별 함수
def ray_sphere_intersection(ray_origin, ray_direction, sphere_center, sphere_radius):
    oc = ray_origin - sphere_center
    a = np.dot(ray_direction, ray_direction)
    b = 2.0 * np.dot(oc, ray_direction)
    c = np.dot(oc, oc) - sphere_radius ** 2
    discriminant = b ** 2 - 4 * a * c

    if discriminant < 0:
        return None  # 충돌 없음
    else:
        t1 = (-b - np.sqrt(discriminant)) / (2.0 * a)
        t2 = (-b + np.sqrt(discriminant)) / (2.0 * a)
        return t1 if t1 < t2 else t2  # 더 가까운 충돌점 반환

# 메인 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 화면 초기화
    screen.fill(BLACK)

    # 각 픽셀에 대해 레이 캐스팅
    step = 2  # 픽셀 간격 (높일수록 해상도 줄고 속도 빨라짐)

    for x in range(0, width, step):
        for y in range(0, height, step):
            # 나머지 코드는 동일
            ray_origin = np.array([x, y, -200])
            ray_direction = np.array([0, 0, 1])
            ray_direction = normalize(ray_direction)
            t = ray_sphere_intersection(ray_origin, ray_direction, sphere_center, sphere_radius)

            if t is not None:
                hit_point = ray_origin + t * ray_direction
                normal = normalize(hit_point - sphere_center)
                light_dir = normalize(light_pos - hit_point)
                brightness = max(np.dot(normal, light_dir), 0)
                color = (
                    int(RED[0] * brightness),
                    int(RED[1] * brightness),
                    int(RED[2] * brightness),
                )
                screen.set_at((x, y), color)


    # 화면 업데이트
    pygame.display.flip()


# Pygame 종료
pygame.quit()
