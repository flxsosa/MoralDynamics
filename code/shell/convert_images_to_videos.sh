#!/bin/bash
cd ~/GitHub/MoralDynamics

for idx in `seq 2 2`;
do 
	python main.py $idx
	echo Running Simulation $idx in Moral Dynamics...
	echo Images generated...
	echo Beginning video conversion...
	echo mp4...
	ffmpeg -hide_banner -loglevel quiet -crf 0 -i image%d.png -pix_fmt yuv420p video$idx.mp4
	echo ogv...
	ffmpeg -hide_banner -loglevel quiet -framerate 50 -i image%d.png -pix_fmt yuv420p video$idx.ogv
	echo mov...
	ffmpeg -hide_banner -loglevel quiet -framerate 50 -i image%d.png -pix_fmt yuv420p video$idx.mov
	echo webm...
	ffmpeg -hide_banner -loglevel quiet -framerate 50 -i image%d.png -pix_fmt yuv420p video$idx.webm
	echo Cleaning up images...
	rm image*
	mv video* experiment_template/static/videos
	echo Done with simulation $idx...
done

echo Video creation complete!
