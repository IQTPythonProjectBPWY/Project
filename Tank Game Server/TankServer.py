
import math
import networks
from socket import *
import time

class Player():
    dead=False
    speeds = {'a':-4,'d':4,'w':3,'s':-3}
    def __init__(self,startingCoords):
        self.x =startingCoords[0]
        self.y=startingCoords[1]
        self.rot = startingCoords[2]
        self.lastshot = time.time()
    def rotate(self,input):
        self.rot = (self.rot-self.speeds[input])% 360
    def move(self,input):
        angle = math.radians(self.rot)
        move = 0
        print(self.x,self.y)
        for wall in walls:
            if (wall.x-6<(self.x + (self.speeds[input] * math.sin(angle)))<wall.x+6 and wall.y-6<(self.y+(self.speeds[input]*math.cos(angle)))<wall.y+6):
                move = 1
        if move == 0:
            self.x += (self.speeds[input] * math.sin(angle))
            self.y += (self.speeds[input] * math.cos(angle))
    def update(self,input):
        if self.dead == False:
            if input == 'a' or input =='d':
                self.rotate(input)
            elif input == 'w' or input == 's':
                self.move(input)
            elif input == ' ':
                if len(bullets) <= 32 and (time.time())-self.lastshot>2:
                    bullets.append(Bullet(self.x,self.y,self.rot))
                    self.lastshot = time.time()

class Bullet():
    x=0
    y=0
    vx=0
    vy=0
    dead=False
    def __init__(self,tankX,tankY,tankRot):
        angle = math.radians(tankRot)
        self.vx= 10 * math.sin(angle)
        self.vy= 10 * math.cos(angle)
        self.x= tankX + self.vx
        self.y= tankY + self.vy
    def update(self):
        self.x+= self.vx
        self.y+= self.vy

class Wall():
    x=0
    y=0
    def __init__(self,coords):
        self.x=coords[0] 
        self.y=coords[1]


players=[]
bullets=[]
walls=[]

def Server():
    print('enter number of players')
    numPlayers = input()
    print('Searching for clients')
    clients = networks.setupClients(int(numPlayers))
    print('Initiaizing walls')
    createWalls()
    print('walls initialized')
    while True:
        print('Initiaizing players')
        createPlayers(numPlayers)
        print('Players initialized')
        endgame= False
        while endgame == False:
            print('sendingdata')
            inputs= networks.sendRecv(buildPacket(endgame),clients)
            print(inputs)
            moveObjects(inputs)
            checkCollisions()
            endgame = checkVictory(int(numPlayers))
        inputs = networks.sendRecv(buildPacket(endgame),clients)
        global players
        global bullets
        players = []
        bullets = []


def createPlayers(numPlayers):
    startingCoords= ((20,20,45),(730,730,225),(20,730,135),(730,20,315))
    for x in range(int(numPlayers)):
        players.append(Player(startingCoords[x]))
        print(players[x])

def createWalls():
    for x in range(751):
        if x%10 == 0:
            print(x)
            walls.append(Wall((x,0))) 
            walls.append(Wall((0,x))) 
            walls.append(Wall((x,750))) 
            walls.append(Wall((750,x))) 
        if x%30 == 0:
            print(x)
            walls.append(Wall((x,x))) 
            walls.append(Wall((x+30,x))) 
            walls.append(Wall((x,x+30))) 
            walls.append(Wall((x,750-x))) 
            walls.append(Wall((x+30,750-x))) 
            walls.append(Wall((x,750-x-30))) 
    

def moveObjects(inputs):
    for x in range(len(players)):
        players[x].update(inputs[x])
    if bullets != None:
        for bullet in bullets:
            bullet.update()

def checkCollisions():
    for bullet in bullets:
        removed = 0
        for player in players:
            if player.x-10<bullet.x<player.x+10 and player.y-10<bullet.y<player.y+10:
                player.dead = True
                bullets.remove(bullet)
                removed = 1
        
        for wall in walls:
            if wall.x-6<bullet.x<wall.x+6 and wall.y-6<bullet.y<wall.y+6:
                if removed == 0:
                    bullets.remove(bullet)
                    removed = 1
        if bullet.x>750 or bullet.y>750 or bullet.x<0 or bullet.y<0:
            if removed == 0:
                    bullets.remove(bullet)
                    removed = 1

def checkVictory(numPlayers):
    numDead = 0
    for player in players:
        if player.dead == True:
            print('player dead')
            numDead+=1
    if numDead==numPlayers-1 and numDead>0:
        return True
    return False

def buildPacket(endgame):
    playerdata = []
    bulletdata = []
    for player in players:
        playerdata.append((player.x,player.y,player.rot,player.dead))
    for bullet in bullets:
        bulletdata.append((bullet.x,bullet.y))
    return [playerdata,bulletdata,endgame]
    
    
Server()
