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

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/canvas"
)

const (
	n        int     = 1500
	width    int     = 800
	height   int     = 600
	dt       float64 = 0.1
	duration int     = 1000
	A        float64 = 50
	omega    float64 = 6
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
		particles[i] = newParticle(1.)
	}
	xWall := newWall(A, omega)

	go loop(myApp, wImg, img, particles, xWall)
	// anything after Run won't be run until the window is closed
	window.ShowAndRun()
}

func loop(myApp fyne.App, wImg *canvas.Image, img *image.Gray, particles []Particle, xWall *Wall) {
	//fmt.Printf("[")
	for frame := 0; frame < duration; frame++ {
		//fmt.Printf("[")
		draw.Draw(img, img.Bounds(), &image.Uniform{color.Black}, image.ZP, draw.Src)
		xWall = xWall.move(frame)
		for i := 0; i < n; i++ {
			//fmt.Printf("[%v,%v,%v],", particles[i].x, particles[i].y, particles[i].m)
			particles[i] = particles[i].move(dt)
			particles[i] = particles[i].wallBounce(xWall)

			for j := i + 1; j < n; j++ {
				var p Particle = particles[i]
				var q Particle = particles[j]
				var dx float64 = float64(p.x - q.x)
				var dy float64 = float64(p.y - q.y)
				var r float64 = math.Pow(dx*dx+dy*dy, 0.5)
				//if r > math.Sqrt(p.m/3.142)+math.Sqrt(q.m/3.142) {
				//	continue
				//}
				//var prevR float64 = math.Sqrt(math.Pow(dx-p.vx+q.vx, 2) + math.Pow(dy-p.vy+q.vy, 2))
				// previous-r calculation?
				//if prevR < r {
				//	continue
				//}
				if r < 0.01 {
					r = 0.01
				}
				var theta float64 = math.Atan2(dy, dx)

				/*// bounce functions are in particleComponent.py and particles.html

				pux := p.vx
				puy := p.vy
				particles[i].vx = pux*((p.m-q.m)/(p.m+q.m)) + (2 * q.vx * q.m / (p.m + q.m))
				particles[j].vx = q.vx + (pux-p.vx)*(p.m/q.m)

				particles[i].vy = puy*((p.m-q.m)/(p.m+q.m)) + (2 * q.vy * q.m / (p.m + q.m))
				particles[j].vy = q.vy + (puy-p.vy)*(p.m/q.m)*/

				var f float64 = 500 / (r * r)
				particles[i].vx += f * math.Cos(theta) * dt / p.m
				particles[i].vy += f * math.Sin(theta) * dt / p.m
				particles[j].vx -= f * math.Cos(theta) * dt / q.m
				particles[j].vy -= f * math.Sin(theta) * dt / q.m
			}

			// draw
			var tempColor color.Color
			if i%2 == 0 {
				tempColor = color.Gray{0x055}
			} else {
				tempColor = color.White
			}
			drawShapes.Circle(img, particles[i].x, particles[i].y, int(math.Round(math.Sqrt(particles[i].m/3.142))), tempColor)
			drawShapes.Rectangle(img, int(math.Round(xWall.A+xWall.pos)), 0, 10, height, color.White, false)
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

func (p Particle) wallBounce(xWall *Wall) Particle {
	if p.x > width {
		p.x = width
		p.vx *= -1
	} else if float64(p.x) < xWall.A+xWall.pos {
		p.x = int(math.Round(xWall.A+xWall.pos)) + 1
		p.vx = -p.vx + xWall.v
	}
	if p.y < 0 {
		p.y = 0
		p.vy *= -1
	} else if p.y > height {
		p.y = height
		p.vy *= -1
	}
	return p
}

type Wall struct {
	A     float64
	omega float64
	pos   float64
	v     float64
}

func newWall(A float64, omega float64) *Wall {
	var w = new(Wall)
	w.A = A
	w.omega = omega
	w = w.move(0)
	return w
}

func (w *Wall) move(t int) *Wall {
	w.pos = -w.A * math.Cos(w.omega*float64(t))
	w.v = w.A * w.omega * math.Sin(w.omega*float64(t))
	return w
}
