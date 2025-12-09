"""
LINEAR RC CIRCUIT - STEP INPUT

Circuit analysis with step input and analytical comparison.
Based on CENG 215 Lecture Notes, Section 4.

Circuit:
    vs(t) = A (step input)
    R, C (linear components)

Analytic Solution:
    vC(t) = A + (vC0 - A)*exp(-t/τ)
    where τ = RC

Reference: Lecture Sections 2-4
"""

import sys
from pathlib import Path

import numpy as np

from plotter.generic_plotter import GenericPlotter
from solvers.rc_linear_solver import LinearRCSolver

sys.path.append(str(Path(__file__).parent.parent))


def main():
    print("=" * 60)
    print("LINEAR RC CIRCUIT: STEP INPUT")
    print("=" * 60)

    # Circuit parameters - MODIFY THESE FOR YOUR PROBLEM
    R = 1000.0  # Resistance in Ohms (1 kΩ)
    C = 1e-4  # Capacitance in Farads (100 µF)
    A = 5.0  # Step amplitude in Volts
    x0 = 0.0  # Initial capacitor voltage in Volts

    # Calculate time constant
    tau = R * C
    t_end = 5 * tau  # Simulate for 5 time constants
    dt = 0.002 * tau  # Timestep (0.2% of tau)

    print("\nCircuit Parameters:")
    print(f"  R         = {R:.1f} Ω ({R/1e3:.1f} kΩ)")
    print(f"  C         = {C:.3e} F ({C*1e6:.1f} µF)")
    print(f"  τ (tau)   = {tau:.3e} s ({tau*1e3:.2f} ms)")
    print(f"  Step A    = {A} V")
    print(f"  Initial   = {x0} V")
    print(f"  Timestep  = {dt:.3e} s")
    print(f"  Duration  = {t_end:.3e} s (5τ)")

    # Initialize solver
    print("\n[1/3] Initializing LinearRCSolver...")
    solver = LinearRCSolver(R, C, dt)
    print(f"      ✓ Solver ready (stability: dt={dt:.2e} < 2τ={2*tau:.2e})")

    # Solve with step input
    print("[2/3] Solving with step input...")
    t, u, x_num, x_ref = solver.solve_step(A=A, t_end=t_end, x0=x0)
    print(f"      ✓ Simulation complete ({len(t)} points)")

    # Calculate error
    error = np.abs(x_num - x_ref)
    max_error = np.max(error)
    mean_error = np.mean(error)

    print("\n[3/3] Results:")
    print(f"  Final value (numerical) = {x_num[-1]:.6f} V")
    print(f"  Final value (analytic)  = {x_ref[-1]:.6f} V")
    print(f"  Expected final value    = {A:.6f} V")
    print(f"  Maximum error           = {max_error:.3e} V")
    print(f"  Mean error              = {mean_error:.3e} V")

    # Key time points
    idx_tau = np.argmin(np.abs(t - tau))
    print(f"\nAt t=τ ({tau:.3e}s):")
    print(f"  vC(τ) = {x_num[idx_tau]:.3f} V")
    print(f"  Expected ≈ {A*(1-np.exp(-1)):.3f} V (63.2% of final)")

    # Plot
    print("\nGenerating plot...")
    plotter = GenericPlotter(dark_mode=True)
    plotter.plot_with_error(
        t,
        x_num,
        x_ref,
        input_signal=u,
        title=f"RC Step Response (τ={tau:.3e}s)",
        ylabel="Voltage (V)",
    )

    print("\n" + "=" * 60)
    print("STEP INPUT SIMULATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
