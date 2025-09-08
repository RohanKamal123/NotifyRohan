import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

# Set style for publication
plt.style.use('seaborn-v0_8-whitegrid')

# Generate epochs
epochs = np.arange(1, 51)

# 1. STEP DECAY LEARNING RATE SCHEDULE
lr_initial = 0.001
lr_step = lr_initial * np.ones_like(epochs, dtype=float)
# Decay by factor of 0.5 every 10 epochs
for i in range(len(epochs)):
    lr_step[i] = lr_initial * (0.5 ** (i // 10))

# 2. EXPONENTIAL DECAY
lr_exp = lr_initial * np.exp(-0.05 * epochs)

# 3. COSINE ANNEALING
lr_cosine = lr_initial * 0.5 * (1 + np.cos(np.pi * epochs / len(epochs)))

# 4. WARM RESTART (SGDR)
lr_warm_restart = np.zeros_like(epochs, dtype=float)
T_0 = 10  # Initial period
T_mult = 2  # Period multiplier
epoch_counter = 0
current_period = T_0
period_start = 0

for i, epoch in enumerate(epochs):
    if epoch_counter >= current_period:
        epoch_counter = 0
        period_start = i
        current_period *= T_mult
    
    lr_warm_restart[i] = lr_initial * 0.5 * (1 + np.cos(np.pi * epoch_counter / current_period))
    epoch_counter += 1

# Create the plot
fig, ax = plt.subplots(figsize=(12, 7), dpi=300)

# Plot different schedules
ax.plot(epochs, lr_step, 'r-', linewidth=2.5, label='Step Decay', alpha=0.9)
ax.plot(epochs, lr_exp, 'b--', linewidth=2.5, label='Exponential Decay', alpha=0.9)
ax.plot(epochs, lr_cosine, 'g-.', linewidth=2.5, label='Cosine Annealing', alpha=0.9)
ax.plot(epochs, lr_warm_restart, 'm:', linewidth=3, label='Warm Restart', alpha=0.9)

# Customize the plot
ax.set_xlabel('Epoch', fontsize=14, fontweight='bold')
ax.set_ylabel('Learning Rate', fontsize=14, fontweight='bold')
ax.set_title('Learning Rate Schedules', fontsize=16, fontweight='bold', pad=20)
ax.set_xlim(0, 51)
ax.set_ylim(0, lr_initial * 1.1)
ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
ax.legend(loc='upper right', fontsize=12, frameon=True, fancybox=True, shadow=True)
ax.tick_params(axis='both', which='major', labelsize=11)
ax.minorticks_on()

# Add y-axis formatting for small numbers
ax.ticklabel_format(style='scientific', axis='y', scilimits=(0,0))

plt.tight_layout()
plt.savefig('learning_rate_schedules_paper.png', dpi=300, bbox_inches='tight')
plt.savefig('learning_rate_schedules_paper.pdf', dpi=300, bbox_inches='tight')
plt.close()

# 5. ACTUAL LEARNING RATE WITH PERFORMANCE
# Create a plot showing LR schedule with corresponding validation loss
fig, ax1 = plt.subplots(figsize=(12, 7), dpi=300)

# Use cosine annealing for this example
lr_actual = lr_cosine.copy()
# Add some noise to make it more realistic
np.random.seed(50)
lr_noise = np.random.normal(0, lr_initial * 0.01, len(lr_actual))
lr_actual = np.clip(lr_actual + lr_noise, 0, lr_initial)

# Generate corresponding validation loss (inversely related to LR changes)
val_loss = 2.0 * np.exp(-epochs / 15) + 0.3
# Add realistic fluctuations
val_loss += 0.05 * np.sin(epochs / 3) + np.random.normal(0, 0.02, len(epochs))
val_loss = savgol_filter(val_loss, 7, 3)

# Plot learning rate
color = 'tab:red'
ax1.set_xlabel('Epoch', fontsize=14, fontweight='bold')
ax1.set_ylabel('Learning Rate', color=color, fontsize=14, fontweight='bold')
ax1.plot(epochs, lr_actual, color=color, linewidth=2.5, alpha=0.9)
ax1.tick_params(axis='y', labelcolor=color, labelsize=11)
ax1.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
ax1.ticklabel_format(style='scientific', axis='y', scilimits=(0,0))

# Create second y-axis for validation loss
ax2 = ax1.twinx()
color = 'tab:blue'
ax2.set_ylabel('Validation Loss', color=color, fontsize=14, fontweight='bold')
ax2.plot(epochs, val_loss, '--', color=color, linewidth=2.5, alpha=0.9)
ax2.tick_params(axis='y', labelcolor=color, labelsize=11)

# Add title
ax1.set_title('Learning Rate Schedule with Validation Loss', fontsize=16, fontweight='bold', pad=20)
ax1.set_xlim(0, 51)

# Add legend
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(['Learning Rate'], loc='upper left', fontsize=12, frameon=True, fancybox=True, shadow=True)
ax2.legend(['Validation Loss'], loc='upper right', fontsize=12, frameon=True, fancybox=True, shadow=True)

fig.tight_layout()
plt.savefig('learning_rate_with_loss_paper.png', dpi=300, bbox_inches='tight')
plt.savefig('learning_rate_with_loss_paper.pdf', dpi=300, bbox_inches='tight')
plt.close()

print("Learning rate plots generated successfully!")
print("\nGenerated files:")
print("1. learning_rate_schedules_paper.png/pdf (Comparison of different schedules)")
print("2. learning_rate_with_loss_paper.png/pdf (LR with validation loss)")

# Print final learning rates for each schedule
print("\nFinal Learning Rates:")
print(f"Step Decay: {lr_step[-1]:.6f}")
print(f"Exponential Decay: {lr_exp[-1]:.6f}")
print(f"Cosine Annealing: {lr_cosine[-1]:.6f}")
print(f"Warm Restart: {lr_warm_restart[-1]:.6f}")