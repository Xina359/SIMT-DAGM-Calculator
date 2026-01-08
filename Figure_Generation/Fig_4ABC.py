# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.offsetbox import AnchoredText

# --- 1. Style Settings for Publication ---

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']
plt.rcParams['mathtext.fontset'] = 'stix' 
sns.set_theme(style="ticks", font_scale=1.2, rc={"font.family": "serif"})

def generate_scenario_data(sigma_val, n_samples=1000000):
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
    tre_values = np.linalg.norm(np.cross(rot_vecs, points), axis=1)
    return tre_values

# --- 2. Generate Data ---
print("Generating data...")
tre_s1 = generate_scenario_data(0.2)
tre_s2 = generate_scenario_data(0.5)
tre_s3 = generate_scenario_data(1.0)
print("Done.")

# --- 3. Plotting ---
fig, axes = plt.subplots(3, 1, figsize=(8, 12), sharex=False) 

scenarios = [
    {
        'data': tre_s1, 
        'title': r'Scenario 1 (High Precision, $\sigma=0.2^\circ$)',
        'color': '#2ca02c', 
        'xlim': 2.0 
    },
    {
        'data': tre_s2, 
        'title': r'Scenario 2 (Standard, $\sigma=0.5^\circ$)',
        'color': '#1f77b4', 
        'xlim': 4.0 
    },
    {
        'data': tre_s3, 
        'title': r'Scenario 3 (Poor/Fail, $\sigma=1.0^\circ$)',
        'color': '#d62728', 
        'xlim': 8.0 
    }
]

for ax, sc in zip(axes, scenarios):
    data = sc['data']
    color = sc['color']
    xlim = sc['xlim']
    
    # 1. Histogram & KDE

    sns.histplot(data, bins=180, stat='density', kde=True,
                 color=color, alpha=0.5, edgecolor='white', linewidth=0.45,
                 line_kws={'linewidth': 1.5}, ax=ax, label='Frequency')
    
    # 2. Stats
    mean_val = np.mean(data)
    std_val = np.std(data)
    p95_val = np.percentile(data, 95)
    
    # 3. Reference Lines
    # P95 (Dashed)
    ax.axvline(p95_val, color=color, linestyle='--', linewidth=2.5, label=r'$P_{95}$')
    # Tolerance (Solid Black)
    ax.axvline(1.0, color='black', linestyle='-', linewidth=2.0, alpha=0.7, label='Tolerance (1.0 mm)')
    
    # 4. Info Box (Moved to Center Right)
    stats_text = (f'Mean: {mean_val:.2f} mm\n'
                  f'SD: {std_val:.2f} mm\n'
                  f'$P_{{95}}$: {p95_val:.2f} mm')
    
    at = AnchoredText(stats_text, prop=dict(size=12, fontfamily='serif'), 
                      frameon=True, loc='center right', pad=0.5)
    at.patch.set_boxstyle("round,pad=0.5,rounding_size=0.2")
    at.patch.set_alpha(0.8) 
    ax.add_artist(at)

    # 5. Legend (Fixed at Upper Right)
    ax.legend(loc='upper right', frameon=True, fontsize=10)

    # 6. Decorations
    ax.set_title(sc['title'], fontsize=14, fontweight='bold', loc='left', fontfamily='serif')
    ax.set_ylabel('Density', fontsize=13, fontfamily='serif')
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.set_xlim(0, xlim)
    
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

# X-axis Label
axes[-1].set_xlabel('Target Registration Error (mm)', fontsize=14, fontfamily='serif')

plt.tight_layout()
plt.subplots_adjust(hspace=0.4) 
plt.savefig('Figure4_Final.png', dpi=300, bbox_inches='tight')
plt.show()