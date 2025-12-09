"""
Input Source Generators

Provides common input waveforms for circuit simulation.
Based on CENG 215 Lecture Notes, Section 4.
"""

from typing import Callable

import numpy as np


class StepSource:
    """
    Step input source: u(t) = A * u(t)

    Where u(t) is the unit step function:
        u(t) = 0 for t < 0
        u(t) = 1 for t ≥ 0

    Reference:
        CENG 215 Lecture Notes, Section 4: "Driven RC: From Model to Simulation"
    """

    def __init__(self, amplitude: float):
        """
        Initialize step source.

        Args:
            amplitude: Step amplitude A in Volts (or Amperes for current source)
        """
        self.A = amplitude

    def __call__(self, t: float) -> float:
        """
        Evaluate step source at time t.

        Args:
            t: Time in seconds

        Returns:
            Source value: 0 if t < 0, A if t ≥ 0
        """
        return self.A if t >= 0 else 0.0

    def vectorized(self, t: np.ndarray) -> np.ndarray:
        """
        Evaluate step source for array of time values.

        Args:
            t: Array of time values in seconds

        Returns:
            Array of source values
        """
        return self.A * np.ones_like(t)

    def __repr__(self) -> str:
        """String representation."""
        return f"StepSource(A={self.A} V)"


class RampSource:
    """
    Ramp input source: u(t) = A * t * u(t)

    Where u(t) is the unit step function.

    Analytic solution for RC circuit:
        x(t) = A(t - τ) + (x₀ + Aτ) * exp(-t/τ)

    Reference:
        CENG 215 Lecture Notes, Section 4
    """

    def __init__(self, slope: float):
        """
        Initialize ramp source.

        Args:
            slope: Ramp slope A in V/s (or A/s for current source)
        """
        self.A = slope

    def __call__(self, t: float) -> float:
        """
        Evaluate ramp source at time t.

        Args:
            t: Time in seconds

        Returns:
            Source value: 0 if t < 0, A*t if t ≥ 0
        """
        return self.A * t if t >= 0 else 0.0

    def vectorized(self, t: np.ndarray) -> np.ndarray:
        """
        Evaluate ramp source for array of time values.

        Args:
            t: Array of time values in seconds

        Returns:
            Array of source values
        """
        return self.A * np.maximum(t, 0.0)

    def __repr__(self) -> str:
        """String representation."""
        return f"RampSource(slope={self.A} V/s)"


class SinusoidSource:
    """
    Sinusoidal input source: u(t) = A * sin(ωt + φ)

    Steady-state solution for RC circuit:
        x_ss(t) = A/√(1+(ωτ)²) * sin(ωt - arctan(ωτ))

    Reference:
        CENG 215 Lecture Notes, Section 4
    """

    def __init__(self, amplitude: float, omega: float, phase: float = 0.0):
        """
        Initialize sinusoidal source.

        Args:
            amplitude: Amplitude A in Volts (or Amperes)
            omega: Angular frequency ω in rad/s
            phase: Phase angle φ in radians (default 0)
        """
        self.A = amplitude
        self.omega = omega
        self.phase = phase
        self.frequency_hz = omega / (2.0 * np.pi)

    def __call__(self, t: float) -> float:
        """
        Evaluate sinusoid at time t.

        Args:
            t: Time in seconds

        Returns:
            Source value: A * sin(ωt + φ)
        """
        return self.A * np.sin(self.omega * t + self.phase)

    def vectorized(self, t: np.ndarray) -> np.ndarray:
        """
        Evaluate sinusoid for array of time values.

        Args:
            t: Array of time values in seconds

        Returns:
            Array of source values
        """
        return self.A * np.sin(self.omega * t + self.phase)

    def period(self) -> float:
        """
        Get period of sinusoid.

        Returns:
            Period T = 2π/ω in seconds
        """
        return 2.0 * np.pi / self.omega

    def __repr__(self) -> str:
        """String representation."""
        return f"SinusoidSource(A={self.A} V, ω={self.omega} rad/s, φ={self.phase} rad)"


def create_source(source_type: str, **kwargs) -> Callable[[float], float]:
    """
    Factory function to create source from type string.

    Args:
        source_type: 'step', 'ramp', or 'sine'
        **kwargs: Parameters for the source

    Returns:
        Source function u(t)

    Examples:
        >>> step = create_source('step', amplitude=5.0)
        >>> ramp = create_source('ramp', slope=2.0)
        >>> sine = create_source('sine', amplitude=10.0, omega=50.0)
    """
    if source_type.lower() == 'step':
        return StepSource(**kwargs)
    elif source_type.lower() == 'ramp':
        return RampSource(**kwargs)
    elif source_type.lower() in ['sine', 'sinusoid']:
        return SinusoidSource(**kwargs)
    else:
        raise ValueError(f"Unknown source type: {source_type}")
