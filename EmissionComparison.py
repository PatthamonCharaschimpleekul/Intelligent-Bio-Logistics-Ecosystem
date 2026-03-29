import matplotlib.pyplot as plt
import numpy as np

#(Data) Estimated CO2 emission (kg per 100 km transport)
label = ["Active cooling (Electric)", "Passive Bio-PCM + AI"]
co2_emissions = [45.5, 2.1]  # Simulated data based on energy consumption

fix, ax = plt.subplots(figsize=(8,6))
colors = ['#ff5252', '#4caf50']

bars = ax.bar(label, co2_emissions, color=colors, width=0.6)

#add label and title
ax.set_ylabel('CO2 emission (kg per 100 km transport', fontsize=12)
ax.set_title('Sustainability Impact: Carbon Footprint Reduction', fontsize=14, fontweight='bold')
ax.set_ylim(0,60)

# Add values on top of bars
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 1, f'{yval} kg', ha='center', va='bottom', fontweight='bold')

plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()