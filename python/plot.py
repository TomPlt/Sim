import numpy as np
import matplotlib.pyplot as plt

# Load the win percentages from the .npy file
win_percentages = np.load("win_percentages.npy")

# Plotting
plt.figure(figsize=(10, 5))
plt.plot(win_percentages, '-o', label='AI Win Percentage', linewidth=2)
plt.xlabel('Epochs [1e3]', fontsize=14)
plt.ylabel('Win Percentage', fontsize=14)
plt.title('AI Win Percentage Over Time', fontsize=16)
plt.legend(loc='best', fontsize=12)
plt.grid(True, which="both", ls="--", c='0.65')
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
plt.savefig("win_percentages.png")
plt.show()
