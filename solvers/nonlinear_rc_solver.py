"""
Nonlinear RC Circuit Solver

Solves RC circuits with nonlinear devices (e.g., quadratic i-v characteristic).
Based on CENG 215 Lecture Notes, Section 7.
"""

import sys
from pathlib import Path
from typing import (
    Callable,
    Tuple,
)

import numpy as np

from interfaces.non_linear_component import NonLinearComponent

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))


class NonlinearRCSolver:
    """
    First-order RC circuit solver with nonlinear device.

    Circuit Model:
        Series connection: vs(t) = vNL(t) + vC(t)

        where:
        - vs(t): Source voltage
        - vNL(t): Voltage across nonlinear device
        - vC(t): Capacitor voltage (state variable)

    Device Characteristic:
        i(vNL) = nonlinear function (e.g., i = 0.01*v²)

    State Equation:
        C*dvC/dt = i(vNL)

        Using vNL = vs - vC:
        dvC/dt = (1/C) * i(vs - vC)

    Reference:
        CENG 215 Lecture Notes, Section 7:
        "Nonlinear RC Simulation with a Quadratic i-v Device"

    Example:
        For quadratic device i = k*v²:
        dvC/dt = (k/C) * (vs - vC)²
    """

    def __init__(self, C: float, dt: float, device: NonLinearComponent):
        """
        Initialize nonlinear RC solver.

        Args:
            C: Capacitance in Farads
            dt: Time step in seconds
            device: Nonlinear device implementing NonLinearComponent interface

        Raises:
            ValueError: If parameters are invalid

        Note:
            Step size must be chosen carefully for nonlinear systems.
            Too large dt can cause numerical instability or blow-up.
            Recommended: Start with small dt (e.g., 1e-5) and verify stability.
        """
        if C <= 0:
            raise ValueError(f"Capacitance must be positive: C={C}")

        if dt <= 0:
            raise ValueError(f"Time step dt must be positive: dt={dt}")

        self.C = C
        self.dt = dt
        self.device = device

    def solve(
        self, source_func: Callable[[float], float], t_end: float, vC0: float = 0.0
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Solve nonlinear RC circuit with arbitrary input source.

        Args:
            source_func: Input voltage source vs(t), callable
            t_end: End time in seconds
            vC0: Initial capacitor voltage in Volts (default 0)

        Returns:
            Tuple of (time, source, vC, iDevice)
            - time: np.ndarray of time points
            - source: np.ndarray of source voltage values
            - vC: np.ndarray of capacitor voltage
            - iDevice: np.ndarray of device current

        Note:
            The state equation is:
            dvC/dt = (1/C) * i_device(vs - vC)
        """
        # Create time grid
        N = int(np.ceil(t_end / self.dt)) + 1
        t = np.linspace(0.0, t_end, N)

        # Initialize state
        vC = np.zeros(N)
        iDevice = np.zeros(N)
        vC[0] = vC0

        # Compute initial current
        vs0 = source_func(t[0])
        vNL0 = vs0 - vC[0]
        iDevice[0] = self.device.current(vNL0)

        # Euler integration
        for k in range(N - 1):
            vs = source_func(t[k])
            vNL = vs - vC[k]

            # Device current
            i_dev = self.device.current(vNL)
            iDevice[k] = i_dev

            # State equation: dvC/dt = (1/C) * i_device
            dvC_dt = (1.0 / self.C) * i_dev

            # Euler update
            vC[k + 1] = vC[k] + self.dt * dvC_dt

        # Compute final current
        vs_final = source_func(t[-1])
        vNL_final = vs_final - vC[-1]
        iDevice[-1] = self.device.current(vNL_final)

        # Evaluate source at all time points
        vs = np.array([source_func(tk) for tk in t])

        return t, vs, vC, iDevice

    def solve_step(
        self, A: float, t_end: float, vC0: float = 0.0
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Solve nonlinear RC circuit with step input: vs(t) = A * u(t)

        Args:
            A: Step amplitude in Volts
            t_end: End time in seconds
            vC0: Initial capacitor voltage in Volts (default 0)

        Returns:
            Tuple of (time, source, vC, iDevice)

        Note:
            For quadratic device i = k*v²:
            - vC(t) approaches A monotonically
            - No overshoot (unlike linear RC)
            - Approach is slower as vC → A (current → 0)
        """

        def source(t):
            return A

        return self.solve(source, t_end, vC0)

    def solve_sinusoid(
        self, A: float, omega: float, t_end: float, vC0: float = 0.0
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Solve nonlinear RC circuit with sinusoidal input: vs(t) = A * sin(ωt)

        Args:
            A: Sinusoid amplitude in Volts
            omega: Angular frequency ω in rad/s
            t_end: End time in seconds
            vC0: Initial capacitor voltage in Volts (default 0)

        Returns:
            Tuple of (time, source, vC, iDevice)

        Note:
            Nonlinear devices produce harmonic distortion.
            Output is NOT a pure sinusoid even with sinusoidal input.
        """

        def source(t):
            return A * np.sin(omega * t)

        return self.solve(source, t_end, vC0)

    def __repr__(self) -> str:
        """String representation of solver."""
        return (
            f"NonlinearRCSolver(C={self.C:.3e} F, dt={self.dt:.3e} s, "
            f"device={self.device})"
        )
