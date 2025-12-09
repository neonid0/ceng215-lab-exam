"""
Linear Component Interface

Defines the abstract base class for linear circuit components.
Linear components follow Ohm's law and superposition principle.
"""

from abc import ABC, abstractmethod


class LinearComponent(ABC):
    """
    Abstract base class for linear circuit components.

    Linear components have constant parameters (R, L, C) and their
    behavior follows linear differential equations.
    """

    @abstractmethod
    def impedance(self, frequency: float = 0.0) -> complex:
        """
        Calculate the impedance of the component at a given frequency.

        Args:
            frequency: Frequency in rad/s (default 0 for DC)

        Returns:
            Complex impedance Z(jω)

        Examples:
            - Resistor: Z = R
            - Capacitor: Z = 1/(jωC)
            - Inductor: Z = jωL
        """
        pass

    @abstractmethod
    def get_parameter(self) -> float:
        """
        Get the component's primary parameter value.

        Returns:
            float: R (Ohms), C (Farads), or L (Henries)
        """
        pass
