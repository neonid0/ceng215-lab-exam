"""
Quadratic Device Component

Implements a nonlinear device with quadratic i-v characteristic: i = k * v²
As described in CENG 215 Lecture Notes, Section 7.
"""

import sys
from pathlib import Path

from interfaces.non_linear_component import NonLinearComponent

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))


class QuadraticDevice(NonLinearComponent):
    """
    Nonlinear device with quadratic current-voltage characteristic.

    Mathematical Model:
        i(v) = k * v²

    Where:
        v: Voltage across device (Volts)
        i: Current through device (Amperes)
        k: Quadratic coefficient (A/V²)

    Reference:
        CENG 215 Lecture Notes, Section 7:
        "Nonlinear RC Simulation with a Quadratic i-v Device"

    Example from lecture:
        k = 0.01 A/V²
        i = 0.01 * v²
    """

    def __init__(self, k: float = 0.01):
        """
        Initialize quadratic device with coefficient k.

        Args:
            k: Quadratic coefficient in A/V² (default 0.01 from lecture)

        Raises:
            ValueError: If k is not positive
        """
        if k <= 0:
            raise ValueError(f"Coefficient k must be positive, got {k}")

        self.k = k

    def current(self, voltage: float) -> float:
        """
        Calculate current for given voltage.

        Args:
            voltage: Voltage across device in Volts

        Returns:
            Current through device in Amperes

        Formula:
            i = k * v²

        Note:
            - Current is always non-negative
            - Device is symmetric (same behavior for +v and -v)
            - Nonlinear: doubling voltage quadruples current
        """
        return self.k * (voltage**2)

    def conductance(self, voltage: float) -> float:
        """
        Calculate incremental conductance (di/dv) at operating point.

        Args:
            voltage: Operating point voltage in Volts

        Returns:
            Incremental conductance in Siemens (A/V)

        Formula:
            g = di/dv = 2 * k * v

        Note:
            Used for linearization and small-signal analysis
        """
        return 2.0 * self.k * voltage

    def resistance(self, voltage: float) -> float:
        """
        Calculate incremental resistance (dv/di) at operating point.

        Args:
            voltage: Operating point voltage in Volts

        Returns:
            Incremental resistance in Ohms

        Formula:
            r = dv/di = 1/(2*k*v)

        Raises:
            ValueError: If voltage is zero (infinite resistance)
        """
        if abs(voltage) < 1e-12:
            raise ValueError("Incremental resistance is infinite at v=0")

        return 1.0 / (2.0 * self.k * voltage)

    def power(self, voltage: float) -> float:
        """
        Calculate power dissipated in device.

        Args:
            voltage: Voltage across device in Volts

        Returns:
            Power dissipation in Watts

        Formula:
            P = v * i = k * v³
        """
        return self.k * (voltage**3)

    def get_current(self, voltage_drop: float) -> float:
        """
        Interface method for NonLinearComponent.
        Delegates to current() method.

        Args:
            voltage_drop: Voltage across device in Volts

        Returns:
            Current through device in Amperes
        """
        return self.current(voltage_drop)

    def __repr__(self) -> str:
        """String representation of quadratic device."""
        return f"QuadraticDevice(k={self.k:.3e} A/V²)"
