""" 
validation.py<br>
python 3.6.7<br>
Definition of a function to get raster values within buffers<br>
@author: Lisa Stubert<br>
@date: 2019-05-30   <br>
"""

import numpy as np
import rasterio
from rasterio.mask import mask
import geopandas as gpd
from shapely.geometry import mapping
from shapely.geometry import Point


def validation(working_dir, result_name, testdata, x_list, y_list, value_list):
    """Validation   

    Parameters
    ----------
    working_dir: str
        Working directory
    result_name: str
        Name of the model
    testdata: geodataframe
        Contains position of sites
    x_list: list
        Contains x_coordinates of sites where validation values were already calculated from other subsets 
    y_list: list
        Contains y_coordinates of sites where validation values were already calculated from other subsets
    value_list: list
        Contains validation values already calculated from other subsets

    Returns
    -------
    x_list: list
        Contains x_coordinates of sites where validation values were already calculated from other subsets
    y_list: list
        Contains y_coordinates of sites where validation values were already calculated from other subsets
    value_list: list
        Contains validation values already calculated from other subsets and from this subset
    percent_good_prediction: int
        Percentage of sites in areas over 0.5 suitability 
    result_gdf: geodaframe
        Contains suitability values of sites and there location
    """

    # Set path to rasterdata
    path_raster = working_dir + 'results/suitability_result' + result_name + '_resampled_cut' + '.tif'
    #path_raster = '/Users/Lisa/Desktop/Analysis/best/supermodel_b5+best_cost.tif'
    # Calculation of rastervalues under buffer
    # import polygons
    shapefile = testdata
    # save crs, needed later
    crs = shapefile.crs
    # make list of polygons as shapely geometries
    g = shapefile.geometry.values

    # for every raster loop over every buffer
    for geometry in g:
        # calculate very small buffer for every site, under which the suitability values will be averaged
        geoms = Point(geometry.centroid.x, geometry.centroid.y).buffer(5)
        # transform to GeJSON format
        geoms = [mapping(geoms)]
        # import raster and extract the raster values within the polygon
        with rasterio.open(path_raster) as src:
            out_image, out_transform = mask(src, geoms, crop=True, all_touched=True)
        out_image = out_image.astype(float)
        # extract the values of the masked array
        data = out_image[0]
       # print('****')
        #print(out_image[0])
        # no data values of the original raster
        no_data = src.nodata
        # extract the row, columns of the valid values
        row, col = np.where(data != no_data)
        # extract the valid values
        value = np.extract(data != no_data, data)
        #print(no_data,value)
        # calculate average value
        _sum = 0
        count = 0
        for i in range(0, len(value)):
            _sum += value[i]
            count += 1
         #   print("Sum " + str(_sum))
         #   print("Count " + str(count))
        average = _sum / count
       # print("Average " + str(average))
        value_list.append(average)
        x_list.append(geometry.centroid.x)
        y_list.append(geometry.centroid.y)
       # print(x_list)
        #print(y_list)
    x = x_list
    y = y_list

    # save coordinates and average values in new GeoDataFrame
    gdf = gpd.GeoDataFrame({'x': x, 'y': y, 'suitability_value': value_list
                            })
    # add center of buffer (location of archeological site) as geometry
    gdf['geometry'] = gdf.apply(lambda row: Point(row['x'], row['y']), axis=1)
    # set coordinate reference system
    gdf.crs = crs
    # export as shapefile
    gdf.to_file(working_dir + 'results/suitability_shapefiles/' + result_name + '.shp',
            driver='ESRI Shapefile')

    # calculate percentage of sites in areas over 0.5 suitability
    #print(gdf)
    counter = 0
    for item in value_list:
      #  print(item)
        if item > 0.5:
            counter += 1
       #     print(counter)
    if counter > 0:
        percent_good_prediction = round((float((counter/len(value_list))*100)), 2)
    else:
        percent_good_prediction = None

    return(x_list, y_list, value_list, percent_good_prediction, gdf)
