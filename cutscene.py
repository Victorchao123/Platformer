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
GRAY = (105, 105, 105)

#Spare Images
bg = pygame.image.load("Backofground.png")
start2 = pygame.image.load("desert.jpg")
lev2 = pygame.image.load("desertback.png")
closeclose = pygame.image.load("playerclose.png")


#Player Properties
ACCELERATION = 0.8
FRICTION = -0.12
GRAVITY = 0.8

#Platforms
PLATFORMS = [(WIDTH / 2 - 50, HEIGHT * 3 / 4, 100, 20),
(125, HEIGHT - 350, 100, 20), (350, 200, 100, 20), (530, HEIGHT - 350, 100, 20)]
PLATDORMS = [(120, 260, 100, 20), (120, 460, 100, 20), (660, 260, 100, 20), (660, 460, 100, 20)]
GROUNDS = [(0, HEIGHT - 40, WIDTH, 40)]

#Background Music
pygame.mixer.init()
pygame.mixer.music.load("suspense.mp3")
pygame.mixer.music.play(-1, 0)

#Sound Effects
squeal = pygame.mixer.Sound('car.wav')
crash = pygame.mixer.Sound('crash.wav')
huh = pygame.mixer.Sound('Spencer.wav')


#Initialization
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer")
clock = pygame.time.Clock()


#Font Initialization
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font('pokemon_pixel_font.ttf', size)
    text_surface = font.render(text, True, BLACK)
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
        self.rect.x = WIDTH - 30
        self.rect.y = HEIGHT - 100
        self.speedx = 0
        self.speedy = 0
        tru = False
    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.speedx = -5
        if keystate[pygame.K_e]:
            self.speedx = 5
        self.rect.x += self.speedx
        if self.rect.x < WIDTH / 2:
            whitebox = pygame.image.load("whitebox.jpg").convert_alpha()
            screen.blit(whitebox, [WIDTH / 4 + 50, HEIGHT / 4 - 130])
            draw_text(screen, "Where am I?", 30, WIDTH / 4 + 190, HEIGHT / 4 - 100)

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
class TimeMachine(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((400, 400))
        self.image = pygame.image.load("timemachine2.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 0 - 10
        self.rect.y = 400
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_r]:
            self.speedx = -10
        if keystate[pygame.K_t]:
            self.speedx = 10
            pygame.mixer.Sound.play(squeal)
        if self.rect.x > WIDTH - 30:
            pygame.mixer.Sound.play(crash)
        self.rect.x += self.speedx

class CloseThing(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((800, 680))
        self.image = pygame.image.load("playerclose.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.count = pygame.time.get_ticks()
        self.delay = 8

    def update(self):
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_j]:
            self.kill()
        

class Dialogue(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((300, 80))
        self.image = pygame.image.load("whitebox.jpg").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 280
        self.rect.y = 500
        self.count = pygame.time.get_ticks()
        self.delay = 8
    
    def update(self):
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_j]:
            self.kill()
        
class TextTing(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((80, 33))
        self.image = pygame.image.load("hello.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 390
        self.rect.y = 520
        self.count = pygame.time.get_ticks()
        self.delay = 8

    def update(self):
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_j]:
            self.kill()
    
def dialogue():
    whitebox = pygame.image.load("whitebox.jpg").convert_alpha()
    screen.blit(whitebox, [WIDTH / 4 + 50, HEIGHT / 4 - 130])

 

#Background Sprite
scroll_background = ScrollBackground()
scrolls = pygame.sprite.Group(scroll_background)
clock = pygame.time.Clock()


#Level 1 Start Screen
def start_screen():
    pygame.mixer.music.stop()
    pygame.display.flip()
    pygame.mixer.init()
    pygame.mixer.music.load("suspense.mp3")
    pygame.mixer.music.play(-1, 0)
    prompt = True
    while prompt:
            clock.tick(FPS)
            scrolls.update()
            scrolls.draw(screen)
            draw_text(screen, "THIS IS NOT THE MAIN GAME", 48, WIDTH / 2, HEIGHT / 4)
            draw_text(screen, "THIS IS A CUTSCENE THAT WILL BE IMPLEMENTED INTO THE MAIN GAME", 22, WIDTH / 2, HEIGHT / 2)
            draw_text(screen, "THE MAIN GAME IS platformer.py!", 20, WIDTH / 2, HEIGHT * 2 / 3 - 50)
            draw_text(screen, "Press Enter to start", 18, WIDTH / 2, HEIGHT * 3 / 4)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RETURN:     
                        prompt = False

#Main Game Loop
game_over = True
running = True
CurrentLevel = 1
while running:
    if game_over:
        start_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        curtime = pygame.time.get_ticks()
        platforms = pygame.sprite.Group()
        grounds = pygame.sprite.Group()
        thentime = pygame.time.get_ticks()
        timemachine = TimeMachine()
        all_sprites.add(timemachine)
        for plat in PLATFORMS:
            p = Platform(*plat)
            all_sprites.add(p)
            platforms.add(p)
        for gro in GROUNDS:
            g = Ground(*gro)
            all_sprites.add(g)
            grounds.add(g)
    clock.tick(FPS)
    screen.blit(bg, [0, 0])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                running = False
            if event.key == pygame.K_f:
                player = Player()
                all_sprites.add(player)
            if event.key == pygame.K_h:
                closething = CloseThing()
                all_sprites.add(closething)
                dialogue = Dialogue()
                all_sprites.add(dialogue)
                textting = TextTing()
                all_sprites.add(textting)
                pygame.mixer.Sound.play(huh)

    #dialogue()
    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
