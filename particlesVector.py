import numpy as np
import math
import random
import pygame
import matplotlib.pyplot as plt
import matplotlib.animation as amtn
import time

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (200, 200, 0)
Areaheight = 600
Areawidth = 800
numBalls = 200
g = (0,np.pi)
#cob == coefficient of bounce
cob = 0.5
drag = 1

class Particle:
	def __init__(self, type):
		self.m = 1 + random.random()
		self.rad = self.m*2
		self.x = random.randrange(round(self.rad),Areawidth-round(self.rad))
		self.y = random.randrange(round(self.rad),Areaheight-round(self.rad))
		#self.vx = random.randrange(-2,3)
		#self.vy = random.randrange(-2,3)
		self.speed = random.randrange(0,2)
		self.vAngle = random.uniform(0,np.pi*2)
		if type == 1:
			self.color = YELLOW
		else:
			self.color= WHITE
			
	def move(self):
		self.x += np.sin(self.vAngle)*self.speed
		self.y -= np.cos(self.vAngle)*self.speed
		(self.speed, self.vAngle) = addVctrs((self.speed,self.vAngle),g)
		self.speed *= drag
		
	def wBounce(self):
		if self.x >= Areawidth - self.rad:
			self.x = Areawidth - self.rad
			self.vAngle = - self.vAngle
			self.speed *= cob
		elif self.x <= self.rad:
			self.x = self.rad
			self.vAngle = - self.vAngle
			self.speed *= cob

		if self.y >= Areaheight - self.rad:
			self.y = Areaheight - self.rad
			self.vAngle = np.pi - self.vAngle
			self.speed *= cob
		elif self.y <= self.rad:
			self.y = self.rad
			self.vAngle = np.pi - self.vAngle
			self.speed *= cob


balls = []
for i in range(numBalls):
	if i % 20 == 0:
		ball=Particle(1)
	else:
		ball = Particle(0)
	balls.append(ball)

def main():
	pygame.init()
	screen = pygame.display.set_mode([Areawidth,Areaheight])
	pygame.display.set_caption('Particle simulation')
	clock = pygame.time.Clock()

	#kEs = []
	#for i in range(numBalls):
	#	kEs.append(0.5*balls[i].m*(balls[i].vx**2 + balls[i].vy**2))
	#plt.hist(kEs)
	#plt.show()
	cntr = 1
	doneP = False

	while not doneP:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				doneP = True
				print('quitting...')
				pygame.quit()
				return 1
			if event.type == pygame.KEYUP:
				if event.key==pygame.K_p:
					doneP = True
					while doneP:
						for event in pygame.event.get():
							if event.type == pygame.KEYUP:
								if event.key==pygame.K_p:
									doneP = False
									print('paused by user')
								if event.key==pygame.K_q:
									doneP=True
									print('quitting...')
									pygame.quit()
									return 1
								
				if event.key==pygame.K_q:
					doneP = True
					print('quitting...')
					pygame.quit()
					return 1
				
				if event.key == pygame.K_h:
					print('plotting histogram...')
					kEs = []
					for i in range(numBalls):
						kEs.append(0.5*balls[i].m*balls[i].speed**2)
					plt.ylabel('freq at '+str(cntr))
					plt.xlabel('KE')
					plt.hist(kEs)
					plt.show()
		n = 0
		for ball in balls:
			#ball.x += ball.vx
			#ball.y += ball.vy
			#ball.vy += g

			#ball.x += np.sin(ball.vAngle)*ball.vel
			#ball.y -= np.cos(ball.vAngle)*ball.vel

##			if ball.x > Areawidth - ball.rad:
##				ball.x = Areawidth-ball.rad
##				ball.vx*=-cob
##			elif ball.x < ball.rad:
##				ball.x = ball.rad
##				ball.vx *= -cob
##			if ball.y > Areaheight - ball.rad:
##				ball.y = Areaheight-ball.rad
##				ball.vy *=-cob
##			elif ball.y < ball.rad:
##				ball.y = ball.rad
##				ball.vy *=-cob

			ball.move()
			ball.wBounce()
			#bounce(ball,n)
			n+=1
		#if cntr > 10000:	
		screen.fill(BLACK)
		for ball in balls:
			pygame.draw.circle(screen, ball.color,[int(ball.x),int(ball.y)],int(ball.rad))

		clock.tick(100)
		#if cntr> 10000:
		pygame.display.flip()

		#plt.savefig('KE_'+str(cntr)+'_grav.png', bbox_inches='tight')
		#plt.show()

		print(cntr)
		cntr+=1
		
	pygame.quit()

def distanceBn(p,q,n):
	if n == 1:
		return ((p.x-p.vx-q.x+q.vx)**2+(p.y-p.vy-q.y+q.vy)**2)**0.5
	else:
		return ((p.x-q.x)**2+(p.y-q.y)**2)**0.5

def addVctrs(vector1,vector2):#, *vector2):#vectors must be of the form (mod, arg)
	x  = math.sin(vector1[1]) * vector1[0] + math.sin(vector2[1]) * vector2[0]
	y  = math.cos(vector1[1]) * vector1[0] + math.cos(vector2[1]) * vector2[0]
	return (np.hypot(x,y), 0.5* np.pi - math.atan2(y,x))



def bounce(p,n):
	for i in range(n+1,numBalls):
		q = balls[i]
		r = distanceBn(p,q,0)
		if r > p.rad + q.rad:
			continue
		prevR = distanceBn(p,q,1)
		if prevR < r:
			continue
		pux = p.vx
		puy = p.vy
		p.vx = pux * ((p.m-q.m)/(p.m+q.m)) + (2*q.vx*q.m/(p.m+q.m))
		q.vx = q.vx + (p.m/q.m)*(pux-p.vx)

		p.vy = puy * ((p.m-q.m)/(p.m+q.m)) + ( 2*q.vy*q.m/(p.m+q.m))
		q.vy = q.vy + (p.m/q.m)*(puy-p.vy)


#if _name_ == '_main_':
main()
