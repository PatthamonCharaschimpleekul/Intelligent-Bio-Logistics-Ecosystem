import matplotlib.pyplot as plt
import numpy as np

# --- Simulation Settings ---
duration_hours = 24
time = np.linspace(0, duration_hours, 500)  # Time axis (0 to 24 hours)

# --- Define Temperature Profiles (Simulated Data) ---

# 1. External Ambient Temperature (Hot Day)
# Starts at 25°C, peaks at 35°C, drops to 28°C
ambient_temp = 25 + 10 * np.sin(np.pi * time / duration_hours)

# 2. Traditional Ice/Gel Pack Profile
# Starts at 0°C, quickly rises, fluctuations due to ambient temp, melts around 8-10h
ice_temp = np.zeros_like(time)
ice_melt_point = 8 # hours
for i, t in enumerate(time):
    if t < ice_melt_point:
        # Slow rise while ice exists
        ice_temp[i] = 0 + 0.5 * t + 0.2 * np.sin(2 * np.pi * t) 
    else:
        # Rapid rise after melting, trying to reach ambient
        ice_temp[i] = ice_temp[i-1] + 0.8 * (ambient_temp[i] - ice_temp[i-1]) * 0.1

# 3. Intelligent Bio-PCM Profile (Our Invention)
# Holds strictly at 4°C (phase change), very slight rise after PCM fully melts (~20h)
pcm_temp = np.full_like(time, 4.0) # Target 4°C Isothermal
pcm_melt_point = 20 # hours (superior insulation + AI pathfinding)
for i, t in enumerate(time):
    if t < pcm_melt_point:
        # Extreme stability due to Latent Heat + VIP insulation
        pcm_temp[i] = 4.0 + 0.05 * np.sin(np.pi * t) # High precision (+/- 0.05°C)
    else:
        # Gentle rise after PCM is exhausted
        pcm_temp[i] = 4.0 + 1.5 * (t - pcm_melt_point)

# --- Plotting ---
plt.figure(figsize=(12, 7), dpi=100)
plt.style.use('seaborn-v0_8-whitegrid')

# Plot Lines
plt.plot(time, ambient_temp, label='External Ambient Temp (Hot Day)', color='#ff9800', linestyle='--', alpha=0.7)
plt.plot(time, ice_temp, label='Traditional Ice/Gel Pack (Passive)', color='#2196f3', linewidth=2)
plt.plot(time, pcm_temp, label='Intelligent Bio-PCM Ecosystem (Invention)', color='#4caf50', linewidth=3)

# Shaded Area for Critical Medical Zone (e.g., 2°C to 8°C for Organs/Vaccines)
plt.axhspan(2, 8, color='#e8f5e9', alpha=0.5, label='Critical Medical Range (2°C - 8°C)')

# Markers & Annotations
plt.axvline(x=ice_melt_point, color='#1565c0', linestyle=':', alpha=0.8)
plt.text(ice_melt_point + 0.2, 15, 'Ice Completely Melted', color='#1565c0', fontsize=10)

plt.axvline(x=pcm_melt_point, color='#2e7d32', linestyle=':', alpha=0.8)
plt.text(pcm_melt_point - 4.5, 6, 'PCM Latent Heat Exhausted', color='#2e7d32', fontsize=10)

# Critical Failure Point Annotation for Ice
failure_time_ice = time[np.where(ice_temp > 8)[0][0]]
plt.scatter(failure_time_ice, 8, color='red', s=100, zorder=5)
plt.text(failure_time_ice + 0.5, 9, 'Critical Failure (Ice)', color='red', fontweight='bold')

# Labels & Title
plt.title('Temperature Stability Comparison: Traditional vs. Intelligent Bio-Logistics', fontsize=16, fontweight='bold')
plt.xlabel('Time Elapsed (Hours)', fontsize=12)
plt.ylabel('Internal Temperature (°C)', fontsize=12)
plt.xlim(0, duration_hours)
plt.ylim(-2, 40) # Set Y-axis to show ambient peaks

# Legend & Grid
plt.legend(loc='upper left', frameon=True, shadow=True)
plt.grid(True, which='both', linestyle='--', linewidth=0.5)

# Save the plot (optional, for embedding in papers)
# plt.savefig('thermal_comparison_graph.png', bbox_inches='tight')

plt.tight_layout()
plt.show()