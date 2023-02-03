# Content of the folder: indices_proximity

<a name="readme-top"></a>

This folder contains all the files which generate, explore, visualize, process, cluster and forecast time series of indices of technological proximity. It contains the following folders:

* data_indices
 <br> This folder regroups all the data files which are created by the coding files present in "indices_proximity".
 
 * forecasting_models
 <br> This folder is used to save the forecasting models generated in the algorithms. This is just a step of the computations
 and it represents utility only because of how the code was written.


We explain below the function of each file in the order they are run in directory_file_dataexploration:

* creation_indices_normalized
 <br> This file generates normalized indices of technological proximity.
 
* creation_indices_notnormalized
 <br> This file generates non-normalized indices of technological proximity. We will then use this type of indices later in our research.
 
* dataexploration_indices_proximity_normalized_interpolate
 <br> This file explores and visualizes in different ways the data of normalized indices focussing on interpolation.
 
 * dataexploration_indices_proximity_normalized_fitting
 <br> This file explores and visualizes in different ways the data of normalized indices focussing on fitting.
 
 * dataexploration_indices_proximity_notnormalized_interpolate
 <br> This file explores and visualizes in different ways the data of non-normalized indices focussing on interpolation.
  
 * dataexploration_indices_proximity_notnormalized_fitting
 <br> This file explores and visualizes in different ways the data of non-normalized indices focussing on fitting.
  
 * timeseries_clusterisation
 <br> This file compares different way of clustering the time series of each specific type of indices, based on their similarities.
 It finally produces a dataframe clustering the time series which has the following columns: 'concept1', 'concept2', 'index',       'cluster'.  
  
 * timeseries_forecasting
 <br> This file compares different forecasting methods and algorithms measuring their effiency using smapes (symmetric mean absolute percentage error) with some visualization.
