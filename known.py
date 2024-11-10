from autograd import elementwise_grad as grad
from autograd.numpy import cos, sin

from config import E, h, nu

dx, dy = 0, 1


D = (E * h**3) / (12 * (1 - nu**2))


def nabla4(w):
    def fn(x, y):
        return (
            grad(grad(grad(grad(w, dx), dx), dx), dx)(x, y)
            + 2 * grad(grad(grad(grad(w, dx), dx), dy), dy)(x, y)
            + grad(grad(grad(grad(w, dy), dy), dy), dy)(x, y)
        )

    return fn


def phi_x(w):
    def fn(x, y):
        return grad(w, dx)(x, y)

    return fn


def phi_y(w):
    def fn(x, y):
        return grad(w, dy)(x, y)

    return fn


def phi_n(w, alpha):
    def fn(x, y):
        return phi_x(w)(x, y) * cos(alpha) + phi_y(w)(x, y) * sin(alpha)

    return fn


def M_x(w):
    def fn(x, y):
        return -D * (grad(grad(w, dx), dx)(x, y) + nu * grad(grad(w, dy), dy)(x, y))

    return fn


def M_y(w):
    def fn(x, y):
        return -D * (grad(grad(w, dy), dy)(x, y) + nu * grad(grad(w, dx), dx)(x, y))

    return fn


def M_xy(w):
    def fn(x, y):
        return D * (1 - nu) * grad(grad(w, dx), dy)(x, y)

    return fn


def M_n(w, alpha):
    def fn(x, y):
        return (
            M_x(w)(x, y) * cos(alpha) ** 2
            + M_y(w)(x, y) * sin(alpha) ** 2
            - 2 * M_xy(w)(x, y) * sin(alpha) * cos(alpha)
        )

    return fn


def M_nt(w, alpha):
    def fn(x, y):
        return M_xy(w)(x, y) * (cos(alpha) ** 2 - sin(alpha) ** 2) + (
            M_x(w)(x, y) - M_y(w)(x, y)
        ) * sin(alpha) * cos(alpha)

    return fn


def Q_x(w):
    def fn(x, y):
        return -D * (
            grad(grad(grad(w, dx), dx), dx)(x, y)
            + grad(grad(grad(w, dx), dy), dy)(x, y)
        )

    return fn


def Q_y(w):
    def fn(x, y):
        return -D * (
            grad(grad(grad(w, dx), dx), dy)(x, y)
            + grad(grad(grad(w, dy), dy), dy)(x, y)
        )

    return fn


def V_x(w):
    def fn(x, y):
        return -D * (
            grad(grad(grad(w, dx), dx), dx)(x, y)
            + (2 - nu) * grad(grad(grad(w, dx), dy), dy)(x, y)
        )

    return fn


def V_y(w):
    def fn(x, y):
        return -D * (
            grad(grad(grad(w, dy), dy), dy)(x, y)
            + (2 - nu) * grad(grad(grad(w, dx), dx), dy)(x, y)
        )

    return fn
