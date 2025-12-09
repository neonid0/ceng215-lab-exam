"""
LINEAR RC CIRCUIT - SINUSOIDAL INPUT

Circuit analysis with sinusoidal input and analytical comparison.
Based on CENG 215 Lecture Notes, Section 4.

Circuit:
    vs(t) = A*sin(ωt)
    R, C (linear components)

Steady-State Analytic Solution:
    vC_ss(t) = A/√(1+(ωτ)²) * sin(ωt - arctan(ωτ))
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
    print("LINEAR RC CIRCUIT: SINUSOIDAL INPUT")
    print("=" * 60)

    # Circuit parameters - MODIFY THESE FOR YOUR PROBLEM
    R = 1000.0  # Resistance in Ohms (1 kΩ)
    C = 1e-4  # Capacitance in Farads (100 µF)
    A = 10.0  # Sinusoid amplitude in Volts
    omega = 50.0  # Angular frequency in rad/s
    x0 = 0.0  # Initial capacitor voltage in Volts

    # Calculate time constant and frequency response
    tau = R * C
    period = 2 * np.pi / omega
    t_end = 10 * period  # Simulate for 10 periods
    dt = period / 100  # 100 points per period

    # Frequency response
    magnitude = 1.0 / np.sqrt(1 + (omega * tau) ** 2)
    phase_shift = -np.arctan(omega * tau)
    cutoff_freq = 1.0 / tau

    print("\nCircuit Parameters:")
    print(f"  R         = {R:.1f} Ω ({R/1e3:.1f} kΩ)")
    print(f"  C         = {C:.3e} F ({C*1e6:.1f} µF)")
    print(f"  τ (tau)   = {tau:.3e} s")
    print(f"  ωc        = {cutoff_freq:.2f} rad/s (cutoff)")

    print("\nInput Signal:")
    print(f"  Amplitude = {A} V")
    print(f"  ω         = {omega} rad/s")
    print(f"  f         = {omega/(2*np.pi):.2f} Hz")
    print(f"  Period    = {period:.4f} s")

    print("\nFrequency Response:")
    print(f"  |H(jω)|   = {magnitude:.4f} (attenuation)")
    print(f"  ∠H(jω)    = {np.degrees(phase_shift):.2f}° (phase lag)")
    print(f"  ωτ        = {omega*tau:.4f}")

    # Initialize solver
    print("\n[1/3] Initializing LinearRCSolver...")
    solver = LinearRCSolver(R, C, dt)
    print("      ✓ Solver ready")

    # Solve with sinusoidal input
    print("[2/3] Solving with sinusoidal input...")
    t, u, x_num, x_ref = solver.solve_sinusoid(
        A=A, omega=omega, t_end=t_end, x0=x0, steady_state_only=True
    )
    print(f"      ✓ Simulation complete ({len(t)} points)")

    # Find steady-state (after 5 time constants)
    idx_ss = np.argmin(np.abs(t - 5 * tau))
    t_ss = t[idx_ss:]
    x_ss = x_num[idx_ss:]
    x_ref_ss = x_ref[idx_ss:]

    # Calculate steady-state error
    error_ss = np.abs(x_ss - x_ref_ss)
    max_error = np.max(error_ss)
    mean_error = np.mean(error_ss)

    print("\n[3/3] Results:")
    print(f"  Input amplitude         = {A:.3f} V")
    print(f"  Output amplitude (meas) ≈ {(x_ss.max() - x_ss.min())/2:.3f} V")
    print(f"  Output amplitude (pred) = {A * magnitude:.3f} V")
    print(
        f"  Attenuation             = {magnitude:.4f} ({20*np.log10(magnitude):.2f} dB)"
    )
    print(f"  Phase lag               = {np.degrees(phase_shift):.2f}°")
    print(f"  Max error (steady-state)= {max_error:.3e} V")
    print(f"  Mean error (steady-state)= {mean_error:.3e} V")

    # Plot
    print("\nGenerating plots...")
    plotter = GenericPlotter(dark_mode=True, figure_size=(14, 8))

    # Prepare data for multi-panel plot
    t_detail = t[-200:]
    u_detail = u[-200:]
    x_detail = x_num[-200:]
    x_ref_detail = x_ref[-200:]

    omega_range = np.logspace(-2, 2, 100) * cutoff_freq
    H_mag = 1.0 / np.sqrt(1 + (omega_range * tau) ** 2)
    H_mag_db = 20 * np.log10(H_mag)

    panels = [
        {
            "t": t,
            "signals": {
                "Input u(t)": u,
                "Output x(t) (numerical)": x_num,
                "Steady-state (analytic)": x_ref,
            },
            "title": "Full Response (Transient + Steady-State)",
            "ylabel": "Voltage (V)",
        },
        {
            "t": t_detail,
            "signals": {
                "Input": u_detail,
                "Output (numerical)": x_detail,
                "Output (analytic)": x_ref_detail,
            },
            "title": "Steady-State Detail (Last 2 Periods)",
            "ylabel": "Voltage (V)",
        },
        {
            "t": t,
            "signals": {"Error": np.abs(x_num - x_ref) + 1e-15},
            "title": "Numerical Error",
            "ylabel": "Absolute Error (V)",
            "type": "semilogy",
        },
        {
            "t": omega_range,
            "signals": {"Magnitude": H_mag_db},
            "title": "Frequency Response |H(jω)|",
            "xlabel": "Frequency (rad/s)",
            "ylabel": "Magnitude (dB)",
            "type": "semilogx",
        },
    ]

    plotter.plot_multi_panel(panels, layout=(2, 2), main_title="RC Sinusoidal Response")

    print("\n" + "=" * 60)
    print("SINUSOIDAL INPUT SIMULATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
