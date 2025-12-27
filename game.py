import random
import pygame
import animation
import sprite
from pygame.locals import*
import widgets

pygame.init()
pygame.mixer.init()
'''
Problem :- Due to using set function more than 1 time for ramp and tile...(solved) 
'''
#TODO :-> add obstacles(water)

class Background:
    def __init__(self,mainbg,scrollbg,size):
        self.mainbg = mainbg
        self.scollbg = scrollbg
        self.size = size
        self.layer_vel = 0.25
        self.static_pos = [0, -250]
        self.static_layer_y = -40
        self.layers = scrollbg
        self.layer_pos = [0, self.size[0]]

    def render(self,win):
        # win.blit(self.mainbg,self.static_pos)
        pygame.draw.rect(win,(0,0,0),(0,self.size[1]-70,self.size[0],self.size[1]))

    def cycle_layer(self,win):
        for i in range(len(self.layers)):
            if self.layer_pos[i] <= -self.size[0]:
                self.layer_pos[i] = self.size[0]-2*self.layer_vel
            else:
                self.layer_pos[i] -= self.layer_vel
                win.blit(self.layers[i],(self.layer_pos[i],self.static_layer_y))
class Game:
    def __init__(self):
        self.size = [1280,720]
        self.screen = pygame.display.set_mode(self.size,pygame.FULLSCREEN)

        self.window = pygame.Surface(self.size)
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.running = True
        self.reference = [0,0]
        pygame.display.set_caption("EndLess")


        #loading background >>>>>>
        self.bg = pygame.image.load("images/background/bg.jpg").convert_alpha()
        # self.bg = pygame.transform.smoothscale(self.bg,self.size).convert_alpha()

        self.layers = [
            pygame.transform.smoothscale(pygame.image.load("images/background/l1.PNG"),self.size).convert_alpha(),
            pygame.transform.flip(pygame.transform.smoothscale(pygame.image.load("images/background/l1.PNG"), self.size)
                                  ,True,False).convert_alpha(),
            # pygame.transform.smoothscale(pygame.image.load("images/background/l1.PNG"), self.size).convert_alpha(),
        ]
        self.background = Background(self.bg,self.layers,self.size)
        # self.background.static_pos = [0,0]

        #creating tint surface >>>>>>
        self.tint = pygame.Surface(self.window.get_size())
        self.tint.fill((50,50,50))
        # self.layer_vel = 0.25
        # self.layer_pos = [0,1280]
        self.scale_fac = (self.screen.get_width()/self.screen.get_height())*(720/1280)

        self.window_scale_size = [int((self.screen.get_width()/self.screen.get_height())*(720/self.scale_fac)),
                                  int(1280*self.scale_fac*(self.screen.get_height()/self.screen.get_width()))]

        '''
        math for scaling the screen 
        W     w
        - = x -
        H     h
        
        '''
        self.world_vel = 5
        self.color = 20
        self.tiles = []
        self.ramps = []
        self.crystal = []
        self.test_surf = pygame.Surface((self.size[0],500))
        self.test_surf.fill((0,0,0))
        self.test_surf.set_colorkey((0,0,0))
        pygame.mixer.set_num_channels(30)

        #sounds and fonts
        self.sounds = {
            "gems":pygame.mixer.Sound("sounds/gems.mp3"),
            "dash":pygame.mixer.Sound("sounds/dash.mp3")
        }
        self.sounds['dash'].set_volume(0.5)

        self.fonts = {"label": pygame.font.Font("data/fonts/mono_2/' Mono Regular.ttf", 20),
                      "Heading": pygame.font.Font("data/fonts/breathe_fire/Breathe Fire.otf", 200),
                      "H2": pygame.font.Font("data/fonts/hack/Hack-Regular.ttf", 40)
                      }

        #loading grasses for ground
        self.grasses = []
        for i in range(self.size[0]//175+2):
            g = sprite.Grass(self.size[0],self.world_vel,[i*175,630])
            g.id = i
            self.grasses.append(g)

        #loading ground tiles
        for i in range(0,self.size[0]+100,50):
            t = sprite.Tile([i,self.size[1]-70],50,type = "ground")
            t.vel = self.world_vel
            self.tiles.append(t)

        #creating sets
        self.sets = []
        self.deadman_set_pos = []
        self.numset = 8
        self.active_set = random.randint(0,self.numset-1)
        # self.active_set = random.randint(0,self.numset-1)
        for i in range(self.numset):
            self.load_set(f"data/set{i+1}.txt")

        #sprites
        self.player = sprite.Player([150,self.size[1]-50-70])
        self.deadman = sprite.DeadMan(random.choice(self.deadman_set_pos[self.active_set]), self.active_set)
        self.deadman.centralize = True
        self.bat = sprite.Bat([self.size[0] + 300, 50])
        #effects
        self.rain = animation.Rain(self.size[1]-90,self.size[0])
        # self.score = 0

        self.framecount = 0

        #resources and labels
        self.gem_count = 0
        self.meter = 0
        # self.ScoreLabel = widgets.Label("EndLess",70,[640,50])

        self.crystal_icon = pygame.image.load("images/crystal/0.png").convert_alpha()

        self.GemsLabel = widgets.Label(str(self.gem_count), 20, [40,4],self.fonts['label'])
        self.GemsLabel.color = (255,255,255)
        self.TitleLabel = widgets.Label("EndLess", 20, [self.screen.get_width()//2,
                                                        200],self.fonts['Heading'])
        self.TitleLabel.color = (100,120,120)
        # self.GemsLabel.font = pygame.font.Font("data/fonts/mono_2/' Mono Regular.ttf",self.GemsLabel.size)

        self.MeterLabel = widgets.Label(f"{self.meter}m",20,[640,25],self.fonts['H2'])
        # self.MeterLabel.color = (255,255,255)
        # self.ScoreLabel.font = pygame.font.Font("data/fonts/mono_2/' Mono Regular.ttf",self.GemsLabel.size)
        self.dataframe = widgets.Frame((0,0),"images/widgets/frame.png")

        #player dash status
        self.dash = [False,10,0,20,3*60]#status ,timer , const timer,velup,cooldown

        while self.running: 
            #updates
            self.screen.fill((0,0,0))
            self.background.layer_vel = self.world_vel/20
            self.tint.fill((self.color,0,0))

            #testing .....
            # self.test_surf.fill((self.color,self.color,self.color))
            # points = [
            #     [0,self.test_surf.get_height()//2],[self.test_surf.get_width(),0],
            #     [self.test_surf.get_width(),self.test_surf.get_height()]
            # ]
            # pygame.draw.polygon(self.test_surf,(self.color,self.color,self.color),points)
            # pygame.draw.polygon(self.test_surf,(255,255,255),points,1)

            #player and tile collisions
            collision = self.player.move(self.tiles+self.sets[self.active_set],self.ramps[self.active_set])
            if collision["bottom"]:
                # if not self.player.state == "ready":
                #     self.player.dirtburst.add()
                #     self.player.dirtburst.y = self.player.rect.bottom
                # if not self.player.state == "dash":
                self.player.state = "ready"
                self.player.movement[1] = 0


            if collision["top"]:
                self.player.movement[1] *= -0.5

            self.player.dirtburst.y = self.player.rect.bottom
            if self.player.movement[1] == 0:
                self.player.dirtburst.add()

            if self.dash[0]:self.player.dash = True
            else: self.player.dash = False

            # if self.player.movement[0] != 0:
            #     self.player.state = "air"

            #bat sprite updates
            self.bat.move(self.world_vel)

            # collision crystals
            for crystal in self.crystal[self.active_set]:
                if crystal.rect.colliderect(self.player.rect):
                    if crystal.state != "collected":
                        self.sounds['gems'].play()
                        crystal.burst.add(crystal.rect.center)
                        crystal.state = "collected"
                        crystal.animation.index = 0
                        self.gem_count += 1
                        self.GemsLabel.text = str(self.gem_count)


            #input handle
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.jump()
                    if event.key == pygame.K_s:
                        self.world_vel = 0

                    if event.key == pygame.K_g:
                        if not self.dash[0]:
                            self.sounds['dash'].play()
                            self.dash[0] = True
                            self.world_vel+= self.dash[3]


            #meter labeling
            # if self.framecount > 30:
            #     self.framecount = 0
            self.meter += (self.world_vel/60)
            self.MeterLabel.text = f"{int(self.meter)}m"
            # else:
            #     self.framecount += 1
            # self.score +=
            # self.ScoreLabel.text = str(self.score)

            #rendering
            self.rain.add()

            self.window.fill((220, 150, 220))
            # self.window.blit(self.bg, (0, -250))
            # self.cycle_layer()
            self.window.blit(self.background.mainbg,self.background.static_pos)
            self.TitleLabel.show(self.window)
            self.background.render(self.window)
            self.background.cycle_layer(self.window)
            self.window.blit(self.tint, (0, 0), special_flags=BLEND_RGBA_SUB)
            self.window.blit(self.test_surf, (200, 350), special_flags=BLEND_RGBA_ADD)
            self.rain.show(self.window, self.sets[self.active_set] + self.ramps[self.active_set])
            # self.deadman.show(self.window,center=self.deadman.rect.center)
            # pygame.draw.rect(self.window, (0, 0, 0), self.player.rect, 1)
            # pygame.draw.rect(self.window, (0, 0, 0), self.bat.rect, 1)
            self.bat.show(self.window)
            self.deadman.show(self.window)
            self.player.show(self.window)

            #frames
            # pygame.draw.rect(self.window,(0,0,0),Rect(-5,10,150,50))
            # pygame.draw.rect(self.window,(255,255,255),Rect(-5,10,150,50),1)
            self.dataframe.show(self.window)

            #Labels
            self.MeterLabel.show(self.window)
            self.window.blit(pygame.transform.smoothscale_by(self.crystal_icon, 0.7), (5, 4))
            length = self.GemsLabel.show_pos(self.window)
            # self.dataframe.size[0] = 40
            self.dataframe.size[1] = 40
            self.dataframe.size[0] = length+70
            # self.ScoreLabel.show(self.window)
            # self.window.blit(self.frame,(-80,5))
            #frames
            # frame = pygame.transform.smoothscale(self.frame, (length+50,self.frame.get_height()))
            # self.window.blit(self.frame, (0, 0))



            for tile in self.tiles:#rendering ground
                tile.show(self.window)
                # pygame.draw.rect(self.window,(200,0,0),tile.rect)

                # tile.vel = self.world_vel
                # tile.move()

                # pygame.draw.rect(self.window,(255,0,0),tile.rect,5)

            #updating tiles in the current set
            for mtile in self.sets[self.active_set]+self.ramps[self.active_set]+self.crystal[self.active_set]:
                mtile.vel = self.world_vel
                mtile.move()
                mtile.show(self.window)
                if mtile.rect.right < -self.size[0]:
                    offset = abs(abs(mtile.rect.right)-self.size[0])
                    self.reset_set_pos(self.active_set,offset)
                    break

            self.deadman.movement[0] = -self.world_vel
            if self.active_set == self.deadman.setid:
                self.deadman.move()

            #dash mechanic
            if self.dash[0]:
                if self.dash[2] >= self.dash[1]:
                    self.dash[0] = False
                    self.dash[2] = 0
                    self.world_vel -= self.dash[3]
                else:
                    self.dash[2] += 1


            # for ramp in self.ramps[self.active_set]:
            #     ramp.vel = self.world_vel
            #     ramp.move()
            #     ramp.show(self.window)
            #     if ramp.rect.left <= -self.size[0]:
            #         ramp.rect.left = -self.size[0]
            #         self.reset_set_pos(self.active_set)

            self.roll_grass()

            keys = pygame.key.get_pressed()
            # if keys[pygame.K_SPACE]:
            #     self.world_vel += 0.1
            #     self.layer_vel  += 0.1/10
            if keys[pygame.K_UP]:
                if self.color < 80:
                    self.color += 1
            if keys[pygame.K_DOWN]:
                if self.color > 0:
                    self.color -= 1
            if keys[pygame.K_w]:
                if self.world_vel < 25:
                    self.world_vel += 0.1
                if self.player.animation.rate < self.player.animation.timmer:
                    self.player.animation.rate += 0.1

            # self.draw_grid()

            self.screen.blit(pygame.transform.smoothscale(self.window,self.window_scale_size),self.reference)
            pygame.display.update()
            self.clock.tick(self.fps)


    def cycle_layer(self):
        for i in range(len(self.layers)):
            if self.layer_pos[i] <= -self.size[0]:
                self.layer_pos[i] = self.size[0]-2*self.layer_vel
            else:
                self.layer_pos[i] -= self.layer_vel
            self.window.blit(self.layers[i],(self.layer_pos[i],-40))

    def roll_grass(self):
        for grass in self.grasses:
            grass.vel = self.world_vel
            grass.move(len(self.grasses))
            grass.show(self.window)


    def load_set(self,path):
        lst = []
        lst2 = []
        deadpos = []
        crystals = []
        with open(path) as file:
            data = list(map(lambda x:x.split(),file.read().split("\n")))
            # print(data)
        for y_index,y in enumerate(data):
            for x_index ,x in enumerate(y):
                if x == "S":
                    lst.append(sprite.Obstacle((self.size[0]+x_index*50,y_index*50),50,"obstacle"))
                if x == "L" or x == "R":
                    lst2.append((sprite.Ramps(self.size[0]+x_index*50,y_index*50,x)))
                if x == "G":
                    lst.append(sprite.Tile((self.size[0]+x_index*50,y_index*50),50,"grass"))
                if x == "T":
                    lst.append(sprite.Tile((self.size[0] + x_index * 50, y_index * 50), 50, "tile"))
                if x == "D":
                    deadpos.append((self.size[0] + x_index * 50, y_index * 50))
                if x == "C":
                    crystals.append(sprite.Crystals((self.size[0] + x_index * 50, y_index * 50),type = "crystal"))

        self.sets.append(lst)
        self.ramps.append(lst2)
        self.crystal.append(crystals)
        self.deadman_set_pos.append(deadpos)


    def reset_set_pos(self,set,offset):
        for tile in self.sets[set]:
            # tile.rect.x += self.size[0]*2+offset
                tile.rect.x = tile.init_pos[0]

        for ramp in self.ramps[set]:
            # ramp.rect.x += self.size[0]*2+offset
            ramp.rect.x = ramp.init_pos[0]

        for crystal in self.crystal[set]:
            # ramp.rect.x += self.size[0]*2+offset
            crystal.rect.x = crystal.init_pos[0]
            crystal.state = "not collected"
            crystal.animation.index = 0

        print(offset)
        self.active_set = random.randint(0,self.numset-1)


        self.deadman.setpos(random.choice(self.deadman_set_pos[self.active_set]))
        self.deadman.setid = self.active_set



    def draw_grid(self):
        for x in range(0,self.size[0],50):
            pygame.draw.line(self.window,(255,255,255),(x,0),(x,self.size[1]))
        for y in range(0,self.size[1],50):
            pygame.draw.line(self.window,(255,255,255),(0,y),(self.size[0],y))



if __name__ == "__main__":
    game = Game()

# create  a 2d charater spritesheet
# specification :
# movement : running
# must have a cape
# looks like a ninja
# colors : dark colors