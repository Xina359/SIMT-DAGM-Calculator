# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats


plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']

def plot_final_schematic_v3():

    sigma = 0.5
    x = np.linspace(0, 2.0, 1000)
    pdf = stats.maxwell.pdf(x, scale=sigma)
    

    fig, ax = plt.subplots(figsize=(9, 6), dpi=300)
    

    ax.fill_between(x, pdf, color='#3b4cc0', alpha=0.08)
    

    line_det = ax.axvline(sigma, color='#d62728', linestyle='--', linewidth=3, 
               label=r'Deterministic Input ($|\vec{\theta}| = 0.5^\circ$)')
    

    line_prob, = ax.plot(x, pdf, color='#3b4cc0', linewidth=3, 
                 label=r'Probabilistic Distribution ($\sigma_{axis}=0.5^\circ$)')
    

    mask = x >= sigma
    

    poly_shift = ax.fill_between(x[mask], pdf[mask], 0, 
                    facecolor='none', 
                    edgecolor='#3b4cc0', 
                    hatch='///', 
                    linewidth=0, 
                    label='Shift due to Vector Superposition')
    

    p95_val = stats.maxwell.ppf(0.95, scale=sigma)
    ax.axvline(p95_val, color='#2ca02c', linestyle=':', linewidth=2.5, 
               label=f'Statistical P95 ({p95_val:.2f}$^\circ$)')
    

    ax.text(0.51, 1.22, 
            r'$\leftarrow$ Deterministic Input ($|\vec{\theta}| = 0.5^\circ$)', 
            color='#d62728', fontsize=12, fontweight='bold')
    

    ax.text(1.04, 0.8, 
            r'$\leftarrow$ Probabilistic Distribution ($\sigma_{axis}=0.5^\circ$)', 
            color='#3b4cc0', fontsize=12, fontweight='bold')


    
    ax.set_title('Theoretical Difference: Deterministic vs. Probabilistic Models', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Resultant Rotation Magnitude (Degrees)', fontsize=14)
    ax.set_ylabel('Probability Density', fontsize=14)
    
    ax.set_xlim(0, 1.85)
    ax.set_ylim(0, 1.3)
    

    ax.legend(loc='upper right', fontsize=11, frameon=True, fancybox=True)


    
    ax.grid(True, linestyle='--', alpha=0.4)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    plt.show()

plot_final_schematic_v3()