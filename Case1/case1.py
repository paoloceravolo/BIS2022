# -*- coding: utf-8 -*-
"""Case1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iFTODJoN2t27eJSr2GS8VmMhIZiBJsOC
"""

# Commented out IPython magic to ensure Python compatibility.
# Commented out IPython magic to ensure Python compatibility.
# %pip install pm4py

# %pip install pm4py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.stats import pareto

import pm4py

# Load Event Log file in CSV

from pm4py.objects.log.util import dataframe_utils
from pm4py.objects.conversion.log import converter as log_converter

log_csv = pd.read_csv('https://raw.githubusercontent.com/paoloceravolo/PM-Regensburg/main/CallCenterLog.csv', sep=',')
log_csv = dataframe_utils.convert_timestamp_columns_in_df(log_csv)
log_csv = log_csv.sort_values('Start Date')
log_csv.rename(columns={'Case ID': 'case:concept:name', 'Start Date': 'start_timestamp', 'End Date': 'time:timestamp', 'Activity': 'concept:name', 'Resource': 'org:resource'}, inplace=True) #change the name to a colum

log_csv

# Covert the dataframe to an event log dictionary 

event_log = log_converter.apply(log_csv)

#print(event_log)

from pm4py.algo.filtering.log.cases import case_filter

filtered_log = case_filter.filter_case_performance(event_log, 60, 7*864000)

print(len(filtered_log))

# Extract the variants from an event log

from pm4py.algo.filtering.log.variants import variants_filter
variants = variants_filter.get_variants(event_log)

print(variants)

# Convert Eent log to DataFrame 

data_log = log_converter.apply(event_log, variant=log_converter.Variants.TO_DATA_FRAME)

profile = data_log.groupby('case:concept:name').agg(
Activity = ('concept:name', 'count'),\
Activity_list = ('concept:name', lambda x: ','.join(x) ),\
Rosource = ('org:resource', 'nunique'),\
Duration = ('start_timestamp', lambda x: x.max()- x.min()),\
)

profile

mean_duration = profile[(profile['Duration'] > '0:0:0')].agg('mean')

mean_duration

# Count the cases per variant 

from pm4py.statistics.traces.generic.log import case_statistics
variants_count = case_statistics.get_variant_statistics(filtered_log)
variants_count = sorted(variants_count, key=lambda x: x['count'], reverse=True)

print(variants_count)

variants_df = pd.DataFrame.from_records(variants_count)
variants_df

# Prepare the dimensions to plot
# Put variants and counts into lists of prefered length

variant = variants_df[0:100].index
frequency = variants_df[0:100]['count']
# return a list of log values from a list 
frequency_log = [math.log(i, 2) for i in frequency] 
#print(frequency)
#print(frequency_log)

# Plot the histogram of the frequencies

fig = plt.figure(figsize = (15, 5))
 
# creating the bar plot
plt.bar(variant, frequency, color ='orange',
        width = 0.4)
 
plt.xlabel("variants sorted by frequency")
plt.ylabel("frequency")
plt.title("bar chart of variants frequency")
plt.show()

# Commented out IPython magic to ensure Python compatibility.

# %matplotlib inline
  
data= variants_df[1:100]['count']

# getting data of the histogram
count, bins_count = np.histogram(data, bins=100)
  
# finding the PDF of the histogram using count values
pdf = count / sum(count)
#print(pdf)
  
# using numpy np.cumsum to calculate the CDF
# We can also find using the PDF values by looping and adding
cdf = np.cumsum(pdf)
#print(cdf)
  
# plotting PDF and CDF
plt.plot(bins_count[1:], pdf, color="red", label="PDF")
plt.plot(bins_count[1:], cdf, label="CDF")
plt.legend()