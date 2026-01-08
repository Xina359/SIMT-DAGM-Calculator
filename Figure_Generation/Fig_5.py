import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
sns.set_theme(style="ticks", font_scale=1.1)


def calculate_theoretical_margin(sigma_deg, distances):
    angle_rad = np.deg2rad(2.45 * sigma_deg)
    return distances * np.sin(angle_rad)


distances = np.linspace(0, 200, 200)
margin_high = calculate_theoretical_margin(0.2, distances)
margin_std  = calculate_theoretical_margin(0.5, distances)
margin_low  = calculate_theoretical_margin(1.0, distances)


fig, ax = plt.subplots(figsize=(10, 6), dpi=300)


ax.axhspan(0, 1.5, color='#e6f4ea', alpha=0.6, lw=0, zorder=0)
ax.text(195, 0.7, 'SAFE ZONE\n(Target Margin)', color='#137333', 
        ha='right', va='center', fontweight='bold', fontsize=11.5, alpha=0.8)


ax.axhspan(1.5, 2.5, color='#fff9c4', alpha=0.6, lw=0, zorder=0)
ax.text(195, 2.0, 'CAUTION\n(Volume Risk)', color='#f57f17', 
        ha='right', va='center', fontweight='bold', fontsize=11.5, alpha=0.8)


ax.axhspan(2.5, 6.0, color='#ffebee', alpha=0.6, lw=0, zorder=0)
ax.text(195, 3.5, 'HIGH RISK\n(Impractical)', color='#c62828', 
        ha='right', va='center', fontweight='bold', fontsize=11.5, alpha=0.8)


ax.axhline(1.5, color='#f9a825', linestyle=':', linewidth=1.0, alpha=0.6, zorder=1)
ax.axhline(2.5, color='#c62828', linestyle=':', linewidth=1.0, alpha=0.6, zorder=1)


ax.grid(True, which='major', linestyle='--', linewidth=0.75, color='#bdbdbd', alpha=0.5, zorder=2)
ax.minorticks_on()
ax.grid(True, which='minor', linestyle=':', linewidth=0.5, color='#e0e0e0', alpha=0.5, zorder=1)


ax.plot(distances, margin_high, color='#2e7d32', linewidth=3, zorder=10, label='High Precision ($\sigma=0.2^\circ$)')

ax.plot(distances, margin_std, color='#1565c0', linewidth=2.5, zorder=9, label='Standard Precision ($\sigma=0.5^\circ$)')

# Low Precision (Red)
ax.plot(distances, margin_low, color='#d32f2f', linewidth=2.5, zorder=8, label='Low Precision ($\sigma=1.0^\circ$)')


# Standard @ 100mm -> 2.14 mm
val_std_100 = calculate_theoretical_margin(0.5, 100) 
ax.plot(100, val_std_100, 'o', color='#1565c0', markersize=6, zorder=11, markeredgecolor='white')
ax.annotate(f'{val_std_100:.2f} mm', xy=(100, val_std_100), xytext=(85, 2.9),
            arrowprops=dict(arrowstyle="->", color='#1565c0', lw=1.5),
            fontsize=12, color='#1565c0', fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#1565c0", alpha=0.95))

# High Prec @ 150mm -> 1.28 mm
val_high_150 = calculate_theoretical_margin(0.2, 150)
ax.plot(150, val_high_150, 'o', color='#2e7d32', markersize=6, zorder=11, markeredgecolor='white')
ax.annotate(f'{val_high_150:.2f} mm', xy=(150, val_high_150), xytext=(150, 0.6),
            arrowprops=dict(arrowstyle="->", color='#2e7d32', lw=1.5),
            fontsize=12, color='#2e7d32', fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#2e7d32", alpha=0.95))


ax.set_xlabel('Distance from Isocenter (mm)', fontsize=16, fontweight='bold', fontname='Times New Roman')
ax.set_ylabel('Required PTV Margin (mm)', fontsize=16, fontweight='bold', fontname='Times New Roman')
ax.set_title('Optimization of Adaptive PTV Margins (Theoretical Model)', fontsize=14, pad=15, fontweight='bold', fontname='Times New Roman')
ax.set_ylim(0, 5.0)
ax.set_xlim(0, 200)
ax.legend(loc='upper left', frameon=True, fontsize=13, framealpha=0.95, edgecolor='#cccccc')


for spine in ax.spines.values(): 
    spine.set_edgecolor('#555555')
    spine.set_linewidth(1.0)

plt.tight_layout()
plt.show()