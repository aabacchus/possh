import math
import random
import pygame
import time

Width = 800
Height = 600
n = 30
dt = 0.1
e=1
cntr=1
is_a_planet = 0
zoom = 1

class Particle():
    def __init__(self,is_a_planet):
        self.rad = 20 if not is_a_planet else 5
        self.x=random.randrange(round(self.rad),Width-round(self.rad))
        self.y=random.randrange(round(self.rad),Height-round(self.rad))
        #self.m = 1#+random.random()
        self.m = 10**3 if not is_a_planet else (10**1 if is_a_planet == 2 else 1)
        self.vx = 0 if not is_a_planet else (random.random()-0.5)*7
        self.vy = 0 if not is_a_planet else (random.random()-0.5)*7
        self.color = (255,255,255)

    def move(self,dt=0.1):
        self.x += self.vx*dt
        self.y += self.vy*dt
        self.vx*=e if self.vx < 1000 else 0.1
        self.vy*=e if self.vy < 1000 else 0.1
        #if abs(self.vx) > 10:
        #    self.vx *= 0.01
        #if abs(self.vy) > 10:
        #    self.vy *=0.1
        #acceleration

    def wBounce(self):
        if self.x > Width - self.rad:
            self.x = Width-self.rad
            self.vx *=-e
        elif self.x < self.rad:
            self.x = self.rad
            self.vx *=-e
        if self.y > Height - self.rad:
            self.y = Height-self.rad
            self.vy *=-e
        elif self.y < self.rad:
            self.y = self.rad
            self.vy *=-e
        

balls = []
for i in range(n):
    balls.append(Particle(is_a_planet))
    is_a_planet+=1

def main():
    pygame.init()
    screen = pygame.display.set_mode([Width,Height])
    pygame.display.set_caption("Particle simulation")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont(None,24)

    refreshing = True # whether or not to redraw the black background on each frame, toggleable by pressing 'r'

    cntr = 1
    done = False
    
    zoom = 1
    mouse_down = False
    mouse_start = (0,0)
    mouse_end = (0,0)
    
    offsetX = 0
    offsetY = 0
    oldOffsetX = 0
    oldOffsetY = 0

    t0=time.time()
    
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                #print("Quitting...")
                pygame.quit()
                return 1
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    #print(event.pos)
                    mouse_down = True
                    mouse_start = event.pos
                    mouse_end = mouse_start
                    oldOffsetX = offsetX
                    oldOffsetY = offsetY
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    #print(event.pos)
                    mouse_down = False
                    mouse_end = event.pos
            if event.type == pygame.MOUSEWHEEL:
                #print("scroll: ",event.y)
                zoom += event.y/100
                offsetX -= pygame.mouse.get_pos()[0]*event.y/100
                offsetY -= pygame.mouse.get_pos()[1]*event.y/100
                #print("zoom: ",zoom)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    refreshing = !refreshing
        
        nI=0
        if refreshing:
            screen.fill((0,0,0))
        for ball in balls:
            ball.move()
            #if ball.m >= 1000:
            #    ball.wBounce()
            #ball.wBounce()
            #bounce(ball,nI)
            attract(ball,nI)
            nI+=1
            if mouse_down:
                offsetX = pygame.mouse.get_pos()[0]-mouse_start[0] + oldOffsetX
                offsetY = pygame.mouse.get_pos()[1]-mouse_start[1] + oldOffsetY
                #print(offsetX,offsetY)
            pygame.draw.circle(screen,ball.color,[round(ball.x*zoom+offsetX),round(ball.y*zoom+offsetY)],round(ball.rad*zoom))
            pygame.draw.rect(screen,(255,255,255),pygame.Rect(offsetX,offsetY,Width*(zoom),Height*(zoom)),1)

            ## logic for writing text on screen
            text = "{:.3f}".format(zoom)
            img = font.render(text,True,(0,0,255))
            screen.blit(img,(20,20))

        clock.tick()
        pygame.display.flip()
        #pygame.image.save(screen,'s_'+str("{:03d}".format(cntr))+'.jpeg')
        if cntr%50==1:
            t1 = time.time()
            rate=(t1-t0)/cntr
            tT=rate*999#total time
            tR=tT-t1+t0#time remaining
            #print(str("{:.2f}".format(tR))+' s remaining')
        
        #print(cntr)
        if cntr>99999:
            done = True
        cntr+=1
        

    pygame.quit()

def attract(p,j):
    for i in range(j+1,n):
        q = balls[i]
        dx = p.x-q.x
        dy = p.y-q.y
        r = math.hypot(dx,dy)
        theta = math.atan2(dy,dx)
        #f = -5*(r-7)*math.exp(0.1*(7-r))
        f = -5*p.m*q.m/r**2
        p.vx += f*math.cos(theta)*dt/p.m
        p.vy += f*math.sin(theta)*dt/p.m
        q.vx -= f*math.cos(theta)*dt/q.m
        q.vy -= f*math.sin(theta)*dt/q.m


main()    
