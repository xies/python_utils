#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 17:11:53 2016

@author: mimi
"""

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable

def plot_stack(im1,cmap1 = 'gray'):

    Z = im1.shape[0]
    nrows = np.int(np.ceil(np.sqrt(Z)))
    ncols = np.int(Z // nrows + 1)
        
    fig, axes = plt.subplots(nrows, ncols, figsize=(3*ncols, 3*nrows))
    
    for z in range(Z):
        i = z // ncols
        j = z % ncols
        axes[i, j].imshow(im1[z, ...], interpolation='nearest', cmap=cmap1)
        
        axes[i, j].set_xticks([])
        axes[i, j].set_yticks([])
    
    ## Remove empty plots 
    for ax in axes.ravel():
        if not(len(ax.images)):
            fig.delaxes(ax)
            
    fig.tight_layout()

def plot_2stacks(im1,im2,cmap1 = 'gray',cmap2='Dark2'):
    assert im1.shape == im2.shape,"Both images must be the same size!"

    Z = im1.shape[0]
    nrows = np.int(np.ceil(np.sqrt(Z)))
    ncols = np.int(Z // nrows + 1)
        
    fig, axes = plt.subplots(nrows, ncols*2, figsize=(3*ncols, 1.5*nrows))
    
    for z in range(Z):
        i = z // ncols
        j = z % ncols * 2
        axes[i, j].imshow(im1[z, ...], interpolation='nearest', cmap=cmap1)
        axes[i, j+1].imshow(im1[z, ...], interpolation='nearest', cmap=cmap2)
        
        axes[i, j].set_xticks([])
        axes[i, j].set_yticks([])
        axes[i, j+1].set_xticks([])
        axes[i, j+1].set_yticks([])
    
    ## Remove empty plots 
    for ax in axes.ravel():
        if not(len(ax.images)):
            fig.delaxes(ax)
            
    fig.tight_layout()

def plot_stack_projections(image_stack,xy_scale,z_scale):
    fig = plt.figure(figsize=(12, 12))
    
    # xy projection:
    ax_xy = fig.add_subplot(111)
    ax_xy.imshow(image_stack.max(axis=0), cmap='gray')
    
    # ZX projection
    divider = make_axes_locatable(ax_xy)
    ax_zx = divider.append_axes("top", 2, pad=0.2, sharex=ax_xy)
    ax_zx.imshow(image_stack.max(axis=1), aspect=z_scale/xy_scale, cmap='gray')

    # YZ projection
    ax_yz = divider.append_axes("right", 2, pad=0.2, sharey=ax_xy)
    ax_yz.imshow(image_stack.max(axis=2).T, aspect=xy_scale/z_scale, cmap='gray')
    plt.draw()

#
#def sitk_show(img, title=None, margin=0.05, dpi=40 ):
#    nda = SimpleITK.GetArrayFromImage(img)
#    spacing = img.GetSpacing()
#    figsize = (1 + margin) * nda.shape[0] / dpi, (1 + margin) * nda.shape[1] / dpi
#    extent = (0, nda.shape[1]*spacing[1], nda.shape[0]*spacing[0], 0)
#    fig = plt.figure(figsize=figsize, dpi=dpi)
#    ax = fig.add_axes([margin, margin, 1 - 2*margin, 1 - 2*margin])
#
#    plt.set_cmap("gray")
#    ax.imshow(nda,extent=extent,interpolation=None)
#    
#    if title:
#        plt.title(title)
#    
#    plt.show()
    
def df_average(df, weights_column):
    '''Computes the average on each columns of a dataframe, weighted
    by the values of the column `weight_columns`.
    
    Parameters:
    -----------
    df: a pandas DataFrame instance
    weights_column: a string, the column name of the weights column 
    
    Returns:
    --------
    
    values: pandas DataFrame instance with the same column names as `df`
        with the weighted average value of the column
    '''
    
    values = df.copy().iloc[0]
    norm = df[weights_column].sum()
    for col in df.columns:
        try:
            v = (df[col] * df[weights_column]).sum() / norm
        except TypeError:
            v = df[col].iloc[0]
        values[col] = v
    return values
