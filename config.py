from shapely import Polygon

# Numbers of approximations of the solution
K = 7
M = N = 5

# Vertices

# Isosceles triangle
vertices = [(-3.0, -3.0), (0.0, 3.0), (3.0, -3.0)]

# Right triangle
# vertices = [(-3.0, -3.0), (-3.0, 3.0), (3.0, -3.0)]

# Acute triangle
# vertices = [(-3.0, -3.0), (-1.5, 3.0), (3.0, -3.0)]

# Obtuse triangle
# vertices = [(-3.0, -3.0), (-4.0, 3.0), (3.0, -3.0)]

# Parallelogram
# vertices = [(-3.0, -3.0), (-1.5, 3.0), (3.0, 3.0), (1.5, -3.0)]

# Trapeze
# vertices = [(-3.0, -3.0), (-3.0, 3.0), (3.0, 0.0), (3.0, -3.0)]

# Regular hexagon
# vertices = [(-3.0, 0.0), (-1.5, 2.598), (1.5, 2.598), (3.0, 0.0), (1.5, -2.598), (-1.5, -2.598)]

# Polygon
polygon = Polygon(vertices)

# Envelope
minx, miny, maxx, maxy = polygon.envelope.bounds
a = 0.5 * (maxx - minx)
b = 0.5 * (maxy - miny)

# Thickness of a plate
h = 0.2  # m

# Young's modulus
E = 3e10  # Pa

# Poisson's ratio
nu = 0.2

# Intensity of a load
q_0 = 10_000.0  # Pa
