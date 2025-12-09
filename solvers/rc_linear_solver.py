"""
Linear RC Circuit Solver

Solves first-order RC circuits with linear resistor and capacitor.
Supports step, ramp, and sinusoidal inputs with analytical reference solutions.

Based on CENG 215 Lecture Notes, Sections 2-4.
"""

from typing import (
    Callable,
    Optional,
    Tuple,
)

import numpy as np


class LinearRCSolver:
    """
    First-order RC circuit solver using Forward Euler method.

    Circuit Model:
        Series RC with voltage source vs(t)

        vs(t) = vR(t) + vC(t)
        i(t) = C * dvC/dt = vR/R

    State Equation:
        dvC/dt = -(1/τ) * vC + (1/τ) * vs(t)
        where τ = RC (time constant)

    Reference:
        CENG 215 Lecture Notes, Section 2: "Series RC as a First-Order Special Case"
    """

    def __init__(self, R: float, C: float, dt: float):
        """
        Initialize RC solver.

        Args:
            R: Resistance in Ohms
            C: Capacitance in Farads
            dt: Time step in seconds

        Raises:
            ValueError: If parameters are invalid or dt violates stability

        Stability Condition:
            For Forward Euler: 0 < dt < 2*τ
            Recommended: dt ≤ 0.05*τ for accuracy
        """
        if R <= 0 or C <= 0:
            raise ValueError(f"R and C must be positive: R={R}, C={C}")

        if dt <= 0:
            raise ValueError(f"Time step dt must be positive: dt={dt}")

        self.R = R
        self.C = C
        self.dt = dt
        self.tau = R * C  # Time constant

        # Check stability condition
        if dt >= 2.0 * self.tau:
            raise ValueError(
                f"Time step dt={dt} violates stability condition dt < 2*τ={2*self.tau}. "
                f"Recommended: dt ≤ {0.05*self.tau:.3e}"
            )

        # Warn if accuracy might be poor
        if dt > 0.05 * self.tau:
            import warnings

            warnings.warn(
                f"Time step dt={dt} is large (> 0.05*τ={0.05*self.tau:.3e}). "
                f"Consider reducing dt for better accuracy."
            )

    def solve(
        self,
        source_func: Callable[[float], float],
        t_end: float,
        v0: float = 0.0,
        analytic_func: Optional[Callable[[np.ndarray], np.ndarray]] = None,
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, Optional[np.ndarray]]:
        """
        Solve RC circuit with arbitrary input source.

        Args:
            source_func: Input voltage source vs(t), callable
            t_end: End time in seconds
            v0: Initial capacitor voltage in Volts (default 0)
            analytic_func: Optional analytic solution for comparison

        Returns:
            Tuple of (time, source, voltage_numerical, voltage_analytic)
            - time: np.ndarray of time points
            - source: np.ndarray of source voltage values
            - voltage_numerical: np.ndarray of capacitor voltage (numerical)
            - voltage_analytic: np.ndarray of analytic solution (or None)
        """
        # Create time grid
        N = int(np.ceil(t_end / self.dt)) + 1
        t = np.linspace(0.0, t_end, N)

        # Initialize state
        x = np.zeros(N)
        x[0] = v0

        # Euler integration
        for k in range(N - 1):
            u = source_func(t[k])
            # State equation: dx/dt = -(1/tau)*x + (1/tau)*u
            f = -(1.0 / self.tau) * x[k] + (1.0 / self.tau) * u
            x[k + 1] = x[k] + self.dt * f

        # Evaluate source at all time points
        u = np.array([source_func(tk) for tk in t])

        # Compute analytic solution if provided
        x_ref = analytic_func(t) if analytic_func is not None else None

        return t, u, x, x_ref

    def solve_step(
        self, A: float, t_end: float, x0: float = 0.0
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Solve RC circuit with step input: vs(t) = A * u(t)

        Analytic Solution:
            vC(t) = A + (x0 - A) * exp(-t/τ)

        Args:
            A: Step amplitude in Volts
            t_end: End time in seconds
            x0: Initial capacitor voltage in Volts (default 0)

        Returns:
            Tuple of (time, source, voltage_numerical, voltage_analytic)

        Reference:
            CENG 215 Lecture Notes, Section 4.1
        """

        def source(t):
            return A

        def analytic(t):
            return A + (x0 - A) * np.exp(-t / self.tau)

        return self.solve(source, t_end, x0, analytic)

    def solve_ramp(
        self, A: float, t_end: float, x0: float = 0.0
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Solve RC circuit with ramp input: vs(t) = A * t * u(t)

        Analytic Solution:
            vC(t) = A(t - τ) + (x0 + Aτ) * exp(-t/τ)

        Args:
            A: Ramp slope in V/s
            t_end: End time in seconds
            x0: Initial capacitor voltage in Volts (default 0)

        Returns:
            Tuple of (time, source, voltage_numerical, voltage_analytic)

        Reference:
            CENG 215 Lecture Notes, Section 4.1
        """

        def source(t):
            return A * t

        def analytic(t):
            return A * (t - self.tau) + (x0 + A * self.tau) * np.exp(-t / self.tau)

        return self.solve(source, t_end, x0, analytic)

    def solve_sinusoid(
        self,
        A: float,
        omega: float,
        t_end: float,
        x0: float = 0.0,
        steady_state_only: bool = True,
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, Optional[np.ndarray]]:
        """
        Solve RC circuit with sinusoidal input: vs(t) = A * sin(ωt)

        Steady-State Analytic Solution:
            vC_ss(t) = A/√(1+(ωτ)²) * sin(ωt - arctan(ωτ))

        Args:
            A: Sinusoid amplitude in Volts
            omega: Angular frequency ω in rad/s
            t_end: End time in seconds
            x0: Initial capacitor voltage in Volts (default 0)
            steady_state_only: If True, return steady-state solution (default)

        Returns:
            Tuple of (time, source, voltage_numerical, voltage_analytic)

        Note:
            The analytic solution is the steady-state response only.
            Transient effects are not included in the reference.

        Reference:
            CENG 215 Lecture Notes, Section 4.1
        """

        def source(t):
            return A * np.sin(omega * t)

        def analytic_ss(t):
            magnitude = A / np.sqrt(1 + (omega * self.tau) ** 2)
            phase_shift = np.arctan(omega * self.tau)
            return magnitude * np.sin(omega * t - phase_shift)

        return self.solve(source, t_end, x0, analytic_ss if steady_state_only else None)

    def get_time_constant(self) -> float:
        """Get circuit time constant τ = RC in seconds."""
        return self.tau

    def __repr__(self) -> str:
        """String representation of solver."""
        return (
            f"LinearRCSolver(R={self.R:.3e} Ω, C={self.C:.3e} F, "
            f"τ={self.tau:.3e} s, dt={self.dt:.3e} s)"
        )
