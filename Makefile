images:
	mkdir -p images
compile:
	g++ pc-nographics-salt.cpp -o pc-nographics-salt
positions.txt: compile
	./pc-nographics-salt > positions.txt
frames: positions.txt images
	python p-graphicsonly.py
%.webm: frames
	ffmpeg -r 15 -i images/s_%04d.jpeg -start_number 001 $@
