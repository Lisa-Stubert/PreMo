""" 
reclassify_rasters.py<br>
python 3.6.7<br>
Definition of a function to get raster values within buffers<br>
@author: Lisa Stubert<br>
@date: 2019-05-30   <br>
"""

import numpy as np
import pandas as pd
from osgeo import gdal


def reclassify_rasters(working_dir, raster_data, result_name, df_boxplot_statistics):
    """Reclassify rasters

    This script reclassifies whole rasters based on their boxplot statistics. The result is a new reclassified raster for every read raster.

    Parameters
    ----------
    working_dir: str
        Working directory
    raster_data: dict
        Names and paths of the predictore variable rasters
    result_name: str
        Name of the model

    Note
    ----
    This is the third function called by the run_model.py script. It needs the output from the function 'boxplots', a Excelsheet located in working_dir + 'results/statistics/'.
    The output file is saved as follows.

    Type: Rasters tif
    File location: working_dir + tmp + '/reclassified/'
    File name: raster_name + '_reclassified' + result_name
    """

    # set path the rasterdata
    path_rasters = working_dir + "data/"
    # set path to table with statistics
    df = df_boxplot_statistics

    # loop over dictionairy with rasters
    for item in raster_data:
        # load raster
        driver = gdal.GetDriverByName('GTiff')
        raster = gdal.Open(path_rasters + raster_data[item]['path'])
        band = raster.GetRasterBand(1)
        raster_array = band.ReadAsArray()
        nodata = band.GetNoDataValue()
        if nodata is not None:
            raster_array = np.ma.masked_equal(raster_array, nodata)
        # copy the raster, not to get problems by reclassifying overwritten values
        raster_array_reclass = raster_array.copy()

        # reclassification
        print('Reclassifying ' + item)
        # the values for the reclassification conditions are taken out of the statistics table
        if 'e_' in item or 'c_' in item:
            raster_array_reclass[np.where(
                raster_array > df[item]['upper_quartile75'])] = 0
            raster_array_reclass[np.where(
                raster_array <= df[item]['median'])] = 2
            raster_array_reclass[np.where((df[item]['median'] < raster_array) & (raster_array <= df[item]['upper_quartile75']))] = 1
            print('distance detected')

        else:
            raster_array_reclass[np.where(raster_array > df[item]['upper_percentile87.5'])] = 0
            raster_array_reclass[np.where(raster_array < df[item]['lower_percentile12.5'])] = 0
            raster_array_reclass[np.where((df[item]['lower_quartile25'] <= raster_array) 
                            & (raster_array <= df[item]['upper_quartile75']))] = 2
            raster_array_reclass[np.where((df[item]['lower_quartile25'] > raster_array)
                            & (raster_array >= df[item]['lower_percentile12.5']))] = 1
            raster_array_reclass[np.where((df[item]['upper_quartile75'] < raster_array)
                            & (raster_array <= df[item]['upper_percentile87.5']))] = 1

        # create new raster
        raster_reclass = driver.Create(working_dir + 'tmp/reclassified/' + item + '_reclassified' + result_name + '.tif', raster.RasterXSize, raster.RasterYSize, 1)
        outband = raster_reclass.GetRasterBand(1)
        outband.SetNoDataValue(-9999)
        outband.WriteArray(raster_array_reclass)
        #raster_reclass.GetRasterBand(1).WriteArray(raster_array_reclass)
        # get and set the spatial ref system
        proj = raster.GetProjection()
        georef = raster.GetGeoTransform()
        raster_reclass.SetProjection(proj)
        raster_reclass.SetGeoTransform(georef) 
        # clear variable
        raster_reclass = None
    print('Reclassification of raster values finished\n')
