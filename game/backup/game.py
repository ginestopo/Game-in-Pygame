#Author: Gines Diaz. All rights reserved.

#https://opensource.com/article/19/11/simulate-gravity-python
#https://opensource.com/article/17/12/game-framework-python
import sys
import os
import pygame
from pygame.locals import *
import random



'''
Setup
'''
BLUE  = (25,25,200)
BLACK = (23,23,23 )
WHITE = (254,254,254)

ALPHA = (0, 0, 0)   #for sprite transparency

pygame.init() #initialize pygame

fps = 60
fpsClock = pygame.time.Clock()

width, height = 640, 360
screen = pygame.display.set_mode((width, height))  #this is the screen itself
pygame.display.set_caption("My game, by Gines Diaz")

main_surface = pygame.Surface((width,height))      #this is the area of the screen we are drawing



scaling_factor = 128 #factor for scaling pixel art (by default displays tiny)

#for moving an enemy randomly
frame_count = 0 #used as a timer for enemy random movement (or global purpose)
idle_time = 0
moving_time = 0
flip_enemy = False

#fps
font = pygame.font.SysFont("Arial", 18)

'''
Class
'''

#for showing fps
def update_fps():
    fps = str(int(fpsClock.get_fps()))
    fps_text = font.render(fps, 1, pygame.Color("coral"))
    return fps_text

class Player(pygame.sprite.Sprite):
    """Spawn a player"""


    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = []

        #variables for moving the character
        self.movex = 0
        self.movey = 0
        self.frame = 0

        self.facing_direction = True


        for i in range(1,5):

            img = pygame.image.load(os.path.join('images','sacha'+str(i)+'.png')).convert()

            #set black as transparent backround
            img.convert_alpha()
            img.set_colorkey(ALPHA)

            self.images.append(img)


        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()

    def control(self,x,y): #function to control the character
        self.movex += x
        self.movey += y



    def update(self):
        global width
        global scrolling
        right_margin = width-120
        left_margin = -right_margin+width-120
        #stop at the edge (for scrolling animation)
        if(self.rect.x >= right_margin) and (self.movex>0) or (self.rect.x <= left_margin) and (self.movex<0):
            self.rect.x = self.rect.x #stop if the vector and position is incorrect
            if(self.rect.x >= right_margin):
                scrolling = "right"
                print(scrolling)
            if(self.rect.x <= left_margin):
                scrolling = "left"
                print(scrolling)
        else:
            self.rect.x = self.rect.x + self.movex
            self.rect.y = self.rect.y + self.movey

        #animation



        #moving left (frames 1,2)
        if self.movex < 0 and ((slowdown%speed_factor)==0):
            self.index += 1
            if self.index  > 2:
                self.index = 0
            self.image = self.images[self.index]
            self.image = pygame.transform.scale(self.image, (scaling_factor, scaling_factor)) #scaling the sprite

            self.facing_direction = True

        #moving right (frames 1,2)
        if self.movex > 0 and ((slowdown%speed_factor)==0):

            self.index += 1
            if self.index > 2:
                self.index = 0
            self.image = self.images[self.index]
            self.image = pygame.transform.scale(self.image, (scaling_factor,scaling_factor)) #scaling the sprite

            self.image = pygame.transform.flip(self.image,True,False)  #vertically mirror
            self.facing_direction = False


        #IDLE (not moving, frames 3,4)

        if self.movex == 0 and (slowdown%speed_factor==0):

            self.index += 1
            if self.index > 3:
                self.index = 2
            self.image = self.images[self.index]
            self.image = pygame.transform.scale(self.image, (scaling_factor, scaling_factor)) #scaling the sprite

            if self.facing_direction == False:
                self.image = pygame.transform.flip(self.image,True,False)  #vertically mirror

    def position(self):
        position_x = self.rect.x
        position_y = self.rect.y
        position = [position_x,position_y]
        return position

class Enemy(pygame.sprite.Sprite):

    def __init__(self,x,y,img):

        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.move_x = 0




        for i in range(0,2):

            img_enemy = pygame.image.load(os.path.join('images',str(img)+str(i)+'.png')).convert()
            img_enemy.convert_alpha()
            img_enemy.set_colorkey(ALPHA)

            self.images.append(img_enemy)


        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

    def position(self):
        position_x = self.rect.x
        position_y = self.rect.y
        position = [position_x,position_y]
        return position

    def update(self):
        #code to move enemy
        #self.rect.x = self.rect.x
        #self.rect.y = self.rect.y

        global frame_count
        global idle_time
        global moving_time
        global flip_enemy

        if(frame_count==0):
            moving_time = random.randint(10,50)
            idle_time = random.randint(50,360)
            '''print("frame count "+str(frame_count))
            print("idle_time "+str(idle_time))
            print("moving_time "+str(moving_time))'''
            #print("\n\n\n")

        if((random.randint(1,100)%2)==0)and(frame_count==0):
            flip_enemy = True #we flip enemy randomly
            #print("<==\n")
        else:
          if(frame_count==0):
                flip_enemy = False
                #print("==>\n")

        '''print("frame count "+str(frame_count))
        print("idle_time "+str(idle_time))
        print("moving_time "+str(moving_time))
        print("\n\n\n")'''


        #idle some time until frame_count reaches idle_time
        if(frame_count<=moving_time):
            if(flip_enemy==True):
                self.rect.x += -steps_enemy
                #print("<----")
            else:
                self.rect.x += steps_enemy
                #print("---->")



        #move some time until we reach moving_time
        if(moving_time<=frame_count<=idle_time):
            self.rect.x = self.rect.x
            #print("STOP")




        #reset frame_count
        if(frame_count == idle_time):
            frame_count = -1

        #animation
        if ((slowdown%speed_factor)==0):    #making animation slower
            if(frame_count<=frame_count<=moving_time):
                self.index += 1
                if self.index  > 1:
                    self.index = 0
                self.image = self.images[self.index]
                self.image = pygame.transform.scale(self.image, (scaling_factor, scaling_factor)) #scaling the sprite
                if(flip_enemy==True):
                    self.image = pygame.transform.flip(self.image,True,False)  #vertically mirror
            else:
                self.image = self.images[0]
                self.image = pygame.transform.scale(self.image, (scaling_factor, scaling_factor)) #scaling the sprite
                if(flip_enemy==True):
                    self.image = pygame.transform.flip(self.image,True,False)  #vertically mirror

class Background(pygame.sprite.Sprite):
    def __init__(self,bk_img):
        self.image = pygame.image.load()
        self.image.convert()
        #seguir...
'''
Add class to world
'''
#SPAWN Player
player = Player() #we spawn the Player
#POSITION
player.rect.x = width/2 #go to x
player.rect.y = height/2 #go to y
player_list = pygame.sprite.Group()
player_list.add(player)
steps = 10 #pixels to move character
slowdown = 0 #slowdown animation with speed_factor (DO NOT TOUCH)
speed_factor = 6 #touch this to increase/Decrease animation speed
facing_direction = False
scrolling = "neutral"   #"left" "right" "neutral"

#SPAWN ENEMY (snake)

enemy = Enemy(width/2 ,height/2,"serpiente")
enemy_list = pygame.sprite.Group() #create group of enemies
enemy_list.add(enemy)
steps_enemy = 5


# add backround
background = pygame.image.load(os.path.join('images','topera_background.png')).convert()
background = pygame.transform.scale(background,(width,height))



'''
Main Loop__________________________________________________________________________________
'''

main = True

# Game loop.
while main == True:
  screen.fill(BLACK)

  for event in pygame.event.get():

    #QUIT
    if event.type == QUIT:
      pygame.quit()
      sys.exit()
      main = False

    #KEYDOWN
    if event.type == pygame.KEYDOWN:
        if event.key == ord('q'):
            pygame.quit()
            sys.exit()
            main = False

        if event.key == pygame.K_LEFT or event.key == ord('a'):
            #move left
            print "key left"
            player.control(-steps,0)
        if event.key == pygame.K_RIGHT or event.key == ord('d'):
            #move right
            print "key right"
            player.control(steps,0)
        if event.key == pygame.K_UP or event.key == ord('w'):
            #move up
            print "key up"

    if event.type == pygame.KEYUP:

        if event.key == pygame.K_LEFT or event.key == ord('a'):
            #move left
            print "release key left"
            player.control(steps,0)
        if event.key == pygame.K_RIGHT or event.key == ord('d'):
            #move right
            print "release key right"
            player.control(-steps,0)

        if event.key == pygame.K_UP or event.key == ord('w'):
            #move up
            print "release key up"


  # Update.
  slowdown += 1 #slows down animation using %
  player.update()   #updates the character position


  enemy.update()
  frame_count += 1 #to count for random movement on enemy


  # draw
  main_surface.fill(BLACK)
  main_surface.blit(background,(0,0))

  player_list.draw(main_surface) #draw player
  enemy_list.draw(main_surface) #draw enemy


  #Show changes and drawings
  main_surface.blit(update_fps(), (10,0))
  screen.blit(main_surface,(0,0))           #draw the main surface on th screen

  pygame.display.flip() #show changes in screen
  fpsClock.tick(fps)
