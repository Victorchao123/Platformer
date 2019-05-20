#Importing Modules
import pygame
import random
import time
import math
import sys

#PlayerView
WIDTH = 800
HEIGHT = 680
FPS = 60
vec = pygame.math.Vector2

#Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

bg = pygame.image.load("bg.jpg")

#Player Properties
ACCELERATION = 0.8
FRICTION = -0.12
GRAVITY = 0.8

#Platforms
PLATFORMS = [(0, HEIGHT - 40, WIDTH, 40),
(WIDTH / 2 - 50, HEIGHT * 3 / 4, 100, 20),
(125, HEIGHT - 350, 100, 20), (350, 200, 100, 20), (530, HEIGHT - 350, 100, 20)]

#Sign
SIGN = [(WIDTH / 2, HEIGHT / 2)]
#Background Music
pygame.mixer.init()
pygame.mixer.music.load("HeroicDemise.mp3")
pygame.mixer.music.play(-1, 0)

#Initialization
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer")
clock = pygame.time.Clock()


'''
Main Map Initialization
map_width = 3000
map_height = 600
map = pygame.Surface((map_width, map_height))
map = map.convert()
def drawmap():
'''

#Font Initialization
font_name = pygame.font.match_font('ailerons-regular')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, RED)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

#Sprites
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 60))
        self.image = pygame.image.load("soldier.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.shoot_delay = 150
        self.last_shot = pygame.time.get_ticks()
        self.leftRight = 0
        self.player_left = pygame.image.load("soldier.png").convert_alpha()
        self.player_right = pygame.transform.flip(self.image, True, False)
    def jump(self):
        self.rect.x += 1
        self.rect.x -= 1
        if pygame.sprite.spritecollide(player, platforms, False):
            self.vel.y = -20
    def toggle(self):
        if self.leftRight == 0:
            self.leftRight += 1
            self.image = self.player_left
        else:
            self.leftRight = 0
            self.image = self.player_right

    def shoot(self):
        now = pygame.time.get_ticks()
        if self.leftRight == 1:
            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                bullet = LeftBullet(self.rect.centerx, self.rect.left)
                bullet.rect.x = player.rect.x
                bullet.rect.y = player.rect.y
                all_sprites.add(bullet)
                bullets.add(bullet)
        else:
            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                bwllet = RightBullet(self.rect.centerx, self.rect.left)
                bwllet.rect.x = player.rect.x
                bwllet.rect.y = player.rect.y
                all_sprites.add(bwllet)
                bullets.add(bwllet)


    def update(self):
        self.acc = vec(0, GRAVITY)
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.acc.x = -ACCELERATION
        if keystate[pygame.K_d]:
            self.acc.x = ACCELERATION

        self.acc.x += self.vel.x * FRICTION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        if self.pos.x > WIDTH:
            self.pos.x = WIDTH
        if self.pos.x < 0:
            self.pos.x = 0

        self.rect.midbottom = self.pos

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 40))
        self.image = pygame.image.load("ghost.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = 0
        self.pos = vec(WIDTH / 2, 0)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.distance_above_player = 1
        self.speed = 5
    def pos_towards_player(self, player_rect):
        #
        c = math.sqrt((player_rect.x - self.rect.x) ** 2 + (player_rect.y - self.distance_above_player - self.rect.y) ** 2)
        try:
            x = (player_rect.x - self.rect.x) / c
            y = ((player_rect.y - self.distance_above_player) - self.rect.y) / c
        except ZeroDivisionError:
            return False
        return (x, y)
    def update(self):
        self.acc = vec(0, GRAVITY)
        self.acc.x += self.vel.x * FRICTION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        new_pos = self.pos_towards_player(player.rect)
        if new_pos:
            self.rect.x, self.rect.y = (self.rect.x + new_pos[0] * self.speed, self.rect.y +
            new_pos[1] * self.speed)

class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((80, 80))
        self.image = pygame.image.load("meteor.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(3, 9)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(3, 9)


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class LeftBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image = pygame.image.load("bullet.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.bottom = x
        self.rect.centerx = x
        self.speedx = -20

    def update(self):
        self.rect.x += self.speedx
        if self.rect.left < 0:
            self.kill()

class RightBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image = pygame.image.load("bullet.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.bottom = x
        self.rect.centerx = x
        self.speedx = 20

    def update(self):
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.kill()
class Yeeld(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((100, 100))
        self.image = pygame.image.load("yield.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.cur = pygame.time.get_ticks()
        self.ti = 100

#Start Screen
def start_screen():
    pygame.mixer.music.stop()
    screen.fill(BLACK)
    draw_text(screen, "Platformer", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "WASD to move, Space to shoot", 22, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Press any key to start", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    pygame.mixer.init()
    pygame.mixer.music.load("HeroicDemise.mp3")
    pygame.mixer.music.play(-1, 0)
    prompt = True
    while prompt:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                prompt = False

#Sounds and Background
jump = pygame.mixer.Sound('Jumps.wav')
land = pygame.mixer.Sound('jumpland.wav')
shoot = pygame.mixer.Sound('shoot.wav')
background = pygame.image.load("bg.jpg")
#Main Game Loop
game_over = True
running = True
while running:
    if game_over:
        start_screen()
        game_over = False
        #Updating Sprites
        all_sprites = pygame.sprite.Group()
        platforms = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        meteors = pygame.sprite.Group()
        yeelds = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for plat in PLATFORMS:
            p = Platform(*plat)
            all_sprites.add(p)
            platforms.add(p)
        for i in range(8):
            m = Mob()
            all_sprites.add(m)
            mobs.add(m)
        score = 0

    clock.tick(FPS)
    #Keypresses
    leftRight = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player.jump()
                pygame.mixer.Sound.play(jump)
            if event.key == pygame.K_f:
                player.toggle()
            if event.key == pygame.K_SPACE:
                player.shoot()
                pygame.mixer.Sound.play(shoot)

    if (score > 0) and (score % 10 == 0):
        naw = pygame.time.get_ticks()
        curTime = 30
        ye = Yeeld(WIDTH / 2 - 50, HEIGHT / 2)
        all_sprites.add(ye)
        yeelds.add(ye)
        
        r = Meteor()
        all_sprites.add(r)
        meteors.add(r)

    all_sprites.update()

    #Sprite Collisions
    if player.vel.y > 0:
        hits = pygame.sprite.spritecollide(player, platforms, False)
        if hits:
            player.pos.y = hits[0].rect.top
            player.vel.y = 0

    hits = pygame.sprite.groupcollide(bullets, mobs, True, True)
    for hit in hits:
        score += 1
        m = Mob()
        all_sprites.add(m)
        all_sprites.update()
        mobs.add(m)
    hits = pygame.sprite.spritecollide(player, mobs, True)
    if hits:
        game_over = True
    hits = pygame.sprite.spritecollide(player, meteors, True)
    if hits:
        game_over = True
    hits = pygame.sprite.groupcollide(meteors, platforms, True, False)



    screen.fill(WHITE)
    screen.blit(bg, [0, 0])
    all_sprites.draw(screen)
    draw_text(screen, str(score), 50, WIDTH / 2, 10)
    pygame.display.flip()

pygame.quit()