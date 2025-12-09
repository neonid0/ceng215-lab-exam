"""
NONLINEAR RC CIRCUIT - QUADRATIC DEVICE

Circuit analysis with quadratic i-v device: i = k*v²
Based on CENG 215 Lecture Notes, Section 7.

Circuit:
    vs(t) = step or sinusoid
    Nonlinear device: i = k*v²
    C (capacitor)

State Equation:
    dvC/dt = (k/C) * (vs - vC)²

No closed-form analytical solution available.

Reference: Lecture Section 7
"""

import sys
from pathlib import Path

import numpy as np

from components.quadratic_device import QuadraticDevice
from plotter.generic_plotter import GenericPlotter
from solvers.nonlinear_rc_solver import NonlinearRCSolver

sys.path.append(str(Path(__file__).parent.parent))


def main():
    print("=" * 60)
    print("NONLINEAR RC CIRCUIT: QUADRATIC DEVICE")
    print("=" * 60)

    # Circuit parameters - MODIFY THESE FOR YOUR PROBLEM
    k = 0.01  # Device coefficient (A/V²)
    C = 1e-4  # Capacitance in Farads (100 µF)
    A = 5.0  # Step amplitude in Volts
    vC0 = 0.0  # Initial capacitor voltage in Volts
    t_end = 0.3  # Simulation time in seconds
    dt = 1e-5  # Timestep (SMALL for nonlinear stability!)

    print("\nCircuit Parameters:")
    print("  Device    = Quadratic (i = k*v²)")
    print(f"  k         = {k} A/V²")
    print(f"  C         = {C:.3e} F ({C*1e6:.1f} µF)")
    print(f"  Step A    = {A} V")
    print(f"  Initial   = {vC0} V")
    print(f"  Timestep  = {dt:.3e} s (SMALL for stability!)")
    print(f"  Duration  = {t_end} s")

    print("\nNonlinear Characteristics:")
    print(f"  At v=1V:  i = {k*1**2*1000:.2f} mA")
    print(f"  At v=2V:  i = {k*2**2*1000:.2f} mA (4× more)")
    print(f"  At v=5V:  i = {k*5**2*1000:.2f} mA (25× more)")

    # Initialize device
    print("\n[1/4] Initializing Quadratic Device...")
    device = QuadraticDevice(k=k)
    print(f"      ✓ Device: i(v) = {k}*v²")

    # Initialize solver
    print("[2/4] Initializing NonlinearRCSolver...")
    solver = NonlinearRCSolver(C, dt, device)
    print(f"      ✓ Solver configured with dt={dt:.2e}s")
    print("      ⚠  Nonlinear systems require small dt for stability")

    # Solve with step input
    print("[3/4] Running simulation (step input)...")
    t, vs, vC, i_dev = solver.solve_step(A=A, t_end=t_end, vC0=vC0)
    print(f"      ✓ Simulation complete ({len(t)} points)")

    # Statistics
    print("\n[4/4] Results:")
    print(f"  Initial vC        = {vC[0]:.3f} V")
    print(f"  Final vC          = {vC[-1]:.3f} V")
    print(f"  Step amplitude    = {A} V")
    print(f"  Settling progress = {(vC[-1]/A)*100:.1f}%")

    # Find time to reach 50%, 90%, 99% of final value
    def find_time(percent):
        target = A * percent / 100
        idx = np.argmin(np.abs(vC - target))
        return t[idx]

    t_50 = find_time(50)
    t_90 = find_time(90)
    t_99 = find_time(99)

    print("\nSettling Times:")
    print(f"  50% of A:  t = {t_50:.4f} s")
    print(f"  90% of A:  t = {t_90:.4f} s")
    print(f"  99% of A:  t = {t_99:.4f} s")

    print("\nNonlinear Behavior:")
    print("  Current decays as vC→A (slows down)")
    print("  NO exponential decay (unlike linear RC)")
    print("  Settling is SLOWER than linear case")

    # Plot
    print("\nGenerating plots...")
    plotter = GenericPlotter(dark_mode=True, figure_size=(14, 6))

    v_dev = vs - vC  # Voltage across device

    panels = [
        {
            "t": t,
            "signals": {"Source vs(t)": vs, "Capacitor vC(t)": vC},
            "title": "Voltage Response (Nonlinear)",
            "ylabel": "Voltage (V)",
        },
        {
            "t": t,
            "signals": {"Device current": i_dev * 1000},
            "title": "Device Current i(t)",
            "ylabel": "Current (mA)",
        },
        {
            "t": v_dev,
            "signals": {"Trajectory": i_dev * 1000},
            "title": "Phase Plane: i vs v_device",
            "xlabel": "Device Voltage (V)",
            "ylabel": "Device Current (mA)",
        },
    ]

    plotter.plot_multi_panel(
        panels, layout=(1, 3), main_title="Quadratic Device Circuit"
    )

    print("\n" + "=" * 60)
    print("QUADRATIC DEVICE SIMULATION COMPLETE")
    print("Key Insight: Nonlinear device causes non-exponential decay")
    print("=" * 60)


if __name__ == "__main__":
    main()
