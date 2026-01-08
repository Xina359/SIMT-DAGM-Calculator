# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import MultipleLocator

# --- Style Settings ---
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']
plt.rcParams['mathtext.fontset'] = 'stix'
sns.set_theme(style="white", font_scale=1.2, rc={"font.family": "serif"}) # Changed to white style for custom grid control

def generate_data_with_distance(sigma_val, n_samples=1000000):
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
    rot_vecs = np.random.normal(0, np.deg2rad(sigma_val), (n_samples, 3))
    tre = np.linalg.norm(np.cross(rot_vecs, points), axis=1)
    return r, tre

# --- Generate Data ---
print("Generating data...")
r1, tre1 = generate_data_with_distance(0.2)
r2, tre2 = generate_data_with_distance(0.5)
r3, tre3 = generate_data_with_distance(1.0)
print("Done.")

# --- Calculate Zonal Failure Rates ---
def calc_zonal_failure(r_data, tre_data, zones, threshold=1.0):
    rates = []
    zone_labels = []
    for i in range(len(zones)-1):
        start, end = zones[i], zones[i+1]
        mask = (r_data >= start) & (r_data < end)
        if np.sum(mask) > 0:
            fails = np.sum(tre_data[mask] > threshold)
            total = np.sum(mask)
            rates.append(fails / total * 100)
        else:
            rates.append(0)
        zone_labels.append(f'{start}-{end} mm')
    return zone_labels, rates

zones = [0, 50, 100, 150, 200]
labels, y1 = calc_zonal_failure(r1, tre1, zones)
_, y2 = calc_zonal_failure(r2, tre2, zones)
_, y3 = calc_zonal_failure(r3, tre3, zones)

# --- Plotting  ---
fig, ax = plt.subplots(figsize=(9, 6), dpi=300)

x_pos = np.arange(len(labels))
width = 0.25  # width of the bars

# Plotting Bars (Grouped Bar Chart is best for Zonal Comparison)
# Scenario 1 (Green)
rects1 = ax.bar(x_pos - width, y1, width, label=r'High Precision ($\sigma=0.2^\circ$)', color='#2ca02c', alpha=0.9, edgecolor='white')
# Scenario 2 (Blue)
rects2 = ax.bar(x_pos, y2, width, label=r'Standard ($\sigma=0.5^\circ$)', color='#1f77b4', alpha=0.9, edgecolor='white')
# Scenario 3 (Red)
rects3 = ax.bar(x_pos + width, y3, width, label=r'Low Precision ($\sigma=1.0^\circ$)', color='#d62728', alpha=0.9, edgecolor='white')

# --- Add Values on Top of Bars (Optional but helpful) ---
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        if height > 0: # Only label non-zero bars
            ax.annotate(f'{height:.1f}%',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=13, rotation=0)

autolabel(rects1)
autolabel(rects2)
autolabel(rects3)

# --- Custom Grid (Requirement #2) ---
# Major ticks (Thick dashed)
ax.yaxis.set_major_locator(MultipleLocator(20)) # Every 20%
ax.grid(which='major', axis='y', linestyle='--', linewidth=1.2, alpha=0.7, color='gray')

# Minor ticks (Thin dashed)
ax.yaxis.set_minor_locator(MultipleLocator(5)) # Every 5%
ax.grid(which='minor', axis='y', linestyle=':', linewidth=0.8, alpha=0.5, color='gray')

# --- Decoration ---
ax.set_ylabel('Geometric Failure Rate (> 1.0 mm) [%]', fontsize=14)
ax.set_xlabel('Distance from Isocenter (mm)', fontsize=15)
ax.set_title('Geometric Failure Rate by Zone Across Precision Scenarios', fontsize=16, fontweight='bold', pad=20)
ax.set_xticks(x_pos)
ax.set_xticklabels(labels, fontsize=12)
ax.set_ylim(0, 105)

ax.legend(loc='upper left', frameon=True, fontsize=11, framealpha=0.95)

# Remove top and right spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('Figure5_Zonal_Failure_Bar.png', dpi=300)
plt.show()