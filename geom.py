import numpy as np
import numpy.typing as npt

from helpers import angle_trunc, perp, pos, swap


class Edge:
    """Represents the edge of the plate."""
    def __init__(self, start_point, end_point, segments=None):
        self.start_point = start_point
        self.end_point = end_point
        self._alpha = None
        if segments:
            self._points = self.split(segments)
        else:
            self._points = []

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, points):
        self._points = points

    @property
    def length(self):
        """The length of the plate edge."""
        dx = self.start_point[0] - self.end_point[0]
        dy = self.start_point[1] - self.end_point[1]
        return np.hypot(dx, dy)

    def split(self, segments):
        """Divides an edge into segments and returns the coordinates of their origins."""
        delta_x = (self.end_point[0] - self.start_point[0]) / float(segments)
        delta_y = (self.end_point[1] - self.start_point[1]) / float(segments)
        points = [
            (self.start_point[0] + i * delta_x, self.start_point[1] + i * delta_y)
            for i in range(1, segments)
        ]
        return points

    @property
    def mid_point(self):
        """The coordinates of the edge's midpoint."""
        x = 0.5 * (self.start_point[0] + self.end_point[0])
        y = 0.5 * (self.start_point[1] + self.end_point[1])
        return x, y

    @property
    def alpha(self):
        """Angle between the normal n and the x axis.

        See: https://numpy.org/doc/stable/reference/generated/numpy.arctan2.html

        Note the role reversal:
        the y-coordinate is the first function parameter,
        the x-coordinate is the second.
        """

        if self._alpha:
            return self._alpha

        self._alpha = angle_trunc(
            np.arctan2(*swap(*perp(*pos(self.start_point, self.end_point))))
        )
        return self._alpha

    @alpha.setter
    def alpha(self, deg):
        """Set the alpha using the deg parameter expressed in degrees."""
        self._alpha = np.deg2rad(deg)

    @property
    def alpha_deg(self):
        """Return alpha in degrees."""
        return np.rad2deg(self.alpha)


class Node:
    def __init__(self, points: list[tuple[float, float]]) -> None:
        self._points = points

    @property
    def coords(self) -> npt.NDArray[np.float64]:
        """Returns the coordinates of points in the form of an array."""
        if not isinstance(self._points, list):
            self._points = [self._points]
        return np.array(self._points)


class BoundaryNode(Node):
    def __init__(self, edge: Edge, boundary_conditions: tuple[str, str]) -> None:
        super().__init__(edge.points)
        self.alpha = edge.alpha
        self.boundary_conditions = boundary_conditions


class SurfaceNode(Node):
    def __init__(self, points: list[tuple[float, float]], load: float = 0) -> None:
        super().__init__(points)
        self.load = load
