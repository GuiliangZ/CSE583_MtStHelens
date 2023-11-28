import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy
import scipy.signal
import datetime
import glob
import math
import sys
sys.path.append('/Users/zheng/Desktop/Fall23/CSE583/project/CSE583_MtStHelens')

from mtsthelens import preprocessing_functions as prefcn

def find_max_min_within_range(df,start_index,end_index):
    # Function to find the max and min within the specified range of Dataframe
    subset = df[start_index:end_index + 1]  # Select the specified range
    max_value = subset.max()
    min_value = subset.min()
    return pd.Series({'Max_Value': max_value, 'Min_Value': min_value})

def importData_extrusion():
    '''
    Read the extrusion rate data (From sparse photograph images)
    Total volume changes(10^6 m^3)
    Total volume change rate (m^3/s)
    Extruded laca volume (10^6 m^3)
    Lava extrusion rate (m^3/s)
    Diff - the total volume changes since previous photographed date (10^6 m^3)
    '''
    df_dome = pd.read_csv('data/dome_extrusion.txt', header=0, skiprows=0)
    df_dome.set_index('Date of photography',inplace=True)
    df_dome.index = pd.to_datetime(df_dome.index).tz_localize(None)
    df_dome['diff'] = df_dome['Total volume change(x 106 m3)']-df_dome['Total volume change(x 106 m3)'].shift(1)
    return df_dome

def station_name():
    '''
    Get a python array of station names
    '''
    all_files = sorted(glob.glob('data/*_*_extended2.csv'))
    sta_list = np.unique([file.split('/')[2].split('_')[1] for file in all_files]) # stations with data
    return sta_list

def importData_seismic(param_name):
    '''
    Read all the pre-processed seismological data (there are 4 sets of data)
    df_rsam_median: Real-Time Amplitude Measurement is a measure of seismic energy
    df_zscrsam: z-score normalization is a technique that scales the\
                measurement point of a feature to have a mean of 0 and a standard deviation of 1

    df_dsar_median: Displacement Seismic Amplitude Ratio is a measure for attenuation
    df_zscdsar_median: z-score normalization. dsar normalized 

    df_rms_median: Root Mean Square is also a measure of emitted seismic energy but over the whole detectable frequency range.
    df_zscrms_median: z-score normalization. rms normalized 

    df_pga_median: Peak Ground Acceleration is giving you the\
                     maximum absolute value in the 10 minute time window after deviate the seismig ground velocity time series.
    df_zscpga_median: z-score normalization. pga normalized 
    
    '''
    df_rsam_median = prefcn.read_data('data/'+param_name+'_extended2_long.csv')
    print(df_rsam_median)
    return df_rsam_median #df_zscrsam_median, df_dsar_median, df_zscdsar_median, df_rms_median, df_zscrms_median, df_pga_median, df_zscpga_median


def stackInSpace(df_rsam_median):
    '''
    Name: Stacking in Space\
    What it does: Analyses Data accross all stations to potential\
                 find a correlation between the climate and the region over the years.
    Input: .csv files of the Reformatted Time Series Data\
    Output: Average Seasonality over all stations, stacked in time series with reasonality removed.\
             Contains a column of maximum and minimum difference per year. Output to .csv file\
    '''
    df_median_stackSpace = pd.DataFrame()
    years = range(2000,2022+1)
    df_rsam_median_f = df_rsam_median.fillna(0)
    df_median_stackSpace['df_rsam_median_SS'] = df_rsam_median_f.apply(lambda row: row[row != 0].mean(),axis = 1)
    #print(df_median_stackSpace)

    df_dict = {} 
    for year in years:
        df_year = df_median_stackSpace['df_rsam_median_SS'].loc[str(year)] # splits df into samaller df for each year
        df_split1 = df_year[df_year.index<datetime.datetime(year,2,28,23,59,59,999)] # inclued dates until 28.2
        df_split2 = df_year[df_year.index>datetime.datetime(year,3,1)] # includes dates from 1.3
        df_concat = pd.concat([df_split1, df_split2]) # concat so that 29.2 removed
        df_dict[year] = df_concat # add shorted years to dict
    key_list = [key for key,value in df_dict.items()]
    time_list = df_dict[2000].index.strftime('%m/%d %H:%M:%S').to_list()
    df_stackSpace_year = pd.DataFrame(index=time_list,columns=key_list)
    for key, value in df_dict.items():
        df_stackSpace_year[key] = value.to_list()
    print(df_stackSpace_year)
    return df_median_stackSpace, df_stackSpace_year

def stackSpace_yearParam(df_stackSpace_year):
    df_yearlyParam_index = pd.Series(['max','min','mean','median'])
    df_yearlyParam = pd.DataFrame(index=df_yearlyParam_index)
    # print(df_yearlyParam)
    years = range(2000,2022+1)
    for year in years:
        df_yearlyParam[str(year)] = 0
    for year in years:
        df_yearlyParam[str(year)].loc['max'] = df_stackSpace_year[year].max()
        df_yearlyParam[str(year)].loc['min'] = df_stackSpace_year[year].min()
        df_yearlyParam[str(year)].loc['mean'] = df_stackSpace_year[year].mean()
        df_yearlyParam[str(year)].loc['median'] = df_stackSpace_year[year].median()
    print(df_yearlyParam)
    return df_yearlyParam

def export_csv(param_name):
    # Specify the path and filename for the CSV file
    csv_file_path_stackSpace = '/Users/zheng/Desktop/Fall23/CSE583/project/CSE583_MtStHelens/output/df_stackSpace_year_'+param_name+'.csv'
    csv_file_path_yearlyParam = '/Users/zheng/Desktop/Fall23/CSE583/project/CSE583_MtStHelens/output/df_yearlyParam_'+param_name+'.csv'

    # Save the DataFrame to a CSV file
    df_stackSpace_year.to_csv(csv_file_path_stackSpace, index=True)  
    print(df_stackSpace_year)
    # Set index=False to exclude the index column in the CSV file
    df_yearlyParam.to_csv(csv_file_path_yearlyParam, index=True)

if __name__ == "__main__":
    param_name = 'zscrsam'
    df_dome = importData_extrusion()
    df_rsam_median = importData_seismic(param_name)
    sta_list = station_name()
    df_median_stackSpace, df_stackSpace_year = stackInSpace(df_rsam_median)
    df_yearlyParam = stackSpace_yearParam(df_stackSpace_year)
    export_csv(param_name)