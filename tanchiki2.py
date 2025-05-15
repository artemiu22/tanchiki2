import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("танчики")

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

tank1_pos = [100, 100]
tank2_pos = [600, 400]
tank_size = 40
tank1_hp = 100         
tank2_hp = 100
tank = [tank2_pos, tank1_pos]

bullets = []
bullets2 = []


def draw_bullet(surface, bullet):
    pygame.draw.rect(surface, WHITE, bullet)



def draw_bullet2(surface, bullet):
    pygame.draw.rect(surface, WHITE, bullet)

def draw_tank(surface, position, hp):
    pygame.draw.rect(surface, GREEN, (position[0], position[1], tank_size, tank_size))

def game_loop():
    global tank1_hp, tank2_hp
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            if tank1_pos[0] >= 10:
                tank1_pos[0] -= 5
        if keys[pygame.K_d]:
            if tank1_pos[0] <= 750:
                tank1_pos[0] += 5
        if keys[pygame.K_w]:
            if tank1_pos[1] >= 10:
                tank1_pos[1] -= 5
        if keys[pygame.K_s]:
            if tank1_pos[1] <= 550:
                tank1_pos[1] += 5
        if keys[pygame.K_SPACE]:
            bullet_rect = pygame.Rect(tank1_pos[0] + tank_size // 2, tank1_pos[1], 5, 5)
            bullets.append(bullet_rect)

        if keys[pygame.K_LEFT]:
            if tank2_pos[0] >= 10:
                tank2_pos[0] -= 5
        if keys[pygame.K_RIGHT]:
            if tank2_pos[0] <= 750:
                tank2_pos[0] += 5
        if keys[pygame.K_UP]:
            if tank2_pos[1] >= 10:
                tank2_pos[1] -= 5
        if keys[pygame.K_DOWN]:
            if tank2_pos[1] <= 550:
                tank2_pos[1] += 5
        if keys[pygame.K_m]:
            bullet_rect = pygame.Rect(tank2_pos[0] + tank_size // 2, tank2_pos[1], 5, 5)
            bullets2.append(bullet_rect)

        for bullet in bullets[:]:
            bullet.x += 10 if bullet.width > 0 else -10
            if bullet.x < 0 or bullet.x > WIDTH:
                bullets.remove(bullet)

        for bullet2 in bullets2[:]:
            bullet2.x -= 10 if bullet2.width > 0 else 10
            if bullet2.x < 0 or bullet2.x > WIDTH:
                bullets2.remove(bullet2)

        for bullet in bullets[:]:
            if bullet.colliderect(pygame.Rect(tank2_pos[0], tank2_pos[1], tank_size, tank_size)):
                print("Танк 2 получил урон!!")
                tank2_hp -= 10
                bullets.remove(bullet)

        screen.fill((0, 0, 0))
        for bullet in bullets:
            draw_bullet(screen, bullet)
        for bullet in bullets2:
            draw_bullet(screen, bullet)



        for bullet2 in bullets2[:]:
            if bullet2.colliderect(pygame.Rect(tank1_pos[0], tank1_pos[1], tank_size, tank_size)):
                tank1_hp -= 10
                print("Танк 1 получил урон!")
                bullets2.remove(bullet2)

        draw_tank(screen, tank1_pos, tank1_hp)
        draw_tank(screen, tank2_pos, tank2_hp)



        pygame.display.flip()
        clock.tick(60)

        if tank1_hp <= 0:
            print("танк 1 побежден")
            running = False
        if tank2_hp <= 0:
            print("танк 2 побежден")
            running = False
    pygame.quit()

if __name__ == "__main__":
    game_loop()