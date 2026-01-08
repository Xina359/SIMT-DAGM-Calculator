# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

def generate_simt_data(n_samples=1000000, sigma_deg=0.5):
    np.random.seed(42)
  
    phi = np.random.uniform(0, 2*np.pi, n_samples)
    costheta = np.random.uniform(-1, 1, n_samples)
    u = np.random.uniform(0, 1, n_samples)
    theta = np.arccos(costheta)
    r = 200 * (u ** (1/3))
    
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)
    points = np.vstack((x, y, z)).T
    distances = np.linalg.norm(points, axis=1)


    sigma_rad = np.deg2rad(sigma_deg)
    angles = np.random.normal(0, sigma_rad, (n_samples, 3))


    cross_prod = np.cross(angles, points)
    tre_approx = np.linalg.norm(cross_prod, axis=1)


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
    
    residuals = np.abs(tre_exact - tre_approx) * 1000 
    return tre_approx, tre_exact, residuals, distances



approx_05, exact_05, _, dist_05 = generate_simt_data(n_samples=1000000, sigma_deg=0.5)


_, _, res_02, dist_02 = generate_simt_data(n_samples=200000, sigma_deg=0.2)
_, _, res_05, dist_05_sub = generate_simt_data(n_samples=200000, sigma_deg=0.5)
_, _, res_10, dist_10 = generate_simt_data(n_samples=200000, sigma_deg=1.0)


import numpy as np
import matplotlib.pyplot as plt


plt.figure(figsize=(6, 5))


idx = np.random.choice(len(dist_05), 50000, replace=False)
dist_plot = dist_05[idx]
exact_plot = exact_05[idx]


plt.scatter(dist_plot, exact_plot, s=1, c='blue', alpha=0.3, label='Exact Calculation')


slopes = exact_plot / (dist_plot + 1e-6) 
max_slope_tight = np.percentile(slopes, 99.99) 

x_line = np.linspace(0, 205, 100)
y_line = x_line * max_slope_tight
plt.plot(x_line, y_line, 'r--', linewidth=2.5, label='Linear Model (Upper Bound)')


#plt.title('Figure 1: Error Propagation\n(Standard Scenario: $\sigma=0.5^\circ$)', fontsize=12, fontweight='bold')
plt.xlabel('Distance to Isocenter (mm)', fontsize=11)
plt.ylabel('Target Registration Error (mm)', fontsize=11)
plt.legend(loc='upper left', fontsize=10)
plt.grid(True, linestyle=':', alpha=0.6)

plt.xlim(0, 205)

plt.ylim(0, np.max(y_line) * 1.05)

plt.tight_layout()
plt.savefig('Fig1_ErrorPropagation_Final.png', dpi=300)
plt.show()
