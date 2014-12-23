#!usr/bin/env python
# -*- coding:utf-8 -*-
# final.py

import pygame
from pygame.locals import *
import random , sys , socket

FPS = 10
CELLSIZE = 10
CELLWIDTH = int(640/10)
CELLHEIGHT = int(480/10)

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (0,255,255)
YANSE = (255,255,0)
DARKGRAY = (40,40,40)

HOST = "127.0.0.1"
PORT = 8889

colorlist = [RED,GREEN,BLUE,YELLOW,YANSE]
snakelist = []
applelist = []


class Game:
    def __init__(self,total,Iam):
        self.total = total
        self.Iam = Iam
        pygame.init()
        self.FPSCLOCK = pygame.time.Clock()
        self.DISPLAYSURF = pygame.display.set_mode((640,480))
        pygame.display.set_caption('game')

        ##debug
        print(total,Iam)
        
    def load(self):
        for i in range(0,self.total):
            snakelist.append(Snake(colorlist[i],25,20,"left"))
    def drawGrid(self,DISPLAYSURF):
        for x in range(0,640,CELLSIZE):
            pygame.draw.line(DISPLAYSURF,DARKGRAY,(x,0),(x,480))
        for y in range(0,480,CELLSIZE):
            pygame.draw.line(DISPLAYSURF,DARKGRAY,(0,y),(640,y))

    def draw(self):
        self.DISPLAYSURF.fill(BLACK)
        self.drawGrid(self.DISPLAYSURF)
        for snake in snakelist:
            snake.draw(self.DISPLAYSURF)
        for apple in applelist:
            apple.draw(self.DISPLAYSURF)
        pygame.display.update()
        self.FPSCLOCK.tick(FPS)
        
    def run(self,recvlist,host,port):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    Iam = self.Iam
                    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                    try:
                        s.connect((host,port))
                    except:
                        print("Connect Failed")
                        pygame.quit()
                        sys.exit()
                    if event.key==K_LEFT or event.key==K_a:
                        #snakelist[Iam].direction = "left"
                        s.send(str(self.Iam)+"l")
                        s.close()
                    elif event.key==K_RIGHT or event.key==K_d:
                        #snakelist[Iam].direction = "right"
                        s.send(str(self.Iam)+"r")
                        s.close()
                    elif event.key==K_UP or event.key==K_w:
                        #snakelist[Iam].direction = "up"
                        s.send(str(self.Iam)+"u")
                        s.close()
                    elif event.key==K_DOWN or event.key==K_s:
                        #snakelist[Iam].direction = "down"
                        s.send(str(self.Iam)+"d")
                        s.close()
                    elif event.key==K_ESCAPE:
                        s.close()
                        pygame.quit()
                        sys.exit()
                    else:
                        s.close()
            if not applelist:
                s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                s.connect((host,port))
                s.send("@")
                s.close()
            for data in recvlist:
                if data[0]>='0' and data[0]<='9':
                    snakelist[int(data[0])].change(data[1])
                else:
                    applelist.append(Apple(data))
                recvlist.remove(data)
            for eachsnake in snakelist:
                eachsnake.move(host,port)
            self.draw()
        
class Snake:
    def __init__ ( self , color , startx , starty , direction ):
        self.color = color
        self.startx = startx
        self.starty = starty
        self.direction = direction
        self.coords = [{'x':startx,'y':starty}]
        if direction == 'right':
            for i in range(1,4):
                self.coords.append({'x':startx-i,'y':starty})
        elif direction == 'left':
            for i in range(1,4):
                self.coords.append({'x':startx+i,'y':starty})
        elif direction == 'up':
            for i in range(1,4):
                self.coords.append({'x':startx,'y':starty-i})
        elif direction == 'down':
            for i in range(1,4):
                self.coords.append({'x':startx,'y':starty+i})

    def change(self,op):
        if op=='l':
            self.direction = "left"
        elif op=='r':
            self.direction = "right"
        elif op=='u':
            self.direction = "up"
        elif op=='d':
            self.direction = "down"

    def move( self , host , port ):
        flag = 0
        for apple in applelist:
            if self.coords[0]['x']==apple.x and self.coords[0]['y']==apple.y:
                applelist.remove(apple)
                s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                s.connect((host,port))
                s.send("@")
                s.close()
                flag = 1
                break
        if flag==0:
            del self.coords[-1]

        if self.direction == 'up':
            self.newhead = {'x':self.coords[0]['x'],'y':self.coords[0]['y']-1}
        elif self.direction == 'down':
            self.newhead = {'x':self.coords[0]['x'],'y':self.coords[0]['y']+1}
        elif self.direction == 'left':
            self.newhead = {'x':self.coords[0]['x']-1,'y':self.coords[0]['y']}
        elif self.direction == 'right':
            self.newhead = {'x':self.coords[0]['x']+1,'y':self.coords[0]['y']}
            
        self.coords.insert(0,self.newhead)

    def draw (self,DISPLAYSURF):
        for coord in self.coords:
            x = coord['x'] * CELLSIZE
            y = coord['y'] * CELLSIZE
            segmentrect = pygame.Rect(x,y,CELLSIZE,CELLSIZE)
            pygame.draw.rect(DISPLAYSURF,self.color,segmentrect)

class Apple:
    def __init__(self,data):
        l = data.split(',')
        s = l[0]
        x = int(s[1:])
        s = l[1]
        y = int(s)
        self.x = x
        self.y = y
    def draw(self,DISPLAYSURF):
        x = self.x * CELLSIZE
        y = self.y * CELLSIZE
        appleRect = pygame.Rect(x,y,CELLSIZE,CELLSIZE)
        pygame.draw.rect(DISPLAYSURF,WHITE,appleRect)
