# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

def generate_figure_d_histogram():
    
    n_samples = 1000000
    sigma_deg = 0.5 
    
    np.random.seed(42)
    

    phi = np.random.uniform(0, 2*np.pi, n_samples)
    costheta = np.random.uniform(-1, 1, n_samples)
    u = np.random.uniform(0, 1, n_samples)
    r = 200 * (u ** (1/3))
    theta = np.arccos(costheta)
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)
    points = np.vstack((x, y, z)).T
    
 
    sigma_rad = np.deg2rad(sigma_deg)
    angles = np.random.normal(0, sigma_rad, (n_samples, 3))


    ca = np.cos(angles[:,0]); sa = np.sin(angles[:,0])
    cb = np.cos(angles[:,1]); sb = np.sin(angles[:,1])
    cg = np.cos(angles[:,2]); sg = np.sin(angles[:,2])
    
    R00 = cg*cb; R01 = cg*sb*sa - sg*ca; R02 = cg*sb*ca + sg*sa
    R10 = sg*cb; R11 = sg*sb*sa + cg*ca; R12 = sg*sb*ca - cg*sa
    R20 = -sb;   R21 = cb*sa;            R22 = cb*ca
    
    px = R00*x + R01*y + R02*z
    py = R10*x + R11*y + R12*z
    pz = R20*x + R21*y + R22*z
    points_prime = np.vstack((px, py, pz)).T
    
    tre_exact = np.linalg.norm(points_prime - points, axis=1)
    
   
    cross_prod = np.cross(angles, points)
    tre_approx = np.linalg.norm(cross_prod, axis=1)
    

    residuals = np.abs(tre_exact - tre_approx) * 1000 
    

    plt.figure(figsize=(6, 5))
    
 
    limit_p995 = np.percentile(residuals, 99.5)
    

    plt.hist(residuals, bins=60, range=(0, limit_p995), 
             color='#1f77b4', alpha=0.75, edgecolor='black', linewidth=0.5)
    

    mean_err = np.mean(residuals)
    max_err = np.max(residuals) 
    std_err = np.std(residuals)
    
    stats_text = (f'Statistics ($N=10^6$):\n'
                  f'Mean Error: {mean_err:.2f} $\mu m$\n'
                  f'Std Dev: {std_err:.2f} $\mu m$\n'
                  f'Max Error: {max_err:.1f} $\mu m$')
    
 
    plt.gca().text(0.55, 0.75, stats_text, transform=plt.gca().transAxes, 
                   fontsize=10, verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='gray'))

    plt.title('Figure D: Error Distribution Analysis\n(Standard Scenario: $\sigma=0.5^\circ$)', fontsize=12, fontweight='bold')
    plt.xlabel('Residual Calculation Error ($\mu m$)', fontsize=11)
    plt.ylabel('Frequency (Count)', fontsize=11)
    plt.grid(True, linestyle=':', alpha=0.6)
    
    plt.tight_layout()
    plt.savefig('FigD_ErrorDistribution.png', dpi=300)
    plt.show()

generate_figure_d_histogram()