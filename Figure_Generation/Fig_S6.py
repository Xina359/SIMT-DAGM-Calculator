# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy.interpolate import interp1d


plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
sns.set_theme(style="white", font_scale=1.1)


base_dist = np.array([0, 50, 80, 100, 120, 150, 200, 300]) 
base_pass = np.array([100.0, 100.0, 88.4, 52.1, 34.5, 12.8, 0.0, 0.0])


get_pass_rate = interp1d(base_dist, base_pass, kind='linear', fill_value="extrapolate")


dist_line = np.array([0, 25, 50, 75, 100, 125, 150, 175, 200])


std_pass = get_pass_rate(dist_line)


high_pass = get_pass_rate(dist_line * (0.2 / 0.5))


low_pass = get_pass_rate(dist_line * (1.0 / 0.5))


c_high = '#2ca02c' 
c_std  = '#1f77b4' 
c_low  = '#d62728' 


fig, ax = plt.subplots(figsize=(10, 6), dpi=300)

ax.plot(dist_line, high_pass, color=c_high, marker='o', markersize=6, linewidth=2.5, label='High Precision ($\sigma=0.2^\circ$)')
ax.plot(dist_line, std_pass,  color=c_std,  marker='s', markersize=6, linewidth=2.5, label='Standard ($\sigma=0.5^\circ$)')
ax.plot(dist_line, low_pass,  color=c_low,  marker='^', markersize=6, linewidth=2.5, label='Low Precision ($\sigma=1.0^\circ$)')


ax.axhline(50, color='black', linestyle='--', alpha=0.4, linewidth=1.5)
ax.text(5, 52, '50% Success Probability', fontsize=10, color='#333')


ax.axvline(50, color=c_low, linestyle=':', alpha=0.6, linewidth=1.5)
ax.text(52, 53, 'Failure Zone\n(Low Precision)', color=c_low, fontsize=9, fontweight='bold')


ax.axvline(100, color=c_std, linestyle=':', alpha=0.6, linewidth=1.5)
ax.text(102, 53, 'Critical Radius\n(Standard)', color=c_std, fontsize=9, fontweight='bold')


ax.set_xlabel('Distance from Isocenter (mm)', fontsize=12, fontweight='bold')
ax.set_ylabel('Probability of Passing (V100% ≥ 95%) [%]', fontsize=12, fontweight='bold')
ax.set_title('Dosimetric Survival Curves Across Precision Scenarios', fontsize=14, pad=15, fontweight='bold')
ax.set_ylim(-2, 105)
ax.set_xlim(0, 205)
ax.grid(True, linestyle='--', alpha=0.3)
ax.legend(loc='lower left', frameon=True, fontsize=11)

plt.tight_layout()
plt.show()
