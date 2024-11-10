import itertools

import ezdxf
import numpy as np
from shapely import LineString, Point

from comp import *
from config import K, M, N, minx, miny, maxx, maxy, polygon, q_0, vertices
from geom import BoundaryNode, Edge, SurfaceNode
from helpers import Block, b2a, calc
from known import D, nabla4


class Model:
    def __init__(self, args):
        # Build geometric model
        self.polygon = polygon
        self.edges = list(itertools.pairwise(self.polygon.boundary.coords))

        edges = [Edge(*e, segments=self.segments[i]) for i, e in enumerate(self.edges)]

        # Boundary nodes
        self.boundary_nodes = []
        bpoints = []
        for e in edges:
            self.boundary_nodes.append(BoundaryNode(e, ("W", "F")))
            bpoints += e.points

        # Surface nodes
        self.surface_nodes = []
        if args.filename:
            # Import model
            doc = ezdxf.readfile(f"{args.filename}")
            msp = doc.modelspace()

            # Read coordinates of points
            pts = {}
            for layer in doc.layers:
                pts[layer.dxf.name] = [
                    (p.dxf.location.x, p.dxf.location.y)
                    for p in msp.query(f'POINT[layer=="{layer.dxf.name}"]')
                ]
            self.points = pts[f"{args.layer}"]
        else:
            rpoints = self.gen_rpoints(self.polygon)
            spoints = vertices + bpoints + rpoints
            self.points = spoints

        self.surface_nodes.append(SurfaceNode(self.points, q_0))

    @staticmethod
    def gen_rpoints(polygon):
        """Generate random points inside a polygon."""
        num_of_surface_nodes = 16 * M * N + 4 * M + 4 * N + 1
        num_of_boundary_nodes = 16 * K
        num_of_vertices = len(vertices)

        num_of_random_points = (
            num_of_surface_nodes - num_of_boundary_nodes - num_of_vertices
        )

        rpoints = []

        i = 0
        while i < num_of_random_points:
            rx = np.random.uniform(minx, maxx)
            ry = np.random.uniform(miny, maxy)
            if (rx, ry) not in rpoints and polygon.contains_properly(Point(rx, ry)):
                rpoints.append((rx, ry))
                i += 1

        return rpoints

    @property
    def X(self):
        return np.array(self.points)[:, 0]

    @property
    def Y(self):
        return np.array(self.points)[:, 1]

    # @property
    # def segments(self):
    #     """Determine the number of segments in proportion to the length of the edges."""
    #     edge_lines = [LineString(edge) for edge in self.edges]
    #     weights = np.array(
    #         [edge_line.length / self.polygon.length for edge_line in edge_lines]
    #     )
    #     num_of_points = 16 * K
    #     N = np.floor(num_of_points * weights)
    #     rest = num_of_points - np.sum(N)
    #     argmin = np.argmin(N)
    #     N[argmin] = N[argmin] + rest
    #     segments = N + 1
    #     segments = segments.astype(int)
    #     return segments

    @property
    def segments(self):
        edges = [LineString((start_point, end_point)) for (start_point, end_point) in self.edges]

        x = np.linspace(minx, maxx, 4*K + 2)[1:-1]
        y = np.linspace(miny, maxy, 4*K + 2)[1:-1]

        vlines = [LineString((Point(i, miny), Point(i, maxy))) for i in x]
        hlines = [LineString((Point(minx, j), Point(maxx, j))) for j in y]

        segments = []
        eh = []
        ev = []

        for e in edges:
            num = 0
            for line in hlines:
                p = e.intersection(line)
                if p and p not in eh:
                    eh.append(p)
                    num += 1
            for line in vlines:
                p = e.intersection(line)
                if p and p not in ev:
                    ev.append(p)
                    num += 1
            segments.append(num + 1)

        return segments

    def load_approx(self, w_star):
        blocks = []
        for node in self.surface_nodes:
            block = Block(w_star, node.coords)
            m, _ = block.shape
            b = np.full((m, 1), node.load / D)
            block = np.hstack((block, b))
            blocks.append(block)
        return blocks

    def boundary_conditions(self, fdict):
        blocks = []
        for node in self.boundary_nodes:
            for name in node.boundary_conditions:
                fs = fdict[name]
                try:
                    block = Block(fs(node.alpha), node.coords)
                except Exception:
                    block = Block(fs, node.coords)
                blocks.append(block)
        return blocks

    def solve(self):
        """Solution to the boundary problem."""

        # Particular solution
        w_star = [nabla4(f) for f in W_p]
        blocks = self.load_approx(w_star)
        A, b = b2a(blocks)
        S = np.linalg.solve(A, b)
        # assert S[0] == q_0 / (64*D)

        W_s = [calc(W_p, S)]
        U_s = [calc(U_p, S)]
        V_s = [calc(V_p, S)]
        X_s = [calc(X_p, S)]
        Y_s = [calc(Y_p, S)]
        Z_s = [calc(Z_p, S)]
        G_s = [calc(G_p, S)]
        H_s = [calc(H_p, S)]
        K_s = [calc(K_p, S)]
        L_s = [calc(L_p, S)]
        F_s = lambda alpha: [calc(F_p(alpha), S)]
        P_s = lambda alpha: [calc(P_p(alpha), S)]

        # The sum of the general and particular solution
        W = W_g + W_s
        U = U_g + U_s
        V = V_g + V_s
        X = X_g + X_s
        Y = Y_g + Y_s
        Z = Z_g + Z_s
        G = G_g + G_s
        H = H_g + H_s
        K = K_g + K_s
        L = L_g + L_s
        F = lambda alpha: F_g(alpha) + F_s(alpha)
        P = lambda alpha: P_g(alpha) + P_s(alpha)

        fdict = {
            "W": W,  # w
            "U": U,  # phi_x
            "V": V,  # phi_y
            "P": P,  # phi_n
            "X": X,  # M_x
            "Y": Y,  # M_y
            "Z": Z,  # M_xy
            "F": F,  # M_n
            "G": G,  # Q_x
            "H": H,  # Q_y
            "K": K,  # V_x
            "L": L,  # V_y
        }

        blocks = self.boundary_conditions(fdict)
        A, b = b2a(blocks)
        R = np.linalg.solve(A, -b)
        R = np.append(R, 1)

        return fdict, R
