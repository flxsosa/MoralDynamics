#!/bin/bash
cd ~/git/MoralDynamics/code/python

for idx in `seq 1 24`;
do 
	echo Running Simulation $idx in Moral Dynamics...
	python main.py $idx
	echo Json generated...
	echo Done with simulation $idx...
done

echo Json creation complete!
