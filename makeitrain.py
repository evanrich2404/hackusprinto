#!/usr/bin/env python3

import pygame
import random

MAX_RAINDROPS = 10

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1200, 600
bg_img = pygame.image.load("images/bg.jpg")
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))

# Colors
WHITE = (255, 255, 255)
DARK_GRAY = (64, 64, 64)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cloud Catch")

# Load images
cloud_img = pygame.image.load("images/cloud.png")  
raindrop_img = pygame.image.load("images/raindrop.png")
holbie_img = pygame.image.load("images/holbie.png")

# Scale the raindrop image
scaled_width = 30  # Adjust this value to your desired width
scaled_height = int(raindrop_img.get_height() * (scaled_width / raindrop_img.get_width()))  # Calculate the new height while maintaining the aspect ratio
raindrop_img = pygame.transform.scale(raindrop_img, (scaled_width, scaled_height))

# Scale the Holbie image
holbie_scaled_width = 50  # Adjust this value to your desired width
holbie_scaled_height = int(holbie_img.get_height() * (holbie_scaled_width / holbie_img.get_width()))  # Calculate the new height while maintaining the aspect ratio
holbie_img = pygame.transform.scale(holbie_img, (holbie_scaled_width, holbie_scaled_height))


class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = cloud_img
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.centery = HEIGHT - 100
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

class Raindrop(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = raindrop_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(max(1, WIDTH - self.rect.width))
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(3, 7)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.rect.y = random.randrange(-100, -40)
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.speedy = random.randrange(5, 10)

class Holbie(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = holbie_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 4)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.rect.y = random.randrange(-100, -40)
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.speedy = random.randrange(5, 10)


all_sprites = pygame.sprite.Group()
cloud = Cloud()
all_sprites.add(cloud)


raindrops = pygame.sprite.Group()

for _ in range(8):
    raindrop = Raindrop()
    all_sprites.add(raindrop)


holbies = pygame.sprite.Group()

holbie = Holbie()
all_sprites.add(holbie)
holbies.add(holbie)


running = True
raindrop_count = 0
start_time = pygame.time.get_ticks()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()

    screen.fill(DARK_GRAY)
    all_sprites.draw(screen)

    # Check for collisions
    collected_raindrops = pygame.sprite.spritecollide(cloud, raindrops, True)
    raindrop_count += len(collected_raindrops)

    # Check for collisions with Holbie icon
    holbie_collision = pygame.sprite.spritecollide(cloud, holbies, True)
    if holbie_collision:
        running = False

    screen.blit(bg_img, (0, 0))
    all_sprites.draw(screen)

    # Display timer and raindrop count
    font = pygame.font.Font(None, 36)
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
    time_left = 60 - elapsed_time
    if time_left < 0:
        time_left = 0
        running = False
    timer_text = font.render(f"Time left: {time_left}", True, WHITE)
    count_text = font.render(f"Raindrops collected: {raindrop_count}", True, WHITE)
    screen.blit(timer_text, (10, 10))
    screen.blit(count_text, (10, 50))

    if len(raindrops) < MAX_RAINDROPS:
        raindrop = Raindrop()
        all_sprites.add(raindrop)
        raindrops.add(raindrop)

    pygame.display.flip()

pygame.quit()
