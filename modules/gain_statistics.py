""" 
gain_statistics.py<br>
python 3.6.7<br>
Definition of a function to get raster values within buffers<br>
@author: Lisa Stubert<br>
@date: 2019-05-30<br>
"""

import numpy as np
import rasterio
from rasterio.mask import mask
import geopandas as gpd
from shapely.geometry import mapping
from shapely.geometry import Point
from osgeo import gdal
import pandas as pd


def gain(working_dir, result_name, buffer_shapefile):
    """Gain statistics

    Parameters
    ----------
    working_dir: str
        Working directory
    result_name: str
        Name of the model
    buffer_shapefile: geodataframe
        Contains shapefiles of sites

    Return
    ------
    gain_df: dataframe
        Contains calculated gain_values
    """

    # Set path to rasterdata with suitability results
    path_raster = working_dir + 'results/suitability_result' + result_name + '_resampled_cut' + '.tif'
    #path_raster = '/Users/Lisa/Desktop/Analysis/best/supermodel_b5+best_cost.tif'
    # Calculation of rastervalues under buffer
    # import polygons
    shapefile = buffer_shapefile
    # save crs, needed later
    crs = shapefile.crs
    # make list of polygons as shapely geometries
    g = shapefile.geometry.values
    x_list = []
    y_list = []
    value_list = []

    # for every raster loop over every buffer
    for geometry in g:  
        # calculate very small buffer for every site, under which the suitability values will be averaged
        geoms = Point(geometry.centroid.x, geometry.centroid.y).buffer(5)
        # transform to GeJSON format
        geoms = [mapping(geoms)]
        # import raster and extract the raster values within the polygon
        with rasterio.open(path_raster) as src:
            out_image, out_transform = mask(
                src, geoms, crop=True, all_touched=True)
        # extract the values of the masked array
        data = out_image[0]
        # no data values of the original raster
        no_data = src.nodata
        # extract the row, columns of the valid values
        row, col = np.where(data != no_data)
        # extract the valid values
        value = np.extract(data != no_data, data)
        # calculate average value
        _sum = 0
        count = 0
        for i in range(0, len(value)):
            _sum += value[i]
            count += 1
        average = _sum / count
        value_list.append(average)
        x_list.append(geometry.centroid.x)
        y_list.append(geometry.centroid.y)

    x = x_list
    y = y_list

    # save coordinates and average values in new GeoDataFrame
    gdf = gpd.GeoDataFrame({'x': x, 'y': y, 'suitability_value': value_list
                            })
    # add center of buffer (location of archeological site) as geometry
    gdf['geometry'] = gdf.apply(lambda row: Point(row['x'], row['y']), axis=1)

    # calculate percentage of sites in different suitability zones
    suitability_zone = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.75, 0.8, 0.9]
    counter = 0
    percent_site_list = []
    for index in suitability_zone:
        counter = 0
        for item in value_list:
            if item > index:
                counter += 1
        percent_site_list.append((counter/len(value_list))*100)

    # calculate percentage of area for different suitability zones
    # load raster
    driver = gdal.GetDriverByName('GTiff')
    raster = gdal.Open(path_raster)
    band = raster.GetRasterBand(1)
    raster_array = band.ReadAsArray()
    row, col = raster_array.shape
    all_pixels = row * col
    percent_area_list = []
    for index in suitability_zone:
        b = raster_array > index
        count_pixels = len(raster_array[b])
        percent_area_list.append((count_pixels/all_pixels)*100)

    # calculate gain metrics
    gain = []
    for i in range(0,len(suitability_zone)):
        if percent_site_list[i] > 0:
            gain.append(round((1 - (percent_area_list[i]/(percent_site_list[i]))),5))
        else: 
            gain.append(None)
    gain_df = pd.DataFrame({'suitability_area_>': suitability_zone,
                            'gain': gain, 'percent area': percent_area_list, 'percent sites': percent_site_list})
    return(gain_df)
