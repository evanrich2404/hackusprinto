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
pygame.display.set_caption("Make It Rain")
font = pygame.font.Font(None, 24)

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
        self.speedy = random.randrange(1, 2)

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

def draw_text(surface, text, font, pos, color):
    rendered_text = font.render(text, True, color)
    rect = rendered_text.get_rect()
    rect.center = pos
    surface.blit(rendered_text, rect)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()
    # ...
    time_left = 60 - (pygame.time.get_ticks() - start_time) // 1000
    draw_text(screen, f"Time left: {time_left}", font, (WIDTH - 250, HEIGHT - 120), WHITE)
    draw_text(screen, f"Raindrops collected: {raindrop_count}", font, (10, HEIGHT - 70), WHITE)

    screen.fill(DARK_GRAY)

    # Check for collisions
    collected_raindrops = pygame.sprite.spritecollide(cloud, raindrops, True)
    raindrop_count += len(collected_raindrops)

    # Remove collected raindrops from all_sprites
    for raindrop in collected_raindrops:
        all_sprites.remove(raindrop)

    # Check for collisions with Holbie icon
    holbie_collision = pygame.sprite.spritecollide(cloud, holbies, True)
    if holbie_collision:
        running = False

    screen.blit(bg_img, (0, 0))

    all_sprites.draw(screen)  # Keep only this line to draw sprites

    # Calculate the time left
    current_time = pygame.time.get_ticks()
    time_left = max(0, (start_time + 30000 - current_time) // 1000)  # 30 seconds timer

    # Display the game title, timer, and raindrop count
    draw_text(screen, "Make It Rain", pygame.font.Font(None, 48), (WIDTH // 10, 20), WHITE)
    draw_text(screen, f"Time left: {time_left}", font, (WIDTH - 75, 75), WHITE)
    draw_text(screen, f"Raindrops collected: {raindrop_count}", font, (125 , 550), WHITE)



    if len(raindrops) < MAX_RAINDROPS:
        raindrop = Raindrop()
        all_sprites.add(raindrop)
        raindrops.add(raindrop)

    pygame.display.flip()  # Update the display after drawing everything


# Game over screen function
def show_game_over_screen():
    screen.fill(DARK_GRAY)
    screen.blit(bg_img, (0, 0))

    # Display the game over message
    font = pygame.font.Font("freesansbold.ttf", 72)
    game_over_text = font.render("Game Over", True, (255, 0, 0))
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))

    # Display the top 3 fictional high scores
    high_score_font = pygame.font.Font("freesansbold.ttf", 36)
    fictional_high_scores = [("JBees", 7654321), ("Gigely_Strudels", 65544), ("Maitreya", 99)]
    for i, (name, score) in enumerate(fictional_high_scores):
        high_score_text = high_score_font.render(f"{i + 1}. {name}: {score}", True, WHITE)
        screen.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, HEIGHT // 2 - high_score_text.get_height() // 2 + 100 + i * 40))

    pygame.display.flip()
    pygame.time.wait(5000)  # Wait for 5 seconds before closing the game


# After the game loop ends, display the game over screen
show_game_over_screen()

pygame.quit()