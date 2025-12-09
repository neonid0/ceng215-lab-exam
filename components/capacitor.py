"""
Capacitor Component

Implements a linear capacitor with time-domain dynamics.
"""

import sys
from pathlib import Path

from interfaces.linear_component import LinearComponent

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))


class Capacitor(LinearComponent):
    """
    Linear capacitor component.

    Mathematical Model:
        I = C * dV/dt  (current-voltage relationship)
        Q = C * V      (charge-voltage relationship)
        W = (1/2) * C * V²  (stored energy)

    Where:
        V: Voltage across capacitor (Volts)
        I: Current through capacitor (Amperes)
        C: Capacitance (Farads)
        Q: Charge (Coulombs)
        W: Energy (Joules)

    State Variable:
        Capacitor voltage vC(t) is a state variable in circuit simulation
    """

    def __init__(self, capacitance: float):
        """
        Initialize capacitor with given capacitance.

        Args:
            capacitance: Capacitance value in Farads (must be positive)

        Raises:
            ValueError: If capacitance is not positive
        """
        if capacitance <= 0:
            raise ValueError(f"Capacitance must be positive, got {capacitance}")

        self.C = capacitance

    def current_from_dv_dt(self, dv_dt: float) -> float:
        """
        Calculate current from voltage rate of change.

        Args:
            dv_dt: Rate of change of voltage (dV/dt) in V/s

        Returns:
            Current through capacitor in Amperes

        Formula:
            I = C * dV/dt
        """
        return self.C * dv_dt

    def dv_dt_from_current(self, current: float) -> float:
        """
        Calculate voltage rate of change from current.

        Args:
            current: Current through capacitor in Amperes

        Returns:
            Rate of change of voltage (dV/dt) in V/s

        Formula:
            dV/dt = I / C

        Note:
            This is the key equation for state-space simulation
        """
        return current / self.C

    def impedance(self, frequency: float) -> complex:
        """
        Calculate impedance at given frequency.

        Args:
            frequency: Angular frequency in rad/s (ω)

        Returns:
            Complex impedance Z = -j/(ωC)

        Formula:
            Z(jω) = 1/(jωC) = -j/(ωC)

        Raises:
            ValueError: If frequency is zero (infinite impedance)
        """
        if frequency == 0.0:
            raise ValueError("Capacitor impedance is infinite at DC (ω=0)")

        # Z = 1/(jωC) = -j/(ωC)
        return complex(0.0, -1.0 / (frequency * self.C))

    def get_parameter(self) -> float:
        """
        Get capacitance value.

        Returns:
            Capacitance in Farads
        """
        return self.C

    def charge(self, voltage: float) -> float:
        """
        Calculate charge stored in capacitor.

        Args:
            voltage: Voltage across capacitor in Volts

        Returns:
            Charge in Coulombs

        Formula:
            Q = C * V
        """
        return self.C * voltage

    def energy(self, voltage: float) -> float:
        """
        Calculate energy stored in capacitor.

        Args:
            voltage: Voltage across capacitor in Volts

        Returns:
            Energy in Joules

        Formula:
            W = (1/2) * C * V²
        """
        return 0.5 * self.C * (voltage**2)

    def __repr__(self) -> str:
        """String representation of capacitor."""
        return f"Capacitor(C={self.C:.3e} F)"
