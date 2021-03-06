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
RED = (255,0,0)
GREEN = (0,255,0)
BLUE  = (25,25,200)
BLACK = (23,23,23 )
WHITE = (254,254,254)

ALPHA = (0, 0, 0)   #for sprite transparency
PINK = (253, 0, 171)

pygame.init() #initialize pygame

fps = 60
fpsClock = pygame.time.Clock()

width, height = 640, 360
screen = pygame.display.set_mode((width, height))  #this is the screen itself
pygame.display.set_caption("My game, by Gines Diaz")

main_surface = pygame.Surface((width,height))      #this is the area of the screen we are drawing
main_surface_rect = main_surface.get_rect()


scaling_factor = 128 #factor for scaling pixel art (by default displays tiny)



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
        self.frame = 0       #for sprite animation
        self.frame_count = 0 #for slowing down taking damage

        self.facing_direction = True

        self.health = 10


        for i in range(1,5):

            img = pygame.image.load(os.path.join('images','sacha'+str(i)+'.png')).convert()
            img = pygame.transform.scale(img, (scaling_factor, scaling_factor)) #scaling sprite
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
        self.frame_count += 1

        global width
        global scrolling
        right_margin = width-120
        left_margin = -right_margin+width-120
        #stop at the edge (for scrolling animation)
        if(self.rect.x >= right_margin) and (self.movex>0) or (self.rect.x <= left_margin) and (self.movex<0):
            self.rect.x = self.rect.x #stop if the vector and position is incorrect
            self.rect.y = self.rect.y + self.movey
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
            self.facing_direction = True

        #moving right (frames 1,2)
        if self.movex > 0 and ((slowdown%speed_factor)==0):

            self.index += 1
            if self.index > 2:
                self.index = 0
            self.image = self.images[self.index]
            self.image = pygame.transform.flip(self.image,True,False)  #vertically mirror
            self.facing_direction = False


        #IDLE (not moving, frames 3,4)

        if self.movex == 0 and (slowdown%speed_factor==0):

            self.index += 1
            if self.index > 3:
                self.index = 2
            self.image = self.images[self.index]

            if self.facing_direction == False:
                self.image = pygame.transform.flip(self.image,True,False)  #vertically mirror

        #collision for HEATLH
        hit_list = pygame.sprite.spritecollide(self,enemy_list,False)
        for enemy in hit_list:
            if self.frame_count > 30:
                self.health -= 3        #difficulty (1 easiest, 10 difficult)
                print(self.health)
                self.frame_count = 0




    def position(self):
        position_x = self.rect.x
        position_y = self.rect.y
        position = [position_x,position_y]
        return position

    def velocity(self):
        velocity_x = self.move.x
        velocity_y = self.move.y
        velocity = [velocity_x,velocity_y]
        return velocity

    def gravity(self):
        self.movey += 0.8 #falling speed

        if self.rect.colliderect(ground) and self.movey > 0:
            #print("collision")
            self.movey = 0
            global jump_counter
            jump_counter = 0


class Enemy(pygame.sprite.Sprite):

    def __init__(self,x,y,img):

        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.move_x = 0
        self.idle_time = 0            #time the sprite will be idle
        self.moving_time = 0          #time the sprite will be moving
        self.flip_enemy = False
        self.frame_count = 0          #timing for moving randomly the enemy

        #gravity
        self.movey = 0



        for i in range(0,2):

            img_enemy = pygame.image.load(os.path.join('images',str(img)+str(i)+'.png')).convert()
            img_enemy = pygame.transform.scale(img_enemy, (scaling_factor-40, scaling_factor-40)) #scaling sprite
            img_enemy.convert_alpha()
            img_enemy.set_colorkey(ALPHA)


            self.images.append(img_enemy)


        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()

        self.rect.width = self.rect.width/2

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
        self.rect.y += self.movey

        if(self.frame_count==0):
            self.moving_time = random.randint(10,50)
            self.idle_time = random.randint(50,200)
            '''print("frame count "+str(self.frame_count))
            print("idle_time "+str(self.idle_time))
            print("moving_time "+str(self.moving_time))'''
            #print("\n\n\n")

            if((random.randint(1,100)%2)==0):
                self.flip_enemy = True #we flip enemy randomly
                #print("<==\n")
            else:
                if(self.frame_count==0):
                    self.flip_enemy = False
                    #print("==>\n")

        '''print("frame count "+str(frame_count))
        print("idle_time "+str(idle_time))
        print("moving_time "+str(moving_time))
        print("\n\n\n")'''


        #idle some time until frame_count reaches idle_time
        if(self.frame_count<=self.moving_time):
            if(self.flip_enemy==True):
                self.rect.x += -steps_enemy

                #prevent snake from going outside
                if(self.rect.x < 0):
                    self.rect.x = -self.rect.x
                if(self.rect.x > 500):
                    self.rect.x = self.rect.x
                #print("<----")
            else:
                self.rect.x += steps_enemy
                #print("---->")



        #move some time until we reach moving_time
        if(self.moving_time<=self.frame_count<=self.idle_time):
            self.rect.x = self.rect.x
            #print("STOP")




        #reset frame_count
        if(self.frame_count == self.idle_time):
            self.frame_count = -1

        #animation
        if ((slowdown%speed_factor)==0):    #making animation slower
            if(self.frame_count<=self.frame_count<=self.moving_time):
                self.index += 1
                if self.index  > 1:
                    self.index = 0
                self.image = self.images[self.index]
                if(self.flip_enemy==True):
                    self.image = pygame.transform.flip(self.image,True,False)  #vertically mirror
            else:
                self.image = self.images[0]
                if(self.flip_enemy==True):
                    self.image = pygame.transform.flip(self.image,True,False)  #vertically mirror

        self.frame_count += 1

        #checking if the enemy is outside of the screen
        global main_surface_rect
        if not main_surface_rect.contains(self.rect):
            self.kill()

    def gravity(self):
        self.movey += 0.3 #how far the enemy falls

        if self.rect.colliderect(ground) and self.movey > 0:
            self.movey = 0

class Background(pygame.sprite.Sprite):
    def __init__(self,bk_img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('images',bk_img+'.png'))
        self.image.convert()
        global width,height
        self.image = pygame.transform.scale(self.image,(width,height))
        self.rect = self.image.get_rect()


class Particles(pygame.sprite.Sprite):
    def __init__(self,image,frames,x,y):    #frames = number of images || number of times to repeat animation
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.frames = frames


        for i in range(0,self.frames):

            img = pygame.image.load(os.path.join('images',str(image)+str(i)+'.png'))
            img = pygame.transform.scale(img, (scaling_factor-30, scaling_factor-30)) #scaling sprite
            #set black as transparent backround
            img.convert()
            img.convert_alpha()
            img.set_colorkey(PINK)
            self.images.append(img)

        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()

        #adjusting hitbox fart
        self.rect.width = self.rect.width/2

        self.rect.x = 0
        self.rect.y = 0


    def update(self,jumping1):  #iterations is the number of times to repear animation

        if ((slowdown%speed_factor))==0 and (jumping1==True):
            self.index += 1
            if self.index > self.frames-1 :
                self.index = 0
                global jumping
                jumping = False
            self.image = self.images[self.index]

    def update_jump_particle_position(self,x,y):
            if jumping != True:
                self.rect.x = x
                self.rect.y = y

    def is_collided_with(self,sprite):
        return self.rect.colliderect(sprite.rect)

    def sprite_is_displaying(self): #true if animation is displaying
        if self.image != self.images[0]:
            return True
        else:
            return False

class Platform(pygame.sprite.Sprite):
    def __init__(self,x,y,w,h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w,h))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Hearts(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.frames = 13 #from 1-13

        for i in range(0,self.frames):
            a = str(0)+str(i) if (i<10) else str(i)
            img = pygame.image.load(os.path.join('images','hearts'+a+'.png'))
            global width,height
            img = pygame.transform.scale(img, (width-130,height-100)) #scaling sprite

            if(i == 12): #scaling end game screen
                img = pygame.transform.scale(img, (width,height)) #scaling sprite
                
            #set black as transparent backround
            img.convert()
            img.convert_alpha()
            img.set_colorkey(ALPHA)
            self.images.append(img)

        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()

    def display_hearts(self,hearts_left): #n from 12 to 0
            for i in range(0,self.frames):
                if(i == hearts_left):
                    self.image = self.images[i]


'''
Add class to world
'''
#PLATFORM
platform_list = pygame.sprite.Group()
ground = Platform(-300,300,width+300,height-300) #(x_pos,y_pos,x_dimension,y_Dimension)
platform_list.add(ground)

#BACKGROUND
background = Background("topera_background")
background_list = pygame.sprite.Group()
background_list.add(background)

#Particles
jumping = False
doublejumpparticles = Particles("doublejumpparticles",7,20,20)
particles_list = pygame.sprite.Group()
particles_list.add(doublejumpparticles)



#SPAWN Player
player = Player() #we spawn the Player
#POSITION
player.rect.x = width/2 #go to x
player.rect.y = height/7 #go to y
player_list = pygame.sprite.Group()
player_list.add(player)
steps = 10 #pixels to move character
jump = 12
max_jumps = 2 #how many consecutive jumps can you make
jump_counter = 0
slowdown = 0 #slowdown animation with speed_factor (DO NOT TOUCH)
speed_factor = 6 #touch this to increase/Decrease animation speed
facing_direction = False
scrolling = "neutral"   #"left" "right" "neutral"

#SPAWN ENEMY (snake)
steps_enemy = 5

enemies = []  #list of enemies

for i in range(0,2):
    enemies.append(Enemy(width/4 ,height/4,"serpiente"))
    enemies.append(Enemy(width/4,height/4,"serpiente_roja"))

enemy_list = pygame.sprite.Group()
enemy_list.add(enemies)


#GUI hearts
hearts = Hearts()
hearts_list = pygame.sprite.Group()
hearts_list.add(hearts)

#screen shake
screenshake = 0

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
            print ("key left")
            player.control(-steps,0)
        if event.key == pygame.K_RIGHT or event.key == ord('d'):
            #move right
            print ("key right")
            player.control(steps,0)
        if event.key == pygame.K_UP or event.key == ord('w'):
            #move up
            print ("key up")
            if(jump_counter < max_jumps):
                player.control(0,-jump - player.movey-1.2) #susbtract -player.movey for 2nd jump realistic
                jump_counter += 1
                if jump_counter == 2 :
                    jumping = True


    if event.type == pygame.KEYUP:

        if event.key == pygame.K_LEFT or event.key == ord('a'):
            #move left
            print ("release key left")
            player.control(steps,0)
        if event.key == pygame.K_RIGHT or event.key == ord('d'):
            #move right
            print ("release key right")
            player.control(-steps,0)

        if event.key == pygame.K_UP or event.key == ord('w'):
            #move up
            print ("release key up")



  # Update.
  slowdown += 1 #slows down animation using %
  player.gravity()
  player.update()   #updates the character position

  #particle effect
  doublejumpparticles.update(jumping)
  doublejumpparticles.update_jump_particle_position(player.position()[0],player.position()[1]+110)

  for obj in enemies:
      obj.gravity()
      obj.update()

  # draw
  main_surface.fill(BLACK)
  background_list.draw(main_surface)

  #hitboxes
  #pygame.draw.rect(main_surface,BLUE,(doublejumpparticles.rect.x,doublejumpparticles.rect.x,doublejumpparticles.rect.width,doublejumpparticles.rect.height))
  #pygame.draw.rect(main_surface,BLUE,(enemies[0].rect.x,enemies[0].rect.y,enemies[0].rect.width,enemies[0].rect.height))
  #pygame.draw.rect(main_surface,RED,(player.rect.x,player.rect.y,player.rect.width,player.rect.height)) #show player hitbox
  player_list.draw(main_surface) #draw player
  enemy_list.draw(main_surface) #draw enemy

  particles_list.draw(main_surface)

  for i in range(0,4):
      if doublejumpparticles.is_collided_with(enemies[i]) and doublejumpparticles.sprite_is_displaying():
          enemies[i].kill()


  #platform_list.draw(main_surface)
  #Show changes and drawings

  #hearts
  hearts.display_hearts(-player.health+10)
  hearts_list.draw(main_surface)

  #screen shake pygame.sprite.spritecollide(self,enemy_list,False)
  if pygame.sprite.spritecollide(player,enemy_list,False):
      screenshake = 30

  if screenshake > 0:
      screenshake -= 1

  render_offset = [0,0]

  if screenshake:
      render_offset[0] = random.randint(0,8) - 4
      render_offset[1] = random.randint(0,8) - 4


  main_surface.blit(update_fps(), (10,0))
  screen.blit(main_surface,render_offset)           #draw the main surface on th screen

  pygame.display.flip() #show changes in screen
  fpsClock.tick(fps)
