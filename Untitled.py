# -*- coding: utf-8 -*-
"""
Created on Sat Nov 29 17:27:36 2014

@author: Sagar
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.stats import gaussian_kde

#mpl.style.use('ggplot')
#plt.hist(np.random.randn(100000))

PATH = '/Volumes/Daten/documents/edu/exploring neural dat/ME Motor Cortex Data Project/motor_dataset.npy'
data = np.load('survey_data_set1.npy')[()]
data2 = np.load('survey_data_set2.npy')[()]
data3 = np.load('survey_data_set3.npy')[()]
df = pd.DataFrame({'stimon': data['stimon'], 'target': data['stim_names'], 'spikes': data['spk_times']})

def raster(event_times_list, color='k'):
    """
    Creates a raster plot

    Parameters
    ----------
    event_times_list : iterable
                       a list of event time iterables
    color : string
            color of vlines

    Returns
    -------
    ax : an axis containing the raster plot
    """
    ax = plt.gca()
    for ith, trial in enumerate(event_times_list):
        plt.vlines(trial, ith + .5, ith + 1.5, color=color)
    plt.ylim(.5, len(event_times_list) + .5)
    return ax


def makeMatrix(df, pic):
    keys=df[df['target']==pic]['spikes'].keys()

    cells = np.size(df[df['target']==pic]['spikes'])
    maxData = 0

    for i in keys:
        if maxData < len(df[df['target']==pic]['spikes'][i]):
            maxData = len(df[df['target']==pic]['spikes'][i])

    matrix = np.zeros((cells, maxData))
    row = 0

    for i in keys:
        currentRow = df[df['target']==pic]['spikes'][i]
        for j in range(0, len(currentRow)):
            matrix[row,j] = currentRow[j]
        row += 1


    return matrix


def sortMatrix(df, pic):
    keys=df[df['target']==pic]['stimon'].keys()
    middleVal = np.size(makeMatrix(df, pic),1)//2
    matrix = makeMatrix(df, pic)

    stimon = []

    for i in keys:
        stimon.append(i)

    row = 0

    for i in range(0, len(stimon)):
        currentRow = matrix[row]
        for j in range(0,len(currentRow)):
            matrix[i,j] -= stimon[i]
            if matrix[i,j] == -stimon[i]:
                matrix[i,j] = 0


    return matrix

def mergeMatrix(df, pic):
    keys=df[df['target']==pic]['stimon'].keys()
    matrix = sortMatrix(df, pic)

    masterArray = []

    for i in range(0, np.size(matrix,1)):
        currentCol = matrix[:, i]
        #[]print currentCol
        currentCol = currentCol[np.nonzero(currentCol)]
        #print "no zero:", currentCol
        while len(currentCol) != 0:
            masterArray.append(currentCol[np.argmin(currentCol[:])])
            currentCol=np.delete(currentCol, np.argmin(currentCol))

    return masterArray


def createHistogram(df, pic):
    data=mergeMatrix(df, pic)
    matrix=sortMatrix(df, pic)
    #xs = np.linspace(min(data), max(data), 1000)
    plt.hist(data, bins=100, histtype='stepfilled', color='grey', alpha=0.5)

    for i in len(matrix):
        currentRow
        plt.plot(data, np.ones(len(data))*25, '|')

    plt.title('Histogram for ' + str(pic))
    plt.xlabel('Time (ms)')
    plt.ylabel('Counts')


def createDensityPlot(data):
    density = gaussian_kde(data)
    xs = np.linspace(min(data), max(data), 1000)
    density.covariance_factor = lambda : .25
    density._compute_covariance()
    plt.plot(xs,density(xs))
