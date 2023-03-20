# Shmup game
import pygame
import random

WIDTH = 1000
HEIGHT = 800
FPS = 60
score = 0
# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A file from some shady dude at the gulag.")
clock = pygame.time.Clock()
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Scrip files/Ship.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (75, 75))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        
    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Scrip files/Enemy ship.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10  or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)
            
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
        
    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
    
game_state = 'start_menu'
def draw_start_menu():
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont('arial', 40)
    title = font.render('A file from some shady dude at the gulag', True, (255, 255, 255))
    start_button = font.render('Press E to start!', True, (255, 255, 255))
    controls = font.render('Press Q for controls', True, (255, 255, 255))
    screen.blit(title, (WIDTH/2 - title.get_width()/2, HEIGHT/2.2 - title.get_height()/2))
    screen.blit(start_button, (WIDTH/2 - start_button.get_width()/2, HEIGHT/2 + start_button.get_height()/2))
    screen.blit(controls, (WIDTH/2 - controls.get_width()/2, HEIGHT/2.23 + controls.get_height()/2))
    pygame.display.update()

def draw_game_over_screen():
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont('arial', 40)
    title = font.render('Game Over', True, (255, 255, 255))
    quit_button = font.render('Q - Quit', True, (255, 255, 255))
    score_text = font.render('You hit ' + str(score) + ' ship(s)', True, (255, 255, 255))
    screen.blit(title, (WIDTH/2 - title.get_width()/2, HEIGHT/2.2 - title.get_height()/3))
    screen.blit(quit_button, (WIDTH/2 - quit_button.get_width()/2, HEIGHT/1.9 + quit_button.get_height()/2))
    screen.blit(score_text, (WIDTH/2 - score_text.get_width()/2, HEIGHT/2.13 + score_text.get_height()/2))
    pygame.display.update()
avariable = True
while avariable == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    if game_state == "start_menu":
        draw_start_menu()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_e]:
            game_state = "game"
            game_over = False
        if keys[pygame.K_q]:
            pass
    elif game_state == "game":
        pygame.mixer.music.load("Scrip files/Happy music.wav")
        pygame.mixer.music.play(-1)
        avariable = False
        pygame.display.update()

    elif game_over:
       game_state = "game_over"
       game_over = False
    
# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Update
    all_sprites.update()
    
    # check to see if a bullet hit a mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
        score += 1
    # check to see if a mob hit the player
    hits = pygame.sprite.spritecollide(player, mobs, False)
    if hits:
        avariable = True
        pygame.mixer.music.stop()
        while avariable == True:
            draw_game_over_screen()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        quit()
                        exit()
    # Draw / render
    imp = pygame.image.load("Scrip files/shutterstock-540775171___01150021748.png").convert()
    
    # Using blit to copy content from one surface to other
    screen.blit(imp, (0, 0))
    
    all_sprites.draw(screen)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
