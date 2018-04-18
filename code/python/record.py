'''
Execute and record values from scenarios.

Felix Sosa
March 8, 2018
'''
import matplotlib.pyplot as plt
import csv

from moral_kinematics_scenarios import long_distance, dodge, bystander, \
									   stays_put, short_distance, med_push, \
									   long_push, push_patient, double_push
from counter_scenarios import med_push_fireball, long_push_patient_moving, \
							 long_push_fireball_moving, push_against_patient, \
							 push_against_fireball, push_patient_oncoming, \
							 push_fireball_oncoming, fireball_walks_away, \
							 patient_walks_away
# List of effort values and scenario names
effort_values = []
scenarios = []
# Append lists with appropriate values
effort_values.append(long_distance(False))
scenarios.append(long_distance.__name__)
effort_values.append(dodge(False))
scenarios.append(dodge.__name__)
effort_values.append(bystander(False))
scenarios.append(bystander.__name__)
effort_values.append(stays_put(False))
scenarios.append(stays_put.__name__)
effort_values.append(short_distance(False))
scenarios.append(short_distance.__name__)
effort_values.append(med_push(False))
scenarios.append(med_push.__name__)
effort_values.append(long_push(False))
scenarios.append(long_push.__name__)
effort_values.append(push_patient(False))
scenarios.append(push_patient.__name__)
effort_values.append(double_push(False))
scenarios.append(double_push.__name__)
effort_values.append(med_push_fireball(False))
scenarios.append(med_push_fireball.__name__)
effort_values.append(long_push_patient_moving(False))
scenarios.append(long_push_patient_moving.__name__)
effort_values.append(long_push_fireball_moving(False))
scenarios.append(long_push_fireball_moving.__name__)
effort_values.append(push_against_patient(False))
scenarios.append(push_against_patient.__name__)
effort_values.append(push_against_fireball(False))
scenarios.append(push_against_fireball.__name__)
effort_values.append(push_patient_oncoming(False))
scenarios.append(push_patient_oncoming.__name__)
effort_values.append(push_fireball_oncoming(False))
scenarios.append(push_fireball_oncoming.__name__)
effort_values.append(fireball_walks_away(False))
scenarios.append(fireball_walks_away.__name__)
effort_values.append(patient_walks_away(False))
scenarios.append(patient_walks_away.__name__)
# Write effort values to csv file
results_csv = open('effort_values_planning.csv','w')
keys = scenarios
writer = csv.DictWriter(results_csv, fieldnames = ['scenario', 'effort'])
writer.writeheader()
# Write the results dictionary to a csv file
for i in range(len(scenarios)):#keys:
	writer.writerow({'scenario':scenarios[i],'effort':effort_values[i]})
# Close the csv file
results_csv.close()
# Plot effort
plt.bar(range(len(effort_values)),effort_values, 
		align='center', color='lightblue',linewidth=2)
plt.xticks(range(len(scenarios)),scenarios,rotation=40)
plt.xlabel("Scenario")
plt.ylabel("Effort Expended by Agent")
plt.tight_layout()
plt.show()