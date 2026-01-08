# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


distances = np.array([50, 80, 100, 120, 150, 200])
mean_coverage = np.array([99.96, 97.57, 95.03, 92.17, 87.60, 79.67])
pass_rates = np.array([100.0, 88.4, 52.1, 34.5, 12.8, 0.0])


plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']
sns.set_theme(style="white", font_scale=1.2)

fig, ax1 = plt.subplots(figsize=(10, 6), dpi=300)


color_bar = '#ffcc00'
color_bar_edge = '#e6a800'

# zorder=1 
bars = ax1.bar(distances, pass_rates, color=color_bar, edgecolor=color_bar_edge, 
               width=15, alpha=0.5, label='Dosimetric Pass Rate (Left Axis)', zorder=1)

ax1.set_xlabel('Distance from Isocenter (mm)', fontsize=12, fontweight='bold')
ax1.set_ylabel('Pass Rate (Probability of Success) [%]', color=color_bar_edge, fontsize=12, fontweight='bold')
ax1.tick_params(axis='y', labelcolor=color_bar_edge, colors=color_bar_edge)
ax1.set_ylim(0, 110) 
ax1.spines['left'].set_color(color_bar_edge)


for bar, rate in zip(bars, pass_rates):
    height = bar.get_height()
    if height > 1: 
        ax1.text(bar.get_x() + bar.get_width()/2., height + 1, f'{rate:.1f}%', 
                 ha='center', va='bottom', color='#b38600', fontsize=10, fontweight='bold')


ax2 = ax1.twinx()

color_line = '#1f77b4'

# zorder=10 
ax2.plot(distances, mean_coverage, color=color_line, marker='o', linewidth=3, 
         markersize=8, label='Mean Target Coverage (Right Axis)', zorder=10)

ax2.set_ylabel('Mean Target Coverage (V100%) [%]', color=color_line, fontsize=12, fontweight='bold')
ax2.tick_params(axis='y', labelcolor=color_line, colors=color_line)
ax2.set_ylim(70, 105) 
ax2.spines['right'].set_color(color_line)
ax2.spines['left'].set_visible(False) 


ax2.grid(True, axis='y', linestyle='--', alpha=0.3)


ax2.axhline(95, color='gray', linestyle='--', linewidth=1.5, alpha=0.8, zorder=5)
ax2.text(110, 95.8, 'Clinical Threshold (Mean > 95%)', color='gray', fontsize=10, fontstyle='italic', ha='left')


plt.title('The "Average Trap": Actual Pass Rate vs. Mean Coverage\n(Standard Scenario, $\sigma=0.5^\circ$)', 
          fontsize=14, pad=20, fontweight='bold')


bars_legend, labels_bars = ax1.get_legend_handles_labels()
lines, labels = ax2.get_legend_handles_labels()
ax1.legend(bars_legend + lines, labels_bars + labels, loc='upper right', frameon=True)

plt.tight_layout()
plt.show()