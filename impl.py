from autograd.numpy import cos, cosh, pi, sin, sinh

from config import a, b


def _a(s):
    match s:
        case 1:
            return a
        case 2:
            return b


def _x(s):
    def fn(x, y):
        match s:
            case 1:
                return x
            case 2:
                return y

    return fn


def gamma(k, s):
    return (k * pi) / _a(s)


def delta(k, s):
    return ((2 * k - 1) * pi) / (2 * _a(s))


def kappa(k, p, s):
    match p:
        case 1 | 3:
            return gamma(k, s)
        case 2 | 4:
            return delta(k, s)


def T(k, p, s):
    def fn(x, y):
        match p:
            case 1 | 2:
                return cos(kappa(k, p, s) * _x(s)(x, y))
            case 3 | 4:
                return sin(kappa(k, p, s) * _x(s)(x, y))

    return fn


def T2(m, n, p, q):
    def fn(x, y):
        return T(m, p, 1)(x, y) * T(n, q, 2)(x, y)

    return fn


def Psi(x, y):
    return (
        x**4 / (24 * _a(1) ** 4)
        + (x**2 * y**2) / (4 * _a(1) ** 2 * _a(2) ** 2)
        + y**4 / (24 * _a(2) ** 4)
    )


def B(k, p, s, n):
    def fn(x, y):
        match n:
            case 1:
                return cosh(kappa(k, p, 3 - s) * _x(s)(x, y))
            case 2:
                return (_x(s)(x, y) / _a(s)) * (sinh(kappa(k, p, 3 - s) * _x(s)(x, y)))
            case 3:
                return sinh(kappa(k, p, 3 - s) * _x(s)(x, y))
            case 4:
                return (_x(s)(x, y) / _a(s)) * (cosh(kappa(k, p, 3 - s) * _x(s)(x, y)))

    return fn


def W(k, p, s, n):
    def fn(x, y):
        return B(k, p, s, n)(x, y) * T(k, p, 3 - s)(x, y)

    return fn


def shape(K):
    return [
        W(k, p, s, ni)
        for k in range(1, K + 1)
        for p in range(1, 5)
        for s in range(1, 3)
        for ni in range(1, 5)
    ]


def force(M, N):
    t0 = [Psi]
    t1 = [T(m, p, s) for m in range(1, M + 1) for p in range(1, 5) for s in range(1, 3)]
    t2 = [
        T2(m, n, p, q)
        for m in range(1, M + 1)
        for n in range(1, N + 1)
        for p in range(1, 5)
        for q in range(1, 5)
    ]
    return t0 + t1 + t2
