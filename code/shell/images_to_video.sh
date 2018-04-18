#!/bin/bash
module add openmind/singularity/2.4

CONT=/om/user/belledon/singularity_imported/blender.img 
DIR=$1
DEST=$2
SIM=$3
IDX=$4

cd $DIR$SIM
echo Converting images from $DIR${SIM[$ITER]}
echo mp4...
singularity exec -B /om2:/om2 $CONT ffmpeg -framerate 50 -i image%d.png -vf vflip -c:v libx264 -profile:v high -crf 20 -pix_fmt yuv420p video${IDX[$ITER]}.mp4
echo webm...
singularity exec -B /om2:/om2 $CONT ffmpeg -framerate 50 -i image%d.png -vf vflip -c:v libvpx-vp9 -b:v 2M -crf 20 -pix_fmt yuv420p video${IDX[$ITER]}.webm
mv video* $DEST
