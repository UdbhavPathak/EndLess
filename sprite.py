import random
import pygame
import animation
pygame.init()

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,size,type):
        super().__init__()
        self.rect = pygame.Rect(*pos,size,size)
        self.gid = 1
        self.grassimage = pygame.transform.flip(pygame.image.load(f"images/tile/grass.png"),
        random.choice((False,True)),False).convert_alpha()
        self.tileimage = pygame.image.load("images/tile/block.png").convert_alpha()
        self.grassx = random.randint(0,100)#random.choice((0,30,80))

        self.vel = 5
        self.type = type
        self.init_pos = [*pos]

    def show(self,win):
        if self.type == "grass":
            pos = (self.rect.x,self.rect.y-25)
            pygame.draw.rect(win,(0,0,0),self.rect)
            win.blit(self.grassimage,pos,(self.grassx,0,50,self.grassimage.get_height()))
            # pygame.draw.line(win,(30,30,30),self.rect.bottomleft,self.rect.bottomright,2)
            win.blit(self.tileimage,(self.rect.x-2,self.rect.y-2))

        else:
            pygame.draw.rect(win,(0,0,0),self.rect)
    def move(self):
        if not self.type == "ground":
            self.rect.x -= self.vel

class Grass:
    def __init__(self,width,velocity,pos):
        self.screenwidth = width
        self.img = pygame.image.load("images/tile/grass.png").convert_alpha()
        self.vel = velocity
        self.pos = pos
        self.id = 0

    def show(self,win):
        win.blit(self.img,self.pos)

    def move(self,n):
        if self.pos[0] < -self.img.get_width():
            self.pos[0] += n*175-self.vel
        else:
            self.pos[0] -= self.vel




class Player(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.rect = pygame.Rect(*pos,50,80)
        self.movement = [0,0]
        self.state = "ready"
        self.gravity = 0.75
        self.imgs = list(map(lambda x:f"images/player/run/{x}.png",range(1,11)))
        self.animation = animation.Animation(images=self.imgs,rate = 2,timmer=12,zoom=[False,0],flip=
                                             [False,False,False],rect = self.rect)

        self.jump_img = pygame.image.load("images/player/run/11.png").convert_alpha()

        self.animation.centralize = True
        self.dirtburst = animation.DirtBurst((self.rect.x,self.rect.right),self.rect.bottom)
        self.darkaura = animation.Aura([(0,0,0),(50,50,50)],[1,6],20,*self.rect.center)
        self.dash = False

        self.dasheffect = animation.DashEffect(*self.rect.midtop,50)




    def show(self,win):
        self.darkaura.x,self.darkaura.y = self.rect.midbottom
        self.darkaura.add()

        self.dirtburst.show(win)
        if self.state == "ready" and not self.dash:
            self.animation.show(win,center = self.rect.center)
        elif self.state != "ready" or self.dash :
            r = self.jump_img.get_rect(center = self.rect.center)
            win.blit(self.jump_img,r)

        self.dasheffect.show(win)

        # self.darkaura.show(win)


    def jump(self):
        if self.state == "ready":
            self.movement[1] = -17.5
            self.state = "air"


    def collision_test(self,tiles):
        hitlist = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                hitlist.append(tile)
        return hitlist
    def move(self,tiles,ramps):
        collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
        self.rect.y += self.movement[1]
        if self.movement[1] > 0:
            self.state = 'air'

        self.movement[1] += self.gravity

        hit_list = self.collision_test(tiles)
        for tile in hit_list:
            if self.movement[1] > 0:
                if self.rect.top < tile.rect.top and self.rect.bottom < tile.rect.bottom:
                    if tile.type != "L" or tile.type != "R":
                        self.rect.bottom = tile.rect.top
                        collision_types['bottom'] = True
            elif self.movement[1] < 0:
                if not self.rect.bottom < tile.rect.bottom+self.rect.h//2:
                    self.rect.top = tile.rect.bottom
                    collision_types['top'] = True
        # hit_list =  self.collision_test(tiles)
        # ramps = [i for i in hit_list if i.type == "L" or i.type == "R"]
        for ramp in ramps:
            if self.rect.colliderect(ramp.rect):
                rel_x = self.rect.x - ramp.rect.x
                if ramp.type == "L":
                    pos_height = rel_x + self.rect.width  # go by player right edge on right ramps
                elif ramp.type == "R":
                    pos_height = 50 - rel_x  # is already left edge by default

                # add constraints
                pos_height = min(pos_height, 50)
                pos_height = max(pos_height, 0)

                target_y = ramp.rect.bottom - pos_height
                if self.rect.bottom > target_y:  # check if the player collided with the actual ramp
                    # adjust player height
                    self.rect.bottom = target_y
                    collision_types['bottom'] = True


        self.dasheffect.set(*self.rect.midright)
        if self.dash:
            for i in range(2):
                self.dasheffect.add()

        return collision_types



class Ramps:
    def __init__(self,x,y,type):
        self.rect = pygame.Rect(x,y,50,50)
        self.type = type
        self.color = (0,0,0)
        if self.type == "L":
            self.heading = "left"
        else:self.heading  = "right"
        self.vel = 0
        self.init_pos = [x,y]


    def show(self,win):
        if self.heading == "left":
            points = [self.rect.bottomleft,self.rect.bottomright,self.rect.topright]
            pygame.draw.polygon(win,self.color,points)
            # pygame.draw.polygon(win,(255,255,255),points,1)

        elif self.heading == "right":
            points = [self.rect.bottomright,self.rect.bottomleft,self.rect.topleft]
            pygame.draw.polygon(win,self.color,points)
            # pygame.draw.polygon(win,(255,255,255),points,1)

    def move(self):
        self.rect.x -= self.vel



class Obstacle(Tile):
    def __init__(self,pos,size,type):
        super().__init__(pos,size,type)
        # self.type = "obstacle"
        self.tileimage = pygame.image.load("images/obstacle/spike2.png").convert_alpha()


    def show(self,win):
        win.blit(self.tileimage,self.rect)


class Bat(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.movement = [0,0]
        self.x_vel = -3
        self.y_vel_timmer = [0,10]
        self.y_vel_range = (-1,2)
        imgs = list(map(lambda x: f"images/bat/{x}.png", range(0, 6)))
        self.animation = animation.Animation(images=imgs, rate=2, timmer=4, zoom=(True, 0.2),
                                             flip=(False, False, False),
                                             rect=pygame.Rect(0,0,0,0)
                                             , colorkey=(255, 255, 255))

        self.rect = pygame.Rect(*pos,self.animation.images[0].get_height(),
                                self.animation.images[0].get_height())
        self.animation.centralize = True
        self.animation.rect = self.rect






    def show(self,win):
        self.animation.show(win,center=self.rect.center)

    def move(self,world_vel):
        self.movement[0] = self.x_vel-world_vel
        self.rect.x += self.movement[0]




        if self.rect.right < -200:
            self.rect.right = 2000
            self.rect.top = random.randint(10,300)

        self.rect.y += self.movement[1]

        if self.y_vel_timmer[0] > self.y_vel_timmer[1]:
            self.y_vel_timmer[0] = 0
            self.movement[1] = random.randint(*self.y_vel_range)
        else:
            self.y_vel_timmer[0] += 1

class DeadMan(pygame.sprite.Sprite):
    def __init__(self,pos,id):
        super().__init__()
        self.movement = [0,0]
        self.setid = id
        imgs  = list(map(lambda x: f"images/deadman/{x}.png", range(0, 8)))
        self.animation = animation.Animation(images=imgs, rate=2, timmer=6, zoom=(True, 0.32),
                                             flip=(False, False, False),
                                             rect=pygame.Rect(0,0,0,0)
                                             , colorkey=(255, 255, 255))

        self.rect = pygame.Rect(*pos,50,50)
        self.animation.centralize = True
        self.animation.rect = self.rect
        self.tombstone = pygame.image.load("images/deadman/tombstone.png").convert_alpha()


    def show(self,win):
        # pygame.draw.circle(win,(255,255,255),self.rect.midtop,)
        win.blit(self.tombstone,(self.rect.x-15,self.rect.bottom-80))
        self.animation.show(win,center= self.rect.midleft)


    def setpos(self,pos):
        self.rect.x,self.rect.y = pos

    def move(self):
        self.rect.x += self.movement[0]
        self.rect.y += self.movement[1]

    def pop_out(self):
        pass



class Crystals(pygame.sprite.Sprite):
    def __init__(self,pos,type):
        self.type = type
        self.rect = pygame.Rect(*pos,50,50)
        self.state = "not collected"
        imgs = list(map(lambda x: f"images/crystal/{x}.png", range(0, 8)))
        self.animation = animation.Animation(images=imgs, rate=2, timmer=10, zoom=(True, 1),
                                             flip=(False, False, False),
                                             rect=self.rect
                                             , colorkey=(255, 255, 255))
        self.init_pos = [*pos]
        self.animation.centralize = True
        self.vel = 0
        self.aura = animation.Aura([(255,255,255),(0,0,100)],[1,3],25,*self.rect.center)
        self.burst = animation.GlowBurst()
        self.burst.limit = 20
    def show(self,win):
        # self.aura.x,self.aura.y = self.rect.center
        # self.aura.add()
        if self.state == "collected":
            self.burst.show(win)

        # self.aura.show(win)
        else:
            self.animation.show(win,center = (self.rect.centerx,self.rect.centery-5))
            # pygame.draw.rect(win,(255,255,0),self.rect,2)

    def move(self):
        self.rect.x -= self.vel


# imagine you are an animator ,now
# you have to make a ninja like character for a 2d platformer game with dark asthetics
# character specifications
# motion : running
# colors : use dark colors
# output : sprite sheet that contains all the frames
