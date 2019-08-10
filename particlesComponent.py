import numpy as np
import math
import random
import pygame
import matplotlib.pyplot as plt
import matplotlib.animation as amtn
import time

histNum = 0

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (200, 200, 0)
Areaheight = 600
Areawidth = 800
numBalls = 600
g = 0
#cob == coefficient of bounce
cob = 1
drag = 1

class Particle:
	def __init__(self, type):
		self.m = 1 + random.random()
		self.rad = 2
		self.x = random.randrange(round(self.rad),Areawidth-round(self.rad))
		self.y = random.randrange(round(self.rad),Areaheight-round(self.rad))
		self.vx = (random.random()-0.5)*16
		self.vy = (random.random()-0.5)*16
		if type == 1:
			self.color = YELLOW
		else:
			self.color= WHITE
			
	def move(self):
		self.x += self.vx
		self.y += self.vy
		self.vy += g
		
	def wBounce(self):
		if self.x > Areawidth - self.rad:
			self.x = Areawidth-self.rad
			self.vx*=-cob
		elif self.x < self.rad:
			self.x = self.rad
			self.vx *= -cob
		if self.y > Areaheight - self.rad:
			self.y = Areaheight-self.rad
			self.vy *=-cob
		elif self.y < self.rad:
			self.y = self.rad
			self.vy *=-cob
	#def draw(self):
	#	pygame.draw.circle(screen, self.color,[int(self.x),int(self.y)],int(self.rad))

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
	
	histNum = 0
	fig = plt.figure()
	
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
						kEs.append(0.5*balls[i].m*(balls[i].vx**2+balls[i].vy**2))
					plt.ylabel('freq at '+str(cntr))
					plt.xlabel('KE')
					plt.hist(kEs)
					plt.show()
				if event.key == pygame.K_j:
					histNum +=1
					if histNum>6:
                                                plt.savefig('KEss.png')
					print('preparing histogram '+str(histNum)+' of 6')
					print('plotting histogram...')
					kEs = []
					for i in range(numBalls):
						kEs.append(0.5*balls[i].m*(balls[i].vx**2+balls[i].vy**2))
					
					fig.add_subplot(int('32'+str(histNum)))
					
					plt.ylabel('freq at '+str(cntr))
					plt.xlabel('KE')
					plt.hist(kEs)
					#plt.savefig('KE_'+str(cntr)+'.png', bbox_inches='tight')
					#print('histogram saved as KE_'+str(cntr)+'.png')
				if event.key == pygame.K_s:
					plt.savefig('KEs.png')
					print('histograms saved as KEs.png')

		if cntr%100==1 and histNum<=8:
			histNum+=1
			print('preparing histogram '+str(histNum)+' of 8')
			print('plotting histogram...')
			kEs = []
			for i in range(numBalls):
				kEs.append(0.5*balls[i].m*(balls[i].vx**2+balls[i].vy**2))
			
			fig.add_subplot(int('42'+str(histNum)))
			
			plt.ylabel('freq at '+str(cntr))
			plt.xlabel('KE')
			plt.hist(kEs)
			if histNum == 8:
				plt.savefig('KEs.png')
				print('histograms saved as KEs.png')
				doneP = True
				print('figure complete, quitting...')
				pygame.quit()
				return 1

		n = 0
		for ball in balls:
			ball.move()
			ball.wBounce()
			bounce(ball,n)
			n+=1
		#if cntr > 10000:	
		screen.fill(BLACK)
		for ball in balls:
			#ball.draw()
			pygame.draw.circle(screen, ball.color,[round(ball.x),round(ball.y)],round(ball.rad))

		clock.tick(100)
		#if cntr> 10000:
		pygame.display.flip()

		#plt.savefig('KE_'+str(cntr)+'_grav.png', bbox_inches='tight')
		#plt.show()

		print(cntr)
		cntr+=1
		
	pygame.quit()

def distanceBn(p,q,frameBefore):
	if frameBefore == 1:
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
		q.vx = q.vx + (pux-p.vx)*(p.m/q.m)

		p.vy = puy * ((p.m-q.m)/(p.m+q.m)) + ( 2*q.vy*q.m/(p.m+q.m))
		q.vy = q.vy + (puy-p.vy)*(p.m/q.m)


#if _name_ == '_main_':
main()
