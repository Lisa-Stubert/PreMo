""" 
prediction.py<br>
python 3.6.7<br>
@author: Lisa Stubert<br>
@date: 2019-05-30<br> 
"""

import numpy as np
import pandas as pd
from osgeo import gdal
from subprocess import call


def prediction(working_dir, raster_data, weighting, buffer_size, result_name):
    """Predictive Model
    
    This script takes the reclassified rasters and the calculated weighting factors. The result is a raster which shows the suitability.

    Parameters
    ----------
    working_dir: str
        Working directory
    raster_data: dict
        Names and paths of the predictore variable rasters
    weighting: str
        Weighting witch will be multiplied with the raster values
    buffer_size:
        str
    result_name: str
        Name of the model

    Note
    ----
    This function needs the output of the function 'reclassify_raster', this means multiple rasters, and the output of the function 'weighting_calculation', a Excelsheet located in working_dir + 'results/statistics/'.
    The output file is saved as follows.

    Type: Raster .tif
    File location: working_dir + 'results/'
    File name: 'suitability_result' + result_name
    """


    # Put the names of the rasters out of the dictionairy into a list
    rasternames = []
    for item in raster_data:
        rasternames.append(str(item))
    # set path to reclassified rasters
    path = working_dir + "tmp" + '/reclassified/'
    # set path to table with weighting factors
    weighting_df = pd.read_excel(working_dir + 
        '/results/statistics/weighting' + result_name + '.xlsx', sheet_name='Sheet1')

    # Calculate suitability 
    # load the first raster
    driver = gdal.GetDriverByName('GTiff')
    raster = gdal.Open(path + rasternames[0] + '_reclassified' + result_name + '.tif')
    band = raster.GetRasterBand(1)
    raster_array = band.ReadAsArray()

    # Multiply every value with personal weighting factor
    print('Multiply ' + rasternames[0] + ' with weighting factor: ' +
          str(weighting_df[rasternames[0]][weighting]))
    raster_array = raster_array * weighting_df[rasternames[0]][weighting]
    print('Add up: ' + rasternames[0])
    raster_array_sum = raster_array.copy()

    # loop over remaining rasters and add them up
    for item in rasternames:
        if item == rasternames[0]:
            continue
        # load raster
        raster = gdal.Open(path + item + '_reclassified' + result_name +'.tif')
        band = raster.GetRasterBand(1)
        raster_array = band.ReadAsArray()

        # Multiply every value with personal weighting factor
        print('Multiply ' + item + ' with weighting factor: ' + str(weighting_df[item][weighting]))
        raster_array = raster_array * weighting_df[item][weighting]
        # and add up values
        print('Add up: ' + item)
        raster_array_sum = np.sum([raster_array_sum, raster_array], axis=0)

    # convert integer values to float values  
    raster_array_sum = raster_array_sum.astype(float)
    print('Highest value: ' + str(np.max(raster_array_sum)))
    print('Lowest value: ' + str(np.min(raster_array_sum)))
    # normalize the raster values by dividing by the highest value
    raster_array_sum_norm = np.divide(raster_array_sum, np.max(raster_array_sum))

    # Export the final raster
    # create new raster
    raster_reclass = driver.Create(working_dir + 'results/suitability_result' + result_name +
                                   '.tif', raster.RasterXSize, raster.RasterYSize, 1, gdal.GDT_Float32)
    raster_reclass.GetRasterBand(1).WriteArray(raster_array_sum_norm)
    # get and set the spatial ref system
    proj = raster.GetProjection()
    georef = raster.GetGeoTransform()
    raster_reclass.SetProjection(proj)
    raster_reclass.SetGeoTransform(georef)
    # clear variable
    raster_reclass = None

    # Resample the result raster to the size of buffer diameter
    #if buffer_size is 'flex':
    #    buffer_size = '250' 
    call(['gdalwarp', '-overwrite', '-tr', buffer_size, buffer_size,'-of', 'GTiff', working_dir + 'results/suitability_result' + result_name + '.tif',
    working_dir + 'results/suitability_result' + result_name + '_resampled.tif'])

    # If needed : 
    # clip raster to landmass by a shapefile that masks the ocean and set nodatavalue to -9999
    path_to_mask = working_dir + 'data' + '/example_data_set/mask_for_no_data_values/oceanmask.shp'

    call(['gdalwarp', '-overwrite', '-of', 'GTiff', '-cutline', path_to_mask, '-crop_to_cutline', '-dstnodata', '-9999.0', working_dir + 'results/suitability_result' + result_name + '_resampled.tif', working_dir + 'results/suitability_result' + result_name + '_resampled_cut.tif'])



    # delete the no longer required uncut raster
    call(['rm', working_dir + 'results/suitability_result' + result_name + '.tif', working_dir + 'results/suitability_result' + result_name + '_resampled.tif'])

    # delete the no longer required reclassified rasters
    call(['rm', '-r', working_dir + 'data/reclassified/*'])
    print('Model prediction finished\n')
