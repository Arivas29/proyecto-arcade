from pygame import *
from config import * 
from random import *

init()

# TRABAJO CON FUENTES
font.init()
f1 = font.SysFont('Arial', 20)

# MAIN WINDOW
screen = display.set_mode((ANCHO, ALTO))
display.set_caption(TITULO)

# CLASE PRINCIPAL
class GameSprite(sprite.Sprite):
    def __init__(self, sprite_img, cord_x, cord_y, width, height, speed=0):
        super().__init__()
        self.width = width
        self.height = height
        try:
            self.image = transform.scale(image.load(sprite_img), (self.width, self.height))
        except:
            # Si no encuentra la imagen, crea un rectángulo de color para que no crashee
            self.image = Surface((self.width, self.height))
            self.image.fill((200, 200, 0))
            
        self.rect = self.image.get_rect()
        self.rect.x = cord_x
        self.rect.y = cord_y
        self.speed = speed

    def reset(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(GameSprite):
    def __init__(self, sprite_img, cord_x, cord_y, width, height, speed, direction):
        super().__init__(sprite_img, cord_x, cord_y, width, height, speed)
        self.direction = direction # 1 para derecha, -1 para izquierda

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.x < 0 or self.rect.x > ANCHO:
            self.kill()

class Player(GameSprite):
    def __init__(self, sprite_img, cord_x, cord_y, width, height, speed=0):
        super().__init__(sprite_img, cord_x, cord_y, width, height, speed)
        self.ammo = 5
        self.last_shot_time = 0
        self.reload_start_time = 0
        self.reloading = False

    def shoot(self, direction, group, bullet_sprite):
        current_time = time.get_ticks()
        
        if not self.reloading:
            # Verificar si ha pasado 1 segundo (1000ms) desde el último tiro
            if self.ammo > 0 and (current_time - self.last_shot_time > 1000):
                # Ahora usamos bullet_sprite que viene desde el ciclo principal
                bullet = Bullet(bullet_sprite, self.rect.centerx, self.rect.centery, 30, 20, 10, direction)
                group.add(bullet)
                self.ammo -= 1
                self.last_shot_time = current_time
            
            # Si se acaba la munición, iniciar recarga
            if self.ammo == 0:
                self.reloading = True
                self.reload_start_time = current_time

        else:
            # Si han pasado 2.5 segundos (2500ms) recargando
            if current_time - self.reload_start_time > 2500:
                self.ammo = 5
                self.reloading = False

    def update1(self): 
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < ALTO - self.rect.h:
            self.rect.y += self.speed
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < (ANCHO // 2) - self.rect.w:
            self.rect.x += self.speed

    def update2(self): 
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < ALTO - self.rect.h:
            self.rect.y += self.speed
        if keys[K_LEFT] and self.rect.x > (ANCHO // 2):
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < ANCHO - self.rect.w:
            self.rect.x += self.speed

# OBJETOS
try:
    background = transform.scale(image.load(BG_IMG), (ANCHO, ALTO))
except:
    background = Surface((ANCHO, ALTO))
    background.fill(BACK_COLOR)

# Jugador 1: Izquierda | Jugador 2: Derecha
player1 = Player(PLAYER_IMG, 50, (ALTO // 2) - 30, 60, 60, 5    )
player2 = Player(PLAYER_IMG2, ANCHO - 110, (ALTO // 2) - 30, 60, 60, 5)

bullets = sprite.Group()

# CICLO DE JUEGO
run = True
finish = False
clock = time.Clock()

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        
        if e.type == KEYDOWN:
            if e.key == K_r:
                finish = False
            
            # DISPAROS PERSONALIZADOS
            if e.key == K_SPACE: # P1 dispara COCACOLA
                player1.shoot(1, bullets, BULLET)
            
            if e.key == K_RETURN: # P2 dispara DÓLAR
                player2.shoot(-1, bullets, BULLET_IMG)

    if not finish:
        screen.blit(background, (0, 0))
        
        # Dibujar línea divisoria
        draw.line(screen, WHITE, (ANCHO // 2, 0), (ANCHO // 2, ALTO), 2)
        
        # Actualización
        player1.update1()
        player2.update2()
        bullets.update()
        
        # Renderizado
        player1.reset()
        player2.reset()
        bullets.draw(screen)

        # Mostrar munición en pantalla
        txt_p1 = f1.render(f"Balas: {player1.ammo if not player1.reloading else 'Recargando...'}", True, WHITE)
        txt_p2 = f1.render(f"Balas: {player2.ammo if not player2.reloading else 'Recargando...'}", True, WHITE)
        screen.blit(txt_p1, (20, 20))
        screen.blit(txt_p2, (ANCHO - 150, 20))

    display.update()
    clock.tick(FPS)

quit()
