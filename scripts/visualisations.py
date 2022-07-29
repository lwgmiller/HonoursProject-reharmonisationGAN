import os, os.path, shutil
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pypianoroll
import scipy
import pandas as pd

from pypianoroll import Multitrack
from scipy.signal import savgol_filter
from scipy import stats


import settings

#A function used to plot the pianoroll of a given pypianoroll multitrack.
def Plot_Pianoroll(multitrack: Multitrack):

#Setting the axis of the plot based on piece size.
    axs = multitrack.plot()
    plt.gcf().set_size_inches((16, 8))
    for ax in axs:
        for x in range(
            settings.measure_resolution,
            4 * settings.measure_resolution * settings.n_measures,
            settings.measure_resolution
        ):
            if x % (settings.measure_resolution * 4) == 0:
                ax.axvline(x - 0.5, color='k')
            else:
                ax.axvline(x - 0.5, color='k', linestyle='-', linewidth=1)
    plt.show()


#Plots the training loss logs for the model, taking in the two loss lists, and also a directory to save the plot to.
def Plot_Loss_Logs(G_loss: list, D_loss: list, train_out_dir_p: str, figSize=(15, 5)):

    plt.ion()
    sns.set()
    plt.figure(figsize=figSize)
    plt.plot(D_loss, alpha=0.5, label='D_loss')
    plt.plot(G_loss, alpha=0.5, label='G_loss')
	
	#The savgol filter is used to smooth the results
    plt.plot(savgol_filter(D_loss, 53, 3))
    plt.plot(savgol_filter(G_loss, 53, 3))
    plt.legend(loc='lower right', fontsize='medium')
    plt.xlabel('Iterations (Sampled every 10 iterations)', fontsize='x-large')
    plt.ylabel('Losses', fontsize='x-large')
    plt.title('Training History', fontsize='xx-large')

#Saves the file to a directory in the repository
    plt.savefig(os.path.join(train_out_dir_p, 'model_loss.png'))


#Function to plot the results of the Mahalanobis distance evaluation, taking up to four data distributions.
def Plot_Mahalonobis_Distance(dataOne: list, dataTwo: list = [], dataThree: list = [], dataFour: list = []):
    range = (0, 30)
    bins = np.linspace(0, 60, 100)
    plt.ion()
    sns.set()
    plt.figure(figsize=(15, 5))
	
	#Distplot is used to plot histograms as well as the KDE filter
    sns.distplot(dataOne, label='Random generation')
    sns.distplot(dataTwo, label='Ordered optimisation')
    sns.distplot(dataThree, label='More samples optimisation')
    sns.distplot(dataFour, label = 'best generation')
    plt.legend(loc='upper right')
    plt.xlabel('Distance', fontsize='large')
    plt.ylabel('Probability Density', fontsize='large')
    plt.title('Mahalonobis Distance', fontsize='xx-large')


    plt.show()
