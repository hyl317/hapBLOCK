"""
Classes and functions to plot the simulated and processed Mosaic ROH Data
Python Functions to keep functions and analysis seperate
@ Author: Harald Ringbauer, 2019, All rights reserved
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib import gridspec

def plot_power(bl_lens, df_call_vec1, powers, df_fp=[], 
               xlim=(0,12.5), figsize=(10,6), n=100, ylim_pow=[0.5, 1.05],
               leg_loc="upper right", fs_l=12, fs = 12, fs_t=10, hspace=0.04,
               lw_power=1.2, color_fp="red", ec="silver", cmap="viridis_r",
               pw_yticks=[0.5,0.75,1.0], s=100,
               alpha=0.8, savepath="", title=""):
    """ bl_lens: Array of Block Lengths
        df_call_vec1: Array of Called Blocks
        powers: Array of Power to call Blocks
    Load, and plot power and power curves
    s: Size of ticks on y axis
    pw_ticks: Where to set the ticks for the power
    lw_power: Line width of power plot""" 
    assert(len(bl_lens)==len(df_call_vec1)==len(powers)) # Sanity Check
    bins = np.linspace(0, 30, 151) # Bins of 0.2 cM
    
    ### Set Colors
    cmap = cm.get_cmap(cmap)
    colors = [cmap(x) for x in np.linspace(0,1, len(bl_lens))]
    
    ####### Do the actual Plot
    plt.figure(figsize=figsize)

    gs = gridspec.GridSpec(2, 1, height_ratios=[1, 4])
    gs.update(hspace=hspace) # set the spacing between axes. 

    ax = plt.subplot(gs[1]) # The lower subplot
    ax1 = plt.subplot(gs[0]) # The upper subplot
    
    ### Set Font Sizes
    ax.tick_params(axis='both', labelsize=fs_t)
    ax1.tick_params(axis='both', labelsize=fs_t)

    # Plot All Histograms        
    for i in range(len(bl_lens)):
        l = bl_lens[i]
        ax.hist(df_call_vec1[i]["CalledLength"], bins = bins, color = colors[i], alpha=alpha, 
                label= str(l) + " cM", ec=ec)
        ax.axvline(l, color = "gray", linewidth=2)
    
    if len(df_fp)>0:
        ax.hist(df_fp["lengthM"]*100, bins = bins, color = color_fp, 
                alpha=1.0, label= "FP", ec=ec)
        
    ax.set_xlim(xlim)
    ax.set_xlabel("Inferred IBD Length [cM]", fontsize = fs)
    ax.set_ylabel("# Inferred \nIBD blocks", fontsize = fs)
    if len(leg_loc)>0:
        legend = ax.legend(loc = leg_loc, fontsize = fs_l, title="Simulated IBD")
        legend.get_title().set_fontsize(fs_l)

    ### Plot the upper panel
    ax1.set_ylabel("Called at \n80% overlap", fontsize = fs)
    ax1.set_xticks([])
    ax1.yaxis.set_ticks(pw_yticks)
    for y in pw_yticks:
        ax1.axhline(y, linestyle='--', color='gray', lw=0.3, zorder=0)
    ax1.scatter(bl_lens, powers, c=colors, s=s, zorder=2, ec=ec)
    ax1.plot(bl_lens, powers, "gray", zorder=1, lw=lw_power)
    ax1.set_xlim(xlim)
    ax1.set_ylim(ylim_pow)

    plt.title(title, fontsize=fs)
    
    if len(savepath)>0:
        plt.savefig(savepath, bbox_inches ='tight', pad_inches = 0, dpi=400)
        print(f"Saved to {savepath}")
    plt.show()
    
    
def plot_fp_distribution(df_call_fp, fs = 14, fs_l = 12, bins = np.linspace(1, 3, 26), xlim = (0, 13), figsize = (10, 4),
                        title = "100 Mosaic Tuscany Samples - Reference: Rest EUR 1000G"):
    """ Plot the Distribution of false positive ROH calls"""
    ### The Actual Plot
    plt.figure(figsize=figsize)

    ax = plt.gca()
    ax.hist(df_call_fp["lengthM"] * 100, bins = bins, color = "green", alpha=0.9, ec="silver")
    ax.set_xlabel("Inferred block Length [cm]", fontsize=fs)
    ax.set_ylabel("Count", fontsize=fs)
    roh1cm = np.sum(df_call_fp["lengthM"]>0.01)
    ax.text(x=0.6, y=0.8, s=f"Tot. #ROH > 1cM: {roh1cm}", transform=ax.transAxes, fontsize=fs)  
    
    plt.title(title, fontsize=fs)
    plt.show()
    
    
# def plot_posterior(basepath, start=-1, end=-1, prefix=""):
#     # I assume the two files, map.npy and posterior.npy, reside in basepath
#     r_map = np.load(f'{basepath}/map.npy', 'r')
#     r_map = 100*r_map # cM is more intuitive for me
#     post = np.load(f'{basepath}/posterior.npy', 'r')
#     _, l = post.shape
#     assert(len(r_map) == l) # sanity check

#     i = np.searchsorted(r_map, start) if start != -1 else 0
#     j = np.searchsorted(r_map, end) if end != -1 else -1

#     for k in range(1,5):
#         plt.plot(r_map[i:j], post[k, i:j], label=f'state {k}', linewidth=0.25, alpha=0.75)
#     plt.plot(r_map[i:j], np.sum(post[1:5, i:j], axis=0), label='sum of IBD1 states', color='black', linewidth=0.75)
#     plt.plot(r_map[i:j], np.sum(post[5:7, i:j], axis=0), label='sum of IBD2 states', color='grey', linewidth=0.75)
#     plt.xlabel('Genomic Position')
#     plt.ylabel('Posterior')
#     plt.legend(loc='upper right', fontsize='xx-small')
#     if len(prefix) == 0:
#         plt.savefig(f'{basepath}/posterior.png', dpi=300)
#     else:
#         plt.savefig(f'{basepath}/posterior.{prefix}.png', dpi=300)
#     plt.clf()
    

#################################################### yilei's version #############################################################
##################################################################################################################################
#################################################################################################################################
def plot_power_yilei(bl_lens, df_call_vec1, powers, df_fp=[], 
               xlim=(0,12.5), figsize=(10,6), n=100, ylim_pow=[0.5, 1.05],
               leg_loc="upper right", fs_l=12, fs = 12, fs_t=10, hspace=0.04,
               lw_power=1.2, color_fp="red", ec="silver", cmap="viridis_r",
               pw_yticks=[0.5,0.75,1.0], s=100,
               alpha=0.8, savepath="", title=""):
    """ bl_lens: Array of Block Lengths
        df_call_vec1: Array of Called Blocks
        powers: Array of Power to call Blocks
    Load, and plot power and power curves
    s: Size of ticks on y axis
    pw_ticks: Where to set the ticks for the power
    lw_power: Line width of power plot""" 
    assert(len(bl_lens)==len(df_call_vec1)==len(powers)) # Sanity Check
    bins = np.linspace(0, 30, 151) # Bins of 0.2 cM
    
    ### Set Colors
    cmap = cm.get_cmap(cmap)
    colors = [cmap(x) for x in np.linspace(0,1, len(bl_lens))]
    
    ####### Do the actual Plot
    plt.figure(figsize=figsize)

    gs = gridspec.GridSpec(2, 1, height_ratios=[1, 4])
    gs.update(hspace=hspace) # set the spacing between axes. 

    ax = plt.subplot(gs[1]) # The lower subplot
    ax1 = plt.subplot(gs[0]) # The upper subplot
    
    ### Set Font Sizes
    ax.tick_params(axis='both', labelsize=fs_t)
    ax1.tick_params(axis='both', labelsize=fs_t)

    # Plot All Histograms        
    for i in range(len(bl_lens)):
        l = bl_lens[i]
        ax.hist(df_call_vec1[i], bins = bins, color = colors[i], alpha=alpha, 
                label= str(l) + " cM", ec=ec)
        ax.axvline(l, color = "gray", linewidth=2)
    
    if len(df_fp)>0:
        ax.hist(df_fp["lengthM"]*100, bins = bins, color = color_fp, 
                alpha=1.0, label= "FP", ec=ec)
        
    ax.set_xlim(xlim)
    ax.set_xlabel("Inferred IBD Length [cM]", fontsize = fs)
    ax.set_ylabel("# Inferred \nIBD blocks", fontsize = fs)
    ax.set_xticks(bl_lens)
    if len(leg_loc)>0:
        legend = ax.legend(loc = leg_loc, fontsize = fs_l, title="Simulated IBD")
        legend.get_title().set_fontsize(fs_l)

    ### Plot the upper panel
    ax1.set_ylabel("Called at \n80% overlap", fontsize = fs)
    ax1.set_xticks([])
    ax1.yaxis.set_ticks(pw_yticks)
    for y in pw_yticks:
        ax1.axhline(y, linestyle='--', color='gray', lw=0.3, zorder=0)
    ax1.scatter(bl_lens, powers, c=colors, s=s, zorder=2, ec=ec)
    ax1.plot(bl_lens, powers, "gray", zorder=1, lw=lw_power)
    ax1.set_xlim(xlim)
    ax1.set_ylim(ylim_pow)

    plt.title(title, fontsize=fs)
    
    if len(savepath)>0:
        plt.savefig(savepath, bbox_inches ='tight', pad_inches = 0, dpi=400)
        print(f"Saved to {savepath}")
    plt.show()