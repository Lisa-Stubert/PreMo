[![License: CC BY-NC 4.0](https://licensebuttons.net/l/by-nc/4.0/80x15.png)](https://creativecommons.org/licenses/by-nc/4.0/)

# PreMo - Predictive modelling Python package
This Python scripts were created and used to calculate predictive models for an archaeological study about viticulture in ancient Spain. The approach was to take a data set (point locations) of existing archeological sites and to determine the underlying factors of their distribution. Therefore the script predicts zones of high suitability that were associated with Roman viticulture, based on the location characteristics of the sites.
As predictor variables different rasters (for example a digital elevation model and cost distances to ancient settlements) of the study area were used.


## What can this approach be used for
The script makes it possible to automate analyses that would otherwise have to be carried out in a classic GIS using many steps. The application of this predictive modelling algorithm is not limited to the specific field of archaeology. In contrast, this methodology may also be used in other scientific fields, such as ecology to model species distributions or in economic geography for production site analysis.


## How it works
The functionality of the predictive modelling algorithm is described in the study "Viticulture in the Laetanian Region (Spain) during the Roman Empire: Predictive modelling and spatial analysis".

## Usage

The script was written for usage with Python 3.6.7.


+ Download or clone the repository:
```bash
git clone https://github.com/lstubert/PreMo.git
```
+ Download all required packages (see Requirements).

+ Set your working directory in *set_data_paths.py*.

+ For testing the script with the provided test data, execute *run_modelling.py*. The output data of a suitability raster and statistical results is saved in the *Results*-Directory.

+ For usage with own data, save the data sets of buffered location points (as shapefiles, make sure to adopt the naming convention of the files) and the predictor rasters (as GeoTiffs) in the *data*-directory. Change the paths to the data in *set_data_paths.py*.

+ Set the parameters that should be used to calculate the predictive models in *run_modelling.py*.

```python
# insert all combinations of predictor variables, used to calculate models
combinations = {
    "example": ['t_slope', 't_wind', 't_dir_in', 'c_rivers', 'c_coast', 'c_prim_set', 'c_sec_set', 'c_allroads'],
}

# set the size(s) of your buffered site location(s)
buffer_sizes = ['50','100'] 

# set the weighting(s) that should be used
weightings = ['w1','w2'] # w0 = no weighting, w1 = weighting with IQRnorm, w2 = weighting wE after Ejstrud, w3 = weighting after Saaty

# set thresholds if you want to calculate models by automated variable selection (if you want to calculate models by experts selection, set statistic threshold to 100 and correlation threshold to 1) 
statistic_thresholds = [3]
statistic_threshold_types = ['iqr_norm'] # w2 = selection by ranked wE after Ejstrud, iqr_norm = selection by ranked IQR norm
corr_thresholds = [1]

# set cross-validation on or off
test = False  # True or False
````

## Documentation of modules

The documentation of the submoduls can be found here:
https://premo.readthedocs.io/en/latest/

## Requirements
+ [rasterio](www.pip.com/rasterio)
+ [pandas](https://pypi.org/project/pandas/)
+ [GDAL](https://pypi.org/project/GDAL/)
+ [numpy](https://pypi.org/project/numpy/)
+ [sklearn](https://pypi.org/project/scikit-learn/)
+ [shapely](https://pypi.org/project/Shapely/)
+ [statistics](https://pypi.org/project/statistics/)
+ [seaborn](https://pypi.org/project/seaborn/)


Please feel free to contact me for bug reports, questions and comments.
