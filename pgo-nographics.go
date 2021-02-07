package main

import (
	"image"
	"image/color"
	"image/draw"
	"image/png"
	"log"
	"math"
	"math/rand"
	"os"
	"strconv"
	"strings"
	"time"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/canvas"
)

const (
	n        int     = 1500
	width    int     = 800
	height   int     = 600
	dt       float64 = 0.1
	duration int     = 100
)

func main() {
	// make image
	img := image.NewGray(image.Rectangle{image.Point{0, 0}, image.Point{width, height}})

	// initialiase gui
	myApp := app.New()
	window := myApp.NewWindow("Particle simulation")
	wImg := canvas.NewImageFromImage(img)
	wImg.FillMode = canvas.ImageFillOriginal
	window.SetContent(wImg)

	// make array
	rand.Seed(time.Now().UnixNano())
	particles := make([]Particle, n)
	for i, _ := range particles {
		particles[i] = newParticle(10.)
	}

	go loop(myApp, wImg, img, particles)
	// anything after Run won't be run until the window is closed
	window.ShowAndRun()
}

func loop(myApp fyne.App, wImg *canvas.Image, img *image.Gray, particles []Particle) {
	//fmt.Printf("[")
	for frame := 0; frame < duration; frame++ {
		//fmt.Printf("[")
		draw.Draw(img, img.Bounds(), &image.Uniform{color.Black}, image.ZP, draw.Src)
		for i := 0; i < n; i++ {
			//fmt.Printf("[%v,%v,%v],", particles[i].x, particles[i].y, particles[i].m)
			particles[i] = particles[i].move(dt)
			particles[i] = particles[i].wallBounce()

			for j := i + 1; j < n; j++ {
				var p Particle = particles[i]
				var q Particle = particles[j]
				var dx float64 = float64(p.x - q.x)
				var dy float64 = float64(p.y - q.y)
				var r float64 = math.Pow(dx*dx+dy*dy, 0.5)
				var theta float64 = math.Atan2(dy, dx)
				var f float64 = -5 * (r - 7) * math.Exp(0.1*(7-r))
				particles[i].vx += f * math.Cos(theta) * dt
				particles[i].vy += f * math.Sin(theta) * dt
				particles[j].vx -= f * math.Cos(theta) * dt
				particles[j].vy -= f * math.Sin(theta) * dt
			}

			// draw
			img.Set(particles[i].x, particles[i].y, color.White)
		}
		//fmt.Printf("],\n")
		wImg.Refresh()

		fname := strconv.Itoa(frame)
		fname = strings.Repeat("0", 4-len(fname)) + fname

		f, err := os.Create("images/s_" + fname + ".png")
		if err != nil {
			log.Fatal(err)
		}
		png.Encode(f, img)
	}
	//fmt.Printf("]\n")
	myApp.Quit()

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
