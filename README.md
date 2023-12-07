# CSE583_MtStHelens

## Background



## Goals
1. **Correlation of Seismic Attenuation and Magma Extrusion**: This project aims to investigate whether seismic attenuation, resulting from near-surface changes, correlates with the magma extrusion rate. Such correlation is expected due to the impact of infiltrating magma on the material properties along the seismic wave path, which should be discernible and linked to the rate of dome growth. Beyond magma influx, various factors like heavy rainfall or snowfall can alter underground pore pressure. To distinguish these dominant influences, which often exhibit strong seasonal patterns, two methods will be tested. First, a high-pass filter will be applied to remove all periods longer than one year. Second, data will be stacked in time, meaning the average waveform over all years for each station. This station-specific average seasonality will be subtracted from the attenuation data. This process should enable the correlation of seismic attenuation with the rate of dome extrusion.<br>

2. **Analysis of Changing Climatic Patterns**: The long-term seismic data is crucial for understanding the broader environmental context. The hypothesis suggests that weather conditions have become more extreme over recent years, potentially resulting in an overall trend. Determining such trends is challenging because local effects often dominate. To mitigate this, data is spatially stacked, involving averaging all seismic data for a given year. This approach generates robust attenuation time series, allowing for trend analysis and the identification of annual minima and maxima. However, it does not enable the identification of potential subpatterns within the region. The study will use both the raw attenuation data and the processed data to explore these subpatterns, as distinct variations may exist between the crater region and the area surrounding the lake, among others.<br>

By addressing these goals, this project aims to contribute to our understanding of seismic and climatic influences on the Mt. St. Helens region, providing valuable insights into volcanic and environmental changes. The analysis mostly bases on originally seismic ground velocity data which are converted in a measure for seismic attenuation. This convertion is not part of this project.

## Installation
### Clone the Repository 
```python
git clone git@github.com:CSE583MtStHelens/CSE583_MtStHelens.git
```
### Run the example notebook
```cd``` to the directory where you have clone the repository untill you see the ```environment.yml``` and copy paste the cell below in your termial.
```python
conda env create --file environment.yml
conda activate pygmt2
jupyter lab
```
navigate in jupyter lab to the directory ```example```

### Create the animation
#### Linux
```python
sudo apt-get install imagemagick
```
#### Mac
```python
brew install imagemagick
```

```cd``` to de directory where you have saved the ```.png``` files
```python
convert -delay 30 -loop 0 *.png myvideo.gif
```


## Data structure
This project is structured in the way that we have a folder ```mtsthelens``` where you can find the python scripts of all the functions written. The folder ```example``` contains some sampled data and a working tutorial to show how our functions work. In our case we do have .csv files of the preprocessed seismic data. Each file contains the data of one seismic station and one year. The column headers indicate different parameters extracted from seismic time series. The rows represent time windows of 10 minutes. The ```docs``` folder contains some information about the project.<br>

Some abbreviations:<br>
- **RSAM:** Real-Time Seismic Amplitude Measurement is a measure of **seismic energy**. We get it by taking seismic groud velocity (that is what a seismometer measures) and apply a bandpass filter to end. The filtered time series then is cut into 10 minute long time windows and the mean of the absolute values than is the RSAM. Our example data has three different RSAM time series (RSAM, MF, HF). Each time series is filtered in a different frequency range (2-5 Hz, 4.5-8 Hz, 8-16Hz). These frequency bands are typical for volcano seismology.
- **DSAR:** Displacement Seismic Amplitude Ratio is a measure for **attenuation**. We get ground displacement by integrating seismic ground velocity. We apply the same bandpass filters as for RSAM. To get an wave attenuation (we assume that the seismic source does not change and the wave attenuation is simply due to changes of the underground) we devide a low frequency band by a high frequency band. For DSAR it is MF/HF, lDSAR is RSAM/MF, lhDSAR is RSAM/HF. VSAR and lhVSAR follows the same procedure without the convertion from ground velocity to ground displacement.
- **RMS:** Root Mean Square is also a measure of emitted **seismic energy** but over the whole detectable frequency range. The RMS is calculated over 10 minute long time windows.
- **RMeS:** Root Median Square is similar to RMS but more robust to individual outliers because we take the median instead of the mean.
- **PGV:** Peak Ground Velocity is giving you the maximum absolute value in the 10 minute time window of the seismig ground velocity time series.
- **PGA:** Peak Ground Acceleration is giving you the maximum absolute value in the 10 minute time window after deviate the seismig ground velocity time series.
- **zsc:** z-score normalization is a technique that scales the measurement point of a feature to have a mean of 0 and a standard deviation of 1. This is done by subtracting the mean of the feature from each measurement point, and then dividing by the standard deviation. We do this in the log-space

## Repository strucutre
```bash
├── LICENSE
├── README.md
├── docs
│   ├── Seismomech_Technology_Review.pptx
│   ├── Use_Case.md
│   ├── User_story.md
│   ├── component_diagram (2).pdf
│   └── component_specifications.md
├── environment.yml
├── example
│   ├── example_data
│   │   ├── dome_extrusion.txt
│   │   ├── example_data_eruption.csv
│   │   ├── mt_st_helens_activity.txt
│   │   ├── sta_log_long.txt
│   │   └── synthetic_data.csv
│   ├── example_tutorial.ipynb
│   └── __init__.py
├── mtsthelens
│   ├── __init__.py
│   │   ├── __init__.cpython-312.pyc
│   │   ├── manipulation_functions.cpython-310.pyc
│   │   ├── manipulation_functions.cpython-312.pyc
│   │   ├── plotting_functions.cpython-310.pyc
│   │   ├── plotting_functions.cpython-312.pyc
│   │   └── preprocessing_functions.cpython-312.pyc
│   ├── manipulation_functions.py
│   ├── plotting_functions.py
│   └── preprocessing_functions.py
└── tests
    ├── __init__.py
    ├── manipulation_test.py
    ├── plotting_test.py
    └── preprocessing_test.py
```
