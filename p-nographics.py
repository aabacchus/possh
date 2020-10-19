import math
import random

import time

Width = 1280
Height = 1060
n = 150
dt = 0.1
e=1
cntr=1
class Particle():
    def __init__(self):
        self.rad = 2
        self.x=random.randrange(round(self.rad),Width-round(self.rad))
        self.y=random.randrange(round(self.rad),Height-round(self.rad))
        self.m = 1#+random.random()
        self.vx = (random.random()-0.5)*10
        self.vy = (random.random()-0.5)*10
        self.proton = round(random.random()*2) # 1=proton, 0=neutron
        self.color = (25,25,255) if self.proton == 1 else (255,25,25) #make protons blue, neutrons red

    def move(self,dt=0.1):
        self.x += self.vx*dt
        self.y += self.vy*dt
        self.vx*=0.99
        self.vy*=0.99
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
    balls.append(Particle())

def main():
    #pygame.init()
    #screen = pygame.display.set_mode([Width,Height])
    #pygame.display.set_caption("Particle simulation")
    #clock = pygame.time.Clock()

    cntr = 1
    done = False

    t0=time.time()
    
    while not done:
        nI=0
#        screen.fill((0,0,0))
        for ball in balls:
            ball.move()
            ball.wBounce()
            #bounce(ball,nI)
            attract(ball,nI)
            nI+=1
#            pygame.draw.circle(screen,ball.color,[round(ball.x),round(ball.y)],round(ball.rad))

#        clock.tick()
#        pygame.display.flip()
#        pygame.image.save(screen,'s_'+str("{:03d}".format(cntr))+'.jpeg')
#        if cntr%10==1:
#            t1 = time.time()
#            rate=(t1-t0)/cntr
#            tT=rate*999#total time
#            tR=tT-t1+t0#time remaining
#            print(str("{:.2f}".format(tR))+' s remaining')
        
        print(cntr)
        if cntr>99:
            done = True
        cntr+=1
#pygame.quit()

def attract(p,j):
    for i in range(j+1,n):
        q = balls[i]
        dx = p.x-q.x
        dy = p.y-q.y
        r = math.hypot(dx,dy)
        theta = math.atan2(dy,dx)
        f=0
        a=7
        s=5
        if p.proton == 1 and q.proton == 1:
            f += 10000/r/r
            a = 9
            s=8
        f += -s*(r-a)*math.exp(0.1*(a-r))
        p.vx += f*math.cos(theta)*dt#/p.m
        p.vy += f*math.sin(theta)*dt#/p.m
        q.vx -= f*math.cos(theta)*dt#/q.m
        q.vy -= f*math.sin(theta)*dt#/q.m


main()    
