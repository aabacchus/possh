#include <stdio.h>
#include <math.h>
#include <iostream>
#include <cmath>
#include <array>
#include <time.h>
int Width = 800;
int Height = 600;
int n = 50;
float dt=0.1;
float e=1;
int cntr=0;

class Particle {
	public:
		float rad = 2;
		float x = std::rand() % Width;
		float y = std::rand() % Height;
		float m = 1;
		float vx = std::rand()%6-3;
		float vy = std::rand()%4 -2;
		int color = (255,255,255);
		float charge = 1; // +1 or -1; this is changed for some in the initialising bit.
		Particle(){
			//std::cout<<"particle class called\n";
			//std::cout<<x<<", "<<y<<"\n";
			//srand(time(NULL));
			//NOTE: don't seed rand() (even before calling it for x,y) because it happens so quickly that all the particles will have the same values!
		}
		void move() {
			x += vx*dt;
			y += vy*dt;
			vx*=0.97;
			vy*=0.97;
		}
		void wBounce() {
			if (x > Width - rad){
				x = Width -rad;
				vx *= -e;
			} else if (x < rad) {
				x = rad;
				vx *= -e;
			}
			if (y > Height - rad) {
				y = Height - rad;
				vy *= -e;
			} else if (y < rad) {
				y = rad;
				vy *= -e;
			}

		}
};
int main()
{
	std::srand(time(NULL));
	Particle balls[n];
	for (int i = 0; i < n/2; i++){ // This makes the first half of the balls have a negative charge (the other half is left with positive)
		balls[i].charge = -1;
	}
	bool done = false;
	printf("[");
	while (!done){
		int nI = 0;
		printf("[");
		for (int i = 0; i<n; i++) {
			printf("[%f, %f],",balls[i].x, balls[i].y);
			balls[i].move();
			balls[i].wBounce();
			
			for (int j = i+1;j<n;j++){
				Particle p=balls[i];
				Particle q=balls[j];
				float dx = p.x-q.x;
				float dy = p.y-q.y;
				float r = hypot(dx, dy);
				float theta = atan2(dy,dx);

				//float f = r!= 0 ? p.charge * q.charge * -1000/(r*r) : -1000;
				r = r == 0 ? 0.001 : r; // to avoid dividing-by-zero errors
				//float f = -1/r + 0.00001/(r*r*r*r*r*r);
				float f = p.charge * q.charge * -1000/(r*r) + 6/(r*r*r*r*r*r*r);

				balls[i].vx -= f*cos(theta)*dt;
				balls[i].vy -= f*sin(theta)*dt;
				balls[j].vx += f*cos(theta)*dt;
				balls[j].vy += f*sin(theta)*dt;
			}
			
			nI++;
		}
		printf("],\n");
		//printf("%d\n",cntr);
		if (cntr>999){
			done = true;
		}
		cntr++;
	}
	printf("]\n");
}
