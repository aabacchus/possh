images:
	mkdir -p images
compile:
	g++ pc-nographics-merge.cpp -o pc-nographics-merge
positions.txt: compile
	./pc-nographics-merge > positions.txt
frames: positions.txt images
	python p-graphicsonly.py
%.webm: frames
	ffmpeg -r 15 -i images/s_%04d.jpeg $@
