# Pygame template - skeleton for a new pygame project
import pygame
import random
from os import path
import math
import networkc
from socket import *

def StartGame(serverIP):
    
    class Player(pygame.sprite.Sprite):
        def __init__(self, player_img, startingData,playerN):
            pygame.sprite.Sprite.__init__(self)
            self.playerNDX = playerN
            self.image_orig = pygame.transform.scale(player_img, (20, 20)) # pygame.Surface((50, 40))
            self.image = self.image_orig.copy()
            self.rect = self.image.get_rect()
            self.rect.centerx = startingData[1]
            self.rect.centery = startingData[0]
            self.rot = 0
            self.bsize = 5
            self.last_update=0
        def update(self):
            self.playerData = gameData[0][self.playerNDX]
            print('playerData')
            print(self.playerData)
            print('playerData3')
            print(self.playerData[3])
            if self.playerData[3] == False:
                self.rect.centerx = self.playerData[0]
                self.rect.centery = self.playerData[1]
                now = pygame.time.get_ticks()
                if now - self.last_update > 50:
                    self.last_update = now
                    self.rot = self.playerData[2]
                    new_image = pygame.transform.rotate(self.image_orig, self.rot)
                    old_center = self.rect.center
                    self.image = new_image
                    self.rect = self.image.get_rect()
                    self.rect.center = old_center
            elif self.playerData[3] == True:
                self.image= pygame.transform.scale(player_imgs[4], (20, 20))

    class Bullet(pygame.sprite.Sprite):
        size = 3
        def __init__(self, bulletData):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((self.size,self.size))
            print('making bullet')
            self.image.fill(BLACK)
            self.rect = self.image.get_rect()
            self.rect.centery = bulletData[1]
            self.rect.centerx = bulletData[0]
            self.life = pygame.time.get_ticks()

        def update(self):
            if (pygame.time.get_ticks()-self.life >100):
                self.kill()
    class Object(pygame.sprite.Sprite):
        def __init__(self,x,y):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((10,10))
            self.image.fill(BLACK)
            self.rect = self.image.get_rect()
            print('fuck you')
            self.rect.centery = y
            self.rect.centerx  = x
            print(self.rect)
            print(self.image)
    serverSocket = networkc.serverConnect(serverIP)
    while True:
        print('restarting')
        gameData = networkc.recvSend('.',serverSocket)
        img_dir = path.join(path.dirname(__file__), 'img')
        WIDTH = 750
        HEIGHT = 750
        FPS = 40
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        RED = (255, 0, 0)
        GREEN = (0, 255, 0)
        BLUE = (0, 0, 255)
        pygame.init()
        pygame.mixer.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("ERMAGERDD! TANKZ!")
        clock = pygame.time.Clock()
        player_imgs = [pygame.image.load(path.join(img_dir,"tank.png")).convert(),pygame.image.load(path.join(img_dir,"tank2p.png")).convert(),pygame.image.load(path.join(img_dir,"tank3p.png")).convert(),pygame.image.load(path.join(img_dir,"tank4p.png")).convert(),pygame.image.load(path.join(img_dir,"tankDead.png")).convert()]
        all_sprites = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        walls = pygame.sprite.Group()  
        
        for x in range(len(gameData[0])):
            all_sprites.add(Player(player_imgs[x],gameData[0][x],x))
        
        for x in range(750):
            if x%10 == 0:
                print(x)
                all_sprites.add(Object(x,0)) 
                all_sprites.add(Object(0,x)) 
                all_sprites.add(Object(x,750)) 
                all_sprites.add(Object(750,x)) 
            if x%30 == 0:
                all_sprites.add(Object(x,x)) 
                all_sprites.add(Object(x+30,x)) 
                all_sprites.add(Object(x,x+30)) 
                all_sprites.add(Object(x+30,750-x))
                all_sprites.add(Object(x,750-x-30))
                all_sprites.add(Object(x,750-x))
        print(walls)
        # Game loop
        running = True
        input='.'
        previnput = '.'
        while running == True:
            # keep loop running at the right speed
            clock.tick(FPS)
            # Process input (events)
            for x in range(len(gameData[1])):
                all_sprites.add(Bullet(gameData[1][x]))
            events = pygame.event.get()
            print(events)
            for event in events:
                # check for closing window
                print(event.type)
                if event.type == pygame.QUIT:
                    running = False
                # Check for keypress, specifically Spacebar to fire
                elif event.type == pygame.KEYDOWN:
                    print('keystroke')
                    if event.key == pygame.K_SPACE:
                        previnput =input
                        input = ' '
                    elif event.key == pygame.K_a:
                        previnput =input
                        input = 'a'
                    elif event.key == pygame.K_d:
                        previnput =input
                        input = 'd'
                    elif event.key == pygame.K_w:
                        previnput =input
                        input = 'w'
                    elif event.key == pygame.K_s:
                        previnput =input
                        input = 's'
                elif event.type == pygame.KEYUP:
                    input = 'w'
            print(input)
            gameData = networkc.recvSend(input,serverSocket)
            # Update
            all_sprites.update()
            # Draw / render
            screen.fill(WHITE)
            all_sprites.draw(screen)
            # *after* drawing everything, flip the display
            pygame.display.flip()
            if gameData[2] == True:
                running = False

        pygame.quit()