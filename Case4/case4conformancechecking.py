# -*- coding: utf-8 -*-
"""Case4ConformanceChecking.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1eYTlchzr8OZ3n9gyxun6xxbUulpLDCb8
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
# %pip install pm4py
import pm4py
from pm4py.objects.log.util import dataframe_utils
from pm4py.objects.conversion.log import converter as log_converter

import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

# Uplaod small source files
from google.colab import files
uploaded = files.upload()

#print(uploaded)

# Load Event Log
log_csv = pd.read_csv('ArtificialPatientTreatmentAnomalies.csv', sep=',')
log_csv = dataframe_utils.convert_timestamp_columns_in_df(log_csv)

log_csv = log_csv.sort_values('datetime')

log_csv.rename(columns={'datetime': 'time:timestamp', 'patient': 'case:concept:name', 'action': 'concept:name', 'resource': 'org:resource'}, inplace=True)
parameters = {log_converter.Variants.TO_EVENT_LOG.value.Parameters.CASE_ID_KEY: 'case:concept:name'} # identify the case_id_key name (if not change it will simply be the mane of the coloumn)


log_csv

# Discover a Petri Net using Alpha Miner
net, im, fm = pm4py.discover_petri_net_alpha(log_csv)
# Visualise 
pm4py.view_petri_net(net, im, fm, format='png')

# Discover a Petri Net using Heuristic Miner
net, im, fm = pm4py.discover_petri_net_heuristics(log_csv, dependency_threshold=0.9, and_threshold=0.5, loop_two_threshold=0.5)

# Visualise 
pm4py.view_petri_net(net, im, fm, format='png')

# Discover process tree using Inductive Miner Infrequent
net, im, fm = pm4py.discover_petri_net_inductive(log_csv, noise_threshold=0.7, multi_processing=False)

# Visualise 
pm4py.view_petri_net(net, im, fm, format='png')

# Discover process tree using ILP Miner
net, im, fm = pm4py.discover_petri_net_ilp(log_csv, alpha=0.9)

# Visualise 
pm4py.view_petri_net(net, im, fm, format='png')

# Conformance checking diagnostic
tbr_diagnostics = pm4py.conformance_diagnostics_token_based_replay(log_csv, net, im, fm)
diagnostics_df = pd.DataFrame.from_dict(tbr_diagnostics)

diagnostics_df

# Get the idnexes of the cases with low fitness values

disfuntional_traces = diagnostics_df.index[diagnostics_df['trace_fitness'] <= 0.7].tolist()

disfuntional_traces

# Filter those cases from the event log
##  add prefix to index value in the list 
prefix = 'patient'
disfuntional_traces_rename = [prefix + str(x) for x in disfuntional_traces]

disfuntional_traces_rename

## apply a filter to remove the list of disfunctional cases 
filtered_dataframe = pm4py.filter_event_attribute_values(log_csv, 'case:concept:name', disfuntional_traces_rename, case_id_key='case:concept:name')

# Discover process tree using Inductive Miner Infrequent
net, im, fm = pm4py.discover_petri_net_inductive(filtered_dataframe, noise_threshold=0, multi_processing=False)

# Visualise 
pm4py.view_petri_net(net, im, fm, format='png')

# Conformance checking diagnostic
tbr_diagnostics = pm4py.conformance_diagnostics_token_based_replay(filtered_dataframe, net, im, fm)
diagnostics_df = pd.DataFrame.from_dict(tbr_diagnostics)

diagnostics_df

alignments_diagnostics = pm4py.conformance_diagnostics_alignments(log_csv, net, im, fm, return_diagnostics_dataframe=False)

print(alignments_diagnostics)