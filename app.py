import pygame
from pygame import mixer

pygame.init()
pygame.mixer.pre_init(44100,-16,2,512)
mixer.init()
FPS = 60
FramePerSec = pygame.time.Clock()

WHITE = (255,255,255)
BLACK = (0, 0, 0)


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

SHIP_WIDTH = 80
SHIP_HEIGHT = 80

WINDOW = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
WINDOW.fill(WHITE)

background = pygame.image.load("images/space.jpg")
pygame.display.set_caption("Space War")

shoot_fx = pygame.mixer.Sound("sounds/ship_shoot.mp3")
shoot_fx.set_volume(0.25)
class Ship:
    COOLDOWN = 500
    def __init__(self,x,y,height,width):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.image = pygame.image.load("images/ship.png")
        self.vel = 6
        self.cool_down_counter = 0
        self.lasers = []
        self.last_shot = pygame.time.get_ticks()
        
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.x - self.vel <= SCREEN_WIDTH - SHIP_WIDTH :
            self.x += self.vel
        if keys[pygame.K_LEFT] and self.x - self.vel >= 0:
            self.x -= self.vel
        if keys[pygame.K_UP] and self.y - self.vel > 0:
            self.y -= self.vel
        if keys[pygame.K_DOWN] and self.y - self.vel <= SCREEN_HEIGHT:
            self.y += self.vel 
        
    def draw(self):
        WINDOW.blit(pygame.transform.scale(self.image, (self.width,self.height)), (self.x, self.y))
  
    def shoot(self):
        keys = pygame.key.get_pressed()
        time_now = pygame.time.get_ticks()
        
        if keys[pygame.K_SPACE] and time_now - self.last_shot > self.COOLDOWN:
            shoot_fx.play()
            laser = Fire(self.x+15,self.y+10)
            self.lasers.append(laser)
            self.last_shot = time_now
        for lasers in self.lasers:
            lasers.move()
            lasers.draw(WINDOW)
            if lasers.y < 0:
                self.lasers.remove(lasers)
              
class Fire:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.height = 50
        self.width = 50
        self.laser_img = pygame.image.load("images/laser.png")
        self.vel = 10
    def draw(self,WINDOW):
        WINDOW.blit(pygame.transform.scale(self.laser_img, (self.width,self.height)), (self.x, self.y))
    def move(self):
        self.y -=self.vel   

ship = Ship(SCREEN_WIDTH//2 - SHIP_WIDTH//2, SCREEN_HEIGHT - SHIP_HEIGHT - 10, SHIP_HEIGHT,SHIP_WIDTH)

run = True
while(run):
    WINDOW.fill(WHITE)
    WINDOW.blit(background, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
    ship.shoot()
    ship.move()
    ship.draw()
    pygame.display.update()
    FramePerSec.tick(FPS)
