# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# --- 1. Global Settings  ---
# Use Times New Roman for all text
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
# White background with grid
sns.set_theme(style="whitegrid", font_scale=1.1)

# --- 2. Data Generation Model (with Continuous X-Axis) ---
def generate_scatter_data_continuous(sigma_scenario, distances):
    """
    Generates scatter data based on physical scaling laws.
    Uses a continuous range of distances to create a 'cloud' effect.
    """
    np.random.seed(42) # Fixed seed for reproducibility
    k = sigma_scenario / 0.5 # Scaling factor relative to standard scenario
    
    x_scatter = [] 
    y_scatter = [] 
    
    slope_base = 18.0 
    
    # Generate samples for each distance point (continuous range)
    for d in distances:
        # Calculate equivalent distance based on scaling law
        d_equiv = d * k
        scale_param = d_equiv * 0.0214 / 2.448 
        
        # Reduced number of samples per point for continuous plotting
        n_samples = 15 
        
        # Generate errors and convert to coverage
        errors = np.random.rayleigh(scale=scale_param, size=n_samples)
        loss = np.maximum(0, errors - 1.0) * slope_base
        coverage = 100.0 - loss
        
        # Add noise
        noise_scale = 0.5 + (d / 200.0) * 1.5
        noise = np.random.normal(0, noise_scale, n_samples)
        coverage += noise
        coverage = np.clip(coverage, 0, 100) 
        
        # For continuous plot, we don't need jitter, just use the distance
        x_scatter.extend([d] * n_samples)
        y_scatter.extend(coverage)
        
    return np.array(x_scatter), np.array(y_scatter)

def calculate_mean_coverage(sigma_scenario, distances):
    """Calculates mean coverage for a given sigma and distances."""
    k = sigma_scenario / 0.5
    x_mean = []
    y_mean = []
    slope_base = 18.0
    
    for d in distances:
        d_equiv = d * k
        scale_param = d_equiv * 0.0214 / 2.448 
        
        # Use a larger sample for a stable mean
        n_samples = 1000
        errors = np.random.rayleigh(scale=scale_param, size=n_samples)
        loss = np.maximum(0, errors - 1.0) * slope_base
        coverage = 100.0 - loss
        coverage = np.clip(coverage, 0, 100)
        
        x_mean.append(d)
        y_mean.append(np.mean(coverage))
    
    return np.array(x_mean), np.array(y_mean)


# --- 3. Prepare Data ---
# Create a continuous range of distances for scatter plot
distances_continuous = np.arange(10, 201, 1) 
# Use the same range for mean calculation
distances_mean = distances_continuous

# --- 4. Plotting ---
fig, axes = plt.subplots(1, 3, figsize=(18, 6), dpi=300, sharey=True, sharex=True)

scenarios = [
    (0.2, "High Precision ($\sigma=0.2^\circ$)", '#2ca02c'),
    (0.5, "Standard Precision ($\sigma=0.5^\circ$)", '#1f77b4'),
    (1.0, "Low Precision ($\sigma=1.0^\circ$)", '#d62728')
]

# Scatter point color (Light Purple)
scatter_color = '#d8b2d8' 

for ax, (sigma, title, color) in zip(axes, scenarios):
    # Generate scatter data with continuous distance
    x_sc, y_sc = generate_scatter_data_continuous(sigma, distances_continuous)
    # Calculate mean coverage
    x_mn, y_mn = calculate_mean_coverage(sigma, distances_mean)
    
    # A. Plot Scatter (Individual Outcomes)
    # alpha=0.4 for transparency, s=8 for size
    ax.scatter(x_sc, y_sc, color=scatter_color, s=18, alpha=0.4, 
               label='Sim. Outcomes', zorder=1)
    
    # B. Plot Mean Line
    ax.plot(x_mn, y_mn, color=color, linewidth=3, 
            label='Mean Coverage', zorder=10)
    
    # C. Threshold Line (95%)
    ax.axhline(95, color='#d62728', linestyle='--', linewidth=1.5, alpha=0.7, 
               zorder=5, label='Threshold (95%)')
    
    # Labels and Titles (English)
    ax.set_title(title, fontsize=16, fontweight='bold', pad=10, fontname='Times New Roman')
    ax.set_xlabel('Distance from Isocenter (mm)', fontsize=20, fontweight='bold', fontname='Times New Roman')
    ax.set_ylim(40, 102) 
    ax.set_xlim(0, 210)  
    
    # Legend for EACH subplot
    # framealpha=0.9 makes the legend background opaque so it covers scatter points
    ax.legend(loc='lower left', frameon=True, fontsize=16, framealpha=0.9)

# Y-label only on the first plot
axes[0].set_ylabel('Target Coverage ($V_{100\%}$) [%]', fontsize=20, fontweight='bold', fontname='Times New Roman')

plt.tight_layout()
plt.subplots_adjust(wspace=0.08) 
plt.show()
