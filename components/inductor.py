"""
Inductor Component

Implements a linear inductor with time-domain dynamics.
"""

import sys
from pathlib import Path

from interfaces.linear_component import LinearComponent

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))


class Inductor(LinearComponent):
    """
    Linear inductor component.

    Mathematical Model:
        V = L * dI/dt  (voltage-current relationship)
        λ = L * I      (flux-current relationship)
        W = (1/2) * L * I²  (stored energy)

    Where:
        V: Voltage across inductor (Volts)
        I: Current through inductor (Amperes)
        L: Inductance (Henries)
        λ: Magnetic flux linkage (Weber-turns)
        W: Energy (Joules)

    State Variable:
        Inductor current iL(t) is a state variable in circuit simulation
    """

    def __init__(self, inductance: float):
        """
        Initialize inductor with given inductance.

        Args:
            inductance: Inductance value in Henries (must be positive)

        Raises:
            ValueError: If inductance is not positive
        """
        if inductance <= 0:
            raise ValueError(f"Inductance must be positive, got {inductance}")

        self.L = inductance

    def voltage_from_di_dt(self, di_dt: float) -> float:
        """
        Calculate voltage from current rate of change.

        Args:
            di_dt: Rate of change of current (dI/dt) in A/s

        Returns:
            Voltage across inductor in Volts

        Formula:
            V = L * dI/dt
        """
        return self.L * di_dt

    def di_dt_from_voltage(self, voltage: float) -> float:
        """
        Calculate current rate of change from voltage.

        Args:
            voltage: Voltage across inductor in Volts

        Returns:
            Rate of change of current (dI/dt) in A/s

        Formula:
            dI/dt = V / L

        Note:
            This is the key equation for state-space simulation
        """
        return voltage / self.L

    def impedance(self, frequency: float) -> complex:
        """
        Calculate impedance at given frequency.

        Args:
            frequency: Angular frequency in rad/s (ω)

        Returns:
            Complex impedance Z = jωL

        Formula:
            Z(jω) = jωL

        Note:
            At DC (ω=0), impedance is zero (short circuit)
        """
        # Z = jωL
        return complex(0.0, frequency * self.L)

    def get_parameter(self) -> float:
        """
        Get inductance value.

        Returns:
            Inductance in Henries
        """
        return self.L

    def flux_linkage(self, current: float) -> float:
        """
        Calculate magnetic flux linkage.

        Args:
            current: Current through inductor in Amperes

        Returns:
            Flux linkage in Weber-turns

        Formula:
            λ = L * I
        """
        return self.L * current

    def energy(self, current: float) -> float:
        """
        Calculate energy stored in inductor's magnetic field.

        Args:
            current: Current through inductor in Amperes

        Returns:
            Energy in Joules

        Formula:
            W = (1/2) * L * I²
        """
        return 0.5 * self.L * (current**2)

    def __repr__(self) -> str:
        """String representation of inductor."""
        return f"Inductor(L={self.L:.3e} H)"
