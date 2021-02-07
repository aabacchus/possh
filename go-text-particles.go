package main

import (
	"fmt"
	"math"
	"math/rand"
	"time"
)

const (
	n        int     = 1
	width    int     = 1000
	height   int     = 1000
	dt       float64 = 0.1
	duration int     = 10
)

func main() {
	// make array
	rand.Seed(time.Now().UnixNano())
	particles := make([]Particle, n)
	for i, _ := range particles {
		particles[i] = newParticle(10.)
	}

	loop(particles)
}

func loop(particles []Particle) {
	//var p = newParticle(10.)
	fmt.Printf("[")
	for frame := 0; frame < duration; frame++ {
		fmt.Printf("[")
		for i := 0; i < len(particles); i++ {
			//fmt.Println(particles[i].x)
			particles[i] = particles[i].move(dt)
			particles[i] = particles[i].wallBounce()
			//fmt.Println(particles[i].x)
			fmt.Printf("[%v,%v,%v],", particles[i].x, particles[i].y, particles[i].m)
		}
		fmt.Printf("],\n")
	}
	fmt.Printf("]\n")

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
	if p.x >= width {
		p.x = width
		p.vx *= -1
	} else if p.x <= 0 {
		p.x = 0
		p.vx *= -1
	}
	if p.y <= 0 {
		p.y = 0
		p.vy *= -1
	} else if p.y >= height {
		p.y = height
		p.vy *= -1
	}
	return p
}
