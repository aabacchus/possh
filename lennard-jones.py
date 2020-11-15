import numpy as np
import pygame
import matplotlib.pyplot as plt

W=800
H=600
dt=0.1
def lj(r, epsilon=2, sigma=2):
    if r == 0:
        r = 0.1
    R = sigma/r
    R6 = R**6
    return 4*epsilon*(R6**2 - R6)
class Particle():
    def __init__(self):
        self.p = np.array([3+10*np.random.random()])
        self.v = np.array([0+np.random.random()])
        self.a = np.array([])
    def move(self,r):
        self.a = np.append(self.a,lj(r))
        self.v = np.append(self.v, (self.a[-1]*dt+self.v[-1])*0.999)
        self.p = np.append(self.p, self.v[-1]*dt+self.p[-1])
        
def mid(f,a,b):
    '''midpoint method for numerical integration'''
    return (b-a)*f((a+b)/2)

def main():
    ps = np.array([Particle(),Particle()])
    pygame.init()
    screen = pygame.display.set_mode([W,H])
    clock = pygame.time.Clock()

    cntr = 0
    while True:
        screen.fill((0,0,0))
        for p in range(len(ps)-1):
            for q in range(p,len(ps)-1):
                r = ps[p].p[-1] - ps[q].p[-1]
                print('R: ',r)
                ps[p].move(r)
                ps[q].move(-r)
            print(ps[p].p[-1])
            pygame.draw.circle(screen, (255,255,255), [round(10*ps[p].p[-1]),round(H/2)],5)
        clock.tick(dt*1000)
        pygame.display.flip()
        cntr+=1
        if cntr > 9999:
            pygame.quit()
            return
main()
