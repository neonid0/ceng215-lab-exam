# Theory Reference

Mathematical foundations and theoretical concepts for circuit simulation.

---

## Table of Contents

- [State Variables and State Equations](#state-variables-and-state-equations)
- [First-Order Systems (RC)](#first-order-systems-rc)
- [Second-Order Systems (RLC)](#second-order-systems-rlc)
- [Nonlinear Systems](#nonlinear-systems)
- [Numerical Methods](#numerical-methods)
- [Stability Analysis](#stability-analysis)
- [Analytic Solutions](#analytic-solutions)

---

## State Variables and State Equations

### Definition

**State**: The minimal set of variables whose values at time t₀ together with the input for t ≥ t₀ determine the future of the system.

### Energy-Storing Elements

In circuit theory, energy-storing elements define natural state choices:

- **Capacitor**: State variable is vC(t)
  - Stored energy: WC = ½Cv²C

- **Inductor**: State variable is iL(t)
  - Stored energy: WL = ½Li²L

### State Vector

For lumped RLC networks, a convenient state vector is:

```
     ⎡vC⎤
x = ⎢  ⎥
     ⎣iL⎦
```

---

## First-Order Systems (RC)

### Linear RC Circuit

**Circuit**:
```
vs(t) ──R──┬──C──
           │
          GND
```

**Equations**:
```
vs(t) = vR(t) + vC(t) = R·i(t) + vC(t)
i(t) = C·dvC/dt
```

**State Equation**:
```
dvC/dt = -(1/τ)·vC + (1/τ)·vs(t)

where τ = RC (time constant)
```

**Standard Form**:
```
ẋ = f(t, x, u) = -(1/τ)·x + (1/τ)·u

where:
  x(t) = vC(t)  (state)
  u(t) = vs(t)  (input)
  τ = RC        (time constant)
```

### Time Constant

The **time constant** τ = RC determines the speed of the circuit's response:

- After time t = τ, exponential has decayed to e⁻¹ ≈ 36.8% of initial value
- After time t = 5τ, response is essentially complete (< 1% error)

**Physical Interpretation**:
- Small τ: Fast response (quick charging/discharging)
- Large τ: Slow response (slow charging/discharging)

---

## Second-Order Systems (RLC)

### Series RLC Circuit

**Circuit**:
```
vs(t) ──R──L──┬──C──
              │
             GND
```

**Second-Order ODE**:
```
LC·d²vC/dt² + RC·dvC/dt + vC = vs(t)
```

**State-Space Form**:

State vector: x = [vC, iL]ᵀ

```
dx₁/dt = (1/C)·x₂
dx₂/dt = (1/L)·(-R·x₂ - x₁ + vs(t))
```

**Matrix Form**:
```
ẋ = Ax + Bu

where:
     ⎡  0     1/C ⎤       ⎡ 0  ⎤
A = ⎢            ⎥   B = ⎢    ⎥
     ⎣-1/L   -R/L ⎦       ⎣1/L ⎦
```

### Natural Frequency and Damping

**Natural Frequency** (ω₀):
```
ω₀ = 1/√(LC)  [rad/s]
f₀ = ω₀/(2π)  [Hz]
T₀ = 2π/ω₀    [s]
```

**Damping Ratio** (ζ):
```
ζ = R/(2√(L/C)) = R/(2ω₀L) = Rω₀C/2
```

**Damping Classifications**:

1. **Underdamped** (ζ < 1):
   - Oscillatory response
   - Damped frequency: ωd = ω₀√(1-ζ²)
   - Overshoot present

2. **Critically Damped** (ζ = 1):
   - Fastest response without overshoot
   - No oscillation
   - R = 2√(L/C)

3. **Overdamped** (ζ > 1):
   - No oscillation
   - Slower than critically damped
   - Two real exponential time constants

### Characteristic Equation

```
s² + (R/L)s + (1/LC) = 0
```

**Roots**:
```
s₁,₂ = -ζω₀ ± ω₀√(ζ²-1)
```

---

## Nonlinear Systems

### General Form

For nonlinear RC with device i = f(v):

```
dvC/dt = (1/C)·f(vs(t) - vC(t))
```

### Quadratic Device (Lecture Section 7)

**Device Model**:
```
i(v) = k·v²
```

**State Equation**:
```
dvC/dt = (k/C)·(vs(t) - vC(t))²
```

**Key Characteristics**:
- No closed-form analytic solution
- Approach to steady-state is NOT exponential
- Dynamics slow down as vC → vs (current → 0)
- Always stable for k > 0

### X-Diode (Exam Prep)

**Piecewise Model**:
```
         ⎧ 0.1·vD              vD < 0
iD(vD) = ⎨ (2/3)·vD            0 ≤ vD ≤ 3
         ⎩ (vD-3)² + 2         vD > 3
```

**Characteristics**:
- Three distinct regions
- Continuous but not differentiable at breakpoints
- Combines linear and quadratic segments

---

## Numerical Methods

### Euler's Forward Method

**Concept**: Approximate derivative with forward difference.

**Formula**:
```
Given: ẋ(t) = f(t, x, u)
Time grid: tk = t₀ + k·h

Update:
xk+1 = xk + h·f(tk, xk, uk)
```

**Algorithm**:
```
1. Initialize: t = t₀, x = x₀
2. Loop until t ≥ tend:
   a. Evaluate: f = f(t, x, u(t))
   b. Update: x ← x + h·f
   c. Advance: t ← t + h
3. Return trajectory
```

### Error Analysis

**Local Truncation Error**: O(h²)
**Global Truncation Error**: O(h)

**Meaning**: Halving h roughly halves the error.

### Higher-Order Methods (Not Implemented)

**Runge-Kutta 4th Order (RK4)**:
- Local error: O(h⁵)
- Global error: O(h⁴)
- Much more accurate than Euler
- 4× function evaluations per step

**When to consider RK4**:
- Stiff systems
- High-frequency oscillations
- When dt must be large (computational cost)

---

## Stability Analysis

### Linear RC Stability

**Homogeneous equation** (u = 0):
```
ẋ = -(1/τ)·x
```

**Euler discretization**:
```
xk+1 = xk + h·(-(1/τ)·xk) = (1 - h/τ)·xk
```

**Stability Condition**:
```
|1 - h/τ| < 1

Solving:
-1 < 1 - h/τ < 1

Right inequality: 1 - h/τ < 1  →  always satisfied
Left inequality: -1 < 1 - h/τ  →  h/τ < 2

Therefore: 0 < h < 2τ
```

**Recommended**: h ≤ 0.05τ for good accuracy

### Damping of Numerical Oscillations

For oscillatory or stiff second-order systems:
- Smaller h provides better damping
- Consider implicit methods (e.g., Backward Euler, Trapezoidal)
- Or higher-order explicit (e.g., RK4)

### Nonlinear Stability

For nonlinear systems, stability depends on:
1. Timestep h
2. Nonlinearity strength
3. Operating region

**Strategy**:
- Start with very small h (e.g., 1e-5)
- Run test simulation
- If stable, can gradually increase h
- If unstable, reduce h further

---

## Analytic Solutions

### RC with Step Input

**Input**: u(t) = A·u(t)

**Solution**:
```
vC(t) = A + (vC0 - A)·e^(-t/τ)
```

**Key Points**:
- Initial value: vC(0) = vC0
- Final value: vC(∞) = A
- Time constant: τ = RC

**Settling Time**: t ≈ 5τ (to within 1%)

### RC with Ramp Input

**Input**: u(t) = A·t·u(t)

**Solution**:
```
vC(t) = A(t - τ) + (vC0 + Aτ)·e^(-t/τ)
```

**Key Points**:
- Transient: (vC0 + Aτ)·e^(-t/τ)
- Steady-state: A(t - τ) (ramp with time lag τ)
- Output lags input by time constant τ

### RC with Sinusoid Input

**Input**: u(t) = A·sin(ωt)

**Steady-State Solution**:
```
vC,ss(t) = (A/√(1+(ωτ)²))·sin(ωt - tan⁻¹(ωτ))
```

**Frequency Response**:
- **Magnitude**: |H(jω)| = 1/√(1+(ωτ)²)
- **Phase**: ∠H(jω) = -tan⁻¹(ωτ)

**Characteristics**:
- Low frequencies (ω → 0): |H| → 1, phase → 0 (passes signal)
- High frequencies (ω → ∞): |H| → 0, phase → -90° (blocks signal)
- Cutoff frequency: ωc = 1/τ (|H| = 1/√2 ≈ 0.707)

### RLC Natural Response

**Underdamped** (ζ < 1):
```
vC(t) = e^(-ζω₀t)·[A·cos(ωdt) + B·sin(ωdt)]

where ωd = ω₀√(1-ζ²)
```

**Critically Damped** (ζ = 1):
```
vC(t) = e^(-ω₀t)·(A + B·t)
```

**Overdamped** (ζ > 1):
```
vC(t) = A·e^(s₁t) + B·e^(s₂t)

where s₁,₂ = -ζω₀ ± ω₀√(ζ²-1)
```

---

## Frequency Domain Analysis

### Transfer Function (RC)

```
H(s) = Vout(s)/Vin(s) = 1/(1 + sτ)
```

**Frequency Response**:
```
H(jω) = 1/(1 + jωτ)
```

**Bode Plot**:
- **Magnitude**: 20log₁₀(|H(jω)|) dB
- **Phase**: ∠H(jω) degrees or radians

**Corner Frequency**: fc = 1/(2πτ) Hz

### Transfer Function (RLC)

```
H(s) = Vout(s)/Vin(s) = 1/(LCs² + RCs + 1)
```

**Standard Form**:
```
H(s) = ω₀²/(s² + 2ζω₀s + ω₀²)
```

**Resonance** (underdamped):
- Resonant frequency: ωr = ω₀√(1-2ζ²) (if ζ < 1/√2)
- Quality factor: Q = 1/(2ζ) = ω₀L/R

---

## Practical Formulas for Exam

### Time Constants and Frequencies

```
RC Circuit:
  τ = RC
  fc = 1/(2πRC)

RLC Circuit:
  ω₀ = 1/√(LC)
  f₀ = 1/(2π√(LC))
  ζ = R/(2√(L/C))
  Q = 1/(2ζ) = √(L/C)/R
```

### Settling Time Estimates

```
RC: ts ≈ 5τ  (to within 1%)

RLC (underdamped): ts ≈ 4/(ζω₀)  (to within 2%)
```

### Peak Overshoot (RLC)

```
For step input (underdamped):
  Overshoot = e^(-πζ/√(1-ζ²)) × 100%
```

### Energy Relations

```
Capacitor: WC = ½CvC²
Inductor: WL = ½LiL²
Resistor: P = i²R = v²/R  (power dissipation)
```

---

## Common Circuit Approximations

### Small Time (t << τ)

For RC step response:
```
vC(t) ≈ vC0 + (A - vC0)·(t/τ)  (linear approximation)
```

### Large Time (t >> τ)

For RC step response:
```
vC(t) ≈ A  (reached steady-state)
```

### Low Frequency (ωτ << 1)

For RC sinusoid:
```
vC,ss(t) ≈ A·sin(ωt)  (passes through)
```

### High Frequency (ωτ >> 1)

For RC sinusoid:
```
vC,ss(t) ≈ (A/ωτ)·sin(ωt - 90°)  (attenuated and phase-shifted)
```

---

## References

**CENG 215 Lecture Notes**:
- Section 1: States and State Variables, General Series RLC
- Section 2: Series RC as First-Order Special Case
- Section 3: Euler's Forward Method for Simulation
- Section 4: Driven RC (Step, Ramp, Sinusoid)
- Section 7: Nonlinear RC Simulation with Quadratic i-v Device

**Key Equations Summary**:

```
RC:  dvC/dt = -(1/τ)vC + (1/τ)vs(t),  τ = RC

RLC: LC·d²vC/dt² + RC·dvC/dt + vC = vs(t)

Euler: xk+1 = xk + h·f(tk, xk, uk)

Stability (RC): 0 < h < 2τ

Accuracy (RC): h ≤ 0.05τ
```
