'''
Runs factual and counterfactual simulations and records
data from them.

Felix Sosa
'''
import csv
from counterfactual import run_csm

from moral_kinematics_scenarios import long_distance, dodge, bystander, \
							  stays_put, short_distance, med_push, long_push, \
							  push_patient, double_push

from counter_scenarios import med_push_fireball, long_push_patient_moving, \
							  long_push_fireball_moving, push_against_patient, push_against_fireball, \
							  push_patient_oncoming, push_fireball_oncoming, fireball_walks_away, \
							  patient_walks_away

# from experiment_4_scenarios_good import good_1, good_2, good_3, good_4, good_5, \
# 							  good_6, good_7, good_8, good_9, good_10, good_11, good_12

# from experiment_4_scenarios_bad import short_distance_fireball, short_distance_patient, \
# 							  push_against_fireball, push_against_patient, bystander_patient, \
# 							  bystander_fireball, long_push_fireball_moving, long_push_patient_moving, \
# 							  stays_put_fireball, stays_put_patient, bump_fireball, bump_patient

# List of scenarios from each of the types
moral_kinematics_scenarios = [long_distance, dodge, bystander,
							  stays_put, short_distance, med_push, long_push,
							  push_patient, double_push]
counter_scenarios = [med_push_fireball, long_push_patient_moving, long_push_fireball_moving,
							  push_against_patient, push_against_fireball, push_patient_oncoming, 
							  push_fireball_oncoming, fireball_walks_away, patient_walks_away]
# experiment_4_scenarios_good =[good_1, good_2, good_3, good_4, good_5, good_6, good_7, 
# 							  good_8, good_9, good_10, good_11, good_12]
# experiment_4_scenarios_bad = [short_distance_fireball, short_distance_patient, push_against_fireball,
# 							  push_against_patient, bystander_patient, bystander_fireball, 
# 							  long_push_fireball_moving, long_push_patient_moving, 
# 							  stays_put_fireball, stays_put_patient, bump_fireball, 
# 							  bump_patient]

# Create list of lists of scenarios
# list_of_scenarios = [moral_kinematics_scenarios, counter_scenarios, experiment_4_scenarios_good,
# 					 experiment_4_scenarios_bad]
# list_of_scenarios = [moral_kinematics_scenarios]
list_of_scenarios = [counter_scenarios]
# list_of_scenarios = [experiment_4_scenarios_good]
# list_of_scenarios = [experiment_4_scenarios_bad]

# Names of lists
# names = ['mk', 'counter', 'exp_4_good', 'exp_4_bad']
# names = ['exp_4_good']
names = ['counter']
# names = ['mk']
# names = ['exp_4_bad']

# # # Iterate through list of scenarios and record effort values
# i = 0
# for scene_list in list_of_scenarios:
# 	effort_values = []
# 	scenarios = []
# 	# Append lists with appropriate values
# 	for scene in scene_list:
# 		effort_values.append(scene(False))
# 		scenarios.append(scene.__name__)
# 	# Write effort values to csv file
# 	results_csv = open('effort_'+names[i]+'_planning.csv','w')
# 	keys = scenarios
# 	writer = csv.DictWriter(results_csv, fieldnames = ['scenario', 'effort'])
# 	writer.writeheader()
# 	# Write the results dictionary to a csv file
# 	for j in range(len(scenarios)):#keys:
# 		writer.writerow({'scenario':scenarios[j],'effort':effort_values[j]})
# 	# Close the csv file
# 	results_csv.close()
# 	i+=1

# Iterate through list of scenarios and record counterfactual values
for sd in range(1,16):
	i = 0
	# 10
	noise = [0,(sd*0.1)]
	num_times = 100
	for scene_list in list_of_scenarios:
		counterfactual_values = []
		scenarios = []
		# Append lists with appropriate values
		for scene in scene_list:
			counterfactual_values.append(run_csm(scene,False,noise,num_times))
			scenarios.append(scene.__name__)
		# Write counterfactual values to csv file
		results_csv = open('counterfactual_'+names[i]+'_planning_'+str((sd*0.1))+'.csv','w')
		keys = scenarios
		writer = csv.DictWriter(results_csv, fieldnames = ['scenario', 'counterfactual'])
		writer.writeheader()
		# Write the results dictionary to a csv file
		for j in range(len(scenarios)):#keys:
			writer.writerow({'scenario':scenarios[j],'counterfactual':counterfactual_values[j]})
		# Close the csv file
		results_csv.close()
		i+=1