import argparse

import numpy as np

from model import Model
from helpers import calc
from plot import plot_2D, plot_3D

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", help="dxf file")
    parser.add_argument("--layer", default=0, help="dxf layer")
    parser.add_argument("--alpha", default=0, type=float, help="angle in degrees")
    parser.add_argument(
        "--plot",
        choices=["2D", "3D"],
        default="3D",
        help="Type of plot",
    )
    args = parser.parse_args()

    # Prepare model
    model = Model(args)

    # Find solution
    fdict, R = model.solve()

    # Get the coordinates of the points
    X = model.X
    Y = model.Y

    # Get results
    for name, f in fdict.items():
        match name:
            case "F" | "P":
                f = f(np.deg2rad(args.alpha))

        Z = calc(f, R)(X, Y)

        print(f"min({name}):", min(Z))
        print(f"max({name}):", max(Z))

        match args.plot:
            case "2D":
                plot_2D(name, X, Y, Z)
            case "3D":
                plot_3D(name, X, Y, Z)
