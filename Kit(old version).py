import pygame
from pygame.locals import *
import sys
import random
import time


pygame.init()
vec = pygame.math.Vector2  # 2 for two dimensional

HEIGHT = 450
WIDTH = 400
ACC = 0.5
FRIC = -0.12
FPS = 50

FramePerSec = pygame.time.Clock()

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")


background_image = pygame.image.load("bg.png")


class Player(pygame.sprite.Sprite):



    def __init__(self):
        super().__init__()
        ##self.image = pygame.image.load("character.png")
                #self.surf = pygame.Surface((30, 30))
                #self.surf.fill((0, 0, 255))
        self.surf = pygame.image.load("basik.jpg").convert_alpha()
        self.rect = self.surf.get_rect()

        self.pos = vec((10, 360))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.jumping = False
        self.score = 0

    def move(self):
        self.acc = vec(0, 0.5)

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos

    def jump(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -15

    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def update(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if self.vel.y > 0:
            if hits:
                if self.pos.y < hits[0].rect.bottom:
                    if hits[0].point == True:  ##
                        hits[0].point = False  ##
                        self.score += 1
                    self.pos.y = hits[0].rect.top + 1
                    self.vel.y = 0
                    self.jumping = False

def youlose():
    displaysurface.blit(pygame.image.load("end.png"),  (-20,0))



def youwin():
    displaysurface.blit(pygame.image.load("win.png"),  (-20,0))




class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #self.surf = pygame.Surface((random.randint(50, 100), 12))
        #self.surf.fill((255, 204, 255))
     



        self.surf = pygame.image.load("cloudy2.png").convert_alpha()
        self.rect = self.surf.get_rect(center=(random.randint(0, WIDTH - 10),
                                               random.randint(0, HEIGHT - 30)))
        self.speed = random.randint(-1, 1)
        self.moving = True
        self.point = True



    def move(self):
        if self.moving == True:
            self.rect.move_ip(self.speed,0)
            if self.speed > 0 and self.rect.left > WIDTH:
                self.rect.right = 0
            if self.speed < 0 and self.rect.right < 0:
                self.rect.left = WIDTH



def check(platform, groupies):
    if pygame.sprite.spritecollideany(platform, groupies):
        return True
    else:
        for entity in groupies:
            if entity == platform:
                continue
            if (abs(platform.rect.top - entity.rect.bottom) < 40) and (
                    abs(platform.rect.bottom - entity.rect.top) < 40):
                return True
        C = False


def plat_gen():
    while len(platforms) < 6:
        width = random.randrange(50, 100)
        p = platform()
        C = True

        while C:
            p = platform()
            p.rect.center = (random.randrange(0, WIDTH - width),
                             random.randrange(-50, 0))
            C = check(p, platforms)
        platforms.add(p)
        all_sprites.add(p)
font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, 255)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)



PT1 = platform()
P1 = Player()

PT1.surf = pygame.Surface((WIDTH, 20))
PT1.surf.fill((255, 255, 255))
PT1.rect = PT1.surf.get_rect(center=(WIDTH / 2, HEIGHT - 10))
all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(P1)

platforms = pygame.sprite.Group()
platforms.add(PT1)
PT1.moving = False
PT1.point = False

for x in range(random.randint(4, 5)):
    C = True
    pl = platform()
    while C:
        pl = platform()
        C = check(pl, platforms)
    platforms.add(pl)
    all_sprites.add(pl)

while True:


    displaysurface.blit(background_image,  (-50,-30))


    f = pygame.font.SysFont('times new roman', 50)  ##

    g = f.render(str(P1.score), True, (255, 255, 255))  ##
    aa = g.get_rect()
    aa.midtop = (WIDTH/2, 15)
    displaysurface.blit(g, aa.midtop )  ##
    P1.update()

    if P1.rect.top > HEIGHT:
        for entity in all_sprites:
            entity.kill()
            time.sleep(1)
            displaysurface.fill((255, 153, 255))

            displaysurface.blit(g, aa.midtop)
            youlose()
            pygame.display.update()
            time.sleep(1.5)
            pygame.quit()
            sys.exit()
    if int(P1.score)> 15:
        for entity in all_sprites:
            entity.kill()
            time.sleep(1)
            displaysurface.fill((255, 255, 255))
            displaysurface.blit(g, aa.midtop)
            youwin()
            pygame.display.update()
            time.sleep(1.5)
            pygame.quit()
            sys.exit()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                P1.jump()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                P1.cancel_jump()

    if P1.rect.top <= HEIGHT / 3:
        P1.pos.y += abs(P1.vel.y)
        for plat in platforms:
            plat.rect.y += abs(P1.vel.y)
            if plat.rect.top >= HEIGHT:
                plat.kill()

    plat_gen()
    displaysurface.blit(background_image,  (-50,-30))
    displaysurface.blit(g, aa.midtop)

    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)
        entity.move()
    pygame.display.update()
    FramePerSec.tick(FPS)
