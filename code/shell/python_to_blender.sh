#!/bin/bash

for idx in `seq 1 1`;
do
	cd ~/GitHub/MoralDynamics/code/python
	python main.py $idx
	echo Running Simulation $idx in Moral Dynamics and gathering kinematics...
	mv simulation.json ../Blender
	cd ../Blender
	blender --background convert_2d_to_3d.blend --python animation.py
done
