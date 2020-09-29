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

ALPHA = (0, 0, 0)

pygame.init() #initialize pygame

fps = 60
fpsClock = pygame.time.Clock()

width, height = 640, 480
screen = pygame.display.set_mode((width, height))

main = True

scaling_factor = 64*2 #factor for scaling pixel art (by default displays tiny)


#for moving an enemy randomly
frame_count = 0 #used as a timer for enemy random movement
idle_time = 0
moving_time = 0
flip_enemy = False

#fps
font = pygame.font.SysFont("Arial", 18)


'''
Objects
'''
#ASSETS



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

    def update(self):
        #code to move enemy
        self.rect.x = self.rect.x
        self.rect.y = self.rect.y

        global frame_count
        global idle_time
        global moving_time

        '''print("frame count "+str(frame_count))
        print("idle_time "+str(idle_time))
        print("moving_time "+str(moving_time))
        print("\n\n\n\n\n\n\n\n")'''


        #idle some time until frame_count reaches idle_time
        if(frame_count<=idle_time):
            self.rect.x = self.rect.x
            #print("STOP")


        #move some time until we reach moving_time
        if(idle_time<=frame_count<=moving_time):
            if(flip_enemy==True):
                self.rect.x += -steps_enemy
                #print("<----")
            else:
                self.rect.x += steps_enemy
                #print("---->")



        #reset frame_count
        if(frame_count == moving_time):
            frame_count = -1

        #animation
        if ((slowdown%speed_factor)==0):    #idle
            if(idle_time<=frame_count<=moving_time):
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


        frame_count += 1 #to count for random movement on enemy




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

#SPAWN ENEMY

enemy = Enemy(width/2 ,height/2,"serpiente")
enemy_list = pygame.sprite.Group() #create group of enemies
enemy_list.add(enemy)
steps_enemy = 5


'''
Main Loop__________________________________________________________________________________
'''
# Game loop.
while main == True:
  screen.fill((0, 0, 0))

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

  # Draw.
  slowdown += 1 #slows down animation using %
  player.update()   #updates the character position


  if(frame_count==0):
      #move some time
      idle_time = random.randint(150,200)
      moving_time = random.randint(200,210)

  if((random.randint(1,100)%2)==0)and(frame_count==0):
      flip_enemy = True #we flip enemy randomly
      print("<==\n")
  else:
      if(frame_count==0):
            flip_enemy = False
            print("==>\n")



  enemy.update()


  screen.fill(BLACK)
  player_list.draw(screen) #drawn player
  enemy_list.draw(screen) #drawn enemy


  screen.blit(update_fps(), (10,0))


  pygame.display.flip()
  fpsClock.tick(fps)
