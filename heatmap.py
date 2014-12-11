# -*- coding: utf-8 -*-
"""
Created on Thu Dec 11 00:08:46 2014

@author: Sagar
"""

# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# ------------------------------------------------------------------------
# Filename   : heatmap.py
# Date       : 2013-04-19
# Updated    : 2014-01-04
# Author     : @LotzJoe >> Joe Lotz
# Description: My attempt at reproducing the FlowingData graphic in Python
# Source     : http://flowingdata.com/2010/01/21/how-to-make-a-heatmap-a-quick-and-easy-solution/
#
# Other Links:
#     http://stackoverflow.com/questions/14391959/heatmap-in-matplotlib-with-pcolor
#
# ------------------------------------------------------------------------

import matplotlib.pyplot as plt
import pandas as pd
from urllib2 import urlopen
import numpy as np
#%pylab inline

page = urlopen("http://datasets.flowingdata.com/ppg2008.csv")
nba = pd.read_csv(page, index_col=0)

# Normalize data columns
nba_norm = (nba - nba.mean()) / (nba.max() - nba.min())

# Sort data according to Points, lowest to highest
# This was just a design choice made by Yau
# inplace=False (default) ->thanks SO user d1337
nba_sort = nba_norm.sort('PTS', ascending=True)

nba_sort['PTS'].head(10)

# Plot it out
fig, ax = plt.subplots()
heatmap = ax.pcolor(nba_sort, cmap=plt.cm.Blues, alpha=0.8)

# Format
fig = plt.gcf()
fig.set_size_inches(8, 11)

# turn off the frame
ax.set_frame_on(False)

# put the major ticks at the middle of each cell
ax.set_yticks(np.arange(nba_sort.shape[0]) + 0.5, minor=False)
ax.set_xticks(np.arange(nba_sort.shape[1]) + 0.5, minor=False)

# want a more natural, table-like display
ax.invert_yaxis()
ax.xaxis.tick_top()

# Set the labels

# label source:https://en.wikipedia.org/wiki/Basketball_statistics
labels = [
    'Games', 'Minutes', 'Points', 'Field goals made', 'Field goal attempts', 'Field goal percentage', 'Free throws made', 'Free throws attempts', 'Free throws percentage',
    'Three-pointers made', 'Three-point attempt', 'Three-point percentage', 'Offensive rebounds', 'Defensive rebounds', 'Total rebounds', 'Assists', 'Steals', 'Blocks', 'Turnover', 'Personal foul']

# note I could have used nba_sort.columns but made "labels" instead
ax.set_xticklabels(labels, minor=False)
ax.set_yticklabels(nba_sort.index, minor=False)

# rotate the
plt.xticks(rotation=90)

ax.grid(False)

# Turn off all the ticks
ax = plt.gca()

for t in ax.xaxis.get_major_ticks():
    t.tick1On = False
    t.tick2On = False
for t in ax.yaxis.get_major_ticks():
    t.tick1On = False
    t.tick2On = False