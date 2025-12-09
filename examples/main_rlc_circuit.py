"""
SERIES RLC CIRCUIT - SECOND-ORDER SYSTEM

Circuit analysis with R, L, C in series.
Based on CENG 215 Lecture Notes, Section 1.

Circuit:
    vs(t) = input (step, sine, etc.)
    R, L, C in series

State Variables:
    x₁ = vC (capacitor voltage)
    x₂ = iL (inductor current)

Second-Order ODE:
    LC*d²vC/dt² + RC*dvC/dt + vC = vs(t)

Natural Frequency: ω₀ = 1/√(LC)
Damping Ratio: ζ = R/(2√(L/C))

Reference: Lecture Section 1
"""

import sys
from pathlib import Path

import numpy as np

from plotter.generic_plotter import GenericPlotter
from solvers.rlc_solver import RLCSolver
from sources.input_sources import (
    SinusoidSource,
    StepSource,
)

sys.path.append(str(Path(__file__).parent.parent))


def main():
    print("=" * 60)
    print("SERIES RLC CIRCUIT: SECOND-ORDER SYSTEM")
    print("=" * 60)

    # Circuit parameters - MODIFY THESE FOR YOUR PROBLEM
    # Try different R values to see underdamped/critically/overdamped
    R = 10.0  # Resistance in Ohms
    L = 0.01  # Inductance in Henries (10 mH)
    C = 1e-4  # Capacitance in Farads (100 µF)

    # Initial conditions
    vC0 = 0.0  # Initial capacitor voltage in Volts
    iL0 = 0.0  # Initial inductor current in Amperes

    # Simulation parameters
    t_end = 0.2  # Simulation time in seconds
    dt = 1e-5  # Timestep

    print("\nCircuit Parameters:")
    print(f"  R         = {R:.1f} Ω")
    print(f"  L         = {L:.3e} H ({L*1e3:.1f} mH)")
    print(f"  C         = {C:.3e} F ({C*1e6:.1f} µF)")
    print(f"  Initial vC= {vC0} V")
    print(f"  Initial iL= {iL0} A")

    # Initialize solver
    print("\n[1/4] Initializing RLCSolver...")
    solver = RLCSolver(R, L, C, dt)

    # Get circuit parameters
    params = solver.get_circuit_params()

    print("\n[2/4] Circuit Characteristics:")
    print(f"  Natural frequency ω₀ = {params['omega_0']:.2f} rad/s")
    print(f"  Natural frequency f₀ = {params['f_0']:.2f} Hz")
    print(f"  Natural period    T₀ = {params['T_0']:.4f} s")
    print(f"  Damping ratio     ζ  = {params['zeta']:.4f}")
    print(f"  Damping type         = {params['damping_type'].upper()}")

    if 'omega_d' in params:
        print(f"  Damped frequency  ωd = {params['omega_d']:.2f} rad/s")
        print(f"  Damped frequency  fd = {params['f_d']:.2f} Hz")

    # Damping interpretation
    zeta = params['zeta']
    if zeta < 1:
        print("\n  → UNDERDAMPED: Oscillatory response with overshoot")
        print("    Overshoot ≈ {np.exp(-np.pi*zeta/np.sqrt(1-zeta**2))*100:.1f}%")
    elif zeta == 1:
        print("\n  → CRITICALLY DAMPED: Fastest response without overshoot")
    else:
        print("\n  → OVERDAMPED: Slow response, no oscillation")

    # Choose input based on damping
    if zeta < 1:
        # Underdamped: use step to see oscillations
        print("\n[3/4] Solving with STEP input (to see oscillations)...")
        source = StepSource(amplitude=10.0)
        source_name = "Step (10V)"
    else:
        # Overdamped: use sinusoid
        print("\n[3/4] Solving with SINUSOIDAL input...")
        source = SinusoidSource(amplitude=10.0, omega=params['omega_0'])
        source_name = "Sine (10V @ ω₀)"

    # Solve
    t, vs, vC, iL = solver.solve(source_func=source, t_end=t_end, vC0=vC0, iL0=iL0)
    print(f"      ✓ Simulation complete ({len(t)} points)")

    # Statistics
    print("\n[4/4] Results:")
    print(f"  Max vC      = {vC.max():.3f} V")
    print(f"  Min vC      = {vC.min():.3f} V")
    print(f"  Max iL      = {iL.max()*1000:.3f} mA")
    print(f"  Min iL      = {iL.min()*1000:.3f} mA")

    # Energy analysis
    W_C = 0.5 * C * vC**2
    W_L = 0.5 * L * iL**2
    W_total = W_C + W_L

    print(f"\n  Initial energy = {W_total[0]:.3e} J")
    print(f"  Final energy   = {W_total[-1]:.3e} J")
    print(f"  Energy lost    = {W_total[0] - W_total[-1]:.3e} J (dissipated in R)")

    # Plot
    print("\nGenerating plots...")
    plotter = GenericPlotter(dark_mode=True, figure_size=(14, 10))

    t_detail_end = min(5 * params["T_0"], t_end)
    idx_detail = np.where(t <= t_detail_end)[0]

    panels = [
        {
            "t": t,
            "signals": {"Source vs(t)": vs, "Capacitor vC(t)": vC},
            "title": f"Capacitor Voltage (Source: {source_name})",
            "ylabel": "Voltage (V)",
        },
        {
            "t": t,
            "signals": {"Inductor iL(t)": iL * 1000},
            "title": "Inductor Current",
            "ylabel": "Current (mA)",
        },
        {
            "t": vC,
            "signals": {"Trajectory": iL * 1000},
            "title": "Phase Portrait",
            "xlabel": "Capacitor Voltage (V)",
            "ylabel": "Inductor Current (mA)",
        },
        {
            "t": t,
            "signals": {
                "Capacitor energy": W_C * 1e3,
                "Inductor energy": W_L * 1e3,
                "Total energy": W_total * 1e3,
            },
            "title": "Energy Distribution",
            "ylabel": "Energy (mJ)",
        },
        {
            "t": t[idx_detail],
            "signals": {"vC(t)": vC[idx_detail]},
            "title": "Early Time Detail (First Few Cycles)",
            "ylabel": "Voltage (V)",
        },
    ]

    plotter.plot_multi_panel(
        panels,
        layout=(3, 2),
        main_title=f"RLC Circuit - {params['damping_type'].upper()}",
    )

    print("\n" + "=" * 60)
    print("RLC SIMULATION COMPLETE")
    print(f"Damping Type: {params['damping_type'].upper()}")
    print("=" * 60)


if __name__ == "__main__":
    main()
