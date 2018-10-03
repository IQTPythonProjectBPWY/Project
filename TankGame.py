"""Tankgame.py
10-3-18 2:40pm

-Cleaned up code (kinda)
-Moar comments
-Combined repetitive tank rotate functions

TODO:
-catch enemy position data from server and move them
-Send own player movement? 
-Bullets aren't removing after collision with enemy.
"""
import pygame
#import random
from os import path
from pygame.math import Vector2
import math
from socket import *
import threading

#################### \/ \/ \/ DEBUGGING GARBAGE FOR TESING \/ \/ \/ ##################################
# Threading process to handle incoming data from main server
def process():
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(("",15000))
    s.listen(3)
    print "Waiting on connection"
    c,a = s.accept()
    print "Client connected"

    while True:
        data = c.recv(1024)

        # Print incomming data for debugging
        print data
        if data == "2u":
            player2.move("u")
        elif data == "2d":
            player2.move("d")
        elif data == "2l":
            player2.move("l")
        elif data == "2r":
            player2.move("r")
        elif data == "2s":
            player2.shoot()
        elif data == "3u":
            player3.move("u")
        elif data == "3d":
            player3.move("d")
        elif data == "3l":
            player3.move("l")
        elif data == "3r":
            player3.move("r")
        elif data == "3s":
            player3.shoot()
        elif data == "4u":
            player4.move("u")
        elif data == "4d":
            player4.move("d")
        elif data == "4l":
            player4.move("l")
        elif data == "4r":
            player4.move("r")
        elif data == "4s":
            player4.shoot()
        elif data == "as":
            player.shoot()
            player2.shoot()
            player3.shoot()
            player4.shoot()

    sock.shutdown(socket.SHUT_RDWR)
    sock.close()

# Start thread tp runn process() function
thread = threading.Thread(target=process)
thread.daemon = True
thread.start()
#################### /\ /\ /\ DEBUGGING GARBAGE FOR TESING /\ /\ /\ ##################################

# Directory where this is running from, and then the /img folder
img_dir = path.join(path.dirname(__file__), 'img')

# Window size
WIDTH = 1000
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

# Handicapped player class made for enemies. Needs to be modified to take input from server
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
        self.alive = True

    # Move enemies? REPLACE WITH X, Y, ANGLE DATA FROM SERVER!
    # Currently filled with rigged controlls for development
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

    # Called on every game loop
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
    # Enemy player fire. Maybe convert to be handled from the server? or keep it here and send server x,y,angle or bullet.
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_pew > self.pew_speed:
            testx = self.rect.centerx + (10 * math.cos(self.rot))
            testy = self.rect.centery + (10 * math.sin(self.rot))
            bullet = Bullet(self.rect.centerx, self.rect.centery, self.rot, self.bsize, self.bspeed, self)
            all_sprites.add(bullet)
            enemy_bullets.add(bullet)
            self.last_pew = pygame.time.get_ticks()

    # Enemy is dead. Set image to destroyed tank.
    def death(self):
        self.image_orig = pygame.transform.scale(player_DEAD, (30, 50))
        new_image = pygame.transform.rotate(self.image_orig, self.rot)
        old_center = self.rect.center
        self.image = new_image
        self.rect = self.image.get_rect()
        self.rect.center = old_center

        # Kill/disable self
        self.alive = False

# Class for current player on game client
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
        self.alive = True
    
    # Rotate funtion for current player tank
    def rotate(self, direction):
        if direction == "L":
            self.rot_speed = -4
        elif direction == "R":
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

    # Called on every game loop
    def update(self):
        self.speedx = 0
        degree = 0
        keystate = pygame.key.get_pressed()

        # Switch to check if player is alive and can move
        if self.alive == True:
            if keystate[pygame.K_a]:
                self.rotate("L")
            if keystate[pygame.K_d]:
                self.rotate("R")
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

    # Current player tank fire
    def shoot(self):
        now = pygame.time.get_ticks()
        # Bullet throttling to prevent spam
        if now - self.last_pew > self.pew_speed:
            bullet = Bullet(self.rect.centerx, self.rect.centery, self.rot, self.bsize, self.bspeed, player)
            all_sprites.add(bullet)
            bullets.add(bullet)
            self.last_pew = pygame.time.get_ticks()

    # Current player is dead. Switch to destroyed tank and flip alive bool (disables keypress input)
    def death(self):
        # Set to dead tank sprite
        self.image_orig = pygame.transform.scale(player_DEAD, (30, 50))
        new_image = pygame.transform.rotate(self.image_orig, self.rot)
        old_center = self.rect.center
        self.image = new_image
        self.rect = self.image.get_rect()
        self.rect.center = old_center

        # Kill/disable self
        self.alive = False

# Class for PeW objects
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, size, speed, owner):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((size,size))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.speedy = 10
        self.speed = speed
        angle = math.radians(angle)
        self.speed_x = self.speed * math.cos(angle)
        self.speed_y = self.speed * math.sin(angle)
        self.rect.centery = y
        self.rect.centerx = x
        self.owner = owner

    def update(self):
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

        # Check if bullets hit anyone
        self.removeBullet(player)
        self.removeBullet(player2)
        self.removeBullet(player3)
        self.removeBullet(player4)

    def checkCollision(self, playercheck):
        return pygame.sprite.collide_mask(self, playercheck)
        # return pygame.sprite.spritecollide(self, all_sprites, False)

    # \/ NOT WORKING!!!! Not sure why O.o
    # Bullet hit something! kill player and remove remove bullet
    def removeBullet(self, playercheck):
        if self.checkCollision(playercheck):
            self.kill()
            player.death()

# Sets images for each player
player_img = pygame.image.load(path.join(img_dir, "tank.png")).convert()
player2_img = pygame.image.load(path.join(img_dir, "tank2p.png")).convert()
player3_img = pygame.image.load(path.join(img_dir, "tank3p.png")).convert()
player4_img = pygame.image.load(path.join(img_dir, "tank4p.png")).convert()
player_DEAD = pygame.image.load(path.join(img_dir, "tankDead.png")).convert()

# Grouping for mass updates and collision detection
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()

# Initialize player and enemies
player = Player(player_img, 20, HEIGHT - 10)
player2 = Enemy(player2_img, 20, 0)
player3 = Enemy(player3_img, WIDTH - 20, 0)
player4 = Enemy(player4_img, WIDTH - 20, HEIGHT - 10)

#
all_sprites.add(player)
all_sprites.add(player2)
all_sprites.add(player3)
all_sprites.add(player4)

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

    # Check for bullet collision with players
    hits = pygame.sprite.spritecollide(player, enemy_bullets, False)
    hits2 = pygame.sprite.spritecollide(player2, bullets, False)
    hits3 = pygame.sprite.spritecollide(player3, bullets, False)
    hits4 = pygame.sprite.spritecollide(player4, bullets, False)
    # Insta-kill players on collision
    if hits:
        player.death()
    elif hits2:
        player2.death()
    elif hits3:
        player3.death()
    elif hits4:
        player4.death()

    # Count how many tanks are alive.
    count = 0
    if player.alive == True:
        count += 1
    if player2.alive == True:
        count += 1
    if player3.alive == True:
        count += 1
    if player4.alive == True:
        count += 1

    # End game if one remains.
    if count == 1:
        running = False

    # Draw / render
    screen.fill(WHITE)
    all_sprites.draw(screen)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
