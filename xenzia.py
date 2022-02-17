from dis import dis
from glob import glob
from logging import root
import math
import random
from re import X
from turtle import circle, position, width
import pygame
import tkinter as tk
from tkinter import W, messagebox 

class cube(object):
    rows = 20
    w = 500
    def __init__(self,start,dirnx=1,dirny=0,color=(255,0,0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self,dirnx,dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny) # change our position

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2,dis-2))
        if eyes:
            centre = dis // 2
            radius = 3
            circleMiddle = (i * dis + centre - radius, j * dis + 8)
            circleMiddle2 = (i * dis + dis - radius*2, j * dis + 8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)

class snake(object):
    body = []
    turns = {} 
    def __init__(self,color,pos):
        self.color = color
        self.head = cube(pos) # the head will be the front of the snake
        self.body.append(self.head) # add head which is a cube object to our body list

        # defining the direction the snake will move in
        self.dirnx = 0
        self.dirny = 1
        

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # check too see if the user hit red x
                pygame.quit() # close window if the user hit red x

            keys = pygame.key.get_pressed() # see which keys are being pressed
            for key in keys: #loop through all the keys
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

            
        for i, c in enumerate(self.body): # loop through every cube in our snake
            p = c.pos[:] # stores the cubes position on the grid
            if p in self.turns: # if the cubes direction is one where we turned
                turn = self.turns[p] # get the direction where we should turn
                c.move(turn[0],turn[1]) # move our cube in that direction
                if i == len(self.body)-1: # if this is the last cube in our body, 
                    self.turns.pop(p) # remove the turn from the dict

            else: # if we are not turning the cube
                if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1]) # if we are moving left and the position the cube reaches 0 or less than 0 then the cube is taken to the opposite side. the y position does not change
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0], c.rows-1)
                else: c.move(c.dirnx, c.dirny) # if the cube has not reached the edge then just keep moving

    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        # we need to know which side of the snake to add the cube to
        # so we check which direction we are currently moving in to determine if 
        # we need to add the cube to the left or right, above or  below

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))

        # we then set the cubes direction to the direction of the snake
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy    


    def draw(self, surface):
        for i, c in enumerate(self.body): #loop through the cubes 
            if i == 0: # for the first cube
                c.draw(surface, True) # we will draw eyes as told by the True
            else:
                c.draw(surface) # otherwise just draw a cube

def drawGrid(w, rows, surface):
    sizeBtwn = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (255, 255, 255), (x,0),(x,w))
        pygame.draw.line(surface, (255, 255, 255), (0,y),(w,y))

def redrawWindow(surface):
    global rows, width, s, snack
    surface.fill((0,0,0)) # fills the screen with black
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface) # draws our grid lines
    pygame.display.update() #will refresh the screen

def randomSnack(rows, item):
    positions = item.body # get all positions of cubes in our snake

    while True: #keep generating random positions until we get a valid one
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0: # this checks if the positions generated are occupied by the snake
            continue
        else:
            break
    return (x,y)

def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

def main():
    global width, rows, s, snack
    width = 500
    rows = 20 # if the rows are 20, then the number of cubes will be 19
    win = pygame.display.set_mode((width, width)) # this line create our screen object
    s = snake((255,0,0), (10,10)) # create a snake object
    snack = cube(randomSnack(rows, s), color=(0,255,0))
    flag = True
    
    clock = pygame.time.Clock() # creates our clock object 
    # start of the main loop
    while flag:
        pygame.time.delay(50) # refresh game so it doesnt run too fast, the lower this is the faster the snake will be 
        clock.tick(10) # the lower this is the slower the snake will be
        s.move()
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows, s), color=(0,255,0))

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                print('Score: ', len(s.body))
                message_box('You Lose!!', 'Plays again?')
                s.reset((10,10))
                break

        redrawWindow(win) # will refresh screen



main()