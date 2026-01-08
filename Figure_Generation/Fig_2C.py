# -*- coding: utf-8 -*-
import numpy as np


def generate_data():

    np.random.seed(42)
    n = 1000000
    

    phi = np.random.uniform(0, 2*np.pi, n)
    costheta = np.random.uniform(-1, 1, n)
    u = np.random.uniform(0, 1, n)
    r = 200 * (u ** (1/3))
    theta = np.arccos(costheta)
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)
    points = np.vstack((x, y, z)).T
    distances = np.linalg.norm(points, axis=1)


    def calc_scenarios(sigma):
        sigma_rad = np.deg2rad(sigma)
        angles = np.random.normal(0, sigma_rad, (n, 3))
        

        ca, sa = np.cos(angles[:,0]), np.sin(angles[:,0])
        cb, sb = np.cos(angles[:,1]), np.sin(angles[:,1])
        cg, sg = np.cos(angles[:,2]), np.sin(angles[:,2])
        
        R00 = cg*cb; R01 = cg*sb*sa - sg*ca; R02 = cg*sb*ca + sg*sa
        R10 = sg*cb; R11 = sg*sb*sa + cg*ca; R12 = sg*sb*ca - cg*sa
        R20 = -sb;   R21 = cb*sa;            R22 = cb*ca
        
        px = R00*x + R01*y + R02*z
        py = R10*x + R11*y + R12*z
        pz = R20*x + R21*y + R22*z
        
        tre_exact = np.linalg.norm(np.vstack((px, py, pz)).T - points, axis=1)
        tre_approx = np.linalg.norm(np.cross(angles, points), axis=1)
        residuals = np.abs(tre_exact - tre_approx) * 1000
        return tre_approx, tre_exact, residuals


    approx_05, exact_05, res_05 = calc_scenarios(0.5) 
    _, _, res_02 = calc_scenarios(0.2)                
    _, _, res_10 = calc_scenarios(1.0)                
    

    return distances, approx_05, exact_05, res_05, res_02, res_10


distances, approx_05, exact_05, res_05, res_02, res_10 = generate_data()

import matplotlib.pyplot as plt


plt.figure(figsize=(7, 5), dpi=300) 


idx_10 = np.random.choice(len(distances), 5000, replace=False)
idx_05 = np.random.choice(len(distances), 5000, replace=False)
idx_02 = np.random.choice(len(distances), 5000, replace=False)

plt.scatter(distances[idx_10], res_10[idx_10], s=8, c='#d62728', alpha=0.4, label=r'Low Precision ($\sigma=1.0^\circ$)')
plt.scatter(distances[idx_05], res_05[idx_05], s=8, c='#1f77b4', alpha=0.4, label=r'Standard ($\sigma=0.5^\circ$)')
plt.scatter(distances[idx_02], res_02[idx_02], s=8, c='#2ca02c', alpha=0.4, label=r'High Precision ($\sigma=0.2^\circ$)')

plt.title('Figure C: Residual Analysis\n(Robustness across Clinical Scenarios)', fontsize=13, fontweight='bold')
plt.xlabel('Distance to Isocenter (mm)', fontsize=12)
plt.ylabel('Residual Calculation Error ($\mu m$)', fontsize=12)
plt.legend(loc='upper left', fontsize=10, markerscale=2)
plt.grid(True, linestyle=':', alpha=0.6)
plt.xlim(0, 205)

plt.ylim(0, np.max(res_10[idx_10])*1.1)

plt.tight_layout()
plt.savefig('FigC_Robustness_Times.png')
plt.show()
