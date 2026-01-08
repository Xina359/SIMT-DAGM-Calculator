# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import MultipleLocator

# --- Style Settings ---
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']
plt.rcParams['mathtext.fontset'] = 'stix'
sns.set_theme(style="white", font_scale=1.2, rc={"font.family": "serif"})

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

# --- Calculate Raw Continuous Curves ---
def calc_raw_curve(r_data, tre_data, bins=40, threshold=1.0):
    bin_edges = np.linspace(0, 200, bins+1)
    centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    rates = []
    
    for i in range(bins):
        mask = (r_data >= bin_edges[i]) & (r_data < bin_edges[i+1])
        if np.sum(mask) > 10: 
            fails = np.sum(tre_data[mask] > threshold)
            rates.append(fails / np.sum(mask) * 100)
        else:
            rates.append(0)
            
    return centers, rates

x1, y1 = calc_raw_curve(r1, tre1)
x2, y2 = calc_raw_curve(r2, tre2)
x3, y3 = calc_raw_curve(r3, tre3)

# --- Plotting Figure 5 (Final Clean Style) ---
fig, ax = plt.subplots(figsize=(8, 6), dpi=300)

# Plot Raw Curves with Markers (NO FILL)
# Green (High Precision)
ax.plot(x1, y1, color='#2ca02c', linewidth=2, marker='o', markersize=4, 
        label=r'High Precision ($\sigma=0.2^\circ$)')

# Blue (Standard)
ax.plot(x2, y2, color='#1f77b4', linewidth=2, marker='s', markersize=4, 
        label=r'Standard ($\sigma=0.5^\circ$)')

# Red (Low Precision)
ax.plot(x3, y3, color='#d62728', linewidth=2, marker='^', markersize=4, 
        label=r'Low Precision ($\sigma=1.0^\circ$)')

# --- Custom Grid (Unified Thickness) ---

# 1. Y-Axis Major (0, 20, 40...) -> Thick Dashed
ax.yaxis.set_major_locator(MultipleLocator(20)) 
ax.grid(which='major', axis='y', linestyle='--', linewidth=0.9, alpha=0.5, color='gray')

# 2. X-Axis Major (0, 25, 50...) -> SAME THICKNESS as Y-Axis
ax.xaxis.set_major_locator(MultipleLocator(25)) 
ax.grid(which='major', axis='x', linestyle='--', linewidth=0.9, alpha=0.5, color='gray')

# 3. Y-Axis Minor (5, 10, 15...) -> Thin Dotted (Keep for precision)
ax.yaxis.set_minor_locator(MultipleLocator(5)) 
ax.grid(which='minor', axis='y', linestyle=':', linewidth=0.8, alpha=0.4, color='gray')

# --- Decoration ---
ax.set_ylabel('Geometric Failure Rate (> 1.0 mm) [%]', fontsize=14)
ax.set_xlabel('Distance from Isocenter (mm)', fontsize=14)
ax.set_title('Geometric Failure Rate vs. Distance', fontsize=16, fontweight='bold', pad=15)
ax.set_xlim(0, 200)
ax.set_ylim(-2, 105)

ax.legend(loc='upper left', frameon=True, fontsize=11, framealpha=0.95)

# Remove top and right spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('Figure5_Final_Clean.png', dpi=300)
plt.show()