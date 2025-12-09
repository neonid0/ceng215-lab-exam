# Solver Guide

Complete guide to all circuit solvers with usage examples and best practices.

---

## Table of Contents

- [Solver Selection Guide](#solver-selection-guide)
- [Linear RC Solver](#linear-rc-solver)
- [RC Diode Solver](#rc-diode-solver)
- [Nonlinear RC Solver](#nonlinear-rc-solver)
- [RLC Solver](#rlc-solver)
- [Time Step Selection](#time-step-selection)
- [Stability and Accuracy](#stability-and-accuracy)

---

## Solver Selection Guide

**Decision Tree**:

```
Is your circuit second-order (has L and C)?
├─ YES → Use RLCSolver
└─ NO → Is it first-order RC?
    ├─ YES → Does it have a nonlinear device?
    │   ├─ YES → Is it X-diode?
    │   │   ├─ YES → Use RC_Diode_Solver (exam prep)
    │   │   └─ NO → Use NonlinearRCSolver
    │   └─ NO → Use LinearRCSolver
    └─ NO → Not supported (or build custom)
```

**Quick Reference Table**:

| Solver | Circuit Type | Lecture Section | Exam Use |
|--------|--------------|-----------------|----------|
| **LinearRCSolver** | RC with linear R | Sections 2-4 | Step/Ramp/Sine analysis |
| **RC_Diode_Solver** | RC with X-diode | Prep Question | Exact exam prep question |
| **NonlinearRCSolver** | RC with any nonlinear | Section 7 | Quadratic device problems |
| **RLCSolver** | Series RLC | Section 1 | Second-order circuits |

---

## Linear RC Solver

**File**: `solvers/rc_linear_solver.py`

**Reference**: CENG 215 Lecture Notes, Sections 2-4

### Circuit Model

```
    vs(t)  R    C
     ┬─────┬────┬
     │     │    │
    [V]   [R]  [C]
     │     │    │
     └─────┴────┴
```

### State Equation

```
dvC/dt = -(1/τ) * vC + (1/τ) * vs(t)

where τ = RC (time constant)
```

### Basic Usage

```python
from solvers.rc_linear_solver import LinearRCSolver

# Initialize solver
R = 1000.0        # 1 kΩ
C = 1e-4          # 100 µF
tau = R * C       # Time constant = 0.1 s
dt = 0.002 * tau  # Timestep (< 2*tau for stability)

solver = LinearRCSolver(R, C, dt)
```

### Solve with Step Input

```python
# Step input: vs(t) = A
t, u, x_num, x_ref = solver.solve_step(
    A=5.0,          # Step amplitude (V)
    t_end=5*tau,    # Simulation time
    x0=0.0          # Initial capacitor voltage
)

# x_ref contains analytic solution for comparison
```

**Analytic Solution**:
```
vC(t) = A + (x0 - A) * exp(-t/τ)
```

### Solve with Ramp Input

```python
# Ramp input: vs(t) = A*t
t, u, x_num, x_ref = solver.solve_ramp(
    A=2.0,          # Ramp slope (V/s)
    t_end=5*tau,
    x0=0.0
)
```

**Analytic Solution**:
```
vC(t) = A(t - τ) + (x0 + Aτ) * exp(-t/τ)
```

### Solve with Sinusoidal Input

```python
# Sinusoid input: vs(t) = A*sin(ωt)
t, u, x_num, x_ref = solver.solve_sinusoid(
    A=10.0,              # Amplitude (V)
    omega=50.0,          # Angular frequency (rad/s)
    t_end=1.0,
    x0=0.0,
    steady_state_only=True  # x_ref is steady-state only
)
```

**Steady-State Analytic Solution**:
```
vC_ss(t) = A/√(1+(ωτ)²) * sin(ωt - arctan(ωτ))
```

### Custom Input Source

```python
# Define custom source function
def my_source(t):
    return 5.0 * np.exp(-t) + 2.0

# Solve
t, u, x, _ = solver.solve(
    source_func=my_source,
    t_end=1.0,
    v0=0.0,
    analytic_func=None  # No analytic solution
)
```

### Time Constant

```python
tau = solver.get_time_constant()
print(f"Time constant: {tau} s")
```

---

## RC Diode Solver

**File**: `solvers/rc_diode_solver.py`

**Reference**: CENG 215 Exam Prep Question

### Circuit Model

```
 Vs(t)  X-diode   Vo(t)
   ┬─────►├─┬─────┬
   │        │     │
  [V]      [R]   [C]
   │        │     │
   └────────┴─────┴
```

### State Equation

```
dVo/dt = (1/C) * (i_diode - i_resistor)

where:
  i_diode = f(Vs - Vo)  [nonlinear]
  i_resistor = Vo / R    [linear]
```

### Basic Usage

```python
from components.x_diode import XDiode
from solvers.rc_diode_solver import RC_Diode_Solver

# Initialize X-diode
diode = XDiode()

# Initialize solver with EXACT exam prep parameters
solver = RC_Diode_Solver(
    R_LOAD=50e3,      # 50 kΩ
    C_FILTER=1e-6,    # 1 µF
    dt=0.0001,        # 0.1 ms
    diode=diode
)

# Solve (automatically uses Vs(t) = 10*sin(10*t))
t, vs, vo = solver.solve(
    T_END=2.0,        # 2 seconds
    V_INIT=3.0        # Initial output voltage
)
```

### Built-in Source

The solver has a built-in sinusoidal source matching the exam prep:
```
Vs(t) = 10 * sin(10*t)
```

Amplitude: 10V, Frequency: 10 rad/s

### Plotting

```python
from plotter.circuit_plotter import CircuitPlotter

plotter = CircuitPlotter(dark_mode=True)
plotter.plot(t, vs, vo, title="X-Diode RC Circuit")
```

---

## Nonlinear RC Solver

**File**: `solvers/nonlinear_rc_solver.py`

**Reference**: CENG 215 Lecture Notes, Section 7

### Circuit Model

```
 vs(t)  Device   C
   ┬─────[NL]───┬
   │            │
  [V]          [C]
   │            │
   └────────────┴
```

### State Equation

```
dvC/dt = (1/C) * i_device(vs - vC)

where i_device is the nonlinear device characteristic
```

### Basic Usage with Quadratic Device

```python
from components.quadratic_device import QuadraticDevice
from solvers.nonlinear_rc_solver import NonlinearRCSolver

# Initialize device
device = QuadraticDevice(k=0.01)  # i = 0.01*v²

# Initialize solver
C = 1e-4          # 100 µF
dt = 1e-5         # Small timestep for stability!

solver = NonlinearRCSolver(C, dt, device)
```

### Solve with Step Input

```python
# Step input
t, vs, vC, i_dev = solver.solve_step(
    A=5.0,          # Step amplitude
    t_end=0.3,      # Simulation time
    vC0=0.0         # Initial capacitor voltage
)

# Returns:
# - t: time array
# - vs: source voltage
# - vC: capacitor voltage
# - i_dev: device current
```

### Solve with Sinusoid

```python
# Sinusoid input
t, vs, vC, i_dev = solver.solve_sinusoid(
    A=10.0,         # Amplitude
    omega=100.0,    # Angular frequency
    t_end=0.2,
    vC0=0.0
)

# Note: Output is NOT sinusoidal due to nonlinearity!
```

### Custom Source

```python
def my_source(t):
    return 5.0 * np.sin(10*t) + 2.0

t, vs, vC, i_dev = solver.solve(
    source_func=my_source,
    t_end=1.0,
    vC0=0.0
)
```

### Important Notes

⚠️ **Stability Warning**: Nonlinear systems can be numerically unstable!
- Start with small dt (e.g., 1e-5)
- If solution "blows up", reduce dt
- Monitor for unrealistic values

---

## RLC Solver

**File**: `solvers/rlc_solver.py`

**Reference**: CENG 215 Lecture Notes, Section 1

### Circuit Model

```
 vs(t)   R    L    C
   ┬────┬────┬────┬
   │    │    │    │
  [V]  [R]  [L]  [C]
   │    │    │    │
   └────┴────┴────┴
```

### State Equations

```
State vector: x = [vC, iL]ᵀ

dvC/dt = (1/C) * iL
diL/dt = (1/L) * (-R*iL - vC + vs(t))
```

### Second-Order ODE

```
LC * d²vC/dt² + RC * dvC/dt + vC = vs(t)
```

### Basic Usage

```python
from solvers.rlc_solver import RLCSolver
from sources.input_sources import SinusoidSource

# Initialize solver
R = 10.0          # 10 Ω
L = 0.01          # 10 mH
C = 1e-4          # 100 µF
dt = 1e-5         # Timestep

solver = RLCSolver(R, L, C, dt)
```

### Circuit Parameters

```python
# Get circuit characteristics
params = solver.get_circuit_params()

print(f"Natural frequency: {params['omega_0']} rad/s")
print(f"Natural frequency: {params['f_0']} Hz")
print(f"Natural period: {params['T_0']} s")
print(f"Damping ratio: {params['zeta']}")
print(f"Damping type: {params['damping_type']}")

# If underdamped:
if 'omega_d' in params:
    print(f"Damped frequency: {params['omega_d']} rad/s")
```

### Damping Types

- **Underdamped** (ζ < 1): Oscillatory response
- **Critically damped** (ζ = 1): Fastest response without overshoot
- **Overdamped** (ζ > 1): Slow response, no oscillation

### Solve with Source

```python
# Create sinusoidal source
source = SinusoidSource(amplitude=10.0, omega=100.0)

# Solve
t, vs, vC, iL = solver.solve(
    source_func=source,
    t_end=0.2,
    vC0=0.0,      # Initial capacitor voltage
    iL0=0.0       # Initial inductor current
)

# Returns two state variables: vC(t) and iL(t)
```

### Plotting Both State Variables

```python
import matplotlib.pyplot as plt

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# Plot capacitor voltage
ax1.plot(t, vC, label='vC(t)')
ax1.plot(t, vs, '--', alpha=0.5, label='vs(t)')
ax1.set_ylabel('Voltage (V)')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Plot inductor current
ax2.plot(t, iL * 1000, label='iL(t)', color='orange')
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Current (mA)')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

---

## Time Step Selection

### General Guidelines

| Circuit Type | Recommended dt | Stability Condition |
|--------------|----------------|---------------------|
| **RC Linear** | dt ≤ 0.05*τ | 0 < dt < 2*τ |
| **RC Nonlinear** | dt ≤ 1e-5 | Depends on nonlinearity |
| **RLC** | dt ≤ T₀/50 | Depends on damping |

### Calculating Appropriate dt

#### For RC Circuits:

```python
tau = R * C
dt_stability = 2 * tau            # Maximum for stability
dt_accuracy = 0.05 * tau          # Recommended for accuracy
dt_precise = 0.002 * tau          # High accuracy

# Choose based on needs
dt = dt_accuracy
```

#### For RLC Circuits:

```python
omega_0 = 1 / np.sqrt(L * C)      # Natural frequency
T_0 = 2 * np.pi / omega_0         # Natural period
dt = T_0 / 50                     # Recommended
```

#### For Nonlinear Circuits:

```python
# Start conservatively
dt = 1e-5  # or smaller

# Run test simulation
# If unstable or inaccurate, reduce dt by factor of 10
# If stable, can try increasing dt for speed
```

---

## Stability and Accuracy

### Stability Issues

**Symptoms**:
- Solution "explodes" to infinity
- Oscillations with increasing amplitude
- NaN or Inf values

**Solutions**:
1. Reduce dt
2. Check initial conditions
3. Verify component parameters (positive values)
4. For nonlinear: ensure device model is reasonable

### Accuracy Issues

**Symptoms**:
- Numerical solution doesn't match analytic
- Visible staircase effect in plots
- Phase lag or amplitude error

**Solutions**:
1. Reduce dt (increase number of points)
2. For RC: ensure dt ≤ 0.01*τ
3. For RLC: ensure dt ≤ T₀/100
4. Consider higher-order methods (not implemented, but RK4 is better)

### Verification Strategies

1. **Compare with Analytic** (if available):
```python
# For LinearRCSolver
t, u, x_num, x_ref = solver.solve_step(A=5.0, t_end=5*tau, x0=0.0)

# Calculate error
error = np.abs(x_num - x_ref)
max_error = np.max(error)
mean_error = np.mean(error)

print(f"Max error: {max_error}")
print(f"Mean error: {mean_error}")
```

2. **Convergence Test**:
```python
# Run with different dt values
dt_values = [1e-3, 1e-4, 1e-5, 1e-6]
results = []

for dt in dt_values:
    solver = LinearRCSolver(R, C, dt)
    t, u, x, _ = solver.solve_step(A=5.0, t_end=0.5, x0=0.0)
    results.append((dt, x[-1]))  # Store final value

# Check convergence
for dt, x_final in results:
    print(f"dt={dt:.0e}: x_final={x_final:.6f}")
```

3. **Energy Conservation** (for conservative systems):
```python
# For RLC, check total energy
W_C = 0.5 * C * vC**2          # Capacitor energy
W_L = 0.5 * L * iL**2          # Inductor energy
W_total = W_C + W_L

# Plot over time (should decrease due to R losses)
```

---

## Solver Comparison

| Feature | LinearRC | RC_Diode | NonlinearRC | RLC |
|---------|----------|----------|-------------|-----|
| **Order** | 1st | 1st | 1st | 2nd |
| **State Var** | vC | Vo | vC | [vC, iL] |
| **Nonlinear** | No | Yes | Yes | No |
| **Analytic** | Yes | No | No | Complex |
| **dt Sensitive** | Moderate | Moderate | High | High |
| **Exam Use** | Common | Prep Q | Section 7 | Section 1 |

---

## Tips for Exam Success

1. **Identify circuit type first** - This determines the solver
2. **Check units** - Convert kΩ to Ω, µF to F, etc.
3. **Calculate time constant/period** - Helps choose dt and t_end
4. **Choose appropriate dt** - Follow guidelines above
5. **Verify solution** - Compare with analytic if available
6. **Plot and inspect** - Visual check for sanity
7. **Know the reference** - Match to lecture section

**Most Common Exam Scenarios**:
- Linear RC with step/ramp/sine → **LinearRCSolver**
- Exam prep question → **RC_Diode_Solver**
- Quadratic device → **NonlinearRCSolver**
- Second-order → **RLCSolver**
