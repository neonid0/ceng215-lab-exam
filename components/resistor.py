"""
Resistor Component

Implements a linear resistor following Ohm's law: V = I * R
"""

import sys
from pathlib import Path

from interfaces.linear_component import LinearComponent

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))


class Resistor(LinearComponent):
    """
    Linear resistor component.

    Mathematical Model:
        V = I * R  (Ohm's law)
        I = V / R

    Where:
        V: Voltage across resistor (Volts)
        I: Current through resistor (Amperes)
        R: Resistance (Ohms)
    """

    def __init__(self, resistance: float):
        """
        Initialize resistor with given resistance.

        Args:
            resistance: Resistance value in Ohms (must be positive)

        Raises:
            ValueError: If resistance is not positive
        """
        if resistance <= 0:
            raise ValueError(f"Resistance must be positive, got {resistance}")

        self.R = resistance

    def current(self, voltage: float) -> float:
        """
        Calculate current through resistor for given voltage.

        Args:
            voltage: Voltage across resistor in Volts

        Returns:
            Current through resistor in Amperes

        Formula:
            I = V / R
        """
        return voltage / self.R

    def voltage(self, current: float) -> float:
        """
        Calculate voltage across resistor for given current.

        Args:
            current: Current through resistor in Amperes

        Returns:
            Voltage across resistor in Volts

        Formula:
            V = I * R
        """
        return current * self.R

    def impedance(self, frequency: float = 0.0) -> complex:
        """
        Calculate impedance (constant for resistor at all frequencies).

        Args:
            frequency: Frequency in rad/s (unused for resistor)

        Returns:
            Complex impedance Z = R + j0
        """
        return complex(self.R, 0.0)

    def get_parameter(self) -> float:
        """
        Get resistance value.

        Returns:
            Resistance in Ohms
        """
        return self.R

    def power(self, voltage: float) -> float:
        """
        Calculate power dissipated in resistor.

        Args:
            voltage: Voltage across resistor in Volts

        Returns:
            Power dissipation in Watts

        Formula:
            P = V² / R = I² * R
        """
        return (voltage**2) / self.R

    def __repr__(self) -> str:
        """String representation of resistor."""
        return f"Resistor(R={self.R:.3e} Ω)"
