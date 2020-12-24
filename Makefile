compile:
	g++ pc-nographics-salt.cpp -o pc-nographics-salt
positions.txt: compile
	./pc-nographics-salt > positions.txt
images: positions.txt
	python p-graphicsonly.py
%.webm: images
	ffmpeg -r 15 -i images/s_%04d.jpeg -start_number 001 $@
