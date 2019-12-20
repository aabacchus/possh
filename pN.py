import math
import random
import pygame

Width = 800
Height = 600
n = 1000
dt = 0.1
e=1
cntr=1
class Particle():
    def __init__(self):
        self.rad = 1
        self.x=random.randrange(round(self.rad),Width-round(self.rad))
        self.y=random.randrange(round(self.rad),Height-round(self.rad))
        self.m = 1
        self.vx = (random.random()-0.5)*10
        self.vy = (random.random()-0.5)*10
        self.color = (255,255,255)

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
    pygame.init()
    screen = pygame.display.set_mode([Width,Height])
    pygame.display.set_caption("Particle simulation")
    clock = pygame.time.Clock()

    cntr = 1
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                print("Quitting...")
                pygame.quit()
                return 1
        nI=0
        screen.fill((0,0,0))
        for ball in balls:
            ball.move()
            ball.wBounce()
            #bounce(ball,nI)
            attract(ball,nI)
            nI+=1
            pygame.draw.circle(screen,ball.color,[round(ball.x),round(ball.y)],round(ball.rad))

        clock.tick()
        pygame.display.flip()
        #pygame.image.save(screen,'s_'+str(cntr)+'.jpeg')
        print(cntr)
        cntr+=1
        

    pygame.quit()

def attract(p,j):
    for i in range(j+1,n):
        q = balls[i]
        #print(q.x)
        dx = p.x-q.x
        dy = p.y-q.y
        r = math.hypot(dx,dy)
        theta = math.atan2(dy,dx)
        f = -5*(r-7)*math.exp(0.1*(7-r))
        #print(f)
        p.vx += f*math.cos(theta)*dt
        p.vy += f*math.sin(theta)*dt
        q.vx -= f*math.cos(theta)*dt
        q.vy -= f*math.sin(theta)*dt


main()    
