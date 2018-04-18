'''
Renames images output from rendering on om in Moral Dynamics.

January 21, 2018
author: Felix Sosa
'''
import os
import re

dest = "../../../../data/MoralDynamics/exp1_figures"

for dirr, subdirs, files in os.walk("../../../../data/MoralDynamics/rendered_images"):
	# Traverse the files
	for file in files:
		# Make sure file is an image.png
		match = re.match("image0.png", file, re.I)

		if match:
			filename = dirr.split('/')[-1]
			new_dest = dest+'/'+filename
			print(new_dest)
			print(dirr,subdirs,file)
			# filename = "image"+str(new_idx)+".png"
			os.rename(dirr+"/"+file, new_dest)