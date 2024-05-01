import sympy as sp
from scipy.optimize import minimize

# Define variables
xs, xw, ys, yw = sp.symbols('xs xw ys yw', real=True, nonnegative=True)
DA, DB, S_max, W_max, C_s, C_w = sp.symbols('DA DB S_max W_max C_s C_w', real=True, positive=True)

# Define objective function
C_total = C_s * (xs + ys) + C_w * (xw + yw)

# Define constraints
constraints = [
    xs + xw - DA,
    ys + yw - DB,
    xs + ys - S_max,
    xw + yw - W_max
]

# Define objective function for SciPy
def objective(values):
    xs_val, xw_val, ys_val, yw_val = values
    return C_total.subs({xs: xs_val, xw: xw_val, ys: ys_val, yw: yw_val})

# Define constraint functions for SciPy
def constraint_eq0(values):
    return values[0] + values[1] - DA
def constraint_eq1(values):
    return values[2] + values[3] - DB
def constraint_eq2(values):
    return values[0] + values[2] - S_max
def constraint_eq3(values):
    return values[1] + values[3] - W_max

# Set initial guess
initial_guess = [0.5 * DA, 0.5 * W_max, 0.5 * DB, 0.5 * W_max]

# Define bounds (non-negative)
bounds = [(0, None)] * 4

# Define equality constraints
constraints_eq = (
    {'type': 'eq', 'fun': constraint_eq0},
    {'type': 'eq', 'fun': constraint_eq1},
    {'type': 'eq', 'fun': constraint_eq2},
    {'type': 'eq', 'fun': constraint_eq3}
)

# Solve the optimization problem using SciPy
result = minimize(objective, initial_guess, bounds=bounds, constraints=constraints_eq)

# Print the optimal values
print("Optimal values:")
for var, val in zip([xs, xw, ys, yw], result.x):
    print(f"{var}: {val}")
