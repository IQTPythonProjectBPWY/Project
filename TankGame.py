# Pygame template - skeleton for a new pygame project
import pygame
import random
from os import path
from pygame.math import Vector2
import math
from socket import *
import threading

# # Setup a socket
# s = socket(AF_INET, SOCK_STREAM)
# s.bind(("",15000))
# s.listen(5)
# c,a = s.accept()

# # Output info
# print("Incomming connection from: {}".format(a))

def process():


    s = socket(AF_INET, SOCK_STREAM)
    s.bind(("",15000))
    s.listen(3)
    print "Waiting on connection"
    c,a = s.accept()

    print "Client connected"

    while True:
        data = c.recv(1024)
        # m = conn[0].recv(4096)
        # conn[0].send(m[::-1])
        print data
        if data == "2u":
            enemyMove(2, "u")
        elif data == "2d":
            enemyMove(2, "d")
        if data == "2l":
            enemyMove(2, "l")
        elif data == "2r":
            enemyMove(2, "r")
        elif data == "2s":
            player2.shoot()

    sock.shutdown(socket.SHUT_RDWR)
    sock.close()

thread = threading.Thread(target=process)
thread.daemon = True
thread.start()

def enemyMove(player, direction):
    if player == 2:
        player2.move(direction)


# Directory where this is running from, and then the /img folder
img_dir = path.join(path.dirname(__file__), 'img')

# Window size
WIDTH = 750
HEIGHT = 750
FPS = 40

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ERMAGERDD! TANKZ!")
clock = pygame.time.Clock()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, player, center, height):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = pygame.transform.scale(player, (30, 50))
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.rect.centerx = center
        self.rect.bottom = height
        self.speedx = 0
        self.speedS = 0
        self.angle = 0
        self.rot = 0
        self.rot_speed = 4
        self.last_update = pygame.time.get_ticks()
        self.last_pew = pygame.time.get_ticks()
        self.pew_speed = 1000
        self.speedF = 3
        self.speedR = -3
        self.bsize = 5
        self.bspeed = 7

    def move(self, direction):
        if direction == "d":
            angle = math.radians(self.rot)
            self.speed_x = self.speedF * math.cos(angle)
            self.speed_y = self.speedF * math.sin(angle)
            self.rect.x += self.speed_y
            self.rect.y += self.speed_x
        if direction == "u":
            angle = math.radians(self.rot)
            self.speed_x = self.speedR * math.cos(angle)
            self.speed_y = self.speedR * math.sin(angle)
            self.rect.x += self.speed_y
            self.rect.y += self.speed_x
        if direction == "r":
            self.rot_speed = 4
            now = pygame.time.get_ticks()
            if now - self.last_update > 50:
                self.last_update = now
                self.rot = (self.rot - self.rot_speed) % 360
                new_image = pygame.transform.rotate(self.image_orig, self.rot)
                old_center = self.rect.center
                self.image = new_image
                self.rect = self.image.get_rect()
                self.rect.center = old_center
        if direction == "l":
            self.rot_speed = -4
            now = pygame.time.get_ticks()
            if now - self.last_update > 50:
                self.last_update = now
                self.rot = (self.rot - self.rot_speed) % 360
                new_image = pygame.transform.rotate(self.image_orig, self.rot)
                old_center = self.rect.center
                self.image = new_image
                self.rect = self.image.get_rect()
                self.rect.center = old_center

    def update(self):
        self.speedx = 0
        degree = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_pew > self.pew_speed:
            testx = self.rect.centerx + (10 * math.cos(self.rot))
            testy = self.rect.centery + (10 * math.sin(self.rot))
            bullet = Bullet(self.rect.centerx, self.rect.centery, self.rot, self.bsize, self.bspeed)
            all_sprites.add(bullet)
            bullets.add(bullet)
            self.last_pew = pygame.time.get_ticks()


class Player(pygame.sprite.Sprite):
    def __init__(self, player, center, height):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = pygame.transform.scale(player, (30, 50)) # pygame.Surface((50, 40))
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.rect.centerx = center
        self.rect.bottom = height
        self.speedx = 0
        self.speedS = 0
        self.angle = 0
        self.rot = 0
        self.rot_speed = 4
        self.last_update = pygame.time.get_ticks()
        self.last_pew = pygame.time.get_ticks()
        self.pew_speed = 1000
        self.speedF = 3
        self.speedR = -3
        self.bsize = 5
        self.bspeed = 7
        
    def rotateR(self):
        self.rot_speed = 4
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot - self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def rotateL(self):
        self.rot_speed = -4
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot - self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center


    def update(self):
        self.speedx = 0
        degree = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.rotateL()
        if keystate[pygame.K_d]:
            self.rotateR()
        if keystate[pygame.K_w]:
            angle = math.radians(self.rot)
            self.speed_x = self.speedF * math.cos(angle)
            self.speed_y = self.speedF * math.sin(angle)
            self.rect.x += self.speed_y
            self.rect.y += self.speed_x
        if keystate[pygame.K_s]:
            angle = math.radians(self.rot)
            self.speed_x = self.speedR * math.cos(angle)
            self.speed_y = self.speedR * math.sin(angle)
            self.rect.x += self.speed_y
            self.rect.y += self.speed_x
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_pew > self.pew_speed:
            testx = self.rect.centerx + (10 * math.cos(self.rot))
            testy = self.rect.centery + (10 * math.sin(self.rot))
            bullet = Bullet(self.rect.centerx, self.rect.centery, self.rot, self.bsize, self.bspeed)
            all_sprites.add(bullet)
            bullets.add(bullet)
            self.last_pew = pygame.time.get_ticks()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, size, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((size,size))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = 10
        self.speed = speed
        angle = math.radians(angle)
        self.speed_x = self.speed * math.cos(angle)
        self.speed_y = self.speed * math.sin(angle)

    def update(self):
        # self.rect.y += self.speedy
        self.rect.x += self.speed_y
        self.rect.y += self.speed_x
        if self.rect.bottom < 5:
            self.kill()
        elif self.rect.top > HEIGHT-5:
            self.kill()
        elif self.rect.left < 5:
            self.kill()
        elif self.rect.right > WIDTH-5:
            self.kill()

# Sets images for each player
player_img = pygame.image.load(path.join(img_dir, "tank.png")).convert()
player2_img = pygame.image.load(path.join(img_dir, "tank2p.png")).convert()
player3_img = pygame.image.load(path.join(img_dir, "tank3p.png")).convert()
player4_img = pygame.image.load(path.join(img_dir, "tank4p.png")).convert()

all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Initialize player1 (local) as first player image (Red)
player = Player(player_img, 20, HEIGHT - 10)
player2 = Enemy(player2_img, 20, 0)

all_sprites.add(player)
all_sprites.add(player2)

# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        # Check for keypress, specifically Spacebar to fire
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Update
    all_sprites.update()

    # Draw / render
    screen.fill(WHITE)
    all_sprites.draw(screen)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
