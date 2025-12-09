"""
EXAM PREP QUESTION - X-Diode RC Circuit

This is the EXACT exam preparation question implementation.

Circuit:
    Vs(t) = 10*sin(10*t)
    X-diode (piecewise characteristic)
    R = 50 kΩ
    C = 1 µF
    Initial: Vo(0) = 3V

Reference: Project #1 - Preparation Question
"""

import sys
from pathlib import Path

from components.x_diode import XDiode
from plotter.generic_plotter import GenericPlotter
from solvers.rc_diode_solver import RC_Diode_Solver

sys.path.append(str(Path(__file__).parent.parent))


def main():
    print("=" * 60)
    print("EXAM PREP QUESTION: X-Diode RC Circuit")
    print("=" * 60)

    # Circuit parameters (EXACT from exam prep)
    R_LOAD = 50e3  # 50 kΩ
    C_FILTER = 1e-6  # 1 µF
    V_INIT = 3.0  # Initial voltage: 3V
    T_END = 2.0  # Simulation time: 2 seconds
    DT = 0.0001  # Timestep: 0.1 ms

    print("\nCircuit Parameters:")
    print(f"  R_LOAD    = {R_LOAD/1e3:.1f} kΩ")
    print(f"  C_FILTER  = {C_FILTER*1e6:.1f} µF")
    print(f"  V_INIT    = {V_INIT} V")
    print("  Source    = 10*sin(10*t) V")
    print(f"  Timestep  = {DT*1e3:.2f} ms")
    print(f"  Duration  = {T_END} s")

    # Initialize X-diode
    print("\n[1/4] Initializing X-diode...")
    diode = XDiode()
    print("      ✓ X-diode created (piecewise characteristic)")

    # Initialize solver
    print("[2/4] Initializing RC_Diode_Solver...")
    solver = RC_Diode_Solver(r_load=R_LOAD, c_filter=C_FILTER, dt=DT, diode=diode)
    print("      ✓ Solver configured")

    # Solve
    print("[3/4] Running simulation...")
    t, vs, vo = solver.simulate(t_end=T_END, initial_voltage=V_INIT)
    print(f"      ✓ Simulation complete ({len(t)} points)")

    # Print statistics
    print("\n[4/4] Results:")
    print(f"  Initial Vo    = {vo[0]:.3f} V")
    print(f"  Final Vo      = {vo[-1]:.3f} V")
    print(f"  Max Vo        = {vo.max():.3f} V")
    print(f"  Min Vo        = {vo.min():.3f} V")
    print(f"  Vs amplitude  = {vs.max():.3f} V")

    # Plot
    print("\nGenerating plot...")
    plotter = GenericPlotter(dark_mode=True)
    plotter.plot_signals(
        t,
        {"Vs(t) Source": vs, "Vo(t) Output": vo},
        title="EXAM PREP: X-Diode RC Circuit (Vs=10sin(10t), R=50kΩ, C=1µF)",
        ylabel="Voltage (V)",
    )

    print("\n" + "=" * 60)
    print("EXAM PREP SIMULATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
