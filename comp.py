from config import K, M, N
from impl import force, shape
from known import M_n, M_x, M_xy, M_y, Q_x, Q_y, V_x, V_y, phi_n, phi_x, phi_y

# Shape functions

W_g = shape(K)
U_g = [phi_x(f) for f in W_g]
V_g = [phi_y(f) for f in W_g]
X_g = [M_x(f) for f in W_g]
Y_g = [M_y(f) for f in W_g]
Z_g = [M_xy(f) for f in W_g]
G_g = [Q_x(f) for f in W_g]
H_g = [Q_y(f) for f in W_g]
K_g = [V_x(f) for f in W_g]
L_g = [V_y(f) for f in W_g]
F_g = lambda alpha: [M_n(f, alpha) for f in W_g]
P_g = lambda alpha: [phi_n(f, alpha) for f in W_g]

# Force functions

W_p = force(M, N)
U_p = [phi_x(f) for f in W_p]
V_p = [phi_y(f) for f in W_p]
X_p = [M_x(f) for f in W_p]
Y_p = [M_y(f) for f in W_p]
Z_p = [M_xy(f) for f in W_p]
G_p = [Q_x(f) for f in W_p]
H_p = [Q_y(f) for f in W_p]
K_p = [V_x(f) for f in W_p]
L_p = [V_y(f) for f in W_p]
F_p = lambda alpha: [M_n(f, alpha) for f in W_p]
P_p = lambda alpha: [phi_n(f, alpha) for f in W_p]
