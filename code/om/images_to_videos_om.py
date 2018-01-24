import argparse
import slurm as om
import os
from fileFuncs import ff

# images = "/om2/user/fsosa/data/MoralDynamics/rendered_images/"
# videos = "/om2/user/fsosa/data/MoralDynamics/videos/"
# script = "/om2/user/fsosa/git/MoralDynamics/code/shell/test.sh"
sims = ["short_distance_v1", "medium_distance_v2", "long_distance_v1", "static",
 	"slow_collision", "fast_collision", "dodge", "double_push", "medium_push",
  	"long_push", "victim_moving_static", "no_touch", "victim_moving_moving",
  	"victim_moving_static", "victim_static_moving", "victim_static_static", 
  	"harm_moving_moving", "harm_moving_static", "harm_static_moving", "harm_static_static",
  	"sim_1_patient", "sim_1_fireball", "sim_2_patient", "sim_2_fireball", "sim_3_patient", 
  	"sim_3_fireball", "sim_4_patient", "sim_4_fireball", "agent_walks_to_fireball", 
  	"patient_walks_to_fireball", "fireball_moving", "agent_saves_patient"]
idx = range(1,33)

def main():

	parser = argparse.ArgumentParser(
		description="Submits batch jobs for rendering Moral Dynamics stims")
	
	# Expected args in command line
	parser.add_argument("script", type = str,
		help = "Shell script for converting images")
	parser.add_argument("imagedir", type = str,
		help = "Directory containing image folders")
	parser.add_argument('videodir', type = str,
		help = "Path to converted videos")
	
	# Initializes the slurm arguments:
	# Type: python moral_dynamics_om.py --help to see info
	# Expected positional args in order are jsondir container
	# Expected optional ards are --blend --python
	args = om.slurm.args(parser).parse_args()
	
	# check to see if blender file exists
	# if not ff.isFile(args.script):
	# 	raise ValueError("File {} did not exist".format(args.script))

	# create a tuple of iteration-specific arguments for each job in the array
	# the blender file is repeated in this case because this is
	# a postional argument for the base script. this could be a flag.
	jobs = [(simulation, index) for simulation,index in zip(sims,idx)]
	nFiles = len(sims)
	print(jobs)
	print("Found {} simulation images in {}".format(nFiles, args.imagedir))

	# flags do not change accross jobs (so they are copied for each job)
	flags = [] #["-s {}".format(args.steps)]
	# flags.append("-o {}".format(args.destination))
	# if args.frames is not None:
	# 	flags.append("-f {}".format(" ".join(map(str,args.frames))))

	interpreter = '#!/bin/bash'
	modules = []#'openmind/singularity/2.4']
	exports = []
        
	# This is equivalent to the job template
	func = '{0} {1} {2}'.format(args.script,
		args.imagedir, args.videodir)

	batch = om.slurm.Batch(interpreter, modules, exports, func, jobs, flags,
			args)

	batch.run()

	print("Submitted under {}".format(batch.jobArray))

if __name__ == '__main__':
	main()
