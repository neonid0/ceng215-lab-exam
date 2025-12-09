"""
Series RLC Circuit Solver

Solves second-order RLC circuits using state-space formulation.
Based on CENG 215 Lecture Notes, Section 1.
"""

from typing import (
    Callable,
    Tuple,
)

import numpy as np


class RLCSolver:
    """
    Second-order series RLC circuit solver using Forward Euler method.

    Circuit Model:
        Series R-L-C with voltage source vs(t)

        vs(t) = vR + vL + vC
              = R*i + L*di/dt + vC
        i = C*dvC/dt

    Second-Order ODE:
        LC*d²vC/dt² + RC*dvC/dt + vC = vs(t)

    State-Space Form:
        State vector: x = [vC, iL]ᵀ

        dx₁/dt = (1/C) * x₂
        dx₂/dt = (1/L) * (-R*x₂ - x₁ + vs(t))

    Or in matrix form:
        dx/dt = Ax + Bu

        where A = [    0      1/C  ]    B = [ 0  ]
                  [ -1/L    -R/L  ]        [1/L ]

    Reference:
        CENG 215 Lecture Notes, Section 1: "General Series RLC (output vC)"
    """

    def __init__(self, R: float, L: float, C: float, dt: float):
        """
        Initialize RLC solver.

        Args:
            R: Resistance in Ohms
            L: Inductance in Henries
            C: Capacitance in Farads
            dt: Time step in seconds

        Raises:
            ValueError: If parameters are invalid

        Note:
            For RLC circuits, dt should be chosen carefully based on:
            - Natural frequency: ω₀ = 1/√(LC)
            - Damping ratio: ζ = R/(2√(L/C))
            Recommended: dt ≤ T₀/50 where T₀ = 2π/ω₀
        """
        if R <= 0 or L <= 0 or C <= 0:
            raise ValueError(f"R, L, C must be positive: R={R}, L={L}, C={C}")

        if dt <= 0:
            raise ValueError(f"Time step dt must be positive: dt={dt}")

        self.R = R
        self.L = L
        self.C = C
        self.dt = dt

        # Calculate circuit parameters
        self.omega_0 = 1.0 / np.sqrt(L * C)  # Natural frequency (rad/s)
        self.zeta = (R / 2.0) * np.sqrt(C / L)  # Damping ratio
        self.T_0 = 2.0 * np.pi / self.omega_0  # Natural period

        # Check if dt is reasonable
        if dt > self.T_0 / 20:
            import warnings

            warnings.warn(
                f"Time step dt={dt:.3e} may be too large. "
                f"Natural period T₀={self.T_0:.3e}. "
                f"Recommended: dt ≤ {self.T_0/50:.3e}"
            )

        # Damping classification
        if self.zeta < 1.0:
            self.damping_type = "underdamped"
            self.omega_d = self.omega_0 * np.sqrt(1 - self.zeta**2)  # Damped frequency
        elif self.zeta == 1.0:
            self.damping_type = "critically damped"
            self.omega_d = None
        else:
            self.damping_type = "overdamped"
            self.omega_d = None

    def solve(
        self,
        source_func: Callable[[float], float],
        t_end: float,
        vC0: float = 0.0,
        iL0: float = 0.0,
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Solve RLC circuit with arbitrary input source.

        Args:
            source_func: Input voltage source vs(t), callable
            t_end: End time in seconds
            vC0: Initial capacitor voltage in Volts (default 0)
            iL0: Initial inductor current in Amperes (default 0)

        Returns:
            Tuple of (time, source, vC, iL)
            - time: np.ndarray of time points
            - source: np.ndarray of source voltage values
            - vC: np.ndarray of capacitor voltage
            - iL: np.ndarray of inductor current
        """
        # Create time grid
        N = int(np.ceil(t_end / self.dt)) + 1
        t = np.linspace(0.0, t_end, N)

        # Initialize state vectors
        vC = np.zeros(N)
        iL = np.zeros(N)
        vC[0] = vC0
        iL[0] = iL0

        # Euler integration
        for k in range(N - 1):
            vs = source_func(t[k])

            # State equations:
            # dvC/dt = (1/C) * iL
            # diL/dt = (1/L) * (-R*iL - vC + vs)
            dvC_dt = (1.0 / self.C) * iL[k]
            diL_dt = (1.0 / self.L) * (-self.R * iL[k] - vC[k] + vs)

            # Euler update
            vC[k + 1] = vC[k] + self.dt * dvC_dt
            iL[k + 1] = iL[k] + self.dt * diL_dt

        # Evaluate source at all time points
        vs = np.array([source_func(tk) for tk in t])

        return t, vs, vC, iL

    def get_circuit_params(self) -> dict:
        """
        Get circuit parameters and characteristics.

        Returns:
            Dictionary with circuit parameters:
            - omega_0: Natural frequency (rad/s)
            - f_0: Natural frequency (Hz)
            - T_0: Natural period (s)
            - zeta: Damping ratio
            - damping_type: 'underdamped', 'critically damped', or 'overdamped'
            - omega_d: Damped frequency (rad/s, if underdamped)
        """
        params = {
            'omega_0': self.omega_0,
            'f_0': self.omega_0 / (2.0 * np.pi),
            'T_0': self.T_0,
            'zeta': self.zeta,
            'damping_type': self.damping_type,
        }

        if self.omega_d is not None:
            params['omega_d'] = self.omega_d
            params['f_d'] = self.omega_d / (2.0 * np.pi)

        return params

    def __repr__(self) -> str:
        """String representation of solver."""
        return (
            f"RLCSolver(R={self.R:.3e} Ω, L={self.L:.3e} H, C={self.C:.3e} F, "
            f"dt={self.dt:.3e} s, {self.damping_type}, ζ={self.zeta:.3f})"
        )
