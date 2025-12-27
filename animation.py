import pygame,random,math
from pygame.locals import*
class Animation:
    def __init__(self, colorkey = False,**kwargs):  # rate,imagespath,pos,timmer,zoom,flip
        self.rate = kwargs["rate"]
        self.images_path = kwargs["images"]
        self.timmer = kwargs["timmer"]
        self.constant_timmer = kwargs["timmer"]
        self.images = []
        self.zoom = kwargs["zoom"]
        self.flip = kwargs['flip']  # permission,xbool,ybool

        for i in self.images_path:
            img = pygame.image.load(i).convert_alpha()
            if self.flip[0]:
                img = pygame.transform.flip(img, self.flip[1], self.flip[2]).convert_alpha()
            if self.zoom[0]:
                img = pygame.transform.rotozoom(img, 0, self.zoom[1]).convert_alpha()
                # img = pygame.transform.smoothscale(img,
                #                    (img.get_width()*self.zoom[1],img.get_height()*self.zoom[1])).convert_alpha()
            if colorkey:
                img.set_colorkey(colorkey)
            self.images.append(img)
        self.frame_number = len(self.images)
        self.index = 0
        self.centralize = False
        self.rect = kwargs['rect']

    def show(self, win, pause=False, **kwargs):
        if self.centralize:
            imgrect = self.images[self.index].get_rect(center=kwargs['center'])
            win.blit(self.images[self.index], imgrect)
        else:
            win.blit(self.images[self.index], self.rect)
        if not pause:
            if self.timmer <= 0:
                self.timmer = self.constant_timmer
                if self.index >= self.frame_number - 1:
                    self.index = 0
                else:
                    self.index += 1
            else:
                self.timmer -= self.rate



class Rain:
    def __init__(self,bottom,width):
        self.data = []
        self.bottom = bottom
        self.width = width
        self.angle = math.radians(120)
        self.gravity = 0.5
        self.vel = [3,10]
        self.burst = DropBurst()
    def add(self):
        pos = [random.randint(0,int(self.width*(1-math.cos(self.angle)))),0]
        vel = random.randint(*self.vel)
        self.data.append([pos,vel])

    def show(self,win,tiles = False):
        for i,drop in enumerate(self.data):
            if tiles:
                if self.check_tile_collide(tiles,drop[0]):
                    self.burst.add(drop[0])
                    self.data.pop(i)

            if drop[0][1] > self.width or drop[0][1] < 0:
                self.data.pop(i)
                self.burst.add(drop[0])
            elif drop[0][1] > self.bottom:
                self.burst.add(drop[0])
                self.data.pop(i)
            else:
                drop[0][0] += drop[1]*math.cos(self.angle)
                drop[0][1] += drop[1]*math.sin(self.angle)
                drop[1] += self.gravity

                pygame.draw.line(win,(255,255,255),drop[0],
                                 (drop[0][0]-drop[1]*math.cos(self.angle),
                                  drop[0][1]-drop[1]*math.sin(self.angle)),1)
        self.burst.show(win)

    def check_tile_collide(self,lst,pos):
        for i in lst:
            if i.rect.collidepoint(pos):
                return True

        else: return False


class DropBurst:
    def __init__(self):
        self.data = []
        self.vel = [-4,-1]
        self.size = [1,3]
        self.gravity = 0.2
        self.color = (200,200,200)
        self.limit = 10

    def add(self,center):
        for i in range(self.limit):
            pos = [*center]
            angle = random.randint(0,360)
            vel = random.randint(*self.vel)
            vx = vel*math.cos(math.radians(angle))
            vy = vel*math.sin(math.radians(angle))
            size = random.randint(*self.size)
            data = [pos,vx,vy,size]
            self.data.append(data)

    def show(self,win):
        for i,data in enumerate(self.data):
            if data[3] <= 0:
                self.data.pop(i)
            else:
                data[0][0] += data[1]
                data[0][1] += data[2]
                data[2] += self.gravity
                data[3] -= 0.2
                pygame.draw.circle(win,self.color,data[0],data[3])


class DirtBurst:
    def __init__(self,xrange,y):
        self.xrange = xrange
        self.y = y
        self.data = []
        self.gravity = 0.2
        self.limit = 1
        self.vel = (3,6)
        self.size = [1,6]
        self.color = (0,0,0)

    def add(self):
        for i in range(self.limit):
            x = random.randint(*self.xrange)
            pos = [x,self.y]
            angle = random.randint(-180,-90)
            vel = random.randint(*self.vel)
            vx = vel * math.cos(math.radians(angle))
            vy = vel * math.sin(math.radians(angle))
            size = random.randint(*self.size)
            data = [pos, vx, vy, size]
            self.data.append(data)

    def show(self, win):
        for i, data in enumerate(self.data):
            if data[3] <= 0:
                self.data.pop(i)
            else:
                data[0][0] += data[1]
                data[0][1] += data[2]
                data[2] += self.gravity
                data[3] -= 0.2
                pygame.draw.circle(win, self.color, data[0], data[3])

class Aura:
    def __init__(self,color,radius,xlimit,x,y):
        self.color = color
        self.particles = []
        self.radius = radius
        self.xlimit = xlimit
        self.x = x
        self.y = y
        self.rate = 0.1

    def add(self,vx = False):
        x = random.randint(self.x-self.xlimit,self.x+self.xlimit)
        y = self.y
        r = random.randint(*self.radius)
        if not vx:
            vx = 0
        vy = random.randint(-6,-1)
        data = [[x,y],r,[vx,vy]]
        self.particles.append(data)

    def show(self,win):
        if not len(self.particles) > 35:
            self.add()
        for i,particle in enumerate(self.particles):
            particle[0][0] += particle[2][0]
            particle[0][1] += particle[2][1]
            # particle[2][1] -= 0.1
            particle[1] -= self.rate
            if particle[1] <= 0:
                self.particles.pop(i)
            surf  = self.circle_surf(particle[1]*2,self.color[1])
            win.blit(surf,(particle[0][0]-1.25*particle[1],particle[0][1]-1.25*particle[1]),special_flags= BLEND_RGB_ADD)
            pygame.draw.circle(win,self.color[0],particle[0],particle[1])

    def circle_surf(self,radius,color):
        surf = pygame.Surface((radius*2,radius*2))
        pygame.draw.circle(surf,color,(radius*0.5,radius*0.5),radius)
        surf.set_colorkey((0,0,0))
        return surf


class GlowBurst:
    def __init__(self):
        self.size = [1,4]
        self.vel = [1,4]
        self.color = [(255,255,255),(0,50,150)]
        self.limit = 20
        self.particles = []
        self.rate = 0.15

    def add(self,center):
        for i in range(self.limit):
            angle = math.radians(random.randint(0,360))
            size = random.randint(*self.size)
            pos = [*center]
            vel = random.randint(*self.vel)
            data = [pos,size,angle,vel]
            self.particles.append(data)

    def show(self,win):
        for i,particle in enumerate(self.particles):
            if particle[1] <= 0:
                self.particles.pop(i)
            else:
                particle[0][0] += particle[3]*math.cos(particle[2])
                particle[0][1] += particle[3]*math.sin(particle[2])
                particle[1] -= self.rate
                surf = self.circle_surf(particle[1] * 2, self.color[1])
                win.blit(surf, (particle[0][0] - 2 * particle[1], particle[0][1] - 2 * particle[1]),
                         special_flags=BLEND_RGB_ADD)
                pygame.draw.circle(win,self.color[0],particle[0],particle[1])


    def circle_surf(self,radius,color):
        surf = pygame.Surface((radius*2,radius*2))
        pygame.draw.circle(surf,color,(radius,radius),radius)
        surf.set_colorkey((0,0,0))
        return surf


class DashEffect:
    def __init__(self,x,y,limit):
        self.data = []
        self.x = x
        self.y = y
        self.limit = limit

    def set(self,x,y):
        self.x = x
        self.y = y

    def show(self,win):
        for i,line in enumerate(self.data):
            if line[2] > 0:
                line[0] -= line[2]
                line[2] -= 0.2
                pygame.draw.line(win,(255,255,255),(line[0]-line[2],line[1]),(line[0],line[1]))
            else:
                del self.data[i]

    def add(self):
        x = self.x
        y = random.randint(self.y-self.limit,self.y+self.limit)
        size = random.randint(5,20)
        self.data.append([x,y,size])