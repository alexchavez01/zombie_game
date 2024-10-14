import pygame
import random

# Initialize Pygame
pygame.init()

# Game Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 300
GROUND_HEIGHT = SCREEN_HEIGHT - 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
FPS = 60

# Bullet class
class Bullet:
    def __init__(self, x, y):
        self.radius = 5
        self.color = RED
        self.speed = 8
        self.x = x
        self.y = y
        self.damage = 7
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius*2, self.radius*2)

    def update(self):
        self.x += self.speed
        self.rect.x = self.x - self.radius  # Update rect position for collision

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

# Player class
class Player:
    def __init__(self):
        self.width = 15
        self.height = 40
        self.color = BLACK
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = GROUND_HEIGHT - self.rect.height
        self.health = 100

    def shoot(self):
        # Create and return a new bullet
        bullet = Bullet(self.rect.x + self.width, self.rect.y + self.height // 2)
        return bullet

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# Zombie class
class Zombie:
    def __init__(self):
        self.width = 20
        self.height = 40
        self.color = GREEN
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = GROUND_HEIGHT - self.height
        self.health = 75
        self.speed = 4  # Zombie speed

    def update(self):
        self.rect.x -= self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# Main game function
def game():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Zombie Attack with Spacebar Click Shooting")
    clock = pygame.time.Clock()

    # Game objects
    player = Player()
    zombie = Zombie()
    bullets = []

    # Game state
    game_over = False
    score = 0
    font = pygame.font.Font(None, 36)

    # Main game loop
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Fire a new bullet on spacebar press
                    bullet = player.shoot()
                    bullets.append(bullet)

        # Update game state
        
        zombie.update()

        # Update bullets
        for bullet in bullets[:]:
            bullet.update()
            # Remove bullet if it goes off-screen
            if bullet.x > SCREEN_WIDTH:
                bullets.remove(bullet)
            # Check collision with zombie
            elif bullet.rect.colliderect(zombie.rect):
                zombie.health -= bullet.damage
                bullets.remove(bullet)

        # Collision detection: If zombie reaches the player
        if zombie.rect.colliderect(player.rect):
            player.health = 0  # Instant kill

        # If zombie dies, respawn a new one and increase score
        if zombie.health <= 0:
            score += 1
            zombie = Zombie()

        # If player dies, game over
        if player.health <= 0:
            game_over = True

        # Draw everything
        screen.fill(WHITE)
        player.draw(screen)
        zombie.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)

        # Draw health and score
        player_health_text = font.render(f"Player Health: {player.health}", True, BLACK)
        screen.blit(player_health_text, (10, 10))
        zombie_health_text = font.render(f"Zombie Health: {zombie.health}", True, BLACK)
        screen.blit(zombie_health_text, (10, 50))
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 90))

        # Update the screen
        pygame.display.flip()
        clock.tick(FPS)

    # Game over screen
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game()  # Restart the game

        screen.fill(WHITE)
        game_over_text = font.render("Game Over! Press Space to Restart", True, BLACK)
        screen.blit(game_over_text, (200, 150))
        final_score_text = font.render(f"Final Score: {score}", True, BLACK)
        screen.blit(final_score_text, (350, 200))
        pygame.display.flip()

if __name__ == "__main__":
    game()
