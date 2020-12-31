#include <stdio.h>
#include <math.h>
#include <iostream>
#include <cmath>
#include <array>
#include <time.h>
int Width = 1000;
int Height = 1000;
int n = 400;
float dt=0.1;
float e=1;
int cntr=0;
float G = pow(10,3);

class Particle {
	public:
		float rad = 1;
		float x = std::rand() % Width;
		float y = std::rand() % Height;
		float m = std::rand()%10;//*pow(10,24);
		float vx = 0.;//std::rand()%4-2; // 0 so that there is 0 total momentum.
		float vy = 0.;//std::rand()%4-2;
		Particle(){
		}
		void move() {
			x += vx*dt;
			y += vy*dt;
			//vx*=0.97;
			//vy*=0.97;
		}
		void wBounce() {
			if (x > Width - m){
				x = Width -m;
				vx *= -e;
			} else if (x < m) {
				x = m;
				vx *= -e;
			}
			if (y > Height - m) {
				y = Height - m;
				vy *= -e;
			} else if (y < m) {
				y = m;
				vy *= -e;
			}

		}
};
int main()
{
	std::srand(time(NULL));
	Particle balls[n];
	bool done = false;
	printf("[");
	while (!done){
		int nI = 0;
		printf("[");
		for (int i = 0; i<n; i++) {
			printf("[%f, %f, %f],",balls[i].x, balls[i].y, balls[i].m);
			if (balls[i].m == 0) continue;
			balls[i].move();
			//balls[i].wBounce();

			
			for (int j = i+1;j<n;j++){
				Particle p=balls[i];
				Particle q=balls[j];
				if (q.m == 0) continue;
				float dx = p.x-q.x;
				float dy = p.y-q.y;
				float r = hypot(dx, dy);
				float theta = atan2(dy,dx);
				if (r <= pow(p.m/3.14,0.5)+pow(q.m/3.14,0.5)){// merging particles makes them increase in area rather than directly in radius
					// This if bit makes it so that the lighter particle merges *into* the heavier one
					int index;
					int other;
					if (p.m > q.m) {
						index = i;
						other = j;
					} else {
						index = j;
						other = i;
					}
					balls[index].vx = (p.vx*p.m + q.vx*q.m ) / (p.m+q.m);
					balls[index].vy = (p.vy*p.m + q.vy*q.m ) / (p.m+q.m);
					balls[index].m = p.m + q.m;
					// setting the other ball's mass to 0 sets it up to be ignored by the rest of the scripts.
					balls[other].m = 0;
					continue;
				}
				float f = - G * p.m * q.m / pow(r,2);

				balls[i].vx += f*cos(theta)*dt/p.m;
				balls[i].vy += f*sin(theta)*dt/p.m;
				balls[j].vx -= f*cos(theta)*dt/q.m;
				balls[j].vy -= f*sin(theta)*dt/q.m;
			}
			
			nI++;
		}
		printf("],");
		//printf("%d\n",cntr);
		if (cntr>999){
			done = true;
		}
		cntr++;
	}
	printf("]\n");
}
