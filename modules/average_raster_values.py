""" 
average_raster_values.py<br>
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


def average_raster_values(working_dir, raster_data, result_name, traindata):
    """Get raster values within buffers
    
    This script calculates the average or median of all values of pixels from a raster
    within the buffered archeological site. Multiple Rasters are processed. The 
    result is a shapefile of the buffered sites with a column for the average 
    values for each raster (predictor variable).

    Parameters
    ----------
    working_dir: str
        Working directory
    raster_data: dict
        Names and paths of the predictor variable rasters
    result_name: str
        Name of the model
    traindata: GeoDataFrame
        Subset of buffered sites

    Note
    ----
    This is the first function called by the run_model.py script as a substep of calculating the predictive model. 
    The output file is saved as follows.

    Type: Shapefile shp
    File location: working_dir + 'tmp/sites_with_rastervalues/'
    File name: 'sites_with_rastervalues_' + result_name
    """

    # get path to rasterdata
    path_rasters = working_dir + "data/"
    # generate empty value list for every raster in the (predictor variables) raster dictionary
    # the list will be filled with calculated values later
    for raster in raster_data:
        raster_data[raster]['values'] = []
    # import buffer polygons
    shapefile = traindata 
    # save crs, needed later
    crs = shapefile.crs 
    # make list of buffers as shapely geometries
    g = shapefile.geometry.values
    # prepare empty lists
    x_list = []
    y_list = []
    value_list = []

    # loop over every raster in raster dictionary
    for raster in raster_data:
        print('Raster: ' + raster)
        # for every raster loop over every buffer
        for geometry in g:
            # transform to GeoJSON format
            geoms = [mapping(geometry)] 
            # import raster and extract the raster values within the polygon
            # include every pixel in the mask that touches the shapes (all_touched = True)
            with rasterio.open(path_rasters + raster_data[raster]['path']) as src:
                out_image, out_transform = mask(src, geoms, crop=True, all_touched=True)
            # extract the values of the masked array
            data = out_image[0]
            # no data values of the original raster
            no_data = src.nodata
            # extract the valide values
            value = np.extract(data != no_data, data)
            # calculate average  of all values within a buffer and append this calculated values to lists
            _sum = 0
            count = 0
            for i in range(0, len(value)):
                _sum += value[i]
                count += 1
            average = _sum / count
            value_list.append(round(average, 8))
            # append x- and y-coordinates of the buffercenter to lists
            x_list.append(geometry.centroid.x)
            y_list.append(geometry.centroid.y)
            
        # fill raster dictionary with the calculated average values
        raster_data[raster]['values'] = value_list 
        x = x_list
        y = y_list
        print('Processed '+ str(len(x_list)) + ' buffered sites')
        # empty lists for next raster
        value_list = [] 
        x_list = []
        y_list = []

    # save coordinates and average values in new GeoDataFrame
    gdf = gpd.GeoDataFrame({'x': x, 'y': y}) 
    for raster in raster_data:
        gdf[raster] = raster_data[raster]['values']
    # add center of buffer (location of archeological site) as geometry
    gdf['geometry'] = gdf.apply(lambda row: Point(row['x'], row['y']), axis=1) 
    # set coordinate reference system
    gdf.crs = crs 
    # export as shapefile
    gdf.to_file(working_dir + 'tmp/sites_with_rastervalues/sites_with_rastervalues_' + result_name + '.shp',
            driver='ESRI Shapefile') 
    print('Calculation of average raster values finished\n')


    
