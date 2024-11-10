import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm


def plot_2D(name, X, Y, Z):
    fig, ax = plt.subplots()
    ax.set_xlabel("x", rotation=0)
    ax.set_ylabel("y", rotation=0)
    surf = ax.tricontourf(X, Y, Z, cmap=cm.coolwarm, antialiased=True)
    fig.colorbar(surf)
    plt.axis("scaled")
    plt.tight_layout()
    plt.savefig(f"plots/mcr_2D_{name}.pdf", bbox_inches="tight")


def plot_3D(name, X, Y, Z):
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    surf = ax.plot_trisurf(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=True)
    ax.set_zticks([])
    ax.set_zlim(ax.get_zlim()[::-1])
    ax.set_box_aspect((1.0, 1.0, 0.5))
    boundaries = np.linspace(min(Z), max(Z), 10, endpoint=True)
    fig.colorbar(surf, shrink=0.5, boundaries=boundaries, pad=0.1)
    plt.tight_layout()
    plt.savefig(f"plots/mcr_3D_{name}.pdf", bbox_inches="tight")
