from typing import Callable

import numpy as np
import numpy.typing as npt


def Block(fs: list[Callable], pts: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
    """Returns a block matrix of `fs` values computed at `pts` points."""
    x = pts[:, 0]
    y = pts[:, 1]
    B = np.array([f(x, y) for f in fs])
    return B.T


def b2a(
    blocks: list[npt.NDArray[np.float64]],
) -> tuple[npt.NDArray[np.float64], npt.NDArray[np.float64]]:
    """Converts a list of blocks to a coefficient matrix `A` and column vector `b`."""
    # Augmented matrix
    M = np.vstack(blocks)
    # Coefficient matrix
    A = M[:, :-1]
    # Column vector of constant terms
    b = M[:, -1]
    return A, b


def calc(fs: list[Callable], R: npt.NDArray[np.float64]) -> Callable:
    """Create a function of variables (x, y) to calculate the desired quantity
    from list of functions `fs` and solution `R`."""

    def fn(x, y):
        A = np.array([f(x, y) for f in fs])
        return np.einsum("ij,i->j", A, R)

    return fn


def angle_trunc(alpha: np.float64) -> np.float64:
    if alpha < 0.0:
        alpha += np.pi * 2
    return alpha


def pos(
    start_point: tuple[np.float64, np.float64], end_point: tuple[np.float64, np.float64]
) -> tuple[np.float64, np.float64]:
    """Return coordinates of position vector."""
    x = end_point[0] - start_point[0]
    y = end_point[1] - start_point[1]
    return x, y


def swap(x: np.float64, y: np.float64) -> tuple[np.float64, np.float64]:
    """Return the swapped coordinates."""
    return y, x


def perp(x: np.float64, y: np.float64) -> tuple[np.float64, np.float64]:
    """Return coordinates of perpendicular vector.

    See: https://mathworld.wolfram.com/PerpendicularVector.html
    """
    return -y, x
