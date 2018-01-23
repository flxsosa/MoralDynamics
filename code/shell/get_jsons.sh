#!/bin/bash
cd ~/git/MoralDynamics/code/python

for idx in `seq 29 32`;
do 
	echo Running Simulation $idx in Moral Dynamics...
	python main.py $idx
	echo Json generated...
	echo Done with simulation $idx...
done

echo Json creation complete!