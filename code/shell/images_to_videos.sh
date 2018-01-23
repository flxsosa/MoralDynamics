
module add openmind/singularity/2.4

CONT=/om/user/belledon/singularity_imported/blender.img
singularity exec -B /om2:/om2 $CONT ffmpeg 

for 
do
	singularity exec -B /om2:/om2 $CONT ffmpeg 
done