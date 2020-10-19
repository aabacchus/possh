#include <stdio.h>
#include <math.h>
#include <iostream>
#include <cmath>
#include <array>
#include <time.h>
int Width = 1280;
int Height = 1061;
int n = 1500;
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
				//std::cout<<r<<std::endl;
				//std::cout << dx << "/" << dy << " -> " << theta<<std::endl;
				float f = -5*(r-7)*exp(0.1*(7-r));
				//if (r<20){ std::cout <<"FORCE for "<<i<<","<<j<<"= "<<f<<"    r="<<r<<std::endl;}
				balls[i].vx += f*cos(theta)*dt;
				balls[i].vy += f*sin(theta)*dt;
				balls[j].vx -= f*cos(theta)*dt;
				balls[j].vy -= f*sin(theta)*dt;
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

