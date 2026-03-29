import matplotlib.pyplot as plt

# Data: Failure rate during unexpected delays (e.g., Traffic Jam > 2 hours)
methods = ['Ice Pack (No AI)', 'Bio-PCM (No AI)', 'Bio-PCM + AI Prediction']
failure_rates = [35, 12, 0.5]  # Percentage of batches lost

plt.figure(figsize=(10, 6))
plt.stem(methods, failure_rates, linefmt='grey', markerfmt='D', basefmt=" ")

plt.ylabel('Probability of Medical Waste (%)', fontsize=12)
plt.title('Reliability & Waste Reduction in Critical Logistics', fontsize=14, fontweight='bold')
plt.ylim(0, 40)

for i, v in enumerate(failure_rates):
    plt.text(i, v + 2, f'{v}%', ha='center', color='black', fontweight='bold')

plt.grid(axis='y', linestyle=':', alpha=0.5)
plt.tight_layout()
plt.show()