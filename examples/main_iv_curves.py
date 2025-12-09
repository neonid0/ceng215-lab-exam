"""
I-V CURVE CHARACTERIZATION

Visualize current-voltage characteristics for all components.
Useful for understanding component behavior and verifying models.

This plots I-V curves for:
  - X-Diode (piecewise)
  - Quadratic Device (i = kv²)
  - Resistor (linear)
  - Comparison between components
"""

import sys
from pathlib import Path

from analyzers.iv_curve_plotter import IVCurvePlotter
from components.quadratic_device import QuadraticDevice
from components.resistor import Resistor
from components.x_diode import XDiode

sys.path.append(str(Path(__file__).parent.parent))


def main():
    print("=" * 60)
    print("I-V CURVE CHARACTERIZATION")
    print("=" * 60)

    # Initialize plotter
    plotter = IVCurvePlotter(dark_mode=True)

    # ========================================
    # 1. X-DIODE CHARACTERISTIC
    # ========================================
    print("\n[1/4] X-Diode Characteristic...")
    diode = XDiode()

    print("      Plotting full I-V curve...")
    plotter.plot_component(
        component=diode,
        v_min=-4,
        v_max=6,
        num_points=1000,
        title="X-Diode I-V Characteristic (Exam Prep)",
    )

    print("      Plotting piecewise regions...")
    plotter.plot_piecewise_regions(
        component=diode,
        breakpoints=[0, 3],
        v_min=-4,
        v_max=6,
        title="X-Diode: Piecewise Regions (Breakpoints at 0V, 3V)",
    )

    # Print key points
    print("\n      Key Points on X-Diode Curve:")
    test_voltages = [-2, -1, 0, 1, 2, 3, 4, 5, 6]
    for v in test_voltages:
        i = diode.get_current(v)
        print(f"        vD = {v:>2}V  →  iD = {i*1000:>6.2f} mA")

    # ========================================
    # 2. QUADRATIC DEVICE CHARACTERISTIC
    # ========================================
    print("\n[2/4] Quadratic Device Characteristic...")
    quad_device = QuadraticDevice(k=0.01)

    plotter.plot_component(
        component=quad_device,
        v_min=-5,
        v_max=5,
        num_points=1000,
        title="Quadratic Device: i = 0.01v² (Lecture Section 7)",
    )

    print("\n      Key Points on Quadratic Curve:")
    test_voltages = [0, 1, 2, 3, 4, 5]
    for v in test_voltages:
        i = quad_device.current(v)
        print(
            f"        v = {v}V  →  i = {i*1000:>6.2f} mA  (i = 0.01*{v}² = {0.01*v**2*1000:.2f} mA)"
        )

    # ========================================
    # 3. LINEAR RESISTOR CHARACTERISTIC
    # ========================================
    print("\n[3/4] Linear Resistor Characteristic...")
    resistor = Resistor(resistance=1000.0)

    plotter.plot_component(
        component=resistor,
        v_min=-10,
        v_max=10,
        num_points=100,
        title="Resistor: i = v/R (R = 1kΩ, Linear)",
    )

    print("\n      Key Points on Resistor Curve:")
    test_voltages = [-10, -5, 0, 5, 10]
    for v in test_voltages:
        i = resistor.current(v)
        print(f"        v = {v:>3}V  →  i = {i*1000:>6.2f} mA  (Ohm's law)")

    # ========================================
    # 4. COMPONENT COMPARISON
    # ========================================
    print("\n[4/4] Comparing All Components...")

    # For fair comparison, scale resistor to match nonlinear components
    resistor_scaled = Resistor(resistance=500.0)

    components = [diode, quad_device, resistor_scaled]

    labels = ["X-Diode (piecewise)", "Quadratic (i=0.01v²)", "Resistor (500Ω)"]

    plotter.compare_components(
        components=components,
        labels=labels,
        v_min=0,
        v_max=6,
        num_points=1000,
        title="Component Comparison: Nonlinear vs Linear",
    )

    print("\n      Component Behavior Summary:")
    print("        X-Diode:    Three regions (reverse, linear, quadratic)")
    print("        Quadratic:  Symmetric parabola (always positive current)")
    print("        Resistor:   Straight line (Ohm's law)")

    # ========================================
    # ANALYSIS SUMMARY
    # ========================================
    print("\n" + "=" * 60)
    print("I-V CHARACTERIZATION COMPLETE")
    print("=" * 60)

    print("\nKey Observations:")
    print("  1. X-Diode has THREE distinct regions:")
    print("     - Reverse bias (v < 0): small linear conductance")
    print("     - Forward linear (0 ≤ v ≤ 3): larger conductance")
    print("     - Forward quadratic (v > 3): nonlinear increase")

    print("\n  2. Quadratic Device is SYMMETRIC:")
    print("     - Current increases with v² (parabola)")
    print("     - Same behavior for +v and -v")
    print("     - Always non-negative current")

    print("\n  3. Resistor is LINEAR:")
    print("     - Straight line through origin")
    print("     - Constant resistance at all voltages")
    print("     - Obeys Ohm's law: i = v/R")

    print("\n  4. Nonlinear devices create HARMONIC DISTORTION:")
    print("     - Input: pure sine wave")
    print("     - Output: distorted (not pure sine)")
    print("     - Important for circuit behavior")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
