'''
Renames images output from rendering on om in Moral Dynamics.

January 21, 2018
author: Felix Sosa
'''
import os
import re

for dirr, subdirs, files in os.walk("../../../../data/MoralDynamics/rendered_images/nameless"):
	# Traverse the files
	for file in files:
		# print(dirr,file)
		# Make sure file is an image.png
		match = re.match(r"([a-z]+)([0-9]+).([a-z]+)", file, re.I)
		if match:
			# Parse the filename into types
			items = match.groups()
			# If the image is of an animation
			if len(str(items[1])) > 3:
				print(file)
				if (len(str(items[1])) == 7):
					idx = int(str(items[1])[:3])
					inc = int(str(items[1])[3:])
					new_idx = idx+inc
					filename = "image"+str(new_idx)+".png"
					os.rename(dirr+"/"+file,dirr+"/"+filename)
				elif (len(str(items[1])) == 6):
					idx = int(str(items[1])[:2])
					inc = int(str(items[1])[2:])
					new_idx = idx+inc
					filename = "image"+str(new_idx)+".png"
					os.rename(dirr+"/"+file,dirr+"/"+filename)
