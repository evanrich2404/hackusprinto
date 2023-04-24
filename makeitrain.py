import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1200, 600

# Colors
WHITE = (255, 255, 255)
DARK_GRAY = (64, 64, 64)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cloud Catch")

# Load images
cloud_img = pygame.image.load("images/cloud.png")  
raindrop_img = pygame.image.load("images/raindrop.png")
bg_img = pygame.image.load("images/bg.jpg")

# Scale the raindrop image
scaled_width = 30  # Adjust this value to your desired width
scaled_height = int(raindrop_img.get_height() * (scaled_width / raindrop_img.get_width()))  # Calculate the new height while maintaining the aspect ratio
raindrop_img = pygame.transform.scale(raindrop_img, (scaled_width, scaled_height))

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

all_sprites = pygame.sprite.Group()
cloud = Cloud()
all_sprites.add(cloud)

for _ in range(8):
    raindrop = Raindrop()
    all_sprites.add(raindrop)

running = True

while running:
    # ...

    all_sprites.update()

    screen.blit(bg_img, (0, 0))  # Draw the background image
    all_sprites.draw(screen)

    # ...

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()

    screen.fill(DARK_GRAY)
    all_sprites.draw(screen)

    pygame.display.flip()

pygame.quit()
