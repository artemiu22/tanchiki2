import pygame
import sys

pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Танчики")

# Цвета
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Параметры танков
tank1_pos = [100, 100]
tank2_pos = [600, 400]
tank_size = 40
tank1_hp = 100
tank2_hp = 500
tank1_color = GREEN
tank2_color = BLUE

# Списки снарядов
bullets = []  # Снаряды первого танка
bullets2 = []  # Снаряды второго танка
bullet_speed1 = 20
bullet_speed2= 40

# Шрифты
font = pygame.font.SysFont(None, 36)


def draw_bullet(surface, bullet, is_tank1=True):
    """Отрисовка снаряда"""
    color = tank1_color if is_tank1 else tank2_color
    pygame.draw.rect(surface, color, bullet)


def draw_tank(surface, position, color, hp):
    """Отрисовка танка с отображением HP"""
    # Рисуем корпус танка
    pygame.draw.rect(surface, color, (position[0], position[1], tank_size, tank_size))



    # Отображаем HP над танком
    hp_text = font.render(str(hp), True, WHITE)
    surface.blit(hp_text, (position[0], position[1] - 30))


def draw_hud(surface):
    """Отрисовка интерфейса"""
    # HP первого танка
    tank1_hp_text = font.render(f"Танк 1 HP: {tank1_hp}", True, GREEN)
    surface.blit(tank1_hp_text, (10, 10))

    # HP второго танка
    tank2_hp_text = font.render(f"Танк 2 HP: {tank2_hp}", True, BLUE)
    surface.blit(tank2_hp_text, (WIDTH - 200, 10))



def check_collision(bullet, tank_pos):
    """Проверка столкновения снаряда с танком"""
    tank_rect = pygame.Rect(tank_pos[0], tank_pos[1], tank_size, tank_size)
    return bullet.colliderect(tank_rect)


def game_loop():
    global tank1_hp, tank2_hp

    clock = pygame.time.Clock()
    running = True

    # Переменные для ограничения скорости стрельбы
    tank1_shoot_cooldown = 0
    tank2_shoot_cooldown = 0
    shoot_delay1 = 30  # Задержка между выстрелами 
    shoot_delay2 = 2
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        if tank1_shoot_cooldown > 0:
            tank1_shoot_cooldown -= 1
        if tank2_shoot_cooldown > 0:
            tank2_shoot_cooldown -= 1

        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and tank1_pos[0] > 0:
            tank1_pos[0] -= 5
        if keys[pygame.K_d] and tank1_pos[0] < WIDTH - tank_size:
            tank1_pos[0] += 5
        if keys[pygame.K_w] and tank1_pos[1] > 0:
            tank1_pos[1] -= 5
        if keys[pygame.K_s] and tank1_pos[1] < HEIGHT - tank_size:
            tank1_pos[1] += 5
        if keys[pygame.K_SPACE] and tank1_shoot_cooldown == 0:
            
            bullet_rect = pygame.Rect(
                tank1_pos[0] + tank_size // 2 - 2,
                tank1_pos[1] + tank_size // 2 - 2,
                5, 5
            )
            bullets.append(bullet_rect)
            tank1_shoot_cooldown = shoot_delay1

        # Управление танком 2
        if keys[pygame.K_LEFT] and tank2_pos[0] > 0:
            tank2_pos[0] -= 5
        if keys[pygame.K_RIGHT] and tank2_pos[0] < WIDTH - tank_size:
            tank2_pos[0] += 5
        if keys[pygame.K_UP] and tank2_pos[1] > 0:
            tank2_pos[1] -= 5
        if keys[pygame.K_DOWN] and tank2_pos[1] < HEIGHT - tank_size:
            tank2_pos[1] += 5
        if keys[pygame.K_m] and tank2_shoot_cooldown == 0:
            bullet_rect = pygame.Rect(
                tank2_pos[0] + tank_size // 2 - 2,
                tank2_pos[1] + tank_size // 2 - 2,
                5, 5
            )
            bullets2.append(bullet_rect)
            tank2_shoot_cooldown = shoot_delay2

        # Обновление позиций снарядов первого танка
        for bullet in bullets[:]:
            bullet.x += bullet_speed2
            if bullet.x > WIDTH or bullet.x < 0:
                bullets.remove(bullet)
            elif check_collision(bullet, tank2_pos):
                tank2_hp -= 50
                bullets.remove(bullet)
                print(f"Танк 2 получил урон! HP: {tank2_hp}")

        # Обновление позиций снарядов второго танка
        for bullet in bullets2[:]:
            bullet.x -= bullet_speed1
            if bullet.x < 0 or bullet.x > WIDTH:
                bullets2.remove(bullet)
            elif check_collision(bullet, tank1_pos):
                tank1_hp -= 2
                bullets2.remove(bullet)
                print(f"Танк 1 получил урон! HP: {tank1_hp}")

        # Очистка экрана
        screen.fill(BLACK)

        # Отрисовка снарядов
        for bullet in bullets:
            draw_bullet(screen, bullet, True)
        for bullet in bullets2:
            draw_bullet(screen, bullet, False)

        # Отрисовка танков
        draw_tank(screen, tank1_pos, tank1_color, tank1_hp)
        draw_tank(screen, tank2_pos, tank2_color, tank2_hp)

        # Отрисовка интерфейса
        draw_hud(screen)

        # Обновление экрана
        pygame.display.flip()

        # Ограничение FPS
        clock.tick(60)

        # Проверка условий победы
        if tank1_hp <= 0:
            print("Танк 1 побежден!")
            running = False
        elif tank2_hp <= 0:
            print("Танк 2 побежден!")
            running = False

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    game_loop()
