""" 
boxplots.py<br>
python 3.6.7<br>
Definition of a function to get raster values within buffers<br>
@author: Lisa Stubert<br>
@date: 2019-05-30<br>
"""

import numpy as np
import pandas as pd
import geopandas as gpd
import statistics
import matplotlib.pyplot as plt
from sklearn.model_selection import RepeatedKFold
import rasterio
import math
import seaborn as sns


def boxplots(working_dir, result_name, raster_data, statistic_threshold, corr_threshold, statistic_threshold_type):
    """ Create boxplots and check predictor variables for correlation
    
    This script takes the average values, calculated by function 1 and prints 
    a boxplot. It also normalizes the values for better comparability and 
    prints a boxplot of this values. In another task it reclassifies the values on the basis of their statistics in three classes: 0, 1, 2. The result is a a shapefile of the sites, extended by the reclassified values and a table with the boxplots statistics.
    Additionally the script calculates Pearson correlation values and saves a 
    figure of the correlation matrix.

    Parameters
    ----------
    working_dir: str
        Working directory
    result_name: str
        Name of the model
    raster_data: dict
    statistic_threshold: int
    corr_threshold: int
    statistic_threshold_type: str

    Return
    ------
    selection_list: list
        Selection of raster that will be used for the model, because they have an iqr_norm lower than the threshold
    correlation_matrix: array
        Contains the pearson correlation values
    df_boxplot_statistics: dataframe
        Contains calculated boxplot statistics

    Note
    ----
    This is the second function called by the run_model.py script as a substep of calculating the predictive model. It needs a shapefile located in working_dir + 'tmp/sites_with_rastervalues/'.
    The output files are saved as follows.

    Type: Excelsheet xlsx
    File location: '/results/statistics/'
    File name: 'Boxplot_statistics_' + result_name

    Type: .png
    File location: working_dir + 'results/statistics/'
    File name: 'Boxplot' + result_name

    Type: .png
    File location: working_dir + 'results/statistics/'
    File name: 'Correlation_matrix' + result_name
    """

    # import the shapefile of buffers with the average values of rasters, generated with average_raster_values.py
    shapefile = gpd.read_file(working_dir +
                            'tmp/sites_with_rastervalues/sites_with_rastervalues_' + result_name + '.shp')
    # calculation of boxplot statistics, normalized values and reclassified values
    # prepare empty lists and dataframes, they will be filled with the calculated normalized values
    variable_list = []
    norm_variable_list = []
    key_list = []
    df_boxplot_statistics = pd.DataFrame()
    df_reclass = pd.DataFrame()

    # iterate over the columns in the shapefile, which include the average or median raster values
    for key, values in shapefile.items():
        if key in ['x', 'y', 'geometry']:
            continue
        # save values in list
        variable_list.append(values)
        key_list.append(key)
        # calculation of the normalized values
        norm_variable_list0 = []
        for value in values:
            # append the normalized value to list
            norm_variable_list0.append((value - min(values))/(max(values)-min(values)))
        # append this list to another list, to print boxplots of all predictor variables later
        norm_variable_list.append(norm_variable_list0)

        raster = rasterio.open(working_dir + "data/"+ raster_data[key]['path'])
        raster_array = raster.read(masked=True)
        raster_min = raster_array.min()
        raster_max = raster_array.max()
        raster_range = raster_max - raster_min

        # calculation of statistics for the not normalized values
        median = np.median(values)
        upper_quartile75 = np.percentile(values, 75)
        lower_quartile25 = np.percentile(values, 25)
        upper_percentile87_5 = np.percentile(values, 87.5)
        lower_percentile12_5 = np.percentile(values, 12.5)
        #iqr = upper_percentile87_5 - lower_percentile12_5
        iqr = upper_quartile75 - lower_quartile25
        #iqr_n = iqr * 0.7413
        std_dev = statistics.stdev(values)
        range_ = max(values)-min(values)
        #raster_range = raster_max - raster_min
        w2 = math.sqrt(1 / (std_dev / range_))
        w2_modified = math.sqrt(1 / (std_dev / raster_range))

        # calculation of statistics for the normalized values
        upper_quartile75_norm = np.percentile(norm_variable_list0, 75)
        lower_quartile25_norm = np.percentile(norm_variable_list0, 25)
        upper_percentile87_5_norm = np.percentile(norm_variable_list0, 87.5)
        lower_percentile12_5_norm = np.percentile(norm_variable_list0, 12.5)
        #iqr_norm = upper_percentile87_5_norm - lower_percentile12_5_norm
        iqr_norm = upper_quartile75_norm - lower_quartile25_norm
        std_dev_norm = statistics.stdev(norm_variable_list0)
        median_norm = np.median(norm_variable_list0)

        # save all statistics in a dataframe
        dataframe_this_key = pd.DataFrame({
            key: {
                'max' : max(values),
                'min': min(values),
                'median': median,
                'median_norm': median_norm,
                'upper_quartile75': upper_quartile75,
                'lower_quartile25': lower_quartile25,
                'upper_percentile87.5': upper_percentile87_5,
                'lower_percentile12.5': lower_percentile12_5,
                'iqr': iqr,
               # 'iqr_n': iqr_n,
                'std_dev': std_dev,
                'std_dev_norm': std_dev_norm,
                'range': range_,
                'iqr_norm': iqr_norm,
                'upper_percentile87.5_norm': upper_percentile87_5_norm,
                'lower_percentile12.5_norm': lower_percentile12_5_norm,
                'w2': w2,
                'w2_modified': w2_modified,
               #'raster_min':raster_min,
               # 'raster_max': raster_max,
            }
        })
        # make one single dataframe including all statistics for all rasters (predictor variables)
        df_boxplot_statistics = pd.concat(
            [df_boxplot_statistics, dataframe_this_key], axis=1)

        # reclassify the values in 3 classes depending on the boxplot statistic: 0, 1, 2
        reclass_list = []
        for value in values:
            if upper_quartile75 >= value >= lower_quartile25:
                reclass_list.append(2)
            elif upper_percentile87_5 >= value >= upper_quartile75:
                reclass_list.append(1)
            elif lower_percentile12_5 <= value <= lower_quartile25:
                reclass_list.append(1)
            else:
                reclass_list.append(0)
        # save the reclassified values in a dictionary and transform it to a dataframe
        dict_reclass = {'recl_' + key: reclass_list}
        dataframe_reclass_this_key = pd.DataFrame.from_dict(dict_reclass)
        # make one single dataframe including all reclassified values for all rasters
        df_reclass = pd.concat([df_reclass, dataframe_reclass_this_key], axis=1)
    # add reclassified values as new columns to shapefile
    shapefile = pd.concat([shapefile, df_reclass], axis=1)

    # check for correlation
    # load shapefiles with values
    data = gpd.read_file(working_dir +
                         'tmp/sites_with_rastervalues/sites_with_rastervalues_' + result_name + '.shp')
    data = data.drop(columns=['x', 'y', 'geometry'])
    data = pd.DataFrame(data)
    # calculate correlation
    correlation_matrix = data.corr('pearson')

    # extract upper triangle matrix without diagonal (k = 1)
    corr_matrix = correlation_matrix.abs()
    corr_matrix_ext = corr_matrix.where(
        np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool))

    cost_distance_list = []
    if statistic_threshold_type == 'w2':
        ranking_direction = False
    else:
        ranking_direction = True

    rank_statistic = df_boxplot_statistics.sort_values(statistic_threshold_type, axis=1, ascending = ranking_direction)
    for item in rank_statistic.columns:
        if item.startswith('c_') and item != 'c_slop+asp':
            print(item + ' distance detected and added as predictor variable')
            cost_distance_list.append(item)
            rank_statistic = rank_statistic.drop(columns=[item])
    
    selection_list = []
    while len(selection_list) < statistic_threshold:
        if len(rank_statistic.columns) == 0:
            break
        for item in rank_statistic.columns:
            print(item)
            if len(selection_list) < statistic_threshold:
                selection_list.append(item)
                print('Add predictor variable' + item)
                rank_statistic = rank_statistic.drop(columns=[item])
            else:
                break

        if statistic_threshold_type == 'iqr_norm':        
            # check for correlations
            idx = corr_matrix_ext.index
            cols = corr_matrix_ext.columns
            for row in range(len(idx)):
                for col in range(len(cols)):
                    # if both variables from a correlation combination are on the selection_list, the correlation value must be checked
                    if idx[row] in selection_list and cols[col] in selection_list:
                        value = corr_matrix_ext.ix[row, col]
                        if np.isnan(value) is True:
                            continue
                        # if the value is lower than the threshold they stay on the list
                        elif value <= corr_threshold:
                            continue
                        # if its higher the one with the higher iqr_norm will be deleted
                        elif value > corr_threshold:
                            if df_boxplot_statistics[idx[row]][statistic_threshold_type] < df_boxplot_statistics[cols[col]][statistic_threshold_type]:
                                selection_list.remove(cols[col])
                                #rank_statistic = rank_statistic.drop(columns=[cols[col]])
                                print(
                                    'Remove variable ' + cols[col] + ' because of high correlation with ' + idx[row])
                            else:
                                selection_list.remove(idx[row])
                                #df_boxplot_statistics = df_boxplot_statistics.drop(columns=[idx[row]])
                                print('Remove variable ' + idx[row] + ' because of high correlation with ' + cols[col])
                    else:
                        continue
        else:
            # check for correlations
                idx = corr_matrix_ext.index
                cols = corr_matrix_ext.columns
                for row in range(len(idx)):
                    for col in range(len(cols)):
                        # if both variables from a correlation combination are on the selection_list, the correlation value must be checked
                        if idx[row] in selection_list and cols[col] in selection_list:
                            value = corr_matrix_ext.ix[row, col]
                            if np.isnan(value) is True:
                                continue
                            # if the value is lower than the threshold they stay on the list
                            elif value <= corr_threshold:
                                continue
                            # if its higher the one with the higher w2 will be deleted
                            elif value > corr_threshold:
                                if df_boxplot_statistics[idx[row]][statistic_threshold_type] > df_boxplot_statistics[cols[col]][statistic_threshold_type]:
                                    selection_list.remove(cols[col])
                                    #rank_statistic = rank_statistic.drop(columns=[cols[col]])
                                    print(
                                        'Remove variable ' + cols[col] + ' because of high correlation with ' + idx[row])
                                else:
                                    selection_list.remove(idx[row])
                                    #df_boxplot_statistics = df_boxplot_statistics.drop(columns=[idx[row]])
                                    print('Remove variable ' + idx[row] + ' because of high correlation with ' + cols[col])
                        else:
                            continue
    
    for item in raster_data:
        if item not in selection_list and item not in cost_distance_list:
            df_boxplot_statistics = df_boxplot_statistics.drop(columns=[item])
    print(df_boxplot_statistics)
    for item in cost_distance_list:
        selection_list.append(item)

    # save correlation matrix as excelsheet
    writer = pd.ExcelWriter(
        working_dir + '/results/statistics/Correlation_matrix_' + result_name + '.xlsx')
    correlation_matrix.to_excel(writer, sheet_name='Sheet1')
    writer.save()
    print(correlation_matrix)

    # export shapefile with reclassified values
    shapefile.to_file(working_dir + '/tmp/sites_with_rastervalues/sites_with_reclass_rastervalues_' + result_name + '.shp',
                      driver='ESRI Shapefile')
    print('Calculation of boxplot statistics finished \n')
    return selection_list, correlation_matrix, df_boxplot_statistics
