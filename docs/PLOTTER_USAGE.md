# Plotter Usage Guide

Complete guide for using the plotting utilities in circuit simulations.

---

## Available Plotters

### 1. CircuitPlotter (Simple)
**File**: `plotter/circuit_plotter.py`

**Use When**: Simple two-signal plot (source + output)

**Best For**: Exam prep question, basic RC/RLC plots

### 2. GenericPlotter (Flexible)
**File**: `plotter/generic_plotter.py`

**Use When**: Complex plots, multi-panel layouts, error analysis

**Best For**: Detailed analysis, comparisons, multi-variable plots

### 3. IVCurvePlotter (Component Analysis)
**File**: `analyzers/iv_curve_plotter.py`

**Use When**: Characterizing component I-V curves

**Best For**: Understanding device behavior

---

## GenericPlotter Usage

### Basic Import

```python
from plotter.generic_plotter import GenericPlotter

# Initialize
plotter = GenericPlotter(dark_mode=True)
```

---

## Use Cases

### 1. Simple Multi-Signal Plot

**When**: Plot input, output, and reference together

```python
from plotter.generic_plotter import GenericPlotter

plotter = GenericPlotter(dark_mode=True)

# After solving...
plotter.plot_signals(
    t,
    {
        'Input u(t)': input_signal,
        'Output x(t)': output,
        'Reference': analytical
    },
    title="RC Step Response",
    ylabel="Voltage (V)"
)
```

**Replaces**:
```python
# Instead of matplotlib directly:
plt.plot(t, input_signal, label='Input')
plt.plot(t, output, label='Output')
plt.legend()
plt.show()
```

---

### 2. Comparison with Error Analysis

**When**: Comparing numerical vs analytical with error plot

```python
plotter.plot_with_error(
    t,
    numerical=x_num,
    analytical=x_ref,
    input_signal=u,  # optional
    title="RC Step Response",
    ylabel="Voltage (V)"
)
```

**Creates**: Side-by-side plot with signals (left) and error (right)

---

### 3. Multi-Panel Layouts

**When**: Multiple related plots (e.g., voltage + current, or multiple state variables)

```python
# Define panels
panels = [
    {
        't': t,
        'signals': {'vC(t)': vC, 'vs(t)': vs},
        'title': 'Capacitor Voltage',
        'ylabel': 'Voltage (V)'
    },
    {
        't': t,
        'signals': {'iL(t)': iL * 1000},  # Convert to mA
        'title': 'Inductor Current',
        'ylabel': 'Current (mA)'
    },
    {
        't': t,
        'signals': {'Error': error},
        'title': 'Numerical Error',
        'ylabel': 'Error (V)',
        'type': 'semilogy'  # Log scale for error
    }
]

plotter.plot_multi_panel(
    panels,
    layout=(2, 2),  # 2 rows, 2 columns
    main_title="RLC Circuit Analysis"
)
```

---

### 4. Phase Portrait

**When**: Plotting state-space trajectory (e.g., vC vs iL)

```python
plotter.plot_phase_portrait(
    x=vC,
    y=iL * 1000,  # Convert to mA
    title="RLC Phase Portrait",
    xlabel="Capacitor Voltage (V)",
    ylabel="Inductor Current (mA)",
    mark_start_end=True
)
```

---

### 5. Frequency Response

**When**: Plotting Bode magnitude

```python
# Create frequency range
omega_range = np.logspace(-2, 2, 100) * cutoff_freq
H_mag = 1.0 / np.sqrt(1 + (omega_range * tau) ** 2)
magnitude_db = 20 * np.log10(H_mag)

plotter.plot_frequency_response(
    frequencies=omega_range,
    magnitude_db=magnitude_db,
    title="RC Frequency Response",
    mark_frequency=omega,  # Current frequency
    cutoff_frequency=1/tau  # Cutoff
)
```

---

## Complete Example: Linear RC with GenericPlotter

```python
from solvers.rc_linear_solver import LinearRCSolver
from plotter.generic_plotter import GenericPlotter
import numpy as np

# Solve
R, C = 1000.0, 1e-4
solver = LinearRCSolver(R, C, dt=0.002*R*C)
t, u, x_num, x_ref = solver.solve_step(A=5.0, t_end=0.5, x0=0.0)

# Initialize plotter
plotter = GenericPlotter(dark_mode=True)

# Method 1: Simple plot
plotter.plot_signals(
    t,
    {'Input': u, 'Output': x_num, 'Analytical': x_ref},
    title="RC Step Response"
)

# Method 2: With error analysis
plotter.plot_with_error(
    t,
    numerical=x_num,
    analytical=x_ref,
    input_signal=u,
    title="RC Step Response"
)

# Method 3: Multi-panel with details
tau = R * C
error = np.abs(x_num - x_ref)

panels = [
    {
        't': t,
        'signals': {'Input': u, 'Numerical': x_num, 'Analytical': x_ref},
        'title': 'Signals',
        'ylabel': 'Voltage (V)'
    },
    {
        't': t,
        'signals': {'Absolute Error': error},
        'title': 'Error',
        'ylabel': 'Error (V)',
        'type': 'semilogy'
    }
]

plotter.plot_multi_panel(
    panels,
    layout=(1, 2),
    main_title=f"RC Step Response (τ={tau:.3e}s)"
)
```

---

## Example: RLC with Multi-Panel

```python
from solvers.rlc_solver import RLCSolver
from sources.input_sources import StepSource
from plotter.generic_plotter import GenericPlotter

# Solve
R, L, C = 10.0, 0.01, 1e-4
solver = RLCSolver(R, L, C, dt=1e-5)
source = StepSource(amplitude=10.0)

t, vs, vC, iL = solver.solve(
    source_func=source,
    t_end=0.2,
    vC0=0.0,
    iL0=0.0
)

# Calculate energy
W_C = 0.5 * C * vC**2
W_L = 0.5 * L * iL**2
W_total = W_C + W_L

# Initialize plotter
plotter = GenericPlotter(dark_mode=True, figure_size=(14, 8))

# Create comprehensive multi-panel
panels = [
    {
        't': t,
        'signals': {'vC(t)': vC, 'vs(t)': vs},
        'title': 'Capacitor Voltage',
        'ylabel': 'Voltage (V)'
    },
    {
        't': t,
        'signals': {'iL(t)': iL * 1000},
        'title': 'Inductor Current',
        'ylabel': 'Current (mA)'
    },
    {
        't': t,
        'signals': {
            'Capacitor': W_C * 1000,
            'Inductor': W_L * 1000,
            'Total': W_total * 1000
        },
        'title': 'Energy Distribution',
        'ylabel': 'Energy (mJ)'
    },
    {
        # Phase portrait in panel 4
        'signals': {},  # Will add manually if needed
        'title': 'Phase Portrait',
        'xlabel': 'vC (V)',
        'ylabel': 'iL (mA)'
    }
]

plotter.plot_multi_panel(
    panels[:3],  # First 3 panels
    layout=(2, 2),
    main_title="RLC Circuit Complete Analysis"
)

# Separate phase portrait
plotter.plot_phase_portrait(
    x=vC,
    y=iL * 1000,
    xlabel="vC (V)",
    ylabel="iL (mA)",
    title="RLC Phase Portrait"
)
```

---

## Plot Type Options

In `plot_multi_panel`, specify `'type'` for each panel:

| Type | Description | Use Case |
|------|-------------|----------|
| `'line'` | Linear axes (default) | Normal signals |
| `'semilogy'` | Log Y-axis | Errors, decay |
| `'semilogx'` | Log X-axis | Frequency sweep |
| `'loglog'` | Log both axes | Power laws |

---

## Dark Mode vs Light Mode

```python
# Dark mode (default)
plotter = GenericPlotter(dark_mode=True)

# Light mode
plotter = GenericPlotter(dark_mode=False)
```

**Colors**:
- Dark mode: cyan (primary), lime (secondary), orange (tertiary)
- Light mode: blue (primary), green (secondary), red (tertiary)

---

## Saving Plots

All plot methods accept `save_path`:

```python
plotter.plot_signals(
    t, signals,
    title="RC Response",
    save_path="rc_response.png"
)
```

---

## Comparison: CircuitPlotter vs GenericPlotter

### Use CircuitPlotter When:
- ✅ Simple two-signal plot (source + output)
- ✅ Quick visualization
- ✅ Exam prep question format
- ✅ Standard format is fine

```python
from plotter.circuit_plotter import CircuitPlotter

plotter = CircuitPlotter(dark_mode=True)
plotter.plot(t, vs, vo, title="Circuit Response")
```

### Use GenericPlotter When:
- ✅ Multiple signals (3+)
- ✅ Error analysis needed
- ✅ Multi-panel layouts
- ✅ Phase portraits
- ✅ Frequency response
- ✅ Custom layouts

```python
from plotter.generic_plotter import GenericPlotter

plotter = GenericPlotter(dark_mode=True)
plotter.plot_signals(t, {'vs': vs, 'vo': vo, 'vref': vref})
```

---

## Quick Reference

| Task | Method | Example |
|------|--------|---------|
| Plot multiple signals | `plot_signals()` | `plotter.plot_signals(t, {'A': a, 'B': b})` |
| Compare with error | `plot_with_error()` | `plotter.plot_with_error(t, num, ref)` |
| Multi-panel layout | `plot_multi_panel()` | `plotter.plot_multi_panel(panels, (2,2))` |
| Phase portrait | `plot_phase_portrait()` | `plotter.plot_phase_portrait(x, y)` |
| Frequency response | `plot_frequency_response()` | `plotter.plot_frequency_response(f, mag)` |

---

## Tips

1. **Use GenericPlotter for exam**: More flexible, handles all cases
2. **Panel layouts**: (2, 2) for 4 plots, (2, 1) for 2 vertical, (1, 2) for 2 horizontal
3. **Log scale for errors**: Use `'type': 'semilogy'` for error panels
4. **Convert units**: mA = A * 1000, mJ = J * 1000, ms = s * 1000
5. **Save plots**: Always specify `save_path` for exam documentation

---

**GenericPlotter gives you maximum flexibility while keeping code clean!**
