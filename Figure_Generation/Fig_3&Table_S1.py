# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Data Verification
def verify_table_data():
    distances_cm = np.arange(2, 22, 2) # 2.0 to 20.0 cm
    distances_mm = distances_cm * 10
    angles = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0])
    
    
    df_calc = pd.DataFrame(index=distances_cm, columns=angles)
    
    for d in distances_mm:
        for theta in angles:
            # TRE = d * sin(theta_rad)
            theta_rad = np.deg2rad(theta)
            tre = d * np.sin(theta_rad)
            df_calc.loc[d/10, theta] = round(tre, 2)
            
    print("Calculated Table 1 Data:")
    print(df_calc)
    return df_calc

# 2. Heatmap with Contours
def plot_heatmap_contour():
    
    d_grid = np.linspace(0, 20, 100) # 0-20 cm
    a_grid = np.linspace(0, 1.0, 100) # 0-1.0 deg
    D, A = np.meshgrid(d_grid, a_grid)
    
    # TRE 
    TRE = (D * 10) * np.sin(np.deg2rad(A))
    
    # Times New Roman
    plt.rcParams["font.family"] = "serif"
    plt.rcParams["font.serif"] = ["Times New Roman"]
    
    fig, ax = plt.subplots(figsize=(8, 6), dpi=300)
    
    # Contourf
    levels = np.linspace(0, 4.0, 21)
    cp = ax.contourf(D, A, TRE, levels=levels, cmap='RdYlBu_r', alpha=0.9, extend='max')
    cbar = fig.colorbar(cp, label='Max Theoretical TRE (mm)')
    
    # 1.0 mm and 2.0 mm
    # 1mm line
    cs1 = ax.contour(D, A, TRE, levels=[1.0], colors='white', linewidths=2.5, linestyles='--')
    ax.clabel(cs1, fmt='1.0 mm (Tol.)', inline=True, fontsize=14)
    
    # 2mm line
    cs2 = ax.contour(D, A, TRE, levels=[2.0], colors='black', linewidths=2.5, linestyles=':')
    ax.clabel(cs2, fmt='2.0 mm (Risk)', inline=True, fontsize=14)
    
    #ax.set_title('Geometric Error Landscape (Heatmap)\nDistance vs. Rotation', fontsize=14, fontweight='bold')
    ax.set_xlabel('Distance to Isocenter (cm)', fontsize=15)
    ax.set_ylabel('Residual Rotation Error (deg)', fontsize=15)
    

    ax.axhline(0.5, color='gray', linestyle='-', alpha=0.5, linewidth=1)
    ax.text(0.5, 0.51, 'Standard Scenario (0.5$^\circ$)', color='black', fontsize=14)
    
    plt.tight_layout()
    plt.savefig('Table1_Visualization_Heatmap.png')
    plt.show()

df_verified = verify_table_data()
plot_heatmap_contour()