#Створи власний Шутер!
from pygame import *
import random
init()
window = display.set_mode((700, 500))
bg = image.load('galaxy.jpg')
bg = transform.scale(bg, (700, 500))
window.blit(bg, (0, 0))

clock = time.Clock()
mixer.init()
mixer.music.load('space.ogg')
mixer.music.set_volume(0.1)
mixer.music.play(1000)
fire = mixer.Sound('fire.ogg')
fire.set_volume(0.3)
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed,w,h):
        super().__init__()
        
        self.image = transform.scale(image.load(player_image), (w, h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

print(1)
class Player(GameSprite):
    def update(self):
        pressed = key.get_pressed()
        if pressed[K_a] and self.rect.x + self.speed > 0:
            self.rect.x -= self.speed
        elif pressed[K_d] and self.rect.x + self.speed <  650:
            self.rect.x += self.speed
        if self.rect.x  > 650:
            self.rect.x -= self.speed
        if self.rect.x  < -50:
            self.rect.x += self.speed
    def update_2(self):
        pressed = key.get_pressed()
        if pressed[K_LEFT] and self.rect.x + self.speed > 0:
            self.rect.x -= self.speed
        elif pressed[K_RIGHT] and self.rect.x + self.speed <  650:
            self.rect.x += self.speed
        if self.rect.x  > 650:
            self.rect.x -= self.speed
        if self.rect.x  < -50:
            self.rect.x += self.speed

lost = 0
class Enemy(GameSprite):
    
    def update(self):

        self.rect.y += self.speed
        global lost
        if self.rect.y  > 500:
            self.rect.y = -50
            self.rect.x = random.randint(50, 600)
            lost += 1
            
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill

class Stone(GameSprite):
    
    def update(self):
        self.rect.y += self.speed
        if self.rect.y  > 500:
            self.rect.y = -50
            self.rect.x = random.randint(50, 600)


#  lose    

hero = Player('rocket.png', 300, 400, 10, 80,100)
stones = sprite.Group()
bullets = sprite.Group()
ufos = sprite.Group()
for i in range(7):
    enemy1 = Enemy('ufo.png', random.randint(50, 600), random.randint(-500, -50), 3, 80, 50)
    ufos.add(enemy1)
for i in range(2):
    stone = Stone('asteroid.png', random.randint(50, 600), random.randint(-500, -50), 2, 65, 65)
    stones.add(stone)

font.init()
font2 = font.SysFont(None, 72)
font1 = font.Font(None, 36)
txt_win = font2.render('You win!', True,(0,255,0))
txt_lose = font2.render('You lose!', True,(0,255,0))
is_duo = False
is_win = 0
btn_solo =  GameSprite('btn_solo.png', 100, 100, 0, 100, 50)
btn_duo =  GameSprite('btn_duo.png', 100, 200, 0, 150, 50)
screen = 'menu'
game =  True
killed = 0
while game:
    window.blit(bg, (0, 0))
    if screen =='menu':
        
        btn_solo.reset()
        btn_duo.reset()

        match is_win:
            case 0:
                ...
            case 1:
                window.blit(txt_lose, (150,50))
            case 2:
                window.blit(txt_win, (150,50))


        
        
        for e in event.get():
            if e.type == QUIT:
                quit()   
            if e.type == MOUSEBUTTONDOWN:
                x, y = e.pos
                if btn_solo.rect.collidepoint(x,y):
                    screen = 'main'
                if btn_duo.rect.collidepoint(x,y):
                    screen = 'main'
                    hero2 = Player('rocket.png', 400, 400, 10, 80,100)
                    is_duo = True
        display.update()
    if screen == 'main':
        for e in event.get():
            if e.type == QUIT:
                quit()   
            if e.type == KEYDOWN:
                if e.key == K_w:
                    bullet1 = Bullet('bullet.png',hero.rect.centerx, hero.rect.y, 15, 15, 20)         
                    bullets.add(bullet1)
                    fire.play()
                if e.key == K_UP and is_duo:
                    bullet1 = Bullet('bullet.png',hero2.rect.centerx, hero2.rect.y, 15, 15, 20)         
                    bullets.add(bullet1)
                    fire.play()
        
        

        text_lost = font1.render(f'Пропущено: {lost}', True, (255,255,255))
        window.blit(text_lost,(10,50))

        sprites = sprite.groupcollide(bullets, ufos, True, True)
        for i in  sprites:
            killed += 1
            enemy1 = Enemy('ufo.png', random.randint(50, 600), random.randint(-500, -50), 3, 80, 50)
            ufos.add(enemy1)
        sprites = sprite.groupcollide(bullets, stones, True, False)
        lose = sprite.spritecollide(hero, stones,False)
        if lose:
            screen = 'menu'
            is_win = 1
        if is_duo:
            lose = sprite.spritecollide(hero2, stones,False)
            if lose:
                screen = 'menu'
                is_win = 1
        if lost == 5:
            screen = 'menu'
            is_win = 1

        killed_enemy = font1.render(f'Вбито: {killed}', True, (255,255,255))
        window.blit(killed_enemy,(10,70))

        
        hero.reset()
        hero.update()
        if is_duo:
            hero2.reset()
            hero2.update_2()

        ufos.draw(window)
        ufos.update()
        bullets.draw(window)
        bullets.update()
        stones.draw(window)
        stones.update()
        display.update()
        clock.tick(40)
