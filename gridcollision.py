import numpy as np
import pygame

fps = 60

class Box():
    def __init__(self):
        self.w = 800
        self.h = 600
box = Box()

class Particle():
    def __init__(self):
        self.p = np.array([np.random.random()*box.w,np.random.random()*box.h])
        self.v = np.array([1.,1.]) * 5*(np.random.random()-0.5)
        self.a = np.array([0.,9.])
        self.r = 5
    def update(self,dt):
        self.v += self.a * dt
        self.p += self.v * dt
    def boxCollision(self):
        if self.p[0] <= 0:
            self.v[0] *= -1
            self.p[0] = 0
        elif self.p[0] >= box.w:
            self.v[0] *= -1
            self.p[0] = box.w
        if self.p[1] <= 0:
            self.v[1] *= -1
            self.p[1] = 0
        elif self.p[1] >= box.h:
            self.v[1] *= -1
            self.p[1] = box.h


def main():
    particles = []
    n = 10
    for i in range(n):
        particles.append(Particle())
    pygame.init()
    screen = pygame.display.set_mode([box.w,box.h])
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                print("quit")
                pygame.quit()
                return 0
        screen.fill((0,0,0))
        for p in particles:
            p.update(1/fps)
            p.boxCollision()
            pygame.draw.circle(screen,(255,255,255),p.p,p.r)
        clock.tick()
        pygame.display.flip()
main()
