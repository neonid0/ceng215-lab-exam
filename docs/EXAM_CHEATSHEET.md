# CENG 215 Lab Exam - Quick Reference Cheat Sheet

## 🚀 Quick Start

```python
# Import what you need
from components.x_diode import XDiode
from components.quadratic_device import QuadraticDevice
from solvers.rc_linear_solver import LinearRCSolver
from solvers.rc_diode_solver import RC_Diode_Solver
from plotter.circuit_plotter import CircuitPlotter
```

---

## 📦 Components Reference

| Component | Equation | File | Usage |
|-----------|----------|------|-------|
| **X-Diode** | Piecewise (see prep) | `components/x_diode.py` | `XDiode()` |
| **Quadratic** | i = 0.01v² | `components/quadratic_device.py` | `QuadraticDevice(k=0.01)` |
| **Resistor** | i = v/R | `components/resistor.py` | `Resistor(R=1000)` |
| **Capacitor** | i = C·dv/dt | `components/capacitor.py` | `Capacitor(C=1e-6)` |
| **Inductor** | v = L·di/dt | `components/inductor.py` | `Inductor(L=1e-3)` |

---

## 🔧 Solvers Reference

| Solver | Circuit Type | When to Use | File |
|--------|--------------|-------------|------|
| **LinearRCSolver** | RC with linear R | Step/Ramp/Sine inputs | `solvers/rc_linear_solver.py` |
| **RC_Diode_Solver** | RC with X-diode | Exam prep question | `solvers/rc_diode_solver.py` |
| **NonlinearRCSolver** | RC with any nonlinear | Quadratic device | `solvers/nonlinear_rc_solver.py` |
| **RLCSolver** | Series RLC | Second-order circuits | `solvers/rlc_solver.py` |

---

## 📝 Common Exam Patterns

### Pattern 1: Exam Prep Question (X-Diode + RC)

```python
# The exact prep question setup
from components.x_diode import XDiode
from solvers.rc_diode_solver import RC_Diode_Solver
from plotter.circuit_plotter import CircuitPlotter

# Initialize
diode = XDiode()
solver = RC_Diode_Solver(
    R_LOAD=50e3,      # 50 kΩ
    C_FILTER=1e-6,    # 1 µF
    dt=0.0001,        # 0.1 ms
    diode=diode
)

# Solve
t, vs, vo = solver.solve(
    T_END=2.0,        # 2 seconds
    V_INIT=3.0        # Initial voltage 3V
)

# Plot
plotter = CircuitPlotter(dark_mode=True)
plotter.plot(t, vs, vo, title="X-Diode Circuit")
```

### Pattern 2: Linear RC with Step Input (Lecture Section 4)

```python
from solvers.rc_linear_solver import LinearRCSolver

# Setup
R = 1000.0        # 1 kΩ
C = 1e-4          # 100 µF
tau = R * C       # Time constant
dt = 0.002 * tau  # Step size

solver = LinearRCSolver(R, C, dt)

# Solve with step input
t, u, x_num, x_ref = solver.solve_step(
    A=5.0,          # 5V step
    t_end=5*tau,
    x0=0.0
)

# Plot (compare with analytic)
import matplotlib.pyplot as plt
plt.plot(t, x_num, label='Numerical')
plt.plot(t, x_ref, '--', label='Analytic')
plt.legend()
plt.show()
```

### Pattern 3: Quadratic Device (Lecture Section 7)

```python
from components.quadratic_device import QuadraticDevice
from solvers.nonlinear_rc_solver import NonlinearRCSolver

# Setup
device = QuadraticDevice(k=0.01)  # i = 0.01*v²
C = 1e-4          # 100 µF
dt = 1e-5         # Small timestep for stability!

solver = NonlinearRCSolver(C, dt, device)

# Solve with step input
t, vs, vC, i_dev = solver.solve_step(
    A=5.0,          # 5V step
    t_end=0.3,
    vC0=0.0
)

# Plot
import matplotlib.pyplot as plt
plt.plot(t, vC, label='vC(t)')
plt.plot(t, vs, '--', label='vs(t)')
plt.legend()
plt.show()
```

### Pattern 4: RLC Circuit (Lecture Section 1)

```python
from solvers.rlc_solver import RLCSolver
from sources.input_sources import SinusoidSource

# Setup
R = 10.0          # 10 Ω
L = 0.01          # 10 mH
C = 1e-4          # 100 µF
dt = 1e-5         # Small timestep

solver = RLCSolver(R, L, C, dt)

# Create sinusoidal source
source = SinusoidSource(amplitude=10.0, omega=100.0)

# Solve
t, vs, vC, iL = solver.solve(
    source_func=source,
    t_end=0.2,
    vC0=0.0,
    iL0=0.0
)

# Plot both state variables
import matplotlib.pyplot as plt
fig, (ax1, ax2) = plt.subplots(2, 1)
ax1.plot(t, vC, label='vC(t)')
ax2.plot(t, iL*1000, label='iL(t) [mA]')
ax1.legend()
ax2.legend()
plt.show()
```

---

## 🎯 Input Source Quick Reference

```python
from sources.input_sources import StepSource, RampSource, SinusoidSource

# Step: u(t) = A
step = StepSource(amplitude=5.0)

# Ramp: u(t) = A*t
ramp = RampSource(slope=2.0)

# Sinusoid: u(t) = A*sin(ωt)
sine = SinusoidSource(amplitude=10.0, omega=50.0)

# Use in solver
t, u, x = solver.solve(source_func=sine, t_end=1.0)
```

---

## ⚠️ Critical Exam Tips

### Time Step Selection

| Circuit Type | Recommended dt |
|--------------|----------------|
| **RC Linear** | dt ≤ 0.05 * τ (τ = RC) |
| **RC Nonlinear** | dt ≤ 1e-5 (start small!) |
| **RLC** | dt ≤ T₀/50 (T₀ = 2π/ω₀) |

**Stability Rule for RC**: Always ensure `0 < dt < 2*τ`

### Common Mistakes to Avoid

1. ❌ **Wrong units**: Remember to convert kΩ → Ω, µF → F, mA → A
2. ❌ **dt too large**: Causes instability or inaccuracy
3. ❌ **Wrong initial conditions**: Read the question carefully!
4. ❌ **Forgot to import**: Import all needed modules
5. ❌ **Comparing wrong variables**: vs(t) vs vC(t) vs vout(t)

### Unit Conversions

```python
# Resistance
1_kΩ = 1000.0          # or 1e3
50_kΩ = 50_000.0       # or 50e3

# Capacitance
1_µF = 1e-6            # 1 microfarad
100_µF = 100e-6

# Current (returned in Amperes, often need mA)
i_mA = i_Amperes * 1000

# Frequency
ω = 10  # rad/s
f_Hz = ω / (2 * np.pi)
```

---

## 📊 Plotting Quick Reference

```python
from plotter.circuit_plotter import CircuitPlotter

# Create plotter
plotter = CircuitPlotter(dark_mode=True)

# Simple plot
plotter.plot(t, vs, vo, title="My Circuit")

# Manual plotting
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))
plt.plot(t, vs, label='Source')
plt.plot(t, vo, label='Output')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

---

## 🔍 I-V Curve Plotting (For Component Analysis)

```python
from analyzers.iv_curve_plotter import IVCurvePlotter
from components.x_diode import XDiode

# Create plotter
plotter = IVCurvePlotter(dark_mode=True)

# Plot single component
diode = XDiode()
plotter.plot_component(
    component=diode,
    v_min=-4,
    v_max=6,
    title="X-Diode I-V Characteristic"
)

# Highlight breakpoints
plotter.plot_piecewise_regions(
    component=diode,
    breakpoints=[0, 3],
    v_min=-4,
    v_max=6
)
```

---

## 🧮 Analytic Solutions (For Verification)

### RC Step Response
```
vC(t) = A + (vC0 - A) * exp(-t/τ)
```

### RC Ramp Response
```
vC(t) = A(t - τ) + (vC0 + Aτ) * exp(-t/τ)
```

### RC Sinusoid (Steady-State)
```
vC_ss(t) = A/√(1+(ωτ)²) * sin(ωt - arctan(ωτ))
```

---

## 💾 File Structure

```
lab-exam/
├── components/
│   ├── x_diode.py              # Exam prep question
│   ├── quadratic_device.py     # Lecture Section 7
│   ├── resistor.py
│   ├── capacitor.py
│   └── inductor.py
├── solvers/
│   ├── rc_diode_solver.py      # Exam prep
│   ├── rc_linear_solver.py     # Lecture Sections 2-4
│   ├── nonlinear_rc_solver.py  # Lecture Section 7
│   └── rlc_solver.py           # Lecture Section 1
├── sources/
│   └── input_sources.py        # Step, Ramp, Sine
├── plotter/
│   └── circuit_plotter.py      # Visualization
├── analyzers/
│   └── iv_curve_plotter.py     # Component analysis
└── main.py                     # Example usage
```

---

## 🎓 Exam Strategy

1. **Read the question carefully** - Identify:
   - Circuit topology (RC? RLC?)
   - Component types (linear? nonlinear?)
   - Input type (step? sine?)
   - Initial conditions
   - What to plot

2. **Choose the right solver** - Use the table above

3. **Set up parameters correctly** - Watch units!

4. **Verify dt is appropriate** - Check stability condition

5. **Run and plot** - Compare with expected behavior

6. **If stuck** - Look at `main.py` or similar examples

---

**Good luck on your exam! 🎉**
