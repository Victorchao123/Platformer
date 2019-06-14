#The basic Class framework that I used in this program was learnt from kidscancode.org
#Following the Player was NOT MY IMPLEMENTATION. I CAN'T FIND THE WEBSITE WHERE I FOUND IT
#Random Movement was found here: https://opensource.com/article/18/5/pygame-enemy

#Importing Modules
import pygame
import random
import time
import math
import sys
import moviepy
#This module has not been used
import pyganim
from moviepy.editor import * 
from time import sleep

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
GRAY = (105, 105, 105)


#Player Properties
ACCELERATION = 0.8
FRICTION = -0.12
GRAVITY = 0.8

#Platforms
PLATFORMS = [(WIDTH / 2 - 50, HEIGHT * 3 / 4, 100, 20),
(125, HEIGHT - 350, 100, 20), (350, 200, 100, 20), (530, HEIGHT - 350, 100, 20)]
PLATDORMS = [(120, 260, 100, 20), (120, 460, 100, 20), (660, 260, 100, 20), (660, 460, 100, 20)]
GROUNDS = [(0, HEIGHT - 40, WIDTH, 40)]
PLATHORMS = [(120, 260, 100, 20), (120, 460, 100, 20), (400, 260, 100, 20), (400, 460, 100, 20),
(660, 260, 100, 20), (660, 460, 100, 20)]
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

punchAnim = pyganim.PygAnimation([('lvl3graphics/punch1.png', 100), ('lvl3graphics/punch2.png', 100),
('lvl3graphics/punch3.png', 100), ('lvl3graphics/hoverboard.png', 100)])
punchAnim.play()


#Font Initialization
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font('SuperMario256.ttf', size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

#Sprites
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.images.append(pygame.image.load("lvl3graphics/hoverboard.png"))
        self.images.append(pygame.image.load("lvl3graphics/punch1.png"))
        self.images.append(pygame.image.load("lvl3graphics/punch2.png"))
        self.images.append(pygame.image.load("lvl3graphics/punch3.png"))
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.shoot_delay = 150
        self.hit_delay = 120
        self.last_shot = pygame.time.get_ticks()
        self.leftRight = 1
        self.punch_right = pygame.transform.flip(pygame.image.load("lvl3graphics/punch3.png").convert_alpha(), True, False)
        self.player_left = pygame.image.load("lvl3graphics/hoverboard.png").convert_alpha()
        self.player_right = pygame.transform.flip(self.image, True, False)
        self.time = pygame.time.get_ticks()
        self.count = 200
        self.track = 0
        
    def jump(self):
        self.rect.x += 1
        self.rect.x -= 1
        if pygame.sprite.spritecollide(player, platforms, False):
            self.vel.y = -20
        if pygame.sprite.spritecollide(player, grounds, False):
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
            self.image = self.player_left
            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                bullet = LeftBullet(self.rect.centerx, self.rect.left)
                bullet.rect.x = player.rect.x
                bullet.rect.y = player.rect.y
                all_sprites.add(bullet)
                bullets.add(bullet)
        else:
            self.image = self.player_right
            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                bwllet = RightBullet(self.rect.centerx, self.rect.left)
                bwllet.rect.x = player.rect.x
                bwllet.rect.y = player.rect.y
                all_sprites.add(bwllet)
                bullets.add(bwllet)

    def punch(self):
        pounch = pygame.time.get_ticks()
        if self.leftRight == 1:
            self.image = self.images[3]
            if pounch - self.last_shot > self.hit_delay:
                fist = Fist(self.rect.centerx, self.rect.left)
                fist.rect.x = player.rect.x - 20
                fist.rect.y = player.rect.y
                all_sprites.add(fist)
                fists.add(fist)
        else:
            self.image = self.punch_right
            if pounch - self.last_shot > self.hit_delay:
                fist = Fist(self.rect.centerx, self.rect.right)
                fist.rect.x = player.rect.x + 50
                fist.rect.y = player.rect.y
                all_sprites.add(fist)
                fists.add(fist)



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
        self.pos = vec(WIDTH / 2, 0)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.distance_above_player = 1
        self.speed = random.randrange(2, 5)
        self.images = []
        self.images.append(pygame.image.load("fly1.png"))
        self.images.append(pygame.image.load("fly2.png"))
        self.index = 0 
        self.image = self.images[self.index]
        self.rect = pygame.Rect(random.randint(0, WIDTH), 0, 80, 80)
        self.count = 0
    def pos_towards_player(self, player_rect):
        #Taken from Somewhere, trying to find source
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
        self.count += 1
        if self.count > 20:
            self.index += 1
            self.count = 0
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]

class Dino(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.count = 0
        self.images = []
        self.images.append(pygame.image.load("triceratops1.png"))
        self.images.append(pygame.image.load("triceratops2.png"))
        self.images.append(pygame.image.load("triceratops3.png"))
        self.images.append(pygame.image.load("triceratops4.png"))
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = 0 - 10
        self.rect.y = HEIGHT - 100
        self.coun = 0 

    def update(self):
        self.count += 1
        self.coun += 1
        if self.coun > 5:
            self.index += 1
            self.coun = 0
            self.speed = 4
            self.rect.x += self.speed
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]
        if self.rect.x == 402:
            d = Dino()
            all_sprites.add(d)
            dinos.add(d)
        if self.rect.x > WIDTH:
            self.kill()

class TRex(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.images.append(pygame.image.load("lvl3graphics/trex1.png"))
        self.images.append(pygame.image.load("lvl3graphics/trex2.png"))
        self.images.append(pygame.image.load("lvl3graphics/trex3.png"))
        self.images.append(pygame.image.load("lvl3graphics/trex4.png"))
        self.count = 0
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH / 2
        self.rect.y = HEIGHT - 300
        self.distance = 80
        self.speed = 4
        self.counter = 0
        self.lastlaunch = pygame.time.get_ticks()
        self.fire_delay = 3000

    def update(self):
        if self.counter >= 0 and self.counter <= self.distance:
            self.rect.x += self.speed
            self.index += 1
        elif self.counter >= self.distance and self.counter <= self.distance * 2:
            self.rect.x -= self.speed
            self.index += 1
        else:
            self.counter = 0
        self.counter += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]
        now = pygame.time.get_ticks()
        if now - self.lastlaunch > self.fire_delay:
            self.lastlaunch = now
            cannonball = CannonBall(self.rect.x, self.rect.y)
            cannonball.rect.x = trex.rect.x
            cannonball.rect.y = trex.rect.y - 10
            all_sprites.add(cannonball)
            cannons.add(cannonball)


class CannonBall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.pos = vec(WIDTH / 2, 0)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.distance_above_player = 1
        self.speed = 5
        self.image = pygame.image.load("lvl3graphics/missile.png")
        self.rect = pygame.Rect(x, y, 80, 80)
        self.time = pygame.time.get_ticks()
        self.deathdelay = 5000
    def pos_towards_player(self, player_rect):
        player = Player()
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
        now = pygame.time.get_ticks()
        if now - self.time > self.deathdelay:
            self.kill()
            self.time = now
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
        self.image = pygame.image.load("formplat.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.image.fill(GRAY)
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

class Fist(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 30))
        self.image = pygame.image.load("invis.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.lasthit = pygame.time.get_ticks()
        self.rect.bottom = x
        self.rect.centerx = x
        self.speedx = 0
        self.fistdelay = 100

    def update(self):
        noww = pygame.time.get_ticks()
        if noww - self.lasthit > self.fistdelay:
            self.lasthit = noww
            self.kill()

class ScrollBackground(pygame.sprite.Sprite):
    def __init__(self):
        super(ScrollBackground, self).__init__()
        self.images = []
        for i in range(1, 181):
            self.images.append(pygame.image.load('ScrollFrames/backscroll' + str(i) +'.png'))
        self.index = 0
        self.image = self.images[self.index]
        self.rect = pygame.Rect(0, 0, 800, 680)
    def update(self):
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]

class VolcanoAnimate(pygame.sprite.Sprite):
    def __init__(self):
        super(VolcanoAnimate, self).__init__()
        self.images = []
        for i in range(1, 17):
            self.images.append(pygame.image.load('volcanoscroll/volcano' + str(i) + '.png'))
        self.index = 0
        self.image = self.images[self.index]
        self.rect = pygame.Rect(0, 0, 800, 680)
    def update(self):
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = pygame.image.load("splat.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.lastupdate = now
            self.frame += 1
            self.kill()
        else:
            center = self.rect.center
            self.image = pygame.image.load("splat.png").convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.center = center

class DeathBall(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((150, 196))
        self.image = pygame.image.load("lvl3graphics/finalkillball.png")
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH / 2
        self.rect.y = 0
        self.speed = 3
    def update(self):
        self.rect.y += self.speed

class DeathNote(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((298, 90))
        self.image = pygame.image.load("deathsg.png")
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH / 2
        self.rect.y = 10

#Background Sprite
scroll_background = ScrollBackground()
scrolls = pygame.sprite.Group(scroll_background)
volcano_animation = VolcanoAnimate()
volcanos = pygame.sprite.Group(volcano_animation)
clock = pygame.time.Clock()


#Level 1 Start Screen
def start_screen():
    pygame.mixer.music.stop()
    pygame.display.flip()
    clip = VideoFileClip('Cutsene.mp4')
    clip.preview()
    pygame.mixer.init()
    pygame.mixer.music.load("HeroicDemise.mp3")
    pygame.mixer.music.play(-1, 0)
    prompt = True
    while prompt:
            clock.tick(FPS)
            scrolls.update()
            scrolls.draw(screen)
            draw_text(screen, "Platformer", 48, WIDTH / 2, HEIGHT / 4)
            draw_text(screen, "WASD to move, Space to shoot, E to switch direction, F to punch", 18, WIDTH / 2, HEIGHT / 2)
            draw_text(screen, "Level One", 20, WIDTH / 2, HEIGHT * 2 / 3 - 50)
            draw_text(screen, "Press Enter to start", 18, WIDTH / 2, HEIGHT * 3 / 4)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RETURN:     
                        prompt = False

#Level 2 Start Screen
def level_2start():
    pygame.mixer.music.stop()
    pygame.display.flip()
    pygame.mixer.init()
    pygame.mixer.music.load("Riseofspirit.mp3")
    pygame.mixer.music.play(-1, 0)
    propt = True
    while propt:
        clock.tick(FPS)
        screen.blit(start2, [0, 0])
        draw_text(screen, "Platformer", 48, WIDTH / 2, HEIGHT / 4)
        draw_text(screen, "WASD to move, Space to shoot, E to switch direction, F to punch", 18, WIDTH / 2, HEIGHT / 2)
        draw_text(screen, "Level Two", 20, WIDTH / 2, HEIGHT * 2 / 3 - 50)
        draw_text(screen, "Press Enter to start", 18, WIDTH / 2, HEIGHT * 3 / 4)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    propt = False
                    screen.blit(lev2, [0, 0])
                    pygame.display.flip()

#Boss Start Screen
def boss_start():
    pygame.mixer.music.stop()
    pygame.display.flip()
    pygame.mixer.init()
    pygame.mixer.music.load("boss.mp3")
    pygame.mixer.music.play(-1, 0)
    prot = True
    while prot:
        clock.tick(15)
        volcanos.update()
        volcanos.draw(screen)
        draw_text(screen, "Platformer", 48, WIDTH / 2, HEIGHT / 4)
        draw_text(screen, "WASD to move, Space to shoot, E to switch direction, F to punch", 18, WIDTH / 2, HEIGHT / 2)
        draw_text(screen, "Boss Level", 20, WIDTH / 2, HEIGHT * 2 / 3 - 50)
        draw_text(screen, "Press Enter to start", 18, WIDTH / 2, HEIGHT * 3 / 4)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    prot = False
                    screen.blit(bosslvl, [0, 0])
                    pygame.display.flip()

#Spare Images
bg = pygame.image.load("Backofground.png")
start2 = pygame.image.load("desert.jpg")
lev2 = pygame.image.load("desertback.png")
bosslvl = pygame.image.load("lvl3graphics/bossback.png")

    
#Sounds and Background
jump = pygame.mixer.Sound('Jumps.wav')
land = pygame.mixer.Sound('jumpland.wav')
shoot = pygame.mixer.Sound('shoot.wav')
background = pygame.image.load("bg.jpg")
#Extra Variables
concount = 0
#Main Game Loop
game_over = True
running = True
CurrentLevel = 1
while running:
    if (game_over) and (CurrentLevel == 1):
        start_screen()
        game_over = False
        #Updating Sprites
        all_sprites = pygame.sprite.Group()
        platforms = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        grounds = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        trexs = pygame.sprite.Group()
        meteors = pygame.sprite.Group()
        dinos = pygame.sprite.Group()
        fists = pygame.sprite.Group()
        cannons = pygame.sprite.Group()
        deaths = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for plat in PLATFORMS:
            p = Platform(*plat)
            all_sprites.add(p)
            platforms.add(p)
        for i in range(4):
            m = Mob()
            all_sprites.add(m)
            mobs.add(m)
        for gro in GROUNDS:
            g = Ground(*gro)
            all_sprites.add(g)
            grounds.add(g)
        score = 0
    if (score > 12) and (CurrentLevel == 1):
        score = 0
        CurrentLevel += 1
        level_2start()
        game_over = False
        all_sprites = pygame.sprite.Group()
        platforms = pygame.sprite.Group()
        grounds = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        trexs = pygame.sprite.Group()
        meteors = pygame.sprite.Group()
        dinos = pygame.sprite.Group()
        fists = pygame.sprite.Group()
        cannons = pygame.sprite.Group()
        deaths = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for plat in PLATDORMS:
            p = Platform(*plat)
            all_sprites.add(p)
            platforms.add(p)
        for i in range(4):
            m = Mob()
            all_sprites.add(m)
            mobs.add(m)
        for gro in GROUNDS:
            g = Ground(*gro)
            all_sprites.add(g)
            grounds.add(g)
        d = Dino()
        all_sprites.add(d)
        dinos.add(d)
    if (game_over) and (CurrentLevel == 2):
        score = 0
        level_2start()
        game_over = False
        all_sprites = pygame.sprite.Group()
        platforms = pygame.sprite.Group()
        grounds = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        trexs = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        meteors = pygame.sprite.Group()
        fists = pygame.sprite.Group()
        dinos = pygame.sprite.Group()
        cannons = pygame.sprite.Group()
        deaths = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for plat in PLATDORMS:
            p = Platform(*plat)
            all_sprites.add(p)
            platforms.add(p)
        for i in range(4):
            m = Mob()
            all_sprites.add(m)
            mobs.add(m)
        for gro in GROUNDS:
            g = Ground(*gro)
            all_sprites.add(g)
            grounds.add(g)
        d = Dino()
        all_sprites.add(d)
        dinos.add(d)
        hits = pygame.sprite.spritecollide(player, dinos, True)
        if hits:
            game_over = True

        hits = pygame.sprite.groupcollide(bullets, dinos, True, False)
        score = 0
    if (score > 12) and (CurrentLevel == 2):
        score = 0
        CurrentLevel += 1
        boss_start()
        game_over = False
        all_sprites = pygame.sprite.Group()
        platforms = pygame.sprite.Group()
        grounds = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        trexs = pygame.sprite.Group()
        meteors = pygame.sprite.Group()
        fists = pygame.sprite.Group()
        dinos = pygame.sprite.Group()
        cannons = pygame.sprite.Group()  
        deaths = pygame.sprite.Group()
        notes = pygame.sprite.Group() 
        player = Player()
        all_sprites.add(player)
        for gro in GROUNDS:
            g = Ground(*gro)
            all_sprites.add(g)
            grounds.add(g)
        for plat in PLATHORMS:
            p = Platform(*plat)
            all_sprites.add(p)
            platforms.add(p)
        trex = TRex()
        all_sprites.add(trex)
        trexs.add(trex)
        hits = pygame.sprite.groupcollide(cannons, platforms, True, False)
    if (game_over) and (CurrentLevel == 3):
        score = 0
        boss_start()
        game_over = False
        all_sprites = pygame.sprite.Group()
        platforms = pygame.sprite.Group()
        grounds = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        trexs = pygame.sprite.Group()
        meteors = pygame.sprite.Group()
        fists = pygame.sprite.Group()
        dinos = pygame.sprite.Group()
        cannons = pygame.sprite.Group()
        deaths = pygame.sprite.Group()
        notes = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for gro in GROUNDS:
            g = Ground(*gro)
            all_sprites.add(g)
            grounds.add(g)
        for plat in PLATHORMS:
            p = Platform(*plat)
            all_sprites.add(p)
            platforms.add(p)
        trex = TRex()
        all_sprites.add(trex)
        trexs.add(trex)
            
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
            if event.key == pygame.K_e:
                player.toggle()
            if event.key == pygame.K_SPACE:
                player.shoot()
                pygame.mixer.Sound.play(shoot)
            if event.key == pygame.K_f:
                player.punch()

    if (score > 0) and (score % 10 == 0):
        r = Meteor()
        all_sprites.add(r)
        meteors.add(r)

    if (CurrentLevel == 3) and (score == 50):
        deathball = DeathBall()
        all_sprites.add(deathball)
        deaths.add(deathball)
        note = DeathNote()
        all_sprites.add(note)
        notes.add(note)


    all_sprites.update()

    #Sprite Collisions
    if player.vel.y > 0:
        hits = pygame.sprite.spritecollide(player, platforms, False)
        if hits:
            player.pos.y = hits[0].rect.top
            player.vel.y = 0

    if player.vel.y > 0:
        hits = pygame.sprite.spritecollide(player, grounds, False)
        if hits:
            player.pos.y = hits[0].rect.top 
            player.vel.y = 0

    hits = pygame.sprite.groupcollide(bullets, mobs, True, True)
    for hit in hits:
        score += 1
        m = Mob()
        all_sprites.add(m)
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        all_sprites.update()
        mobs.add(m)


    hits = pygame.sprite.spritecollide(player, mobs, True)
    if hits:
        game_over = True
    hits = pygame.sprite.spritecollide(player, meteors, True)
    if hits:
        game_over = True
    hits = pygame.sprite.groupcollide(meteors, platforms, True, False)

    hits = pygame.sprite.groupcollide(meteors, grounds, True, False)

    hits = pygame.sprite.groupcollide(fists, mobs, True, True)
    for hit in hits:
        score += 1
        m = Mob()
        all_sprites.add(m)
        all_sprites.update()
        mobs.add(m)
    
    hits = pygame.sprite.spritecollide(player, dinos, True)
    if hits:
        game_over = True

    hits = pygame.sprite.groupcollide(bullets, dinos, True, False)

    #hits = pygame.sprite.groupcollide(cannons, platforms, True, False)

    hits = pygame.sprite.spritecollide(player, trexs, True)
    if hits:
        game_over = True
    
    hits = pygame.sprite.spritecollide(player, cannons, True, False)
    if hits:
        game_over = True

    hits = pygame.sprite.groupcollide(bullets, cannons, True, True)

    hits = pygame.sprite.groupcollide(bullets, trexs, True, False)
    for hit in hits:
        score += 1

    hits = pygame.sprite.groupcollide(deaths, grounds, True, True)
    if hits:
        pygame.quit()

    screen.fill(WHITE)
    if CurrentLevel == 1:
        screen.blit(bg, [0, 0])
    if CurrentLevel == 2:
        screen.blit(lev2, [0, 0])
    if CurrentLevel == 3:
        screen.blit(bosslvl, [0, 0])
    all_sprites.draw(screen)
    draw_text(screen, str(score), 50, WIDTH / 2, 10)
    pygame.display.flip()

pygame.quit()