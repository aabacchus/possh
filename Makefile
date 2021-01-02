images:
	mkdir -p images
compile:
	g++ pc-nographics-merge.cpp -o pc-nographics-merge.bin
positions.txt: compile
	./pc-nographics-merge.bin > positions.txt
frames: positions.txt images
	python p-graphicsonly.py
%.webm: frames
	ffmpeg -r 15 -i images/s_%04d.jpeg $@
