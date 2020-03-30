#!/usr/bin/env python3
""" 
run_modelling.py<br>
python 3.6.7<br>
Description:<br>
@author: Lisa Stubert<br>
@date: 2019-05-30<br>
"""

from set_data_paths import data_input
from modules.process import modelling_process

################## Set the combinations and parameters for the model here #####

# insert all combinations of predictor variables, used to calculate models (as dictionary)
combinations = {
    "example": ['t_slope', 't_wind', 't_insola', 'c_coast', 'c_prim_set'],
}

# set parameters 
buffer_sizes = ['50','100'] # set the size(s) of your buffered site location(s)
# set the weighting(s) that should be used
weightings = ['w1','w2'] # w0 = no weighting, w1 = weighting with IQRnorm, w2 = weighting wE after Ejstrud, w3 = weighting after Saaty

# set thresholds if you want to calculate models by automated variable selection (if you want to calculate models by experts selection, set statistic threshold to 100 and correlation threshold to 1) 
statistic_thresholds = [100]
statistic_threshold_types = ['iqr_norm'] 
corr_thresholds = [1]

# set cross-validation on or off, if validation is deactivated, the calculation duration is shortened
test = False  # True or False
 

##################Start modelling ###########################################

# loading the paths to the data
all_raster_data, buffer_dir, working_dir = data_input()

# loop over predictore variable combinations, buffers and weightings
for combination, variables in combinations.items():
        for buffer_size in buffer_sizes:
                for weighting in weightings:
                        for statistic_threshold in statistic_thresholds:
                            for corr_threshold in corr_thresholds:
                                for statistic_threshold_type in statistic_threshold_types:
                                    # give all parameters to the modelling function
                                    modelling_process(buffer_size, weighting,statistic_threshold,corr_threshold,statistic_threshold_type, all_raster_data, variables, combination, test, working_dir, buffer_dir)

print("No combinations left. Calculation finished")