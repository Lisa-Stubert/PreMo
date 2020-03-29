""" 
weighting.py<br>
python 3.6.7<br>
Definition of a function to get raster values within buffers<br>
@author: Lisa Stubert<br>
@date: 2019-05-30   <br>
"""

import numpy as np
import pandas as pd
from osgeo import gdal
import math
from numpy import linalg as LA


def weighting_calculation(working_dir, result_name, df_boxplot_statistics):
    """Weighting
    
    This script takes the boxplots statistics and uses them to calculate weighting factors w1 and w2, as described in Vogel et. al 2015. The result is a table with all weighting factors.

    Parameters
    ----------
    working_dir: str
        Working directory
    result_name: str
        Name of the model
    df_boxplot_statistics: dataframe
        Contains calculated boxplot statistics

    Note
    ----
    This is the fourth function called by the run_model.py script. It needs the output from the function 'boxplots', a Excelsheet located in working_dir + 'results/statistics/'.
    The output file is saved as follows.

    Type: Excelsheet xlsx
    File location: working_dir + '/results/statistics/' 
    File name: 'weighting' + result_name
    """

    # table with boxplot statistics
    df = df_boxplot_statistics
    
    # save weighting w0
    w0 = []
    for item in df.keys():
        w0.append(1)
    df.loc['w0'] = w0

    # calculate weighting w1
    w1 = []
    for item in df.keys():
        w1.append(1 - (df[item]['iqr_norm']))
    df.loc['w1']= w1

    # calculate weighting wE
    w2 = []
    for item in df.keys():
        w2.append(math.sqrt(1 / (df[item]['std_dev'] / df[item]['range'])))
    df.loc['w2']= w2

    # calculate w3 (AHP after Saaty), but with standart deviation instead of normalized iqr
    shape = (len(df.loc['std_dev_norm']), len(df.loc['std_dev_norm']))
    w3 = np.zeros(shape)
    i = 0
    for item in df.loc['std_dev_norm']:
        j = 0
        for item2 in df.loc['std_dev_norm']:
            # inverse ranking
            w3[i, j] = item2/item
            j += 1
        i += 1
    w3 = w3*w3
    w3 = w3*w3
    w3 = w3 * w3
    liste = []
    j = 0
    for i in range(0, len(df.loc['std_dev_norm'])):
        v = 0
        for j in range(0, len(df.loc['std_dev_norm'])):
            v += w3[i, j]
        liste.append(v)
    neu = []
    for i in liste:
        neu.append(i/sum(liste))
    df.loc['w3'] = neu

    #Export table with weighting factors
    writer = pd.ExcelWriter(working_dir + '/results/statistics/weighting' + result_name + '.xlsx')
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()
    print('Calculation of weightings finished\n')

