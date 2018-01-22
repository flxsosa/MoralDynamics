import argparse
import slurm as om
import os


# Path to blend file. Contained in the git repo /git/MoralDynamics/om/
blend = ff.join(ff.step(ff.absPath(__file__), -2), ff.join("./",
	"convert.blend"))

# Path to python file that will render one scene at a time.
# Contained in the git repo /git/MoralDynamics/om/
# This is iterated over in each job of the job-array
py = ff.join(ff.step(ff.absPath(__file__), -2), ff.join("./",
	"animation.py"))

def main():

	parser = argparse.ArgumentParser(
		description="Submits batch jobs for rendering Moral Dynamics stims")
	
	# Expected args in command line
	# jsondir is contained in git repo /git/MoralDynamics/om/jsons/
	parser.add_argument("jsondir", type = str,
		help = "Directory containing json files")
	parser.add_argument('blender', type = str,
		help = "Path to blender executable")
	parser.add_argument("--blend", "-b", type=str, default=blend,
        help = "Path to blender file. Default :".format(blend))
	parser.add_argument("--python", "-p", type=str, default=py,
		      help = "Path to python file. Default :".format(py))
	
	# Initializes the slurm arguments:
	# Type: python moral_dynamics_om.py --help to see info
	# Expected positional args in order are jsondir container
	# Expected optional ards are --blend --python
	args = om.slurm.args(parser).parse_args()
	
	# check to see if blender file exists
	if not ff.isFile(args.blend):
		raise ValueError("File {} did not exist".format(args.blend_file))

	# find the json files from the input path
	files = ff.find(args.jsondir, "*.json")

	# create a tuple of iteration-specific arguments for each job in the array
	# the blender file is repeated in this case because this is
	# a postional argument for the base script. this could be a flag.
	jobs = [(args.blend, file) for file in files]
	nFiles = len(files)

	print("Found {} simulation jsons in {}".format(nFiles, args.jsondir))

	# flags do not change accross jobs (so they are copied for each job)
	flags = [] #["-s {}".format(args.steps)]
	flags.append("-o {}".format(args.destination))
	if args.frames is not None:
		flags.append("-f {}".format(" ".join(map(str,args.frames))))

	interpreter = '#!/bin/bash'
	modules = ['openmind/singularity/2.4']
	exports = []
        
	# This is equivalent to the job template
	func = '{0} --background {1} --python {2}'.format(args.blender,
		args.blend, args.py)

	batch = om.slurm.Batch(interpreter, modules, exports, func, jobs, flags,
			args)

	batch.run()

	print("Submitted under {}".format(batch.jobArray))

if __name__ == '__main__':
	main()
