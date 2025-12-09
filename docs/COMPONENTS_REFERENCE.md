# Component Reference Guide

Complete reference for all circuit components in the lab exam toolkit.

---

## Table of Contents

- [Nonlinear Components](#nonlinear-components)
  - [X-Diode](#x-diode)
  - [Quadratic Device](#quadratic-device)
- [Linear Components](#linear-components)
  - [Resistor](#resistor)
  - [Capacitor](#capacitor)
  - [Inductor](#inductor)
- [Input Sources](#input-sources)
  - [Step Source](#step-source)
  - [Ramp Source](#ramp-source)
  - [Sinusoid Source](#sinusoid-source)

---

## Nonlinear Components

### X-Diode

**File**: `components/x_diode.py`

**Description**: Special piecewise-linear diode from exam preparation question.

**I-V Characteristic**:

```
          ⎧ 0.1 * vD              for vD < 0
iD(vD) = ⎨ (2/3) * vD            for 0 ≤ vD ≤ 3
          ⎩ (vD - 3)² + 2         for vD > 3
```

**Usage**:

```python
from components.x_diode import XDiode

# Create X-diode
diode = XDiode()

# Calculate current for voltage
v = 2.5  # Volts
i = diode.current(v)  # Returns current in Amperes
print(f"At {v}V: {i*1000:.3f} mA")

# Piecewise regions
i_negative = diode.current(-2.0)   # Reverse bias: 0.1*(-2) = -0.2 mA
i_linear = diode.current(1.5)      # Forward linear: (2/3)*1.5 = 1.0 mA
i_quadratic = diode.current(4.0)   # Forward high: (4-3)² + 2 = 3.0 mA
```

**Key Characteristics**:

- Three distinct regions (reverse, linear forward, quadratic forward)
- Breakpoints at vD = 0V and vD = 3V
- Used in exam preparation question
- Returns current in **Amperes** (convert to mA with * 1000)

---

### Quadratic Device

**File**: `components/quadratic_device.py`

**Description**: Nonlinear device with quadratic i-v characteristic from Lecture Section 7.

**I-V Characteristic**:

```
i(v) = k * v²
```

**Parameters**:

- `k`: Quadratic coefficient (default: 0.01 A/V²)

**Usage**:

```python
from components.quadratic_device import QuadraticDevice

# Create with default k=0.01
device = QuadraticDevice()

# Or specify custom k
device = QuadraticDevice(k=0.02)

# Calculate current
v = 5.0  # Volts
i = device.current(v)  # Returns k*v² = 0.01*25 = 0.25 A

# Incremental conductance at operating point
g = device.conductance(v)  # di/dv = 2*k*v

# Power dissipation
p = device.power(v)  # P = k*v³
```

**Key Characteristics**:

- Symmetric: same behavior for +v and -v
- Nonlinear: doubling voltage quadruples current
- Always positive current (i ≥ 0)
- Used in Lecture Section 7 nonlinear RC analysis

**Mathematical Properties**:

```python
# Incremental conductance
g(v) = di/dv = 2*k*v

# Incremental resistance
r(v) = dv/di = 1/(2*k*v)  # undefined at v=0

# Power
P(v) = v*i = k*v³
```

---

## Linear Components

### Resistor

**File**: `components/resistor.py`

**Description**: Linear resistor following Ohm's law.

**Equations**:

```
V = I * R  (Ohm's law)
I = V / R
P = V² / R (power dissipation)
```

**Usage**:

```python
from components.resistor import Resistor

# Create resistor
R = Resistor(resistance=1000.0)  # 1 kΩ

# Calculate current from voltage
v = 5.0  # Volts
i = R.current(v)  # Returns 0.005 A (5 mA)

# Calculate voltage from current
i = 0.01  # Amperes
v = R.voltage(i)  # Returns 10.0 V

# Power dissipation
p = R.power(v)  # Returns V²/R in Watts

# Impedance (constant at all frequencies)
z = R.impedance(freq=0)  # Returns R + j0

# Get parameter
r_value = R.get_parameter()  # Returns resistance value
```

**Key Characteristics**:

- Linear: i ∝ v
- Dissipates power (converts to heat)
- Frequency-independent (pure resistance)
- Used in RC and RLC circuits

---

### Capacitor

**File**: `components/capacitor.py`

**Description**: Linear capacitor for energy storage and AC coupling.

**Equations**:

```
I = C * dV/dt          (current-voltage relationship)
dV/dt = I / C          (state equation form)
Q = C * V              (charge storage)
W = (1/2) * C * V²     (energy storage)
Z(jω) = 1/(jωC)        (AC impedance)
```

**Usage**:

```python
from components.capacitor import Capacitor

# Create capacitor
C = Capacitor(capacitance=1e-6)  # 1 µF

# Current from voltage rate of change
dv_dt = 1000.0  # V/s
i = C.current_from_dv_dt(dv_dt)  # Returns 0.001 A (1 mA)

# Voltage rate from current (for state equations)
i = 0.002  # Amperes
dv_dt = C.dv_dt_from_current(i)  # Returns 2000 V/s

# Stored charge
v = 5.0  # Volts
q = C.charge(v)  # Returns 5e-6 Coulombs

# Stored energy
w = C.energy(v)  # Returns 1.25e-5 Joules

# AC impedance
omega = 100.0  # rad/s
z = C.impedance(omega)  # Returns -j/(ωC)

# Get parameter
c_value = C.get_parameter()  # Returns capacitance
```

**Key Characteristics**:

- State variable in circuits: vC(t)
- Stores energy in electric field
- Blocks DC (infinite impedance at ω=0)
- Passes AC (impedance decreases with frequency)

**Important for Simulation**:

```python
# In state equations: dv_C/dt = i_C / C
# Capacitor voltage is typically the state variable
```

---

### Inductor

**File**: `components/inductor.py`

**Description**: Linear inductor for energy storage and filtering.

**Equations**:

```
V = L * dI/dt          (voltage-current relationship)
dI/dt = V / L          (state equation form)
λ = L * I              (flux linkage)
W = (1/2) * L * I²     (energy storage)
Z(jω) = jωL            (AC impedance)
```

**Usage**:

```python
from components.inductor import Inductor

# Create inductor
L = Inductor(inductance=0.01)  # 10 mH

# Voltage from current rate of change
di_dt = 100.0  # A/s
v = L.voltage_from_di_dt(di_dt)  # Returns 1.0 V

# Current rate from voltage (for state equations)
v = 5.0  # Volts
di_dt = L.di_dt_from_voltage(v)  # Returns 500 A/s

# Flux linkage
i = 0.5  # Amperes
flux = L.flux_linkage(i)  # Returns 0.005 Wb

# Stored energy
w = L.energy(i)  # Returns 0.00125 Joules

# AC impedance
omega = 100.0  # rad/s
z = L.impedance(omega)  # Returns j*ωL

# Get parameter
l_value = L.get_parameter()  # Returns inductance
```

**Key Characteristics**:

- State variable in circuits: iL(t)
- Stores energy in magnetic field
- Passes DC (zero impedance at ω=0)
- Blocks AC (impedance increases with frequency)

**Important for Simulation**:

```python
# In state equations: di_L/dt = v_L / L
# Inductor current is typically the state variable
```

---

## Input Sources

### Step Source

**File**: `sources/input_sources.py`

**Description**: Unit step input u(t) = A for t ≥ 0.

**Mathematical Form**:

```
u(t) = A * u(t)

where u(t) = { 0  for t < 0
             { 1  for t ≥ 0
```

**Usage**:

```python
from sources.input_sources import StepSource

# Create step source
source = StepSource(amplitude=5.0)  # 5V step

# Evaluate at single time
t = 0.5
v = source(t)  # Returns 5.0

# Evaluate at array of times
import numpy as np
t = np.linspace(0, 1, 100)
v = source.vectorized(t)  # Returns array of 5.0s

# Use in solver
from solvers.rc_linear_solver import LinearRCSolver
solver = LinearRCSolver(R=1000, C=1e-4, dt=1e-5)
t, u, x, _ = solver.solve(source_func=source, t_end=0.5)
```

**Analytic Solution (RC)**:

```
vC(t) = A + (vC0 - A) * exp(-t/τ)
```

---

### Ramp Source

**File**: `sources/input_sources.py`

**Description**: Linear ramp input u(t) = A*t for t ≥ 0.

**Mathematical Form**:

```
u(t) = A * t * u(t)

where A is the slope (V/s or A/s)
```

**Usage**:

```python
from sources.input_sources import RampSource

# Create ramp source
source = RampSource(slope=2.0)  # 2 V/s slope

# Evaluate at single time
t = 1.5
v = source(t)  # Returns 3.0 V

# Evaluate at array of times
import numpy as np
t = np.linspace(0, 2, 100)
v = source.vectorized(t)  # Returns array: A*t

# Use in solver
t, u, x, _ = solver.solve(source_func=source, t_end=1.0)
```

**Analytic Solution (RC)**:

```
vC(t) = A(t - τ) + (vC0 + Aτ) * exp(-t/τ)
```

---

### Sinusoid Source

**File**: `sources/input_sources.py`

**Description**: Sinusoidal input u(t) = A*sin(ωt + φ).

**Mathematical Form**:

```
u(t) = A * sin(ωt + φ)

where:
  A = amplitude
  ω = angular frequency (rad/s)
  φ = phase angle (radians)
```

**Usage**:

```python
from sources.input_sources import SinusoidSource
import numpy as np

# Create sinusoid source
source = SinusoidSource(
    amplitude=10.0,
    omega=50.0,      # 50 rad/s
    phase=0.0        # 0 radians (optional)
)

# Evaluate at single time
t = 0.1
v = source(t)  # Returns 10*sin(50*0.1)

# Evaluate at array of times
t = np.linspace(0, 1, 1000)
v = source.vectorized(t)

# Get period
T = source.period()  # Returns 2π/ω

# Get frequency in Hz
f_hz = source.frequency_hz  # Returns ω/(2π)

# Use in solver
t, u, x, _ = solver.solve(source_func=source, t_end=0.5)
```

**Analytic Steady-State Solution (RC)**:

```
vC_ss(t) = A/√(1+(ωτ)²) * sin(ωt - arctan(ωτ))
```

**Properties**:

- Magnitude: `A/√(1+(ωτ)²)`
- Phase shift: `-arctan(ωτ)` (lag)
- Period: `T = 2π/ω`
- Frequency: `f = ω/(2π)` Hz

---

## Component Comparison Table

| Component | Type | State Variable | Equation | File |
|-----------|------|----------------|----------|------|
| X-Diode | Nonlinear | - | i = piecewise(v) | `x_diode.py` |
| Quadratic | Nonlinear | - | i = k*v² | `quadratic_device.py` |
| Resistor | Linear | - | i = v/R | `resistor.py` |
| Capacitor | Linear | vC(t) | i = C*dv/dt | `capacitor.py` |
| Inductor | Linear | iL(t) | v = L*di/dt | `inductor.py` |

---

## Tips for Component Selection

1. **X-Diode**: Use for exam prep question exactly as specified
2. **Quadratic Device**: Use for Lecture Section 7 nonlinear RC problems
3. **Resistor**: Use for linear RC analysis (Sections 2-4)
4. **Capacitor**: Always present in RC and RLC circuits
5. **Inductor**: Only for RLC (second-order) circuits

**Remember**: All currents are returned in **Amperes**. Multiply by 1000 for **milliamperes**.
