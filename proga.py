from pygame import *
from random import randint
import sys

mixer.init()
font.init()

clock = time.Clock()
FPS = 60
w = 700
h = 500
speed = 5
window = display.set_mode((w, h))
display.set_caption("Шутер")
background = transform.scale(image.load('клас.jpg'), (w, h))

#font = font.SysFont('Arial', 40)

mixer.music.load('фон.mp3')
mixer.music.set_volume(0.1)
miss = 0

shoot = mixer.Sound('постріл.mp3')
lost = mixer.Sound('праіграла.mp3')
win = mixer.Sound('війграла.mp3')

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update (self):
        if key_pressed[K_d] and self.rect.x < 625:
            self.rect.x += self.speed
        if key_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if key_pressed[K_w] and self.rect.y > 250:
            self.rect.y -= self.speed
        if key_pressed[K_s] and self.rect.y < 425:
            self.rect.y += self.speed
    def fire(self):
        bullet = Weapon('два.png', self.rect.centerx , self.rect.top, 7, 50 , 50)
        bullets.add(bullet)

        
    
teacher = Player('учітілька.png', 330, 400, 5, 120, 70)

class Pupils(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global miss
        if self.rect.y > 480:
            miss += 1
            self.rect.y = 0
            self.rect.x = randint(0, 700)

students = sprite.Group()



i= 0
while i!= 5:
    p = Pupils('nerd.png', randint(50, 750), -100, 2, 50, 50)
    students.add(p)
    i += 1

class Weapon(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

bullets = sprite.Group()




BLUE = (102, 178, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
count = 0
text = font.Font(None, 25)
text1 = font.Font(None, 50)
running = True
finish = False
mixer.music.play()

while running:
    for e in event.get(): 
        if e.type == QUIT:
                running = False
    key_pressed = key.get_pressed()
    if finish != True:
        window.blit(background, (0,0))

        label_count = text.render('Рахунок: ', True, BLUE)
        l_c = text.render(str(count), True, BLUE)

        label_miss = text.render('Пропущених:', True, BLUE)
        l_m = text.render(str(miss), True, BLUE)

        label_WIN = text1.render('YOU DEFEATED ANGRY TEACHER ', True, GREEN)
        label_LOOSE = text1.render('ANGRY TEACHER PUT YOU 2', True, RED)

        window.blit(label_count, (20, 20))
        window.blit(label_miss, (20, 50))
        window.blit(l_c, (100, 20))
        window.blit(l_m, (135, 50))
        
        # window.blit(label_LOOSE, (200, 200))
    
        teacher.reset()
        teacher.update()

        students.draw(window)
        students.update()
        
        bullets.draw(window)
        bullets.update()
        
        if key_pressed[K_SPACE]:
            shoot.play()
            teacher.fire()

        sprites_list = sprite.groupcollide(students, bullets, True, True)
        
        for s in sprites_list:
            count += 1
            p = Pupils('nerd.png', randint(50, 750), -100, 2, 50, 50)
            students.add(p)
        
        if count >= 10: 
            finish= True
            window.blit(label_WIN, (100, 200))
            win.play()

        if sprite.spritecollide(teacher, students, False) or miss >= 3:
            finish= True
            window.blit(label_LOOSE, (100, 200))
            lost.play()


        display.update()    
        clock.tick(FPS)