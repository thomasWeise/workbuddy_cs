import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

# Keep 1 + x strictly positive so both curves are valid on a log-scaled y-axis.
x = np.linspace(-0.9, 3.0, 600)
y_linear = 1.0 + x
y_exp = np.exp(x)

fig, ax = plt.subplots(figsize=(7, 5))
ax.plot(x, y_linear, label=r"$1 + x$", color="#1f77b4", linewidth=2)
ax.plot(x, y_exp, label=r"$\exp(x)$", color="#d62728", linewidth=2)
ax.set_yscale("log")
ax.set_xlabel("x")
ax.set_ylabel("y (log scale)")
ax.set_title("Comparison of 1 + x and exp(x)")
ax.grid(True, which="both", linestyle="--", alpha=0.4)
ax.legend()
fig.tight_layout()
fig.savefig("/home/user/workbuddy-data/plot.pdf", format="pdf")
plt.close(fig)
