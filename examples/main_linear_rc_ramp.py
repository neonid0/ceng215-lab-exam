"""
LINEAR RC CIRCUIT - RAMP INPUT

Circuit analysis with ramp input and analytical comparison.
Based on CENG 215 Lecture Notes, Section 4.

Circuit:
    vs(t) = A*t (ramp input)
    R, C (linear components)

Analytic Solution:
    vC(t) = A(t - τ) + (vC0 + Aτ)*exp(-t/τ)
    where τ = RC

Reference: Lecture Section 4
"""

import sys
from pathlib import Path

import numpy as np

from plotter.generic_plotter import GenericPlotter
from solvers.rc_linear_solver import LinearRCSolver

sys.path.append(str(Path(__file__).parent.parent))


def main():
    print("=" * 60)
    print("LINEAR RC CIRCUIT: RAMP INPUT")
    print("=" * 60)

    # Circuit parameters - MODIFY THESE FOR YOUR PROBLEM
    R = 1000.0  # Resistance in Ohms (1 kΩ)
    C = 1e-4  # Capacitance in Farads (100 µF)
    A = 2.0  # Ramp slope in V/s
    x0 = 0.0  # Initial capacitor voltage in Volts

    # Calculate time constant
    tau = R * C
    t_end = 5 * tau  # Simulate for 5 time constants
    dt = 0.002 * tau  # Timestep (0.2% of tau)

    print("\nCircuit Parameters:")
    print(f"  R         = {R:.1f} Ω ({R/1e3:.1f} kΩ)")
    print(f"  C         = {C:.3e} F ({C*1e6:.1f} µF)")
    print(f"  τ (tau)   = {tau:.3e} s ({tau*1e3:.2f} ms)")
    print(f"  Ramp A    = {A} V/s")
    print(f"  Initial   = {x0} V")
    print(f"  Timestep  = {dt:.3e} s")
    print(f"  Duration  = {t_end:.3e} s (5τ)")

    # Initialize solver
    print("\n[1/3] Initializing LinearRCSolver...")
    solver = LinearRCSolver(R, C, dt)
    print("      ✓ Solver ready")

    # Solve with ramp input
    print("[2/3] Solving with ramp input...")
    t, u, x_num, x_ref = solver.solve_ramp(A=A, t_end=t_end, x0=x0)
    print(f"      ✓ Simulation complete ({len(t)} points)")

    # Calculate error
    error = np.abs(x_num - x_ref)
    max_error = np.max(error)
    mean_error = np.mean(error)

    print("\n[3/3] Results:")
    print(f"  Final value (numerical) = {x_num[-1]:.6f} V")
    print(f"  Final value (analytic)  = {x_ref[-1]:.6f} V")
    print(f"  Input at end            = {u[-1]:.6f} V")
    print(f"  Time lag                ≈ {tau:.3e} s (τ)")
    print(f"  Maximum error           = {max_error:.3e} V")
    print(f"  Mean error              = {mean_error:.3e} V")

    # Steady-state check (after transient dies out)
    idx_5tau = np.argmin(np.abs(t - 5 * tau))
    ss_lag = u[idx_5tau] - x_num[idx_5tau]
    print("\nSteady-State Analysis:")
    print(f"  At t=5τ, input leads output by {ss_lag:.3f} V")
    print(f"  Expected lag: A*τ = {A*tau:.3f} V")

    # Plot
    print("\nGenerating plot...")
    plotter = GenericPlotter(dark_mode=True)
    plotter.plot_with_error(
        t,
        x_num,
        x_ref,
        input_signal=u,
        title=f"RC Ramp Response (slope={A} V/s, τ={tau:.3e}s)",
        ylabel="Voltage (V)",
    )

    print("\n" + "=" * 60)
    print("RAMP INPUT SIMULATION COMPLETE")
    print("Note: Output lags input by τ in steady-state")
    print("=" * 60)


if __name__ == "__main__":
    main()
