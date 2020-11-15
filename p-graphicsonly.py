import ast
import time
import pygame

Width = 1280
Height = 1060
n=150

f = open('positions.txt', 'r')
posits = ast.literal_eval(f.read())
f.close()

def main():
    '''main method'''
    pygame.init()
    screen=pygame.display.set_mode([Width,Height])
    clock=pygame.time.Clock()

    cntr=1
    t0 = time.time()

    for i in range(len(posits)):
        screen.fill((0,0,0))
        for j in range(len(posits[i])):
            pygame.draw.circle(screen,(255,255,255),[round(posits[i][j][0]),round(posits[i][j][1])],2)
        pygame.image.save(screen,'images/s_'+str("{:03d}".format(cntr))+'.jpeg')
        cntr+=1
    
    print("Done in "+str(time.time()-t0)+" seconds.")
    pygame.quit()
main()
