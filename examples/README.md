# Example Programs - All Exam Scenarios

This directory contains complete, ready-to-run examples for every exam scenario.

---

## 📂 Files Overview

| File | Scenario | Lecture Section | Run Command |
|------|----------|-----------------|-------------|
| `main_exam_prep.py` | X-Diode RC Circuit | Exam Prep | `python main_exam_prep.py` |
| `main_linear_rc_step.py` | Linear RC + Step | Sections 2-4 | `python main_linear_rc_step.py` |
| `main_linear_rc_ramp.py` | Linear RC + Ramp | Section 4 | `python main_linear_rc_ramp.py` |
| `main_linear_rc_sine.py` | Linear RC + Sinusoid | Section 4 | `python main_linear_rc_sine.py` |
| `main_quadratic_device.py` | Nonlinear RC (i=kv²) | Section 7 | `python main_quadratic_device.py` |
| `main_rlc_circuit.py` | Series RLC (2nd order) | Section 1 | `python main_rlc_circuit.py` |
| `main_iv_curves.py` | Component Analysis | Analysis | `python main_iv_curves.py` |

---

## 🚀 Quick Start

### Run Any Example

```bash
cd examples/
python main_exam_prep.py
```

### Run All Examples

```bash
cd examples/
for file in main_*.py; do python "$file"; done
```

---

## 📝 How to Adapt for Your Exam Question

Each file has a section marked **"MODIFY THESE FOR YOUR PROBLEM"**:

### Example: Linear RC Step

```python
# Circuit parameters - MODIFY THESE FOR YOUR PROBLEM
R = 1000.0          # Your resistance value
C = 1e-4            # Your capacitance value
A = 5.0             # Your step amplitude
x0 = 0.0            # Your initial voltage
```

**Steps**:
1. Open the appropriate example file
2. Find the "MODIFY THESE" section
3. Change the values to match your problem
4. Run the file
5. Get your results!

---

## 🎯 Which Example Should I Use?

### Decision Tree

```
What's in your circuit?
├─ X-Diode (piecewise characteristic)
│  └─ Use: main_exam_prep.py
│
├─ Quadratic device (i = kv²)
│  └─ Use: main_quadratic_device.py
│
├─ Just R and C (linear)
│  ├─ Step input → main_linear_rc_step.py
│  ├─ Ramp input → main_linear_rc_ramp.py
│  └─ Sine input → main_linear_rc_sine.py
│
├─ R, L, and C (second-order)
│  └─ Use: main_rlc_circuit.py
│
└─ Need to understand component behavior
   └─ Use: main_iv_curves.py
```

---

## 📖 File Descriptions

### 1. main_exam_prep.py
**Exact exam preparation question implementation**
- Circuit: Vs(t) = 10sin(10t), X-diode, R=50kΩ, C=1µF
- Initial: Vo(0) = 3V
- Plots: Vs(t) and Vo(t)
- **Use this if**: Question asks for X-diode circuit

### 2. main_linear_rc_step.py
**Linear RC with step input**
- Includes analytical solution comparison
- Error analysis
- **Use this if**: Step input u(t) = A

### 3. main_linear_rc_ramp.py
**Linear RC with ramp input**
- Demonstrates time lag (τ)
- Analytical comparison
- **Use this if**: Ramp input u(t) = A*t

### 4. main_linear_rc_sine.py
**Linear RC with sinusoidal input**
- Frequency response analysis
- Magnitude and phase calculation
- **Use this if**: Sinusoid input u(t) = A*sin(ωt)

### 5. main_quadratic_device.py
**Nonlinear RC with quadratic device**
- Device: i = 0.01*v²
- Non-exponential decay
- Phase plane analysis
- **Use this if**: Nonlinear device i = k*v²

### 6. main_rlc_circuit.py
**Series RLC second-order circuit**
- Damping analysis (underdamped/critical/overdamped)
- Phase portrait
- Energy distribution
- **Use this if**: Circuit has R, L, AND C

### 7. main_iv_curves.py
**Component characterization**
- Plots I-V curves for all components
- Comparison visualization
- **Use this if**: Need to understand component behavior

---

## 💡 Example Modifications

### Change Circuit Values

```python
# Original
R = 1000.0
C = 1e-4

# For your problem: R=2.2kΩ, C=47µF
R = 2200.0
C = 47e-6
```

### Change Input Source

```python
# Original: 5V step
A = 5.0

# For your problem: 12V step
A = 12.0
```

### Change Initial Conditions

```python
# Original
x0 = 0.0

# For your problem: starts at 3V
x0 = 3.0
```

### Change Simulation Time

```python
# Original
t_end = 5 * tau

# For your problem: 2 seconds
t_end = 2.0
```

---

## 🔧 Troubleshooting

### Problem: "Simulation explodes" (values go to infinity)

**Solution**: Reduce timestep `dt`

```python
# If this fails:
dt = 0.002 * tau

# Try this:
dt = 0.0002 * tau  # 10× smaller
```

### Problem: "Results don't match expected"

**Check**:
1. Units (kΩ → Ω, µF → F, mA → A)
2. Initial conditions (x0, vC0, iL0)
3. Source parameters (amplitude, frequency)

### Problem: "Import errors"

**Solution**: Run from examples directory

```bash
cd examples/
python main_exam_prep.py
```

Or ensure parent directory is in path (already done in files).

---

## 📊 Output Interpretation

All examples print:
1. **Circuit parameters** - Your input values
2. **Simulation progress** - What's happening
3. **Results** - Key values and statistics
4. **Plots** - Visual output

### Reading the Output

```
Initial vC    = 0.000 V     ← Starting point
Final vC      = 4.997 V     ← Ending point (should approach input)
Max error     = 2.34e-04 V  ← Numerical accuracy
```

---

## 🎓 Exam Tips

1. **Before Exam**:
   - Run all examples once to see what they do
   - Practice modifying parameters
   - Understand which example maps to which question

2. **During Exam**:
   - Identify circuit type → choose example
   - Modify parameters → run
   - Verify output makes sense
   - Save plots

3. **Common Patterns**:
   - RC with diode → `main_exam_prep.py`
   - RC with R,C values given → `main_linear_rc_*.py`
   - RLC given → `main_rlc_circuit.py`
   - i=kv² mentioned → `main_quadratic_device.py`

---

## 📁 File Structure

```
examples/
├── README.md                    ← This file
├── main_exam_prep.py           ← Exam prep question
├── main_linear_rc_step.py      ← RC + step
├── main_linear_rc_ramp.py      ← RC + ramp
├── main_linear_rc_sine.py      ← RC + sine
├── main_quadratic_device.py    ← Nonlinear RC
├── main_rlc_circuit.py         ← RLC circuit
└── main_iv_curves.py           ← Component analysis
```

---

**All examples are fully documented, ready to run, and easy to modify!**

Happy simulating! 🚀
