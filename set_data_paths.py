""" 
data_input.py<br>
python 3.6.7<br>
Definition of a function that returns the paths to the data and<br>
a function that makes subsets out of the raster dictionary<br>
@author: Lisa Stubert<br>
@date: 2019-05-30<br>
"""

from itertools import combinations

def data_input():
    """Return data paths

    This script defines the data basis used. The correct paths to the predictor variable rasters have to be defined here.

    Returns
    -------
    all_raster_data: dict
        Names an paths of predictor variable rasters
    """

    # set your working directory (location of the PreMo folder)
    working_dir = '/Users/User/Desktop/PreMo/'

    # set directory path to buffered sites (inside the data folder)
    buffer_dir = 'example_data_set/buffered_sites/'

    # generate dictionary with predictor variables and their directory paths (inside the data folder)
    #Note : keys must me limited to max. 10 characters
    all_raster_data = {
        # topography:
        # Note: Topography variables must be named with t_ in the beginning, because the algorithm only recognize them as topography variables by there name. This is import when variables are selected automatically by thresholds.
        't_slope': {'path': 'example_data_set/topography/slope.tif'},
        't_insola': {'path': 'example_data_set/topography/direct_insolation.tif'},
        't_wind': {'path': 'example_data_set/topography/wind_exposition.tif'},

        # cost distances:
        # Note: Cost distance must be named with c_ in the beginning, because the algorithm only recognize them as cost distances by there name. This is import when variables are selected automatically by thresholds.
        'c_coast': {'path': 'example_data_set/distance_cost/coastline.tif'},
        'c_prim_set': {'path': 'example_data_set/distance_cost/primary_settlements.tif'},
    }
    
    return(all_raster_data, buffer_dir, working_dir)




def rasterfilter(all_raster_data, variables):
    """Get subset out of raster dictionary

    Parameters
    ----------
    all_raster_data: dict
    variables: list

    Returns
    -------
    raster_data: dict
        Subset of raster dictionary

    """
    raster_data = dict([(i, all_raster_data[i]) for i in all_raster_data if i in set(variables)])

    return(raster_data)


