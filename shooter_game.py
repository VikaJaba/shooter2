from pygame import *
from random import randint


game = True
finish = False
FPS = 60
clock = time.Clock()
clock.tick(FPS)
font.init()
font = font.SysFont('Arial', 30)

class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(65,65))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.speed = player_speed

    def reset(self):
        win.blit(self.image,(self.rect.x,self.rect.y))

bullets = sprite.Group()

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_RIGHT] and self.rect.x< 632:
            self.rect.x+=self.speed
        if keys_pressed[K_LEFT] and self.rect.x> 3:
            self.rect.x-=self.speed
    def fire(self):
            bullet = Bullet('bullet.png',self.rect.x,self.rect.y+10,10)
            bullets.add(bullet)
            fire_sound.play()
missed = 0

class Enemy(GameSprite):
    def update(self):
        self.rect.y+=self.speed
        global missed
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(200,500)
            missed+=1

class Bullet(GameSprite):
    def update(self):
        self.rect.y-=self.speed
        self.reset()
        if self.rect.y <= -20:
            self.kill()

class Asteroid(GameSprite):
    def update(self):
        self.rect.y+=self.speed
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(200,500)
        
mixer.init()
mixer.music.load('space.ogg')
fire_sound = mixer.Sound('fire.ogg')
mixer.music.play()

win = display.set_mode((700,500))
#nice
display.set_caption('space shooter')
background = transform.scale(image.load('galaxy.jpg'),(700,500))

rocket = Player('rocket.png',350,430,6)
monsters = sprite.Group()
for i in range(5):
    ufo = Enemy('ufo.png',randint(200,500),50,randint(1,4))
    monsters.add(ufo)
sprite.groupcollide(monsters,bullets,True,True)
score = 0
asteroids = sprite.Group()
for i in range(3):
    asteroid = Asteroid('asteroid.png',randint(200,500),50,3)
    asteroids.add(asteroid)
lives = 2
mortality = True
m_time = 1
the_time = 0
while game:
    import time
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            keys_pressed = key.get_pressed()
            if keys_pressed[K_SPACE]:
                rocket.fire()
        else:
            pass
    if finish != True:
        if mortality == False:
            end = time.time()
            the_time = end - start
            if the_time < m_time:
                pass
            else:
                mortality = True
        win.blit(background,(0,0))
        rocket.update()
        monsters.update()
        asteroids.update()
        monsters.draw(win)
        asteroids.draw(win)
        rocket.reset()
        missed_count = font.render('missed:'+str(missed),True,(255,255,255))
        win.blit(missed_count,(50,50))
        score_count = font.render('score:'+str(score),True,(255,255,255))
        win.blit(score_count,(50,25))
        bullets.update()
        bullets.draw(win)
        lives_count = font.render(str(lives),True,(255,255,255))
        win.blit(lives_count,(650,50))
        if sprite.spritecollide(rocket,monsters,False)or sprite.spritecollide(rocket,asteroids,False):
            if lives < 1:
                finish = True
                you_lost = font.render('YOU LOST!',True,(255,255,255))
                win.blit(you_lost,(280,230))
            else:
                if mortality == True:
                    lives-=1
                    mortality = False
                    start = time.time()
        if sprite.groupcollide(monsters,bullets,True,True):
            score+=1
            ufo = Enemy('ufo.png',randint(50,650),50,randint(1,4))
            monsters.add(ufo)
        if score == 25:
            finish = True
            you_won = font.render('YOU WON!',True,(255,255,255))
            win.blit(you_won,(280,230))
        if missed >= 10:
            finish = True
            you_lost = font.render('YOU LOST!',True,(255,255,255))
            win.blit(you_lost,(280,230))
    else:
        pass
        '''rocket.kill()
        for e in monsters:
            e.kill()
        for e in bullets:
            e.kill()
        for e in asteroids:
            e.kill()
        finish = False
        time.delay(3000)'''
    display.update()
    clock.tick(FPS)
    #жаба
