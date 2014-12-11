# -*- coding: utf-8 -*-
"""
Created on Sat Nov 29 17:27:36 2014

@author: Sagar
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import matplotlib as mpl
from scipy.stats import gaussian_kde
#import matplotlib.image as img
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
from matplotlib._png import read_png
import Image
from scipy import misc
import ImageChops
#mpl.style.use('ggplot')
#plt.hist(np.random.randn(100000))

PATH = '/Volumes/Daten/documents/edu/exploring neural dat/ME Motor Cortex Data Project/motor_dataset.npy'
data1 = np.load('distractor_data_set1.npy')[()]
data2 = np.load('distractor_data_set2.npy')[()]
data3 = np.load('distractor_data_set3.npy')[()]
df1 = pd.DataFrame({'stimon': data1['stimon'], 'target': data1['stim_names'], 'spikes': data1['spk_times'], 'stim_scales':data1['stim_scales']})
df2 = pd.DataFrame({'stimon': data2['stimon'], 'target': data2['stim_names'], 'spikes': data2['spk_times'], 'stim_scales':data2['stim_scales']})
df2=df2[158:-1]
df3 = pd.DataFrame({'stimon': data3['stimon'], 'target': data3['stim_names'], 'spikes': data3['spk_times']})

# (*) Import plotly package
import plotly

# Check plolty version (if not latest, please upgrade)
print plotly.__version__
import os

lm = np.load('dm.npy')

def getPic(pic):

    for filename in os.listdir("./stimuli/"):
        if filename.startswith(pic):
            print filename
            picture = read_png('./stimuli/'+str(filename))

    return picture

def getPic2():
    pList = {}
    for filename in os.listdir("./stimuli/"):
        if filename.endswith('00.png'):
            picture = misc.imread('./stimuli/'+str(filename))
            pList[filename] = picture

    return pList

def getImgDiff(pic1, pic2):
    img1 = Image.fromarray(pic1)
    img2 = Image.fromarray(pic2)
    #img1.show()

    diff = ImageChops.difference(img1, img2)

    return diff

def createDistanceMatrix():
    myPictures = getPic2()
    rc=np.size(myPictures.keys())
    distanceM = np.zeros([rc,rc])
    keys = myPictures.keys()

    try:
        for i in range(0, len(keys)):
            for j in range(0, len(keys)):
                distanceM[i,j]=np.sum(getImgDiff(myPictures[keys[i]], myPictures[keys[j]]))
    except KeyError:
        pass

    return distanceM

def createHeatMap():
    myPics=getPic2()
    keys = myPics.keys()
    df=pd.DataFrame(lm, columns=keys)
    fig, ax = plt.subplots()
    heatmap = ax.pcolor(df, cmap=plt.cm.Blues, alpha=0.8)
    return df



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

def sortMatrix2(df, pic, ms):
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
    
    #print matrix
    # get total rows
    rows = np.size(matrix, 0)
    #print rows
    freq = {} 
    intervall = range(0, 3500, ms)    
    #print intervall
    
    for i in range(0, rows):
        #print i
        data = matrix[i,:][np.where(matrix[i]>0)]
        #print data
        frequencies = []
        for j in range(0, len(intervall)):
        #print i
            try:
                count = np.size(np.where((data > intervall[j]) & (data <= intervall[j+1])))
            #print count
            #num = len(np.where((data > intervall[i]) & (data <= intervall[i+1])))
                frequencies.append(count/float(ms*10**-3))
            #print rate
            except IndexError:
                pass
            
        freq[i]=frequencies
    
    return freq


def createFPlot(dic, ms):
    rows = len(dic)
    cols = 0
    keys = dic.keys()
    for k in keys:
        if len(dic[k]) > cols:
            cols = len(dic[k]) 
    
    fMatrix = np.zeros([rows, cols])
    
    for i in keys:
        for j in range(0, len(dic[i])):
            fMatrix[i,j] = dic[i][j]
    
    np.sqrt(np.mean(fMatrix, 0))
    
    x = range(0, np.size(fMatrix, 1))
    plt.errorbar(x, np.mean(fMatrix, 0), yerr=np.sqrt(np.var(l, 0)))
    plt.xlabel('Timeframe ' + str(ms) + 'ms' )
    plt.ylabel('Frequency (Hz)')
    
    return fMatrix
    

def createFPlot2(df, pic, ms):
    dic=sortMatrix2(df, pic, 100)

    rows = len(dic)
    cols = 0
    keys = dic.keys()
    for k in keys:
        if len(dic[k]) > cols:
            cols = len(dic[k]) 
    
    fMatrix = np.zeros([rows, cols])
    
    for i in keys:
        for j in range(0, len(dic[i])):
            fMatrix[i,j] = dic[i][j]
    
    #np.sqrt(np.mean(fMatrix, 0))
    x = range(0, np.size(fMatrix, 1))
    color=['b', 'g', 'r', 'c', 'm', 'y', 'b', 'grey', 'Purple', 'Violet', 'Plum', 'Khaki', 'Lime', 'Pink']
        
    f = plt.figure(figsize=(6, 5))
    
    for i in range(0, rows):
        plt.plot(x, fMatrix[i,:], color=color[i], linestyle='-')
    
    plt.xlim([-1, x[-1]+1])
    plt.title('Single unit activity in ' + str(ms) + ' ms timeframes (' + str(pic) + ')')
    plt.xlabel('Timeframe (' + str(ms) + ' ms)' )
    plt.ylabel('Frequency (Hz)')
    plt.legend(['N1', 'N2', 'N3', 'N4','N5', 'N6','N7', 'N8', 'N9', 'N10', 'N11', 'N12', 'N13', 'N14', 'N15'])
    
    plt.savefig('dis2su' + pic, dpi=100)

    

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


def get_rate(df, pic):
    """Return the rate for a single set of spike times given
    a spike counting interval of start to stop (inclusive)."""

    ####
    #### Programming Problem 6:
    ####    Get rate from list of spk_times and [start,stop) window
    ####

    # rate = *** YOUR CODE HERE ***
    # Remember that rate should be in the units spikes/sec
    # but start and stop are in msec (.001 sec)
    data=mergeMatrix(df, pic)
    data=np.sort(data)
    intervall = [-1000, 0, 1000, 2000, 3000]
    rates = []

    for i in intervall:
        count = np.size(data[(data > i) & (data <= i+1000)])
        print count
        rate = count
        rates.append(rate)
    return rates

def get_rate2(df, pic, ms):
    """Return the rate for a single set of spike times given
    a spike counting interval of start to stop (inclusive)."""

    ####
    #### Programming Problem 6:
    ####    Get rate from list of spk_times and [start,stop) window
    ####

    # rate = *** YOUR CODE HERE ***
    # Remember that rate should be in the units spikes/sec
    # but start and stop are in msec (.001 sec)
    data=mergeMatrix(df, pic)
    data=np.sort(data)
    #print data
    intervall = range(0, 3500, ms)
    #print intervall
    rates = []

    for i in range(0, len(intervall)):
        #print i
        try:
            count = np.size(np.where((data > intervall[i]) & (data <= intervall[i+1])))
            #print count
            #num = len(np.where((data > intervall[i]) & (data <= intervall[i+1])))
            rate = count/float(ms*10**-3)
            #print rate
        except IndexError:
            pass
        rates.append(rate)

    return rates


def createHistogram(df, pic, bins=45, rates=False):
    data=mergeMatrix(df, pic)
    matrix=sortMatrix(df, pic)


    density = gaussian_kde(data)
    xs = np.linspace(min(data), max(data), max(data))
    density.covariance_factor = lambda : .25
    density._compute_covariance()
    #xs = np.linspace(min(data), max(data), 1000)

    fig,ax1 = plt.subplots()
    #plt.xlim([0, 4000])
    plt.hist(data, bins=bins, range=[-500, 4000], histtype='stepfilled', color='grey', alpha=0.5)
    lims = plt.ylim()
    height=lims[1]-2
    for i in range(0,len(matrix)):
        currentRow = matrix[i][np.nonzero(matrix[i])]
        plt.plot(currentRow, np.ones(len(currentRow))*height, '|', color='black')
        height -= 2

    plt.axvline(x=0, color='red', linestyle='dashed')
    #plt.axvline(x=1000, color='black', linestyle='dashed')
    #plt.axvline(x=2000, color='black', linestyle='dashed')
    #plt.axvline(x=3000, color='black', linestyle='dashed')

    if rates:
        rates = get_rate(df, pic)
        ax1.text(-250, 4, str(rates[0]), size=15, ha='center', va='center', color='green')
        ax1.text(500, 4, str(rates[1]), size=15, ha='center', va='center', color='green')
        ax1.text(1500, 4, str(rates[2]), size=15, ha='center', va='center', color='green')
        ax1.text(2500, 4, str(rates[3]), size=15, ha='center', va='center', color='green')
        ax1.text(3500, 4, str(rates[4])+ r' $\frac{\mathsf{Spikes}}{\mathsf{s}}$', size=15, ha='center', va='center', color='green')
    plt.ylim([0,lims[1]+5])
    plt.xlim([0, 4000])
    plt.title('Histogram for ' + str(pic))
    ax1.set_xticklabels([-500, 'Start\nStimulus', 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000])
    plt.xlabel('Time (ms)')
    plt.ylabel('Counts (Spikes)')


    print lims
    arr_hand = getPic(pic)
    imagebox = OffsetImage(arr_hand, zoom=.3)
    xy = [3200, lims[1]+5]               # coordinates to position this image

    ab = AnnotationBbox(imagebox, xy, xybox=(30., -30.), xycoords='data',boxcoords="offset points")
    ax1.add_artist(ab)

    ax2 = ax1.twinx() #Necessary for multiple y-axes

    #Use ax2.plot to draw the hypnogram.  Be sure your x values are in seconds
    ax2.plot(xs, density(xs) , 'g', drawstyle='steps')
    plt.ylim([0,0.001])
    plt.yticks([0.0001,0.0002, 0.0003, 0.0004, 0.0005, 0.0006, 0.0007, 0.0008, 0.0009])
    ax2.set_yticklabels([1,2,3,4, 5, 6, 7, 8, 9])
    plt.ylabel(r'Density ($\cdot \mathsf{10^{-4}}$)', color='green')
    plt.gcf().subplots_adjust(right=0.89)
    plt.gcf().subplots_adjust(bottom=0.2)
    plt.savefig(pic, dpi=150)

from matplotlib import gridspec
from matplotlib.lines import Line2D
from matplotlib.text import Text
from mpl_toolkits.axes_grid.axislines import Subplot

def cHisto(df, pic, bins=45):
    data=mergeMatrix(df, pic)
    matrix=sortMatrix(df, pic)
    
    f = plt.figure(figsize=(6, 5))
    plt.subplots_adjust(hspace=0.001)
    
    height = 7
    
    gs = gridspec.GridSpec(2,1, height_ratios=[0.2, .8])
    
    ax1 = plt.subplot(gs[0])
    #ax1 = f.add_axes([0., 0., 0., 1., ])
    ax1.axes.get_xaxis().set_visible(False)
    #ax1.axis["bottom"].toggle(all=False)
    for i in range(0,len(matrix)):
        currentRow = matrix[i][np.nonzero(matrix[i])]
        ax1.plot(currentRow, np.ones(len(currentRow))*height, '|', color='black')
        height -= 1.5
    plt.ylim([0,8])
    plt.yticks([])
    
    plt.title('Histogram for ' + str(pic))
    

    # Lower Plot    
    ax2 = plt.subplot(gs[1], sharex=ax1)
    #ax2.axes.get_xaxis().set_visible(False)
    ax2.hist(data, bins=bins, range=[-500, 4000], histtype='stepfilled', color='grey', alpha=0.5)
    ax2.get_xaxis().tick_bottom()
    
    xmin, xmax = ax2.get_xaxis().get_view_interval()
    ymin, ymax = ax2.get_yaxis().get_view_interval()
    
    thumb = getPic(pic)
    imagebox = OffsetImage(thumb, zoom=.3)
    xy = [xmax-750, ymax]               # coordinates to position this image

    ab = AnnotationBbox(imagebox, xy, xybox=(30., -30.), xycoords='data',boxcoords="offset points")
    ax2.add_artist(ab)
    
    
    plt.xlim([-500, 4000])
    
    ax2.set_xticklabels([-500, 'Start\nStimulus', 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000])
    plt.xlabel('Time (ms)')
    plt.ylabel('Counts (Spikes)')
    plt.axvline(x=0, color='red', linestyle='dashed')
    
    #print ymax, ymin    
    #ax2.add_artist(Line2D((xmin, xmax), (ymax+1, ymax+1), color='w', linewidth=5))
    
    #plt.xticklabels = ax1.get_xticklabels()+ax2.get_xticklabels()
    #plt.setp(xticklabels, visible=False)

    plt.savefig('dis3' + pic, dpi=100)



def createDensityPlot(data):
    
    density = gaussian_kde(data)
    xs = np.linspace(min(data), max(data), 1000)
    density.covariance_factor = lambda : .25
    density._compute_covariance()
    plt.plot(xs,density(xs))


for key in np.unique(df2['target']):
    try:
        createFPlot2(df2, key, 100)
    except IndexError:
        pass
