# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt


n_simulations = 1000000
sigma_rot = 0.5 
d = 10.0 


np.random.seed(42)
rot_errors = np.random.normal(0, sigma_rot, (n_simulations, 3))
# columns: [rx, ry, rz] (Pitch, Roll, Yaw)




#  delta = theta x r
# delta_x = ry * d - rz * 0 = ry * d
# delta_y = rz * 0 - rx * d = -rx * d
# delta_z = rx * 0 - ry * 0 = 0



# displacement_mag = sqrt((ry*d)^2 + (-rx*d)^2) = d * sqrt(rx^2 + ry^2)


displacement_mag = d * np.sqrt(rot_errors[:, 0]**2 + rot_errors[:, 1]**2)


k_values = displacement_mag / (d * sigma_rot)


k_95 = np.percentile(k_values, 95)

print(f"Corrected Simulation Result (Rayleigh): k = {k_95:.3f}")

sorted_k = np.sort(k_values)
cdf = np.arange(1, n_simulations + 1) / n_simulations

plt.figure(figsize=(7, 6), dpi=300)
plt.plot(sorted_k, cdf, color='#1f77b4', linewidth=2)
plt.axhline(y=0.95, color='#d62728', linestyle='--')
plt.axvline(x=k_95, color='#d62728', linestyle='--')
plt.scatter([k_95], [0.95], color='#d62728', zorder=5)

plt.annotate(f'$P_{{95}}$ (k = {k_95:.2f})', xy=(k_95, 0.95), xytext=(k_95 + 0.5, 0.85),
             fontsize=16, fontweight='bold', color='#d62728',
             arrowprops=dict(facecolor='#d62728', shrink=0.05, width=1))

#plt.title('Supplementary Figure S1: CDF of Rotational Error Components', fontsize=12)
plt.rcParams['font.serif'] = ['Times New Roman']
plt.xlabel('Normalized Scaling Factor $k$ ($M_{rot} / (d \cdot \sin \sigma_{rot})$)', fontsize=16)
plt.ylabel('Cumulative Probability', fontsize=16)
plt.xlim(0, 4.0)
plt.grid(True, linestyle=':', alpha=0.4)
plt.show()