 #!/usr/bin/env python3
""" 
run_modelling.py<br>
python 3.6.7<br>
Description:<br>
@author: Lisa Stubert<br>
@date: 2019-05-30<br>
"""

import json
import geopandas as gpd
import pandas as pd
from sklearn.model_selection import KFold
from subprocess import call
from os import path

# Load own functions, this are the modules for calculating the model
from set_data_paths import rasterfilter
from modules.average_raster_values import average_raster_values
from modules.boxplots import boxplots
from modules.reclassify_rasters import reclassify_rasters
from modules.weighting import weighting_calculation
from modules.prediction import prediction
from modules.validation import validation
from modules.gain_statistics import gain
 
 
def modelling_process(buffer_size, weighting,statistic_threshold,corr_threshold,statistic_threshold_type, all_raster_data, variables,combination, test, working_dir, buffer_dir):
    # make a subset of only the current predictore variable combination
    raster_data = rasterfilter(all_raster_data, variables)
    iqr_start = statistic_threshold
    corr_start = corr_threshold
    # generate a name for the currently calculated model
    result_name = "{}_{}m_{}_{}_{}_{}_{}".format(
        combination, buffer_size,  weighting,  iqr_start, corr_start,statistic_threshold_type, test)
    # load json-file including names of already calculated combinations
    already_done = json.loads(
        open(working_dir + 'calculated_combinations.json').read())      
    # skip over already calculated combinations
    if result_name in already_done.keys():
        print("This combination of variables and parameters was already calculated. Skip to the next combination.\n")

    else:
        # import the shapefile of buffers
        buffer_shapefile = gpd.read_file(
            working_dir + 'data/' + buffer_dir + buffer_size + '_m_sites.shp')
        print(working_dir + 'data/' + buffer_dir + buffer_size + '_m_sites.shp')
        # prepare empty variables to be filled with data
        x_list = []
        y_list = []
        value_list = []
        percent_good_prediction = None
        gdf = None
        result_gdf = gpd.GeoDataFrame({'suitability_value': [0,0], 'geometry': [0,0] })

        print('\n Calculating model: ' + str(result_name))
        print('Predictore variable rasters: ' + str(raster_data.keys()) + '\n')

        # start model calculation
        traindata = buffer_shapefile
        testdata = buffer_shapefile
        # get raster values within buffers
        average_raster_values(
            working_dir, raster_data, result_name, traindata)

        raster_selection, correlation_matrix, df_boxplots_results  = boxplots(
            working_dir, result_name, raster_data, statistic_threshold, corr_threshold, statistic_threshold_type)

        raster_data = rasterfilter(
            raster_data, raster_selection)

        reclassify_rasters(
            working_dir,  raster_data, result_name, df_boxplots_results)

        weighting_calculation(working_dir, result_name, df_boxplots_results )

        prediction(working_dir, raster_data,
                weighting, buffer_size, result_name)

        gain_df = gain(working_dir, result_name,
                    buffer_shapefile)

        print('Calculation of model ' +
            str(result_name) + ' is finished.\n')

        # if validation is turned on, data is splitted in subsets for crossvalidation
        if test is True:
            # prepare empty variables to be filled with data
            x_list = []
            y_list = []
            value_list = []
            percent_good_prediction = None
            gdf = None
            result_gdf = gpd.GeoDataFrame(
                {'suitability_value': [0, 0], 'geometry': [0, 0]})
            # set threshold very high, to be sure that the same rasters are used for the crossvalidation model as in the 'normal' model
            statistic_threshold = 100
            corr_threshold = 1

            print('\n Start crossvalidation: ')

            kf = KFold(n_splits=5, random_state=None)
            repeat_index = 0
            # loop over the 5 subsets
            for train_index, test_index in kf.split(buffer_shapefile):
                repeat_index += 1
                # print("Train:", train_index, "Validation:", test_index)
                # get the current train- and testdata buffers
                traindata, testdata = buffer_shapefile.loc[train_index], buffer_shapefile.loc[test_index]
                # print(traindata)
                # print(testdata)

                # model calculation for current combination starts
                # get raster values within buffers
                average_raster_values(working_dir,  raster_data, result_name, traindata)

                raster_selection, correlation_matrix, df_boxplots_results  = boxplots(working_dir, result_name, raster_data, statistic_threshold, corr_threshold, statistic_threshold_type)

                reclassify_rasters(working_dir,  raster_data, result_name, df_boxplots_results )

                weighting_calculation(working_dir, result_name, df_boxplots_results )

                prediction(working_dir, raster_data, weighting, buffer_size, result_name)

                x_list, y_list, value_list, percent_good_prediction, result_gdf = validation(working_dir, result_name, testdata, x_list, y_list, value_list)
                print('Round ' + str(repeat_index) + ' of 5 from crossvalidation finished')

        if test is False:
            x_list, y_list, value_list, percent_good_prediction, result_gdf = validation(
                working_dir, result_name, testdata, x_list, y_list, value_list)
            print(str(percent_good_prediction) +
                ' percent of data is located in suitability area > 0.5\n')


        weighting_df = pd.read_excel(working_dir +'/results/statistics/weighting' + result_name + '.xlsx', sheet_name='Sheet1')
        # write model parameters, correlation matrix and validation output to text file
        file = open(working_dir + 'results/info_and_validation_' + result_name + '.txt', 'w')
        file.write('Model name: \n')
        file.write(str(result_name) + '\n \n')
        file.write('Parameters: \n')
        for item in raster_data:
            file.write(
                item + ' * ' + str(weighting_df[item][weighting]) + '\n')
        #if test is False:
        #    file.write('Correlation:\n')
        #    file.write(str(correlation_matrix) + '\n')
        if test is True:
            file.write('\nCross-validation results: \n')
            file.write(str(result_gdf[['suitability_value', 'geometry']]) + '\n \n')
        gain_075 = (gain_df.iloc[8]['gain'])
        file.write(str(percent_good_prediction) +
                    ' percent of data is located in suitability area > 0.5 \n\n')
        #file.write('Gain values of suitability areas > 0.8: ' + str(gain_over_08) + '\n\n')
        file.write('Gain statistics: \n')
        file.write(str(gain_df))
        file.close()

        gain_df.to_excel(
            working_dir +
            'results/gain' + result_name + '.xlsx')

        # delete the no longer required reclassified rasters
        #call(['rm', '-r', working_dir + 'tmp/sites_with_rastervalues/*'])

        # delete result rasters and shapefiles
        #call(['rm', working_dir + 'results/suitability_result' + result_name + '_resampled_cut.tif'])
        #call(['rm', '-r', working_dir + 'results/suitability_shapefiles/*'])
        #call(['rm', '-r', working_dir + 'results/statistics/*'])

        # save results in excel
        new_results = pd.DataFrame({'Combination name': combination, 'buffer size': buffer_size, 'weighting': weighting, 'statistic_threshold': iqr_start, 'corr_threshold': corr_start, 'crossvalidation active': test, 'rasters': [raster_selection], 'percent good prediction': percent_good_prediction, 'gain_0.5': gain_df.iloc[5]['gain'],
        'gain_0.75': gain_075, 'statistic threshold type': statistic_threshold_type
        })

        if path.exists(working_dir + 'results/results.xlsx'):
            all_results = pd.read_excel(working_dir + 'results/results.xlsx')
            all_results = all_results.append(
                new_results, ignore_index=True)
            all_results.to_excel(working_dir + 'results/results.xlsx')
        else:
            new_results.to_excel(
                working_dir + 'results/results.xlsx')

        # add entry with current model name and prediction value to json-file
        already_done[result_name] = percent_good_prediction,  gain_df.iloc[5]['gain'], gain_075
        with open(working_dir + 'calculated_combinations.json', 'w') as outfile:
            json.dump(already_done, outfile)
