from pygame import*
from random import randint
#definicion de la clase para los objetos
class GameSprite (sprite.Sprite):
    #constructor de la clase
    def __init__(self, player_image, player_x, player_y,size_x,size_y, player_speed):
        super().__init__()
        #inicializando las propiedades del objeto
        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = player_speed
        #cada objeto debe tener la propiedad rect(rectangulo donde esta)
        self.rect= self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        wn.blit(self.image,(self.rect.x,self.rect.y))
#creando la clase heredera(player)
class Player(GameSprite):
    #metodo para controlar el objeto on las teclas
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x>5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x<wn_width-80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png',self.rect.centerx,self.rect.top,15,20,10)
        bullets.add(bullet)

#creando la clase enemigo
class Enemy(GameSprite):
    #definiedno metodo update(movimiento del enemigo)
    def update(self):
        self.rect.y += self.speed
        global fallos
        if self.rect.y > wn_height:
            self.rect.y = 0
            self.rect.x = randint(80,wn_width-80)
            fallos = fallos+1

#definiendo bullet
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

#creando la ventana principal de juego
wn_width = 700
wn_height = 500
image_back = 'galaxy.jpg'
wn = display.set_mode((wn_width,wn_height))
display.set_caption('Tirador')
background = transform.scale(image.load(image_back),(wn_width,wn_height))
#cargando la musica
mixer.init()
mixer.music.load('glitch-1-33356.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

#creando las fuentes y subtitulos
font.init()
font1 = font.SysFont('Arial',36)
#carteles ganaste y perdiste
font2 = font.SysFont('Arial', 80)
win = font2.render('¡Ganaste!',True,(0,255,0))
lose = font2.render('Perdiste',True,(255,0,0))
#creando objetos
ship = Player('rocket.png',5,wn_height-100,80,100,10)
monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy('ufo.png',randint(80,wn_width-80),-40,80,50,randint(1,5))
    monsters.add(monster)
bullets = sprite.Group()

#ciclo principal de juego
fallos = 0
max_fallos = 3
score = 0
#variable del juego
finish = False
game = True
FPS = 60
clock = time.Clock()
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                ship.fire()
                fire_sound.play()
    if not finish:
        wn.blit(background,(0,0))
        #escribiendo los textos de pantalla
        text_lose = font1.render('Fallados:'+ str(fallos),1,(255,255,255))
        text_puntos = font1.render('Puntaje:'+ str(score),1,(255,255,255))
        #ejecuta los movimientos del objeto
        ship.update()
        monsters.update()
        bullets.update()
        wn.blit(text_lose,(10,20))
        wn.blit(text_puntos,(10,50))
        #pone la nave en las coordenadas en la pantalla
        ship.reset()
        monsters.draw(wn)
        bullets.draw(wn)
    #comprobado o iniciando logica de colision
    #obteninedo lista de collisiones
        collides = sprite.groupcollide(monsters,bullets,True,True)
        for collide in collides:
            #nuestro jugador gana un punto
            score += 1
            monster = Enemy('ufo.png',randint(80,wn_width-80),-40,80,50,randint(1,5))
            monsters.add(monster)
        #comprobacion de una posible derrota
        if sprite.spritecollide(ship,monsters,False) or fallos >= max_fallos:
            finish = True
            wn.blit(lose,(200,200))
        #comprobacion de victoria
        if score >= 10:
            wn.blit(win,(200,200))
            finish = True
        display.update()
    else:
        finish = False
        fallos = 0
        score = 0
        #matando todas las balas
        for b in bullets:
            b.kill()
        #matando toods los ennemigos
        for m in monsters:
            m.kill()
        #esperado tres segundo
        time.delay(3000)
        for i in range(1,6):
            monster = Enemy('ufo.png',randint(80,wn_width-80),-40,80,50,randint(1,5))
            monsters.add(monster)

    time.delay(50)
#clock.tick(FPS)