
import pygame
from pygame.locals import *
import sys
import random
import time


pygame.init()
vec = pygame.math.Vector2  

HEIGHT = 450
WIDTH = 400
ACC = 0.5
FRIC = -0.12
FPS = 50

FramePerSec = pygame.time.Clock()

#Создаем окно на котором будет игра

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")
background_image = pygame.image.load("bg.png")
menu_image=pygame.image.load("Menu.png")

class Player(pygame.sprite.Sprite):
          
    #Инициализируем игрока как кота и создаем область реакции персонажа"rect"

    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("basik.jpg").convert_alpha()
        self.rect = self.surf.get_rect()
        
        self.pos = vec((10, 360))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.jumping = False
        self.score = 0
        
#Функция движения нашего котика
        
    def move(self):
        self.acc = vec(0, 0.5)
        pressed_keys = pygame.key.get_pressed()
        
        #Устанавливаем движение на стрелочки вправо и влево
        
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC
        
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        # Позволяем Kity переходить через границы окна на ругую часть экрана
        
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos

    #Функция прыжка
        
    def jump(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -15
    
    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    #Обновление счета и сдвижения фона вверх
    
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

#Экран поражения

def youlose():
    displaysurface.blit(pygame.image.load("lose2.png"),  (-25,0))
    #displaysurface.blit(pygame.image.load("Menu.png"),  (0,0))   
#Экран победы

def youwin():
    displaysurface.blit(pygame.image.load("win2.png"),  (-25,0))
        

#Класс для движушихся облачков

class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("cloudy2.png").convert_alpha()
        self.rect = self.surf.get_rect(center=(random.randint(0, WIDTH - 10),
                                               random.randint(0, HEIGHT - 30)))

        #Используя рандом устанавливаем скорость
        
        self.speed = random.randint(-1, 1)
        self.moving = True
        self.point = True

          
    #Функция их полета
        
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
        С = False

#Генератор облаков
        
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

#Вывод любого текста

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, 255)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


#Основные настройки самой игры

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

displaysurface.blit(menu_image,  (0,0))

f = pygame.font.SysFont('times new roman', 20)
g = f.render("by Sofa Revak in 2024 May to 1580", True, (255, 255, 255))
aa = g.get_rect()
aa.midtop = (5, 420)
displaysurface.blit(g, aa.midtop ) 
pygame.display.update()
time.sleep(1.5)


#Сам цикл игры
    
while True:
    
    #Ставим фон
          
    displaysurface.blit(background_image,  (-50,-30))

    #Выводим Счет
    
    f = pygame.font.SysFont('times new roman', 50)
    g = f.render(str(P1.score), True, (255, 255, 255))
    aa = g.get_rect()
    aa.midtop = (WIDTH/2, 15)
    displaysurface.blit(g, aa.midtop )  
    P1.update()

    
    #Прописываем что будет если котик будет ниже экрана
    
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


    #Условия победы
            
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



    #Прописываем управление через стрелочки
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


    #Если игрок ниже трети экрана
                
    if P1.rect.top <= HEIGHT / 3:
        P1.pos.y += abs(P1.vel.y)
        for plat in platforms:
            plat.rect.y += abs(P1.vel.y)
            if plat.rect.top >= HEIGHT:
                plat.kill()


    #Генерируем облака
                
    plat_gen()
    displaysurface.blit(background_image,  (-50,-30))
    displaysurface.blit(g, aa.midtop)


    #Каждый объект добавляем на экран
    
    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)
        entity.move()


    #Обнавляем дисплей
        
    pygame.display.update()
    FramePerSec.tick(FPS)
                                                  #всё






        
