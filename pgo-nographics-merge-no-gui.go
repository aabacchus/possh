package main

import (
	"image"
	"image/color"
	"image/draw"
	"image/png"
	"log"
	"math"
	"math/rand"
	"me/drawShapes"
	"os"
	"strconv"
	"strings"
	"time"
)

const (
	n        int     = 1500
	width    int     = 800
	height   int     = 600
	dt       float64 = 0.1
	duration int     = 1000
	g        float64 = 100
)

func main() {
	// make image
	img := image.NewGray(image.Rectangle{image.Point{0, 0}, image.Point{width, height}})

	// make array
	rand.Seed(time.Now().UnixNano())
	particles := make([]Particle, n)
	for i, _ := range particles {
		particles[i] = newParticle(rand.Float64() * 5)
	}

	loop(img, particles)
}

func loop(img *image.Gray, particles []Particle) {
	//fmt.Printf("[")
	for frame := 0; frame < duration; frame++ {
		//fmt.Printf("[")
		draw.Draw(img, img.Bounds(), &image.Uniform{color.Black}, image.ZP, draw.Src)
		for i := 0; i < n; i++ {
			//fmt.Printf("[%v,%v,%v],", particles[i].x, particles[i].y, particles[i].m)
			if particles[i].m == 0 {
				continue
			}
			particles[i] = particles[i].move(dt)
			//particles[i] = particles[i].wallBounce()

			for j := i + 1; j < n; j++ {
				var p Particle = particles[i]
				var q Particle = particles[j]
				if q.m == 0 {
					continue
				}
				var dx float64 = float64(p.x - q.x)
				var dy float64 = float64(p.y - q.y)
				var r float64 = math.Pow(dx*dx+dy*dy, 0.5)
				if r <= math.Pow(p.m/3.142, 0.5)+math.Pow(q.m/3.142, 0.5) {
					var index int
					var other int
					if p.m > q.m {
						index = i
						other = j
					} else {
						index = j
						other = i
					}
					particles[index].vx = (p.vx*p.m + q.vx*q.m) / (p.m + q.m)
					particles[index].vy = (p.vy*p.m + q.vy*q.m) / (p.m + q.m)
					particles[index].m = p.m + q.m
					particles[other].m = 0
					continue
				}
				var theta float64 = math.Atan2(dy, dx)
				//var f float64 = -5 * (r - 7) * math.Exp(0.1*(7-r))
				var f float64 = -g * p.m * q.m / (r * r)
				particles[i].vx += f * math.Cos(theta) * dt / p.m
				particles[i].vy += f * math.Sin(theta) * dt / p.m
				particles[j].vx -= f * math.Cos(theta) * dt / q.m
				particles[j].vy -= f * math.Sin(theta) * dt / q.m
			}

			// draw
			//img.Set(particles[i].x, particles[i].y, color.White)
			drawShapes.Circle(img, particles[i].x, particles[i].y, int(math.Round(math.Sqrt(particles[i].m/3.142))), color.White)
		}
		//fmt.Printf("],\n")

		fname := strconv.Itoa(frame)
		fname = strings.Repeat("0", 4-len(fname)) + fname

		f, err := os.Create("images/s_" + fname + ".png")
		if err != nil {
			log.Fatal(err)
		}
		png.Encode(f, img)
	}
	//fmt.Printf("]\n")
	//myApp.Quit()

}

type Particle struct {
	x  int
	y  int
	m  float64
	vx float64
	vy float64
}

func newParticle(m float64) Particle {
	var p = new(Particle)
	p.m = m
	p.x = rand.Int() % width
	p.y = rand.Int() % height
	p.vx = (rand.Float64() - 0.5) * 60
	p.vy = (rand.Float64() - 0.5) * 60
	return *p
}

func (p Particle) move(dt float64) Particle {
	p.x += int(math.Round(p.vx * dt))
	p.y += int(math.Round(p.vy * dt))
	return p
}

func (p Particle) wallBounce() Particle {
	if p.x >= width-int(p.m) {
		p.x = width - int(p.m)
		p.vx *= -1
	} else if p.x <= int(p.m) {
		p.x = int(p.m)
		p.vx *= -1
	}
	if p.y <= int(p.m) {
		p.y = int(p.m)
		p.vy *= -1
	} else if p.y >= height-int(p.m) {
		p.y = height - int(p.m)
		p.vy *= -1
	}
	return p
}
