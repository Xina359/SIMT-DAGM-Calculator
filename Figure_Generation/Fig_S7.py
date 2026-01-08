# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.patches import Rectangle

def generate_final_heatmap_s1():

    distances_cm = np.array([2, 4, 6, 8, 10, 12, 14, 16, 18, 20]) 
    sigmas_deg = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0]) 
    

    data = np.zeros((len(distances_cm), len(sigmas_deg)))
    
    for i, d_cm in enumerate(distances_cm):
        for j, sigma in enumerate(sigmas_deg):
            d_mm = d_cm * 10 
            #  M = d * sin(2.45 * sigma)

            angle_rad = np.deg2rad(2.45 * sigma)
            data[i, j] = d_mm * np.sin(angle_rad)


    plt.figure(figsize=(11, 8), dpi=300)
    

    colors = ['#e6f4ea', '#c8e6c9', 
              '#fff9c4', '#fff59d', 
              '#ffccbc', '#ffab91', '#ff8a65', '#e57373'] 
    

    bounds = [0, 1.0, 1.5, 2.0, 2.5, 3.5, 5.0, 7.0, 10.0] 
    cmap = ListedColormap(colors)
    norm = BoundaryNorm(bounds, cmap.N)


    ax = sns.heatmap(data, annot=True, fmt=".2f", annot_kws={"size": 14, "fontfamily": "Times New Roman"},
                     cmap=cmap, norm=norm,
                     xticklabels=sigmas_deg, yticklabels=distances_cm,
                     linewidths=1.5, linecolor='white', 
                     cbar_kws={'label': 'Required PTV Margin (mm)', 'shrink': 1})
    

    cbar = ax.collections[0].colorbar
    cbar.set_ticks([0.75, 2.0, 5.0]) 
    cbar.set_ticklabels(['Safe Zone\n(<1.5mm)', 'Caution\n(1.5-2.5mm)', 'High Risk\n(>2.5mm)'])
    cbar.ax.tick_params(labelsize=13)


    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = ['Times New Roman']
    

    #plt.title('PTV Margin Lookup Table\n(Calculated via: $M_{req} = d \cdot \sin(2.45\sigma)$)', 
    #          fontsize=14, pad=20, fontweight='bold')
    plt.xlabel('Mechanical Precision $\sigma$ (degree)', fontsize=16, fontweight='bold')
    plt.ylabel('Distance to Isocenter (cm)', fontsize=16, fontweight='bold')
    


    plt.tight_layout()
    plt.show()

generate_final_heatmap_s1()